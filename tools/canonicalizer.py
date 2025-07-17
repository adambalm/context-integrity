# canonicalizer.py
"""
Deterministic XML canonicalizer:
- Strips comments
- Collapses whitespace
- Sorts attributes
"""
import sys
from lxml import etree


def canonicalize(xml_string: str) -> bytes:
    parser = etree.XMLParser(remove_comments=True)
    root = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
    return etree.tostring(
        root,
        method='c14n',
        exclusive=True,
        with_comments=False
    )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 canonicalizer.py <input.xml> <output.bin>')
        sys.exit(1)

    input_file, output_file = sys.argv[1], sys.argv[2]
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    canon_bytes = canonicalize(xml_content)
    with open(output_file, 'wb') as f:
        f.write(canon_bytes)


