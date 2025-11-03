#!/usr/bin/env python3
"""
Validate email addresses stored in the SQLite database produced by extract_emails.py.
Invalid addresses are removed alongside their associated records.
"""

from __future__ import annotations

import argparse
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

from apt_toolkit.email_repository import open_email_database

EMAIL_PATTERN = re.compile(
    r"^(?=.{1,320}$)[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$",
    re.IGNORECASE,
)


def is_valid_email(address: str) -> bool:
    """Apply conservative validity checks for email syntax."""
    if not EMAIL_PATTERN.match(address):
        return False

    local_part, domain_part = address.rsplit("@", 1)

    if len(local_part) > 64 or not local_part or not domain_part:
        return False
    if local_part[0] == "." or local_part[-1] == "." or ".." in local_part:
        return False
    if domain_part[0] in ".-" or domain_part[-1] in ".-":
        return False
    if ".." in domain_part:
        return False
    if "." not in domain_part:
        return False
    return True


def purge_invalid_emails(db_path: Path) -> Tuple[int, int]:
    """Remove invalid email addresses and return (inspected, removed)."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys=ON;")
        total_rows = conn.execute("SELECT COUNT(*) FROM emails").fetchone()[0]

        cursor = conn.execute("SELECT id, email FROM emails")
        invalid_rowids = [(row_id,) for row_id, email in cursor if not is_valid_email(email)]

        removed_rows = len(invalid_rowids)
        if removed_rows:
            with conn:
                conn.executemany("DELETE FROM emails WHERE id = ?", invalid_rowids)

        remaining = conn.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
        conn.execute(
            """
            INSERT INTO metadata(key, value) VALUES
                ('valid_emails', ?),
                ('validated_at', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value;
            """,
            (
                str(remaining),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()

        return total_rows, removed_rows
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Validate emails in the deduplicated SQLite database and remove invalid entries."
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=script_dir / "unique_emails.db",
        help="Path to the SQLite database produced by extract_emails.py",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db_path = args.db_path.resolve()
    if not db_path.exists():
        # Attempt to materialise the sharded distribution automatically.
        try:
            conn = open_email_database(db_path)
        except Exception as exc:  # pragma: no cover - propagates meaningful error
            raise SystemExit(f"Database not found: {db_path}") from exc
        else:
            conn.close()

    inspected, removed = purge_invalid_emails(db_path)
    remaining = inspected - removed
    print(
        f"Inspected {inspected} emails in {db_path}; "
        f"removed {removed} invalid entries; {remaining} remaining."
    )


if __name__ == "__main__":
    main()
