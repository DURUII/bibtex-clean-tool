import re


def parse_bib_file(bib_name):
    """Parses a .bib file and returns a dictionary of entries.

    Args:
        bib_name (str): The name of the .bib file.

    Returns:
        dict: A dictionary where keys are entry keys and values are BibTeX entries.
    """
    with open(bib_name, 'r', encoding='utf-8') as f:
        bib = f.read()

    bib_entries = {}
    current_entry = []
    current_key = None

    for line in bib.splitlines():
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

    return bib_entries


def extract_title(entry):
    """Extracts the title from a BibTeX entry.

    Args:
        entry (str): A BibTeX entry.

    Returns:
        str: The title of the entry, or None if no title is found.
    """
    match = re.search(r'\btitle\s*=\s*\{(.+?)\}', entry, re.IGNORECASE)
    return match.group(1) if match else None
