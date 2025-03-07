import re
import argparse
import time
from ieee_utils import search_ieee, fetch_bibtex
from tqdm import tqdm


def parse_bib_file(bib_name):
    """Parses a .bib file and returns a dictionary of entries."""
    with open(bib_name, 'r', encoding='utf-8') as f:
        bib = f.read()

    bib_entries = {}
    current_entry = []
    current_key = None

    for line in bib.splitlines():
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
    """Extracts the title from a BibTeX entry."""
    match = re.search(r'\btitle\s*=\s*\{(.+?)\}', entry, re.IGNORECASE)
    return match.group(1) if match else None


def update_entry(original_key, original_entry):
    """Searches IEEE for the title, fetches the updated BibTeX, and keeps the original key."""
    title = extract_title(original_entry)
    if not title:
        return original_entry  # If no title, keep the original entry

    link = search_ieee(title, human_mode=False)
    if not link:
        return original_entry  # No valid link found, keep original

    bibtex = fetch_bibtex(link, human_mode=False)
    if not bibtex:
        return original_entry  # No valid BibTeX found, keep original

    # Replace the key in the new BibTeX with the original key
    updated_entry = re.sub(r'(@\w+\{)[^,]+', f'\1{original_key}', bibtex, count=1)
    return updated_entry


def batch_check(bib_name, num_entries=80):
    """Processes the first `num_entries` in the .bib file, updates them, and writes a new file."""
    bib_entries = parse_bib_file(bib_name)
    keys = list(bib_entries.keys())[:num_entries]
    updated_bib_entries = {}

    for key in tqdm(keys, desc="Updating BibTeX entries", unit="entry"):
        updated_bib_entries[key] = update_entry(key, bib_entries[key])
        time.sleep(1)  # Avoid being rate-limited by IEEE Xplore

    # Combine updated and unchanged entries
    updated_bib = '\n\n'.join(updated_bib_entries.values()) + '\n\n' + '\n\n'.join(
        [bib_entries[k] for k in bib_entries if k not in updated_bib_entries])

    updated_filename = 'updated_' + bib_name
    with open(updated_filename, 'w', encoding='utf-8') as f:
        f.write(updated_bib)

    print(f"Updated BibTeX saved as {updated_filename}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update BibTeX entries using IEEE Xplore.')
    parser.add_argument('bib_file', nargs='?', default='cleaned_ref.bib', help='The name of the bib file (default: ref.bib)')
    parser.add_argument('--num', type=int, default=60, help='Number of entries to check (default: 80)')
    args = parser.parse_args()

    batch_check(args.bib_file, args.num)
