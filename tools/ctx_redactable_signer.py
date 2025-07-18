# filename: ctx_redactable_signer.py
"""
Enhanced Redactable Signing Tool (Encoding-Hardened):
- Reads an XML file, assuming UTF-8 encoding.
- Traverses the XML tree, computing a SHA-256 hash for each element's canonical byte representation.
- Stores each "leaf hash" in a 'sha256_leaf' attribute.
- Computes a final "root hash" from the concatenated leaf hashes.
- Writes the fully signed, redactable XML to an output file, explicitly as UTF-8.
"""
import sys
import hashlib
from lxml import etree

def create_redactable_signature(input_path: str, output_path: str) -> None:
    """Signs an XML file in a way that makes individual elements redactable."""
    try:
        parser = etree.XMLParser(remove_comments=True)
        tree = etree.parse(input_path, parser)
        root = tree.getroot()

        # Remove any pre-existing main signature to avoid hashing it.
        old_sig = root.find('sha256')
        if old_sig is not None:
            root.remove(old_sig)

        leaf_hashes = []
        
        # Iterate over every element to create its leaf hash.
        for elem in root.xpath('.//*[not(self::sha256)]'):
            # Canonicalize with the same C14N method used in the loader
            c14n_bytes = etree.tostring(elem, method='c14n')
            
            # Hash those bytes directly
            leaf_hash = hashlib.sha256(c14n_bytes).hexdigest()
            
            elem.set('sha256_leaf', leaf_hash)
            leaf_hashes.append(leaf_hash)

        # Combine all the leaf hashes to create the root hash.
        combined_hashes_str = "".join(leaf_hashes)
        root_hash = hashlib.sha256(combined_hashes_str.encode('utf-8')).hexdigest()

        # Create the main signature element with the root hash.
        sha_elem = etree.Element('sha256')
        sha_elem.text = root_hash
        root.append(sha_elem)

        # Write the file with explicit UTF-8 encoding and XML declaration.
        tree.write(
            output_path,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        )
        print(f"Redactable signed context written to {output_path}")

    except FileNotFoundError:
        print(f" ERROR: Input file not found at '{input_path}'")
        sys.exit(1)
    except etree.XMLSyntaxError as e:
        print(f" ERROR: Input file '{input_path}' is not well-formed XML. Details: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ctx_redactable_signer.py <input_unsigned.xml> <output_signed.xml>')
        sys.exit(1)
    create_redactable_signature(sys.argv[1], sys.argv[2])

