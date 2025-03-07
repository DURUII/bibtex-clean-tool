import re
import argparse


def main(bib_name, tex_name, keep_unused):
    """Main function to clean and reorder bib entries based on citations in the tex file.

    Args:
        bib_name (str): The name of the bib file.
        tex_name (str): The name of the tex file.
        keep_unused (bool): Whether to keep unused entries.
    """
    # Load bib file from local directory
    with open(bib_name, 'r') as f:
        bib = f.read()

    # Load tex file from local directory
    with open(tex_name, 'r') as f:
        tex = f.read()

    # Delete empty citations from tex file
    tex = re.sub(r'\\citeA\{\}', '', tex)
    tex = re.sub(r'\\cite\{\}', '', tex)

    # Get all citations from tex file
    citations = [*re.findall(r'\\cite\{(.+?)\}', tex), *re.findall(r'\\citeA\{(.+?)\}', tex)]

    # Remove duplicates while preserving order
    seen = set()
    ordered_citations = []
    for entries in citations:
        # Split citations that are separated by comma
        if ',' in entries:
            entries = entries.replace(' ', '')
            entries = entries.split(',')
        else:
            entries = [entries]

        for entry in entries:
            entry = entry.strip()
            if entry in seen:
                continue
            seen.add(entry)
            ordered_citations.append(entry)
    citations = ordered_citations

    seen = set()
    citations = [x for x in citations if not (x in seen or seen.add(x))]

    # Clean the bib file by removing comments and empty lines between entries
    bib = re.sub(r'(?m)^\s*%.*\n?', '', bib)  # Remove comments
    bib = re.sub(r'\n\s*\n', '\n', bib)  # Remove multiple empty lines

    # Go through bib file line by line and store entries in a dictionary
    bib = bib.splitlines()
    bib_entries = {}
    current_entry = []
    current_key = None
    for line in bib:
        if line.startswith('%'):
            continue  # Skip comment lines
        if line.startswith('@'):
            if current_key:
                bib_entries[current_key] = '\n'.join(current_entry)
            current_key = line.split('{')[1].split(',')[0]
            current_entry = [line]
        else:
            current_entry.append(line)
    if current_key:
        bib_entries[current_key] = '\n'.join(current_entry)

    # Reorder bib entries according to the order of citations in the tex file
    cleaned_bib = []
    reference_count = 1
    for citation in citations:
        if citation in bib_entries:
            cleaned_bib.append(f'% reference {reference_count}\n{bib_entries[citation]}')
            del bib_entries[citation]
            reference_count += 1

    # Add remaining bib entries that were not cited if keep_unused is True
    if keep_unused:
        reference_count = 1
        for entry in bib_entries.values():
            cleaned_bib.append(f'% unused {reference_count}\n{entry}')
            reference_count += 1

    # Join bib file again including line breaks
    cleaned_bib = '\n\n'.join(cleaned_bib)

    # Save cleaned bib file to local directory
    with open('cleaned_' + bib_name, 'w') as f:
        f.write(cleaned_bib)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean and reorder bib entries based on citations in the tex file.')
    parser.add_argument('bib_file', nargs='?', default='ref.bib', help='The name of the bib file (default: ref.bib)')
    parser.add_argument('tex_file', nargs='?', default='main.tex', help='The name of the tex file (default: main.tex)')
    parser.add_argument('--keep', action='store_true', help='Keep unused entries in the cleaned bib file')
    args = parser.parse_args()

    main(args.bib_file, args.tex_file, args.keep)
