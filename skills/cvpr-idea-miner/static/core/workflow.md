# Workflow

## Default Full Pipeline

```text
topic-map -> gap-analysis -> method-recombination -> idea-cards -> experiment-plan
```

## Operating Rules

1. Load `manifest.yaml` and all files listed in `always_load`.
2. Identify input evidence level with `static/core/evidence-policy.md`.
3. Select one or more workflow fragments from `manifest.yaml`.
4. Load only selected workflow fragments; do not read all workflow files by default.
5. Produce Markdown files under `outputs/computer_vision/cvpr/ideas/{year}/`.
6. Mark every output with evidence level, source material, and status.
7. Keep CVPR-only scope and refuse requests that require other conferences or external enrichment APIs.

## Workflow Selection

| User intent | Workflow |
| --- | --- |
| topic map, direction map, cluster these papers | `topic-map` |
| gaps, limitations, future work, opportunities | `gap-analysis` |
| combine methods, recombine modules, new architecture idea | `method-recombination` |
| generate ideas, idea cards, research inspirations | `idea-cards` |
| experiments, first runnable experiment, validation plan | `experiment-plan` |

If a user asks for "research directions from CVPR 2026" and provides only a paper list, start with `topic-map` and mark `title_only` or `title_abstract` according to available fields.

