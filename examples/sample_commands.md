# Sample Commands

Run the full CVPR pipeline:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026
```

Run the full pipeline with cautious page enrichment:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --year 2026 --enrich-pages --limit 100 --sleep 0.5 --resume
```

Run individual steps for advanced debugging:

```bash
python skills/conference-cvpr/scripts/collect_cvpr.py --year 2026
python skills/conference-cvpr/scripts/normalize_cvpr.py --year 2026
python skills/conference-cvpr/scripts/export_cvpr.py --year 2026
python skills/conference-cvpr/scripts/check_completeness.py --year 2026
```

Check script options:

```bash
python skills/conference-cvpr/scripts/run_pipeline.py --help
python skills/conference-cvpr/scripts/collect_cvpr.py --help
```

Runtime outputs are written under:

```text
data/
outputs/
logs/
```

These directories are runtime artifacts and should not be committed.
