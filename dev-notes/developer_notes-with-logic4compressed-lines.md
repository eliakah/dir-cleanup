# Developer Notes – dirclean v1.0

## Philosophy

* **Simplicity first**: Favor clarity over cleverness. Code should be easy to read, edit, and extend.
* **Safety first**: All operations in v1.0 are non-destructive. Files are only scanned, flagged, moved, or organized — never deleted.
* **Unix-only**: Keep the tool lean by targeting Unix-based environments first (Linux, macOS, WSL). Cross-platform support can come later.
* **Hackable by design**: Someone with moderate Python skills should be able to edit and customize behavior immediately.

---

## Project Structure

```
dirclean/
├── main.py          # CLI entrypoint
├── ops/
│   ├── scan.py      # Scan directories and list files
│   ├── dedupe.py    # Detect duplicate files by hash
│   ├── archive.py   # Move old files into Archive/ (safe)
│   ├── organize.py  # Organize files by type or date
│   └── common.py    # Shared helpers (hashing, parsing)
├── tests/           # Unit tests for each module
└── developer_notes/ # Notes, diagrams, docs
```

---

## Coding Conventions

* **Type hints**: All functions should use Python typing (mypy friendly).
* **Keep functions small**: Each function should do one job clearly.
* **Minimal dependencies**: Stick to stdlib (hashlib, shutil, pathlib, argparse).
* **Comments required**: Every module and key function should explain what it does.
* **Favor readability**: One-liners are okay for performance-critical sections only.

---

## Command Summaries

* **scan** → Lists files, metadata, sizes; no changes.
* **dedupe** → Flags duplicate files via hash comparison; does *not* delete.
* **archive** → Moves old files into `Archive/` with date subfolders; keeps originals safe.
* **organize** → Groups files into folders by extension (type) or modification date.

All are **non-destructive** in v1.0.

---

## Hotspots (dense efficiency-first sections)

These are places optimized for speed over clarity:

1. **`dedupe.py` – Hash lookups**

   ```python
   hashes = {}
   file_hash = get_file_hash(path)
   if file_hash in hashes:
       duplicates.append((path, hashes[file_hash]))
   else:
       hashes[file_hash] = path
   ```

2. **`archive.py` – Cutoff calculation**

   ```python
   cutoff = now - parse_age_threshold(args.age)
   if file_mtime < cutoff:
       move_to_archive(file)
   ```

3. **`organize.py` – Extension mapping**

   ```python
   ext = Path(file).suffix.lower()
   target = EXT_MAP.get(ext, "Other")
   ```

---

## Future Enhancements (v2.0+)

* **Inheritance / BaseCommand**: Introduce `BaseCommand` + subclasses if GUI or plugin support is added.
* **GUI frontend**: Tkinter (simple) or PyQt (polished). Wraps CLI commands.
* **Plugins**: Allow third parties to add cleanup rules.
* **Cloud/remote support**: Extend to S3, Google Drive, etc.
* **Parallelism**: Speed up hashing with multiprocessing.
* **Config files**: Allow `.dircleanrc` YAML/JSON configs for default rules.

---

## Monetization Notes

Potential paths if project matures:

1. **Freemium CLI**: Core (scan, archive) free, advanced (parallel dedupe, reporting) paid.
2. **Pro GUI version**: One-time purchase or subscription for GUI + cloud integrations.
3. **Enterprise offering**: Bulk cleanup, compliance features, log archiving.
4. **Donations**: GitHub Sponsors, Patreon, “buy me a coffee” links.

---

## Reminder for Future Work

When GUI or plugins are introduced, revisit structure:

* `BaseCommand` with lifecycle (`setup()`, `run()`, `teardown()`).
* Consistent logging and error handling.
* Unified config management across modules.
