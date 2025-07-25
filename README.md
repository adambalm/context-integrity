# Context-Integrity: An XML Signer in the Ruins

*A learning artifact reflecting both the original ambitions and the post-mortem insights of the Context-Integrity project.*

## Overview

A cryptographic context-management toolkit for LLM sessions, offering XML canonicalization, SHA-256 signing, Merkle-tree redactable signatures, and runtime verification. While fully functional for document integrity, its session-level enforcement proved architecturally impossible in stateless LLM environments.

## What This Is

* A functional XML signing and verification toolkit.
* Merkle tree support for redactable signatures.
* Designed for cryptographic document integrity in CLI workflows.

## What This Was Supposed To Be

Prevent context drift in human-LLM conversations via:

* Session-layer hooks for context injection.
* Real-time runtime verification within the LLM session.
* Cross-session state persistence.

## Why It Failed

LLM providers operate as stateless inference engines without persistent session memory or injection APIs—making in-chat enforcement infeasible and economically disincentivized.

## Technical Reference

* **Anthropic MCP Assessment**: [docs/candidate.md](docs/candidate.md)

## Learning Takeaways

* **Stateless Limitation**: True enforcement requires stateful agents or external orchestrators.
* **Protocol vs. Architecture**: Protocols define intent; LLM runtime must support enforcement.
* **Drift Detection**: Requires external counters and signed snapshots.

## Available Components

### CLI Tools

* `tools/ctx_new.py`: Signs XML documents with SHA-256.
* `tools/ctx_loader.py`: Verifies signatures.
* `tools/ctx_redactable_signer.py`: Merkle-tree signer.
* `tools/ctx_redactable_loader.py`: Redactable verifier.
* `tools/redact.py`: Selective redaction while preserving proofs.
* `tools/canonicalizer.py`: XML canonicalization.

### Documentation

* `docs/POSTMORTEM_2025-07-25.md`: Post-mortem analysis of context enforcement.
* `docs/ACTUAL_USES.md`: Real-world use cases for signed contexts.
* `protocol/black-flag/README.md`: Black Flag Protocol v1.3 for operational rules.

## File Structure

```
context-integrity/
├── contexts/           # Example signed XML snapshots
├── contextPackages/    # ContextSnapshot packages with metadata
├── tools/              # Core CLI implementation scripts
├── docs/               # Project docs, PRDs, post-mortems, assessments
└── protocol/           # Signed operational protocols (e.g., Black Flag)
```

## Status

* ✅ XML signing and verification: complete and functional.
* ❌ LLM session enforcement: architecturally impossible.
* 🔄 Pivoting to context portability and audit workflows.

## Roadmap

* **Planned**: Salt integration, HIPAA compliance, MCP compatibility.
* **Future**: GUI plugins, CI/CD actions, multi-agent integration.

## Requirements

* **Python**: 3.10+
* **Dependencies**: `lxml`

## Contributing

Maintain the cryptographic integrity model and prioritize security-first patterns.


*"La tierra es redonda como una naranja.* -- José Arcadio Buendía
