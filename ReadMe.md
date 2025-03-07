# BibTeX Cleaner & Formatter

## Clean & Reorder

> This is adapted from the repo [SFRL/clean_bibtex](https://github.com/SFRL/clean_bibtex)

Manually maintaining `.bib` files is time-consuming, especially when working with long research papers with dozens or even hundreds of citations.

This Python script `cleaner.py` automates the cleaning and reordering of `.bib` bibliography files based on citation usage in a corresponding LaTeX (`.tex`) document. It ensures that your bibliography entries are neatly organized, appear in the order they're cited, and are easily verifiable.

- **Automatically organizes `.bib` entries** according to their citation order in the `.tex` file.
- **Adds numbered reference comments** (`% reference 01`, `% reference 02`, etc.) to each entry, making it easier to cross-check with the final PDF.
- **Removes  duplicate citations**, keeping the `.bib` file clean and concise.
- **Preserves unreferenced entries**, appending them at the end for potential later use.


### Usage

```bash
python script.py [-h] [bib_file] [tex_file]
```

- `bib_file` *(optional, default: ref.bib)*: Path to your `.bib` bibliography file.
- `tex_file` *(optional, default: main.tex)*: Path to your `.tex` file containing LaTeX citations.