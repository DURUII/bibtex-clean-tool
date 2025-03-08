import re
import argparse
import time
import os  # Add if not already imported
from utils.ieee import search_ieee, fetch_bibtex
from utils.bib import parse_bib_file, extract_title
from tqdm import tqdm


def update_entry(original_key, original_entry):
    """Searches IEEE for the title, fetches the updated BibTeX, and keeps the original key.

    Args:
        original_key (str): The original key of the BibTeX entry.
        original_entry (str): The original BibTeX entry.

    Returns:
        str: The updated BibTeX entry with the original key, or the original entry if no update is found.
    """
    title = extract_title(original_entry)
    print(title)
    if not title:
        return original_entry  # If no title, keep the original entry

    link = search_ieee(title, human_mode=False)
    if not link:
        return original_entry  # No valid link found, keep original

    bibtex = fetch_bibtex(link, human_mode=False)
    if not bibtex:
        return original_entry  # No valid BibTeX found, keep original

    # Replace the key in the new BibTeX
    updated_entry = re.sub(r'(@\w+\{)[^,]+', rf'\g<1>{original_key}', bibtex, count=1)
    return updated_entry


def batch_check(bib_name, num_entries=60, keep_unselected=True):  # changed code: added keep_unselected parameter
    """Processes the first `num_entries` in the .bib file, updates them,
       and writes a new file. Optionally keeps unselected entries.
    """
    bib_entries = parse_bib_file(bib_name)

    keys = list(bib_entries.keys())[:num_entries]
    updated_bib_entries = {}

    for key in tqdm(keys, desc="Updating BibTeX entries", unit="entry"):
        updated_bib_entries[key] = update_entry(key, bib_entries[key])
        time.sleep(1)  # Avoid being rate-limited by IEEE Xplore

    # Combine updated entries and add unchanged ones if keep_unselected is True
    updated_bib = '\n\n'.join(updated_bib_entries.values())
    if keep_unselected:
        unchanged = [bib_entries[k] for k in bib_entries if k not in updated_bib_entries]
        if unchanged:
            updated_bib += '\n\n' + '\n\n'.join(unchanged)

    updated_filename = 'updated_' + os.path.basename(bib_name)
    with open(updated_filename, 'w', encoding='utf-8') as f:
        f.write(updated_bib)

    print(f"Updated BibTeX saved as {updated_filename}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update BibTeX entries using IEEE Xplore.')
    parser.add_argument('bib_file', nargs='?', default='cleaned_ref.bib', help='The name of the bib file (default: ref.bib)')
    parser.add_argument('--num', type=int, default=60, help='Number of entries to check (default: 60)')
    parser.add_argument('--remove_unselected', action='store_true', help='Remove unselected entries')  # changed code
    args = parser.parse_args()
    keep_unselected = not args.remove_unselected  # changed code
    batch_check(args.bib_file, args.num, keep_unselected)  # changed code
