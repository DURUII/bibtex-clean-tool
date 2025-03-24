import re
import argparse
import os  # Added import if not already present
from utils.textcolor import remove_textcolor  # modified import

# New helper function to wrap the first word in the title field
def wrap_first_word_in_title(entry):
    # Feature Description:
    # This function modifies a BibTeX entry by adding \text{} around the first word in the title field to ensure proper formatting in LaTeX-rendered citations.
    pattern = r'(title\s*=\s*{)(\S+)'
    return re.sub(pattern, r'\1\\text{\2}', entry, count=1)


def main(bib_name, tex_name, keep_unused, wrap_text=False, remove_review_textcolor=False):  # modified signature
    """Main function to clean and reorder bib entries based on citations in the tex file.

    Args:
        bib_name (str): The name of the bib file.
        tex_name (str): The name of the tex file.
        keep_unused (bool): Whether to keep unused entries.
        wrap_text (bool, optional): If True, wraps the first word in the title field with \text{}.
        remove_review_textcolor (bool, optional): If True, removes textcolor commands from the tex file.
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
            entry = bib_entries[citation]
            if wrap_text:
                entry = wrap_first_word_in_title(entry)
            cleaned_bib.append(f'% reference {reference_count}\n' + entry)
            del bib_entries[citation]
            reference_count += 1

    # Add remaining bib entries that were not cited if keep_unused is True
    if keep_unused:
        reference_count = 1
        for entry in bib_entries.values():
            if wrap_text:
                entry = wrap_first_word_in_title(entry)
            cleaned_bib.append(f'% unused {reference_count}\n' + entry)
            reference_count += 1

    # Join bib file again including line breaks
    cleaned_bib = '\n\n'.join(cleaned_bib)

    # Save cleaned bib file to local directory
    cleaned_file = 'cleaned_' + os.path.basename(bib_name)  # changed code
    with open(cleaned_file, 'w') as f:  # changed code
        f.write(cleaned_bib)
    
    # New change: Process tex file if remove_review_textcolor flag is set
    if remove_review_textcolor:
        cleaned_tex = 'cleaned_' + os.path.basename(tex_name)
        remove_textcolor(tex_name, cleaned_tex)  # call helper from utils/textcolor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean and reorder bib entries based on citations in the tex file.')
    parser.add_argument('bib_file', nargs='?', default='ref.bib', help='The name of the bib file (default: ref.bib)')
    parser.add_argument('tex_file', nargs='?', default='main.tex', help='The name of the tex file (default: main.tex)')
    parser.add_argument('--keep', action='store_true', help='Keep unused entries in the cleaned bib file')
    parser.add_argument('--wrap-text', action='store_true', help="Wrap the first word in the title field with \\text{} for proper LaTeX formatting.")
    # New argument:
    parser.add_argument('--remove-review-textcolor', action='store_true', help='Remove textcolor commands from the tex file')
    
    args = parser.parse_args()

    main(args.bib_file, args.tex_file, args.keep, args.wrap_text, args.remove_review_textcolor)
