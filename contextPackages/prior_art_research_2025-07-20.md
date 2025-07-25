# Prior Art Research: Portable Context Capsules
**Date:** 2025-07-20  
**Researcher:** Claude Sonnet 4  
**Black Flag Protocol:** Active  

## Research Summary

Comprehensive search for existing systems providing portable encrypted data blobs that are (a) cryptographically signed, (b) require explicit human interaction to decrypt/activate, and (c) designed for context or identity transfer between software agents.

## Findings by Category

### 1. Hardware Security Keys & Authentication

| Project | Year | Core Goal | Mechanism | Human-in-loop | Open Specs | Adoption |
|---------|------|-----------|-----------|---------------|------------|----------|
| YubiKey FIDO2 | 2018+ | Passwordless authentication | FIDO2/WebAuthn, CTAP | Physical touch | ✅ FIDO2 standard | High enterprise |
| Trezor Hardware Wallets | 2014+ | Cryptocurrency security | Ed25519/NIST256P1 signing | Physical button press | ❌ Proprietary | Medium crypto |
| Ledger Hardware Wallets | 2014+ | Crypto + PGP operations | Secure element storage | Physical confirmation | ❌ Proprietary | Medium crypto |

**Key Findings:**
- YubiKey stores no data, acts as authentication provider with hardware-bound keys
- Trezor supports GPG signing but cannot import keys (device-generated only)
- Ledger claims PGP smartcard compatibility but has reported compatibility issues

### 2. Biometric Data Encryption

| Project | Year | Core Goal | Mechanism | Human-in-loop | Open Specs | Adoption |
|---------|------|-----------|-----------|---------------|------------|----------|
| Dataram QBKEY | 2018 | Portable biometric encryption | Hardware fingerprint sensor + AES | Biometric scan | ❌ Proprietary | Low commercial |
| AndroidX.Biometric | 2019+ | Mobile app security | Hardware-backed keystore | Face/fingerprint | ✅ Android API | High mobile |

**Key Findings:**
- Biometric encryption typically creates templates, not portable context
- Hardware-backed keystore requires device presence, limits portability
- Focus on protecting keys, not transferring signed context data

### 3. Signed Context & Metadata Protection

| Project | Year | Core Goal | Mechanism | Human-in-loop | Open Specs | Adoption |
|---------|------|-----------|-----------|---------------|------------|----------|
| Signal Sealed Sender | 2018 | Hide message sender metadata | Encrypted envelopes + certificates | User approval for registration | ✅ Signal Protocol | High messaging |
| TPM 2.0 | 2014+ | Hardware attestation | PCR policies + signed attestation | Physical presence detection | ✅ ISO/IEC 11889 | High enterprise |

**Key Findings:**
- Signal's sealed sender encrypts sender identity but limited to messaging context
- TPM provides signed attestation but for device state, not user context
- Both focus on specific use cases, not general context transfer

## Gap Analysis

### What Exists:
- **Hardware authentication:** YubiKey, TPM for device-bound signing
- **Portable encryption:** Hardware wallets for crypto operations
- **Signed attestation:** TPM for device state, Signal for message metadata
- **Human verification:** Biometric unlocking, physical button confirmation

### What's Missing:
- **Cross-platform context transfer:** No system for moving verified user context between different LLMs/agents
- **Selective redaction:** No Merkle-tree-like approach for partial data disclosure
- **Human-gated context loading:** No protocol requiring human approval for context rehydration
- **Model-agnostic memory:** No standardized format for LLM session continuity

## Failure Mode Analysis (Top 3 Similar Projects)

### 1. YubiKey FIDO2
**150-word failure analysis:** YubiKey's strength is device-bound authentication, but this becomes a limitation for context portability. The "no data storage" design prevents context transfer—keys are generated per-service and cannot carry user context. Human interaction (touch) is for authentication only, not context approval. The system works excellently for authentication but cannot address the core problem of preserving and transferring rich user context between agents. Adoption is high but limited to authentication use cases.

### 2. Trezor Hardware Wallets
**150-word failure analysis:** Trezor supports GPG operations but with severe constraints: keys must be device-generated (no imports), limiting cross-device workflows. The hardware button confirmation model works for transaction signing but doesn't scale to complex context verification. The proprietary nature prevents standardization across vendors. While secure, the device-centric approach conflicts with portable context needs. Users report difficulty using multiple devices or integrating with existing GPG workflows. High security but poor interoperability.

### 3. Signal Sealed Sender
**150-word failure analysis:** Signal's sealed sender excellently hides message metadata but operates within a narrow scope—messaging only. The certificate-based approach could theoretically extend to context verification, but the system is purpose-built for real-time communication, not persistent context storage. The sealed sender works for hiding "who talked to whom" but doesn't address "what context was shared." The protocol innovations are solid but application-specific. Limited to Signal's ecosystem.

## Novelty Assessment

**Novelty Score: 7/10**

**Reasoning:**
- **Cryptographic primitives:** All exist individually (signing, encryption, human verification)
- **Novel combination:** Human-gated context capsules for LLM session continuity appears unprecedented
- **Selective redaction with integrity:** Merkle-tree-like approach for partial disclosure is innovative
- **Cross-platform context transfer:** No existing protocol for model-agnostic context handoff
- **Human-verified memory:** Focus on epistemic integrity rather than just authentication is unique

## Prior Art Patents (Expired/Weak)

**Research Status:** Incomplete - requires patent database search
**Notable gaps:** Hardware wallet patents may be relevant but focus on cryptocurrency, not context transfer

## Critical Recommendation

**Build/Kill/Pivot Assessment:** **BUILD** - but with caveats

The research reveals no direct prior art for human-verified, portable context capsules designed for LLM continuity. While individual components exist, the specific combination of:
1. Cryptographically signed user context
2. Human-in-loop verification for loading
3. Cross-platform agent compatibility
4. Selective redaction capabilities

...appears to be novel enough to warrant development.

**Risk factors:**
- Complex integration requirements
- User adoption challenges (manual verification burden)
- Hardware dependency for security model

**Recommendation:** Proceed with software prototype first, validate user value proposition before hardware investment.
