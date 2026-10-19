# Repository maintenance

Public repository: https://github.com/gaffeyn03/ACE-Compression

```bash
git clone https://github.com/gaffeyn03/ACE-Compression.git
cd ACE-Compression
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

Review staged files before uploading. Do not commit private packaging workspaces, snapshots, weights, datasets, credentials, raw responses, logs or working records. `.gitignore` does not untrack committed files.

CI runs offline checks, not inference. After intentional source edits use `validate_release.py --skip-manifest`; regenerate packaging hashes for a new archive. Do not claim an unassigned paper identifier or release DOI.
