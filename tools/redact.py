# filename: redact.py
"""
Enhanced Redaction Tool (Encoding-Hardened):
- Reads a redactable XML artifact, assuming UTF-8.
- Removes text content from specified tags.
- Writes the redacted XML to an output file, explicitly as UTF-8.
"""
import sys
from lxml import etree

def redact_fields(input_path: str, output_path: str, fields_to_redact: list) -> None:
    """Removes the content of specified XML elements."""
    try:
        # Assume the input file is UTF-8, as written by our signer.
        parser = etree.XMLParser(remove_comments=True)
        tree = etree.parse(input_path, parser)
        root = tree.getroot()

        for field_name in fields_to_redact:
            elements = root.findall(f'.//{field_name}')
            if not elements:
                print(f"🟡 Warning: No elements found with tag '{field_name}' to redact.")
                continue
            
            for elem in elements:
                # This is the redaction. We set the text content to None.
                # This leaves the tag and all its attributes (like sha256_leaf) in place.
                elem.text = None
                print(f"  - Redacted content of <{field_name}>")

        # CRITICAL: Write the redacted file with explicit UTF-8 encoding
        # to maintain consistency for the verifier.
        tree.write(
            output_path,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        )
        print(f"✅ Redacted file saved to {output_path}")

    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{input_path}'")
        sys.exit(1)
    except etree.XMLSyntaxError as e:
        print(f"❌ ERROR: Input file '{input_path}' is not well-formed XML. Details: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 redact.py <input_signed.xml> <output_redacted.xml> <tags_to_redact>')
        print('Example: python3 redact.py signed.xml redacted.xml date,os,python')
        sys.exit(1)
        
    tags = sys.argv[3].split(',')
    redact_fields(sys.argv[1], sys.argv[2], tags)
