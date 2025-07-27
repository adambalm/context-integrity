# Context Snapshot – Session Resume (macmini · 2025-07-27)

## Purpose
Restore this session’s full operational context after environment reset or assistant degradation.

## Current Status
- Logged into OpenAI via Firefox Developer Edition (new install, no prior cookies)
- ChatGPT running in browser on macOS 12.6.9, device: Mac Mini
- Terminal operational, using zsh shell
- Docker installed
- Ollama install successful, model `gemma` is downloading (confirmed)
- No desktop LLM clients installed yet (e.g. LM Studio or MacWhisper)
- GitHub is accessible and used; Codespaces not active on this device (yet)
- Context snapshots are being structured as Markdown files with verified ≥90% data

## Protocol Enforcement
- All context snapshots require:
  - (1) Environment profile
  - (2) Session resume
- Each must be ≥90% verified (not inferred)
- Hash fingerprinting of markdown file to simulate future signature pipelines
- Signed XML variants will be generated using CLI later (repo: `tools/`)

## Next Steps
- Finalize and upload these two files to GitHub in correct directories
- Create missing verification steps (storage, CLI tools, git, Python)
- Track ongoing downloads and confirm when `gemma` completes
- Resume Docker/Ollama test run after download is complete

## File Naming Convention (Rule)
Use format: `[TYPE]-[DEVICE]-[DATE]-[CONTEXT].md`, e.g.:
- `env-profile_macmini-2025-07-27.md`
- `context-resume_macmini-2025-07-27.md`
