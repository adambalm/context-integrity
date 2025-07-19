# Context-Integrity

A cryptographic context management system for LLM sessions that prevents context drift through XML canonicalization, SHA-256 signing, and runtime verification.

## Purpose

Eliminate context drift in LLM conversations by providing **one-command context loading** with **real-time integrity enforcement**. When context integrity is violated, sessions halt with a clear violation signal.

## Features

### Core Capabilities
- **Cryptographic Context Signing**: SHA-256 signatures with XML canonicalization
- **Runtime Drift Detection**: Automatic session halting on context violations  
- **Git Integration**: Versioned context snapshots with PowerShell tooling
- **One-Command Loading**: Simple CLI for context verification and injection

### Advanced: Redactable Contexts
- **Merkle-Tree Architecture**: Individual leaf element signing for selective verification
- **Selective Redaction**: Remove sensitive data while preserving cryptographic proof
- **HIPAA-Ready Design**: Architecture prepared for compliance requirements
- **Granular Integrity**: Each XML element can be independently validated

## Quick Start

### Basic Context Operations

```bash
# Create and sign a new context
pwsh tools/ctx-new.ps1 userContext 2025-07-23

# Load and verify context
python tools/ctx_loader.py contexts/userContext_2025-07-23.xml
# Output: 🟢 CONTEXT LOADED

# On integrity violation: 🔴 CONTEXT VIOLATION
```

### Redactable Context Operations

```bash
# Sign with individual leaf hashes
python tools/ctx_redactable_signer.py input.xml signed_output.xml

# Verify redactable context
python tools/ctx_redactable_loader.py signed_output.xml

# Redact sensitive fields while preserving integrity
python tools/redact.py signed_output.xml redacted.xml date os
```

## Architecture

### Generation 2 Security Model

The system implements a **second-generation** hashing approach with:

- **Core Signing**: Whole-document SHA-256 with C14N canonicalization
- **Merkle-Tree Redaction**: Individual `sha256_leaf` attributes on XML leaf elements
- **Selective Verification**: Independent validation of redacted content
- **Future-Ready**: Designed for salt integration and HIPAA compliance

### File Structure

```
context-integrity/
├── contexts/           # Signed XML context files
├── contextPackages/    # Context package definitions
├── tools/              # Core implementation scripts
│   ├── ctx_new.py              # Basic context signer
│   ├── ctx_loader.py           # Basic context verifier
│   ├── ctx_redactable_signer.py # Merkle-tree signer
│   ├── ctx_redactable_loader.py # Redactable verifier
│   ├── redact.py               # Content redaction tool
│   └── canonicalizer.py        # XML canonicalization
└── docs/               # Project documentation
```

## Security Features

### Cryptographic Integrity
- **Deterministic Canonicalization**: C14N ensures consistent hashing across platforms
- **Tamper Detection**: Any modification breaks cryptographic signatures
- **Self-Verification**: Signatures exclude themselves to prevent circular dependencies

### Privacy & Compliance
- **Selective Redaction**: Remove sensitive data while proving original content
- **Merkle-Tree Verification**: Validate individual elements without full context
- **HIPAA Preparation**: Architecture designed for healthcare compliance requirements

## Roadmap

### Current (Generation 2)
- ✅ Merkle-tree-like redactable contexts
- ✅ Individual leaf element signing
- ✅ Selective content redaction

### Planned
- 🔄 **Salt Integration**: Enhanced security with randomized salting
- 🔄 **HIPAA Compliance**: Full healthcare data protection capabilities
- 🔄 **MCP Integration**: Model Context Protocol compatibility

### Future Considerations
- GUI/IDE plugins for context management
- CI/CD integration and GitHub Actions
- Multi-agent system compatibility
- External watchdog processes

## Requirements

- **Python**: 3.10+
- **Dependencies**: `lxml` for XML processing
- **Optional**: PowerShell 7+ for enhanced tooling

## Contributing

This project implements defensive security patterns for LLM context management. Contributions should maintain the cryptographic integrity model and security-first approach.

## License

Licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.

---

**Context-Integrity**: Preventing LLM context drift through cryptographic verification.
