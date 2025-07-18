# filename: ctx_redactable_loader.py
"""
Enhanced Redactable Loader and Verifier (Encoding-Hardened) with Debugging:
- Reads a signed XML artifact (redacted or not), assuming UTF-8.
- Verifies or trusts each 'sha256_leaf' hash by re-calculating the canonical byte representation without including its own attribute.
- Re-creates the root hash and verifies the overall signature.
- On tampering detection, prints both recorded and calculated hashes for debugging.
"""
import sys
import hashlib
import copy
from lxml import etree

def load_and_verify_redactable(file_path: str) -> None:
    """Verifies a signed XML file that supports redaction, with debug output on mismatch."""
    try:
        parser = etree.XMLParser(remove_comments=True)
        tree = etree.parse(file_path, parser)
        root = tree.getroot()

        # 1. Extract and remove the main root hash.
        sha_elem = root.find('sha256')
        if sha_elem is None or not sha_elem.text:
            print('❌ ERROR: No main <sha256> root hash found.')
            sys.exit(1)
        expected_root_hash = sha_elem.text.strip()
        root.remove(sha_elem)

        verified_leaf_hashes = []

        # 2. Walk every element that has a sha256_leaf.
        for elem in root.xpath('.//*[@sha256_leaf]'):
            leaf_hash = elem.get('sha256_leaf')

            # Detect if redacted (no text and no child nodes).
            has_content = bool(elem.text and elem.text.strip()) or len(elem) > 0
            if has_content:
                # Create a copy without the sha256_leaf attribute for accurate canonicalization
                elem_copy = copy.deepcopy(elem)
                elem_copy.attrib.pop('sha256_leaf', None)

                # Re‑canonicalize exactly as the signer uses C14N
                c14n_bytes = etree.tostring(elem_copy, method='c14n')
                calculated_hash = hashlib.sha256(c14n_bytes).hexdigest()

                if calculated_hash != leaf_hash:
                    print(f"\n❌ TAMPERING DETECTED on element <{elem.tag}>!")
                    print(f"   recorded: {leaf_hash}")
                    print(f"   calculated: {calculated_hash}")
                    sys.exit(1)

                verified_leaf_hashes.append(calculated_hash)
            else:
                # Trust the existing hash for redacted elements
                verified_leaf_hashes.append(leaf_hash)

        # 3. Rebuild the overall root hash
        actual_root_hash = hashlib.sha256(
            "".join(verified_leaf_hashes).encode('utf-8')
        ).hexdigest()

        # 4. Final comparison
        if actual_root_hash == expected_root_hash:
            print(f"\n🟢 CONTEXT LOADED. Signature valid.")
        else:
            print("\n❌ HASH MISMATCH! The overall signature is invalid.")
            print(f"   expected root: {expected_root_hash}")
            print(f"   actual root:   {actual_root_hash}")
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{file_path}'")
        sys.exit(1)
    except etree.XMLSyntaxError as e:
        print(f"❌ ERROR: Input file '{file_path}' is not well-formed XML. Details: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 ctx_redactable_loader.py <signed_or_redacted_context.xml>')
        sys.exit(1)
    load_and_verify_redactable(sys.argv[1])
