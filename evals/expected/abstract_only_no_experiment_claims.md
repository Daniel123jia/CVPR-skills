# Expected Behavior: abstract_only_no_experiment_claims

- Use evidence level `abstract_only`.
- Output must be a `preliminary summary`.
- The reader may summarize the title and abstract only.
- It 不能输出实验细节, dataset details, ablation, baseline tables, leaderboard claims, code links, or numerical results unless explicitly present in the abstract.
- It must not claim full-paper reading or fulltext evidence.
- Missing method and experiment sections should be marked as insufficient evidence.
