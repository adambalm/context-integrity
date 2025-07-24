# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a context-integrity system that implements XML-based context management with cryptographic signing for LLM sessions. The system prevents context drift through canonicalization, SHA-256 signing, and runtime verification.

## Architecture

### Core Components

- **Canonicalizer** (`tools/canonicalizer.py`): Deterministic XML canonicalization (C14N) with comment stripping, whitespace collapse, and attribute sorting
- **Context Signer** (`tools/ctx_new.py`): Signs XML contexts by removing existing signatures, canonicalizing content, computing SHA-256 hash, and injecting signature
- **Context Loader/Verifier** (`tools/ctx_loader.py`): Validates signed contexts by re-canonicalizing and verifying SHA-256 signatures
- **Redactable System**: Merkle-tree-inspired signing/loading system for selective redaction (`tools/ctx_redactable_*.py`)

### Redactable System Architecture

The redactable system implements a **Merkle-tree-like** approach for selective content redaction:

- **Leaf Signing** (`tools/ctx_redactable_signer.py`): Traverses XML leaf elements (no child elements), computes SHA-256 for each element's canonical representation, stores as `sha256_leaf` attributes, builds root hash from concatenated leaf hashes
- **Selective Verification** (`tools/ctx_redactable_loader.py`): Independently validates each `sha256_leaf` attribute by re-canonicalizing without the hash attribute itself
- **Content Redaction** (`tools/redact.py`): Removes text content from specified elements while preserving `sha256_leaf` attributes and element structure

### File Structure

```
contexts/           # Signed XML context files (environmentContext.xml, etc.)
contextPackages/    # Context package definitions  
tools/              # Core implementation scripts
docs/               # Project documentation (PRD.xml, userStories.xml)
```

## Development Commands

### Python Environment
- **Dependencies**: `lxml` library required for XML processing
- **Python Version**: 3.10+ (based on environment context)

### Core Operations

#### Creating Signed Contexts
```bash
# Create and sign contexts
python tools/ctx_new.py <input.xml> <output.xml>
```

#### Loading/Verifying Contexts  
```bash
python tools/ctx_loader.py <signed_context.xml>
# Success: prints "🟢 CONTEXT LOADED"
# Failure: prints error and exits with code 1
```

#### XML Canonicalization
```bash
python tools/canonicalizer.py <input.xml> <output.bin>
```

### Redactable Contexts (Merkle-tree System)
```bash
# Sign with individual leaf hashes
python tools/ctx_redactable_signer.py <input.xml> <output.xml>

# Verify redactable context (validates each sha256_leaf)
python tools/ctx_redactable_loader.py <signed_context.xml>

# Redact specific fields while preserving integrity
python tools/redact.py <signed_context.xml> <redacted_output.xml> <field1> <field2>
```

## Key Technical Details

### Core Hashing (Generation 2)
- Uses lxml with C14N (Canonical XML) for deterministic serialization
- SHA-256 signatures exclude the `<sha256>` element itself to prevent circular dependencies
- Context verification is designed to halt LLM sessions on integrity violations (🔴 CONTEXT VIOLATION)
- Python tools provide clean, focused implementation of core signing/verification logic

### Redactable System (Merkle-tree Approach)
- Individual `sha256_leaf` attributes on leaf elements enable selective verification
- Root hash computed from concatenated leaf hashes provides overall integrity
- Content can be redacted while preserving cryptographic proof of original values
- Each element can be independently validated without requiring full context

### Development Status
- **Current**: Second iteration of security/hashing implementation
- **Planned**: Salt integration for enhanced security
- **Future**: HIPAA compliance capabilities
- **Roadmap**: MCP (Model Context Protocol) integrations

## Security Model

The system implements a defensive security pattern:
- **Generation 2 hashing**: Enhanced cryptographic integrity with Merkle-tree-like leaf verification
- **Selective redaction**: Remove sensitive data while maintaining proof of original content
- **Deterministic canonicalization**: Ensures consistent hashing across platforms
- **Runtime verification**: Enforces context compliance in LLM interactions
- **Future-ready**: Architecture designed for salting and HIPAA compliance

## Black Flag Protocol

The authoritative Black Flag rules now live at: `protocol/black-flag/README.md`

Before doing anything, you **must** load and obey the rules in that file.
