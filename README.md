# Automated BibTeX Cleaner & Double-Checker

> Try it online: https://bibtex-clean-tool.streamlit.app/

Actually, After the repo is built, I find there are also many repo, like [bib-cleaner](https://bib-cleaner.readthedocs.io/en/latest/) and [bib-world](https://bib-world.com/unused), they can also remove duplicates and unused entries. I like the use case of the [bib-cleaner](https://bib-cleaner.readthedocs.io/en/latest/).

## Overview

Inspired by the cool repos [bibtex-tidy](https://github.com/FlamingTempura/bibtex-tidy) and [arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner), this repository automates the process of cleaning, organizing, and verifying `.bib` bibliography files. 

It consists of two primary components:

1. **BibTeX Cleaner & Formatter (`cleaner.py`)** - Reorders `.bib` entries based on citation order in the `.tex` file, removes duplicates, and appends unused references at the end. This is adapted from the repo [SFRL/clean_bibtex](https://github.com/SFRL/clean_bibtex).
2. **Double-Checker (`checker.py`)** - Searches IEEE Xplore for accurate BibTeX citations and updates `.bib` entries while preserving the original keys. This is necessary because sources like Google Scholar often have incorrect years, incomplete metadata, or lack authoritative information.

## Features

### Cleaner (`cleaner.py`)

- **Reorder `.bib` entries** according to citation order in the `.tex` file.
- **Add reference comments** (`% reference 01`, `% reference 02`, etc.) to track ordering.
- **Remove duplicate citations**, ensuring a concise bibliography.
- **Remove/Preserve unused entries**, appending them at the end for later use.

### Double-Checker (`checker.py`)

- **Automatically searche IEEE Xplore** for a given BibTeX title.
- **Fetch the latest BibTeX citation**, ensuring accurate metadata.
- **Maintain original BibTeX keys**, replacing only outdated information.
- **Process a configurable number of entries** (default: 60) with a progress bar.

## Installation

Ensure you have Python installed, then install dependencies:

```bash
pip install -r requirements.txt
```

You also need to install the appropriate WebDriver (e.g., ChromeDriver for Google Chrome) if using automated web scraping.

## Local Streamlit Usage

```bash
streamlit run app.py
```

## Command-Line Usage

### Running the Cleaner

```bash
python cleaner.py [bib_file] [tex_file]
```

- `bib_file` *(optional, default: ref.bib)*: Path to your `.bib` file.
- `tex_file` *(optional, default: main.tex)*: Path to your `.tex` file.

### Running the Double-Checker

```bash
python checker.py [bib_file] --num [number_of_entries]
```

- `bib_file` *(optional, default: cleaned_ref.bib)*: Path to your `.bib` file.
- `--num` *(optional, default: 60)*: Number of entries to check and update.
- `--remove_unselected`: Remove unselected entries.

---

## Contributing & Support

> Developed and tested on Apple M1, macOS Sonoma 14.7.3.

Feel free to open issues or pull requests if you encounter any problems or have suggestions for improvement. If you find this project useful, consider giving it a ⭐ on GitHub!

## Additional Notes

Actually, after the repo was built, I found that there are also many other repositories, like [bib-cleaner](https://bib-cleaner.readthedocs.io/en/latest/) and [bib-world](https://bib-world.com/unused), that can also remove duplicates and unused entries. I particularly like the use case of [bib-cleaner](https://bib-cleaner.readthedocs.io/en/latest/).

However, our tool provides more features, such as automatic ordering of `.bib` entries according to citation sequence, IEEE Xplore verification. Hope it helps you to some extent!!! 😊