import re
import argparse
import os
from utils.textcolor import remove_textcolor

def wrap_first_word_in_title(entry):
    """Wraps the first word in the title field of a BibTeX entry with \text{}.

    Args:
        entry (str): A single BibTeX entry.

    Returns:
        str: The modified BibTeX entry.
    """
    pattern = r'(title\s*=\s*{)(\S+)'
    return re.sub(pattern, r'\1\\text{\2}', entry, count=1)

def extract_citations(tex):
    """Extracts all citation keys from a LaTeX file.

    Args:
        tex (str): Contents of the .tex file.

    Returns:
        list: Ordered list of citation keys without duplicates.
    """
    tex = re.sub(r'\\citeA\{\}', '', tex)
    tex = re.sub(r'\\cite\{\}', '', tex)

    raw_citations = re.findall(r'\\cite\{(.+?)\}', tex) + re.findall(r'\\citeA\{(.+?)\}', tex)
    seen = set()
    ordered = []

    for entries in raw_citations:
        for entry in entries.replace(' ', '').split(','):
            if entry and entry not in seen:
                seen.add(entry)
                ordered.append(entry)
    return ordered

def parse_bib_entries(bib):
    """Parses BibTeX entries into a dictionary.

    Args:
        bib (str): Raw contents of a .bib file.

    Returns:
        dict: Mapping from citation key to full BibTeX entry.
    """
    bib = re.sub(r'(?m)^\s*%.*\n?', '', bib)  # Remove comments
    bib = re.sub(r'\n\s*\n', '\n', bib)      # Remove empty lines
    bib_lines = bib.splitlines()

    entries = {}
    current = []
    key = None
    for line in bib_lines:
        if line.startswith('@'):
            if key:
                entries[key] = '\n'.join(current)
            key = line.split('{')[1].split(',')[0]
            current = [line]
        else:
            current.append(line)
    if key:
        entries[key] = '\n'.join(current)
    return entries

def write_cleaned_bib(entries, ordered_keys, wrap_text, keep_unused):
    """Generates a cleaned BibTeX content.

    Args:
        entries (dict): All parsed BibTeX entries.
        ordered_keys (list): Citation keys in order of appearance.
        wrap_text (bool): Whether to wrap the first word in the title.
        keep_unused (bool): Whether to include uncited entries.

    Returns:
        str: Cleaned BibTeX content.
    """
    cleaned = []
    ref_count = 1

    for key in ordered_keys:
        if key in entries:
            entry = entries.pop(key)
            if wrap_text:
                entry = wrap_first_word_in_title(entry)
            cleaned.append(f'% reference {ref_count}\n' + entry)
            ref_count += 1

    if keep_unused:
        for i, entry in enumerate(entries.values(), 1):
            if wrap_text:
                entry = wrap_first_word_in_title(entry)
            cleaned.append(f'% unused {i}\n' + entry)

    return '\n\n'.join(cleaned)

def save_cleaned_files(bib_name, tex_name, bib_content, remove_review_textcolor):
    """Saves cleaned bib and tex files, with optional cleanup.

    Args:
        bib_name (str): Original .bib filename.
        tex_name (str): Original .tex filename.
        bib_content (str): Cleaned bib content.
        remove_review_textcolor (bool): If True, remove color markup.
    """
    cleaned_bib = 'cleaned_' + os.path.basename(bib_name)
    cleaned_tex = 'cleaned_' + os.path.basename(tex_name)

    with open(cleaned_bib, 'w') as f:
        f.write(bib_content)

    if remove_review_textcolor:
        remove_textcolor(cleaned_bib, cleaned_bib)
        remove_textcolor(tex_name, cleaned_tex)
    else:
        with open(tex_name, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        with open(cleaned_tex, 'w', encoding='utf-8') as f:
            f.write(tex_content)

def main(bib_name, tex_name, keep_unused, wrap_text=False, remove_review_textcolor=False):
    """Main processing function for cleaning BibTeX entries.

    Args:
        bib_name (str): Input .bib filename.
        tex_name (str): Input .tex filename.
        keep_unused (bool): Whether to retain uncited entries.
        wrap_text (bool, optional): Wrap the first word of the title field. Defaults to False.
        remove_review_textcolor (bool, optional): Clean textcolor markup. Defaults to False.
    """
    with open(bib_name, 'r') as f:
        bib_raw = f.read()
    with open(tex_name, 'r') as f:
        tex_raw = f.read()

    citations = extract_citations(tex_raw)
    bib_entries = parse_bib_entries(bib_raw)
    cleaned_bib = write_cleaned_bib(bib_entries, citations, wrap_text, keep_unused)
    save_cleaned_files(bib_name, tex_name, cleaned_bib, remove_review_textcolor)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean and reorder bib entries based on citations in the tex file.')
    parser.add_argument('bib_file', nargs='?', default='ref.bib', help='BibTeX file name (default: ref.bib)')
    parser.add_argument('tex_file', nargs='?', default='main.tex', help='TeX file name (default: main.tex)')
    parser.add_argument('--keep', action='store_true', help='Keep uncited entries in the cleaned .bib file')
    parser.add_argument('--wrap-text', action='store_true', help='Wrap first word in title with \\text{}')
    parser.add_argument('--remove-review-textcolor', action='store_true', help='Remove textcolor markup from files')

    args = parser.parse_args()
    main(args.bib_file, args.tex_file, args.keep, args.wrap_text, args.remove_review_textcolor)
