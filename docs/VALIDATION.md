# Validation scope

Offline checks cover all 13 tables: required columns, rectangular rows, original row counts, nonempty model names and model uniqueness where appropriate. Tests exercise malformed tables, missing files and manifest tampering. PsychoBench's two-row header and multiple 16P outcomes are intentional exceptions.

Packaging checks parse Python source, run `bash -n` on shell scripts, compare original CSVs byte-for-byte with the source package, verify SHA-256 hashes and check ZIP integrity. Syntax checks are not full dependency/import or runtime tests.

Prepared source is scanned for common credentials, private-key headers, source-machine locations, weights, logs and caches. Pattern scanning cannot prove arbitrary private information is absent.

No checkpoint pruning, GPU inference, external API evaluation, full environment installation or dataset re-download is included. Passing packaging checks does not independently validate stored scientific results.
