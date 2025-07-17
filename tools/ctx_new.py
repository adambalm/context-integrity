# ctx_new.py
"""
Signing tool:
- Reads an XML file
- Removes existing <sha256>
- Canonicalizes the rest
- Computes SHA-256 digest
- Injects <sha256> element
- Writes signed XML to output
"""
import sys
import hashlib
from lxml import etree
from canonicalizer import canonicalize


def sign_context(input_path: str, output_path: str) -> None:
    parser = etree.XMLParser(remove_comments=True)
    tree = etree.parse(input_path, parser)
    root = tree.getroot()

    # Remove old signature
    old = root.find('sha256')
    if old is not None:
        root.remove(old)

    # Serialize without <sha256>
    xml_bytes = etree.tostring(root, encoding='utf-8').decode('utf-8')
    canon_bytes = canonicalize(xml_bytes)

    digest = hashlib.sha256(canon_bytes).hexdigest()
    sha_elem = etree.Element('sha256')
    sha_elem.text = digest
    root.append(sha_elem)

    # Write signed XML
    tree.write(
        output_path,
        encoding='utf-8',
        xml_declaration=True,
        pretty_print=True
    )
    print(f'Signed context written to {output_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ctx_new.py <input.xml> <output.xml>')
        sys.exit(1)

    sign_context(sys.argv[1], sys.argv[2])
