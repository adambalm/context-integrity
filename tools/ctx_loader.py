# ctx_loader.py
"""
Loader and verifier:
- Re-canonicalizes XML (excluding <sha256>)
- Validates SHA-256 hash
- Emits 🟢 CONTEXT LOADED or exits on violation
"""
import sys
import hashlib
from lxml import etree
from canonicalizer import canonicalize


def load_and_verify(file_path: str) -> None:
    tree = etree.parse(file_path)
    root = tree.getroot()

    sha_elem = root.find('sha256')
    if sha_elem is None or not sha_elem.text:
        print('❌ No <sha256> element found.')
        sys.exit(1)

    expected = sha_elem.text.strip()
    root.remove(sha_elem)

    # Serialize without SHA element
    xml_bytes = etree.tostring(root, encoding='utf-8').decode('utf-8')
    canon_bytes = canonicalize(xml_bytes)

    actual = hashlib.sha256(canon_bytes).hexdigest()
    if actual != expected:
        print(f'❌ Hash mismatch! Expected {expected}, got {actual}.')
        sys.exit(1)

    print('🟢 CONTEXT LOADED')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 ctx_loader.py <signed_context.xml>')
        sys.exit(1)

    load_and_verify(sys.argv[1])


