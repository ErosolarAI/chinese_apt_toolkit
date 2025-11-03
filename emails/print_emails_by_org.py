#!/usr/bin/env python3
"""
Print every email address associated with a specified organization.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from signal import SIGPIPE, SIG_DFL, signal

from apt_toolkit.email_repository import EmailRepository, EmailRepositoryError


signal(SIGPIPE, SIG_DFL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List all email addresses tied to an organization."
    )
    parser.add_argument(
        "organization",
        help="Organization name to match (case insensitive, exact match).",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        help="Optional path to the deduplicated email database.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit results as JSON instead of plain text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        repo = EmailRepository(db_path=args.db_path)
    except EmailRepositoryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    records = repo.emails_by_organization(args.organization)
    repo.close()

    if args.json:
        print(json.dumps(records, indent=2))
    else:
        if not records:
            print(f"No entries found for organization '{args.organization}'.")
        else:
            try:
                for entry in records:
                    print(entry["email"])
            except BrokenPipeError:
                return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
