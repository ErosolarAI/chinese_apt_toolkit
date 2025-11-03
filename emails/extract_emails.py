#!/usr/bin/env python3
"""
Aggregate all email CSV dumps in this directory into a structured SQLite database.

The resulting database retains every original CSV row while providing a deduplicated
view of targets for quick lookups elsewhere in the toolkit.
"""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

EMAIL_FIELD = "Email address"

# Columns we surface directly on the `emails` table. Every CSV row is preserved in
# the `email_records` table as JSON to avoid data loss when the source files are removed.
DETAIL_COLUMNS = {
    "domain": "Domain name",
    "organization": "Organization",
    "country": "Country",
    "state": "State",
    "city": "City",
    "postal_code": "Postal code",
    "street": "Street",
    "confidence_score": "Confidence score",
    "email_type": "Type",
    "num_sources": "Number of sources",
    "pattern": "Pattern",
    "first_name": "First name",
    "last_name": "Last name",
    "department": "Department",
    "position": "Position",
    "twitter_handle": "Twitter handle",
    "linkedin_url": "LinkedIn URL",
    "phone_number": "Phone number",
}


def discover_csv_files(emails_dir: Path) -> Iterable[Path]:
    """Yield CSV files inside emails_dir sorted for determinism."""
    yield from sorted(path for path in emails_dir.glob("*.csv") if path.is_file())


def normalize_str(value: Optional[str], *, lower: bool = False) -> str:
    """Strip whitespace and optionally lowercase text values."""
    if value is None:
        return ""
    text = value.strip()
    return text.lower() if lower else text


def parse_int(value: Optional[str]) -> Optional[int]:
    """Safely parse integers from string fields."""
    if value is None:
        return None
    try:
        return int(value.strip())
    except (TypeError, ValueError):
        return None


def row_to_details(row: Dict[str, str], source_file: str) -> Tuple[str, Dict[str, object]]:
    """Return normalized email and structured column details for the row."""
    email = normalize_str(row.get(EMAIL_FIELD))
    if not email:
        return "", {}

    lower_email = email.lower()
    details: Dict[str, object] = {
        "email": lower_email,
        "first_seen_file": source_file,
        "last_seen_file": source_file,
    }

    for column, header in DETAIL_COLUMNS.items():
        raw_value = row.get(header)
        if column in {"confidence_score", "num_sources"}:
            details[column] = parse_int(raw_value)
        elif column == "domain":
            details[column] = normalize_str(raw_value, lower=True)
        else:
            details[column] = normalize_str(raw_value)

    return lower_email, details


def initialize_database(conn: sqlite3.Connection) -> None:
    """Create the database schema from scratch."""
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=NORMAL;
        PRAGMA temp_store=MEMORY;
        PRAGMA foreign_keys=ON;

        CREATE TABLE emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            domain TEXT,
            organization TEXT,
            country TEXT,
            state TEXT,
            city TEXT,
            postal_code TEXT,
            street TEXT,
            confidence_score INTEGER,
            email_type TEXT,
            num_sources INTEGER,
            pattern TEXT,
            first_name TEXT,
            last_name TEXT,
            department TEXT,
            position TEXT,
            twitter_handle TEXT,
            linkedin_url TEXT,
            phone_number TEXT,
            first_seen_file TEXT,
            last_seen_file TEXT,
            total_records INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE email_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id INTEGER NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
            source_file TEXT NOT NULL,
            source_row INTEGER NOT NULL,
            raw_record TEXT NOT NULL
        );

        CREATE INDEX idx_email_records_email_id ON email_records(email_id);

        CREATE TABLE metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )


def insert_or_update_email(
    cursor: sqlite3.Cursor,
    email_cache: Dict[str, int],
    email: str,
    details: Dict[str, object],
) -> int:
    """Insert a new email row or update existing metadata."""
    if email not in email_cache:
        cursor.execute(
            """
            INSERT INTO emails (
                email, domain, organization, country, state, city, postal_code, street,
                confidence_score, email_type, num_sources, pattern, first_name, last_name,
                department, position, twitter_handle, linkedin_url, phone_number,
                first_seen_file, last_seen_file, total_records
            )
            VALUES (
                :email, :domain, :organization, :country, :state, :city, :postal_code, :street,
                :confidence_score, :email_type, :num_sources, :pattern, :first_name, :last_name,
                :department, :position, :twitter_handle, :linkedin_url, :phone_number,
                :first_seen_file, :last_seen_file, 1
            )
            ON CONFLICT(email) DO NOTHING;
            """,
            details,
        )
        if cursor.lastrowid:
            email_cache[email] = cursor.lastrowid
            return cursor.lastrowid

        # If ON CONFLICT triggered due to race with previous rows we still resolve the id below.

    email_id = email_cache.get(email)
    if email_id is None:
        cursor.execute("SELECT id FROM emails WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            raise RuntimeError(f"Failed to resolve email id for {email!r}")
        email_id = row[0]
        email_cache[email] = email_id

    update_params = details.copy()
    update_params["email_id"] = email_id
    cursor.execute(
        """
        UPDATE emails
        SET
            total_records = total_records + 1,
            last_seen_file = :last_seen_file,
            domain = CASE WHEN (domain IS NULL OR domain = '') AND :domain != '' THEN :domain ELSE domain END,
            organization = CASE WHEN (organization IS NULL OR organization = '') AND :organization != '' THEN :organization ELSE organization END,
            country = CASE WHEN (country IS NULL OR country = '') AND :country != '' THEN :country ELSE country END,
            state = CASE WHEN (state IS NULL OR state = '') AND :state != '' THEN :state ELSE state END,
            city = CASE WHEN (city IS NULL OR city = '') AND :city != '' THEN :city ELSE city END,
            postal_code = CASE WHEN (postal_code IS NULL OR postal_code = '') AND :postal_code != '' THEN :postal_code ELSE postal_code END,
            street = CASE WHEN (street IS NULL OR street = '') AND :street != '' THEN :street ELSE street END,
            confidence_score = CASE WHEN confidence_score IS NULL AND :confidence_score IS NOT NULL THEN :confidence_score ELSE confidence_score END,
            email_type = CASE WHEN (email_type IS NULL OR email_type = '') AND :email_type != '' THEN :email_type ELSE email_type END,
            num_sources = CASE WHEN num_sources IS NULL AND :num_sources IS NOT NULL THEN :num_sources ELSE num_sources END,
            pattern = CASE WHEN (pattern IS NULL OR pattern = '') AND :pattern != '' THEN :pattern ELSE pattern END,
            first_name = CASE WHEN (first_name IS NULL OR first_name = '') AND :first_name != '' THEN :first_name ELSE first_name END,
            last_name = CASE WHEN (last_name IS NULL OR last_name = '') AND :last_name != '' THEN :last_name ELSE last_name END,
            department = CASE WHEN (department IS NULL OR department = '') AND :department != '' THEN :department ELSE department END,
            position = CASE WHEN (position IS NULL OR position = '') AND :position != '' THEN :position ELSE position END,
            twitter_handle = CASE WHEN (twitter_handle IS NULL OR twitter_handle = '') AND :twitter_handle != '' THEN :twitter_handle ELSE twitter_handle END,
            linkedin_url = CASE WHEN (linkedin_url IS NULL OR linkedin_url = '') AND :linkedin_url != '' THEN :linkedin_url ELSE linkedin_url END,
            phone_number = CASE WHEN (phone_number IS NULL OR phone_number = '') AND :phone_number != '' THEN :phone_number ELSE phone_number END
        WHERE id = :email_id;
        """,
        update_params,
    )

    return email_id


def build_database(emails_dir: Path, db_path: Path) -> Tuple[int, int]:
    """Populate the database with deduplicated emails and raw records."""
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        initialize_database(conn)
        cursor = conn.cursor()

        total_rows = 0
        email_cache: Dict[str, int] = {}

        for csv_file in discover_csv_files(emails_dir):
            with csv_file.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames or EMAIL_FIELD not in reader.fieldnames:
                    continue

                for row_index, row in enumerate(reader, start=1):
                    email, details = row_to_details(row, csv_file.name)
                    if not email:
                        continue

                    row_json = json.dumps(row, ensure_ascii=False, sort_keys=True)
                    email_id = insert_or_update_email(cursor, email_cache, email, details)

                    cursor.execute(
                        """
                        INSERT INTO email_records (email_id, source_file, source_row, raw_record)
                        VALUES (?, ?, ?, ?);
                        """,
                        (email_id, csv_file.name, row_index, row_json),
                    )
                    total_rows += 1

        conn.commit()

        unique_count = conn.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
        conn.execute(
            """
            INSERT INTO metadata(key, value) VALUES
                ('total_rows', ?),
                ('unique_emails', ?),
                ('ingested_at', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value;
            """,
            (
                str(total_rows),
                str(unique_count),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()

        return total_rows, unique_count
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Extract all email addresses into a deduplicated SQLite database with full record retention."
    )
    parser.add_argument(
        "--emails-dir",
        type=Path,
        default=script_dir,
        help="Directory containing the CSV dumps (default: script directory)",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=script_dir / "unique_emails.db",
        help="Path to the SQLite database to create (default: unique_emails.db next to script)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    emails_dir = args.emails_dir.resolve()
    db_path = args.db_path.resolve()

    if not emails_dir.exists():
        raise SystemExit(f"Email directory not found: {emails_dir}")

    total_rows, unique_rows = build_database(emails_dir, db_path)
    print(
        f"Processed {total_rows} rows across {emails_dir} "
        f"and stored {unique_rows} unique emails in {db_path}"
    )


if __name__ == "__main__":
    main()
