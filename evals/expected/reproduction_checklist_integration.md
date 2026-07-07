# Expected Behavior

- `reader_notes_index.json` includes `files.reproduction_checklist` when `reproduction_checklist.md` exists.
- The top-level `note_files` mapping includes `reproduction_checklist: reproduction_checklist.md`.
- Idea cards may cite the checklist as an evidence source for `dependency_on_original_code`, `data_availability`, `implementation_difficulty`, `first_week_action`, and `stop_condition`.
- `experiment_plan.md` may cite it for required inputs, missing details, and risks.
- Missing code, supplementary details, hyperparameters, or datasets remain explicit evidence gaps.
- A missing `reproduction_checklist.md` does not block collection or idea mining from the other reader notes.
