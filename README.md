# Context-Integrity: An XML Signer in the Ruins

## What This Is
A functional XML signing and verification toolkit with Merkle tree support for redactable signatures. The tools work exactly as designed for cryptographic document integrity.

## What This Was Supposed To Be  
A system for preventing context drift in human-LLM conversations through runtime verification and session-level enforcement.

## Why It Failed

**The fundamental problem**: We tried to build persistent context management in a stateless architecture.

**What we assumed existed:**
- Session-layer hooks for context injection
- Runtime verification capabilities
- Cross-session state persistence

**What actually exists:**
- Stateless request/response cycles
- No session management APIs
- Economic incentives against context persistence (retained context = lost revenue)

## The Learning
LLM providers offer stateless inference, not persistent memory. Building context integrity tools taught us why the architecture makes session-level enforcement impossible.

## What You'll Find Here
- `tools/ctx_new.py` - Signs XML documents with SHA-256
- `tools/ctx_loader.py` - Verifies signatures 
- `tools/ctx_redactable_signer.py` - Merkle tree signatures
- `tools/ctx_redactable_loader.py` - Verifies with redaction support
- `docs/POSTMORTEM_2025-07-25.md` - Why runtime context enforcement is impossible
- `docs/ACTUAL_USES.md` - Real applications for signed conversations

## Quick Start

### Basic XML Signing

```bash
# Create and sign a new context
python tools/ctx_new.py input_context.xml signed_context.xml

# Verify signature
python tools/ctx_loader.py signed_context.xml
# Output: 🟢 CONTEXT LOADED
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

## Technical Architecture

### What Actually Works
- **XML Signing**: SHA-256 with C14N canonicalization  
- **Merkle Trees**: Individual `sha256_leaf` attributes for selective redaction
- **Verification**: Cryptographic integrity checking for document tampering
- **Redaction**: Remove sensitive data while preserving cryptographic proof

### File Structure
```
context-integrity/
├── tools/              # Functional XML signing toolkit
│   ├── ctx_new.py              # Document signer
│   ├── ctx_loader.py           # Signature verifier  
│   ├── ctx_redactable_signer.py # Merkle tree signer
│   ├── ctx_redactable_loader.py # Redactable verifier
│   └── redact.py               # Content redaction
├── contexts/           # Example signed documents
├── docs/               # PRD showing original ambitions + postmortem
└── CLAUDE.md           # Black Flag Protocol (the real success)

## Status
✅ XML signing - Complete and functional  
❌ LLM context enforcement - Architecturally impossible  
🔄 Pivoting to context portability workflows

## Evidence of Architectural Reality
- **Commit c95b744**: PowerShell integration layer removed with no replacement
- **PRD.xml vs Implementation**: Documents promise "banner-check middleware" and "system prompt injection" - zero session management code exists
- **Economic Constraint**: Persistent context = lost revenue for LLM providers

## Requirements
- **Python**: 3.10+
- **Dependencies**: `lxml` for XML processing

---
*"In the ruins of great ambitions, we often find our most useful tools."*
