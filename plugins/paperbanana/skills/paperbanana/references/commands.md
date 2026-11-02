# Backend command examples

Run these in the selected PaperBanana Python environment. Replace placeholders
with actual paths and check `<command> --help` first; upstream, the maintained
fork and installed releases can differ. None of these examples configures keys.

```bash
python -m paperbanana.cli generate --input method.txt --caption "Method overview"
python -m paperbanana.cli plot --data results.csv --intent "Compare accuracy by condition"
python -m paperbanana.cli slide --input slide-prompt.md
python -m paperbanana.cli slide-batch --prompts-dir prompts --output-dir deck
python -m paperbanana.cli evaluate --generated generated.png --reference reference.png --context method.txt --caption "Method overview"
```

For an explicitly selected provider, use the supported command flags, for example
`--image-provider google_imagen`. Do not assume VLM names also work as image
factory names. Preserve an existing Vertex configuration in the user's backend.

For `generate`, a supported `--continue-run <run-id> --feedback <text>` can revise
a specific run. Verify the run's input, provider and output before continuing.
Do not use an unspecified latest run when several tasks are present.

Use `slide --list-styles` to discover installed backend presets. Bundled deck
style documents and backend preset names are separate resources.

Concurrency and early-stop features depend on the installed backend. Select
parallelism within its documented limits and the authorized resource scope;
do not infer timing, cost or quality guarantees from historical sample runs.
