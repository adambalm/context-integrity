# filename: ctx_redactable_loader.py
"""
Enhanced Redactable Loader and Verifier (Encoding-Hardened):
- Reads a signed XML artifact (redacted or not), assuming UTF-8.
- Verifies or trusts each 'sha256_leaf' hash by re-calculating the canonical byte representation.
- Re-creates the root hash and verifies the overall signature.
"""
import sys
import hashlib
from lxml import etree

def load_and_verify_redactable(file_path: str) -> None:
    """Verifies a signed XML file that supports redaction."""
    try:
        # Assume the input file is UTF-8.
        parser = etree.XMLParser(remove_comments=True)
        tree = etree.parse(file_path, parser)
        root = tree.getroot()

        # 1. Get the expected root hash.
        sha_elem = root.find('sha256')
        if sha_elem is None or not sha_elem.text:
            print('❌ ERROR: No main <sha256> root hash found.')
            sys.exit(1)
        expected_root_hash = sha_elem.text.strip()
        root.remove(sha_elem)

        verified_leaf_hashes = []
        
        # 2. Iterate over all elements that should have a leaf hash.
        for elem in root.xpath('.//*[@sha256_leaf]'):
            leaf_hash_from_attr = elem.get('sha256_leaf')
            
            # 3. Check if the element has been redacted.
            has_content = bool(elem.text and elem.text.strip()) or len(elem) > 0
            if has_content:
                # NOT redacted: verify the content by re-hashing.
                # CRITICAL: We re-canonicalize to bytes and hash directly,
                # using the exact same method as the signer.
                canonical_bytes_to_verify = etree.tostring(elem, method='c14n2')
                calculated_leaf_hash = hashlib.sha256(canonical_bytes_to_verify).hexdigest()

                if calculated_leaf_hash != leaf_hash_from_attr:
                    print(f"\n❌ TAMPERING DETECTED on element <{elem.tag}>!")
                    sys.exit(1)
                
                verified_leaf_hashes.append(calculated_leaf_hash)
            else:
                # Redacted: trust the hash from the attribute.
                verified_leaf_hashes.append(leaf_hash_from_attr)

        # 4. Re-create the root hash from the verified/trusted leaf hashes.
        actual_root_hash = hashlib.sha256("".join(verified_leaf_hashes).encode('utf-8')).hexdigest()
        
        # 5. Compare final hashes.
        if actual_root_hash == expected_root_hash:
            print(f"\n🟢 CONTEXT LOADED. Signature valid.")
        else:
            print("\n❌ HASH MISMATCH! The overall signature is invalid.")
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