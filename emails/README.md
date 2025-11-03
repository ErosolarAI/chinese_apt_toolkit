# Email Dataset

This directory contains the canonical email dataset for the toolkit.  
Raw CSV dumps are ingested into a SQLite database that is distributed in shards
under `emails/shards` to keep each file under GitHub's 100 MB limit. The toolkit
automatically stitches these shards together at runtime, so no manual steps are
required to query the data.

The logical database exposes:

- Deduplicated view of every email address (`emails` table)
- Full-fidelity storage of every CSV row (`email_records` table)
- Metadata describing import and validation timestamps (`metadata` table)

## Maintenance

- `extract_emails.py` rebuilds the database from any CSV files placed in this directory.
- `validate_emails.py` prunes syntactically invalid addresses and updates metadata.

After ingestion, CSV files can be removed because their contents are preserved in
`email_records`. Place any new CSV dumps in this directory and rerun the extractor to
incorporate them.

To (re)create the shard files from a monolithic database, run:

```
python scripts/split_unique_emails_db.py --source emails/unique_emails.db --dest-dir emails/shards --overwrite
```

The script copies the schema and data into sequential shard files named
`unique_emails_XXX.db`, each capped to roughly 100 MB.

## Programmatic Access

Use `apt_toolkit.email_repository.EmailRepository` to query the dataset:

```python
from apt_toolkit.email_repository import EmailRepository

with EmailRepository() as repo:
    print(repo.count())
    print(repo.random_email())
```

The CLI exposes helper commands as well:

```
python -m apt_toolkit.cli emails --random --domain apple.com --json
python -m apt_toolkit.cli emails --search tesla --limit 5
```

## Utility Scripts

- `print_emails_by_org.py` – print every address linked to an organization:
  ```
  python3 print_emails_by_org.py "Molson Coors Beverage"
  python3 print_emails_by_org.py "Molson Coors Beverage" --json
  ```
