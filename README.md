# Automated BibTeX Cleaner & Double-Checker

## Overview

This repository automates the process of cleaning, organizing, and verifying `.bib` bibliography files. It consists of two primary components:

1. **BibTeX Cleaner & Formatter (`cleaner.py`)** - Reorders `.bib` entries based on citation order in the `.tex` file, removes duplicates, and appends unused references at the end. This is adapted from the repo [SFRL/clean_bibtex](https://github.com/SFRL/clean_bibtex)
2. **Double-Checker (`checker.py`)** - Searches IEEE Xplore for accurate BibTeX citations and updates `.bib` entries while preserving the original keys. This is necessary because sources like Google Scholar often have incorrect years, incomplete metadata, or lack authoritative information.

## Features

### Cleaner (`cleaner.py`)

- **Reorders `.bib` entries** according to citation order in the `.tex` file.
- **Adds reference comments** (`% reference 01`, `% reference 02`, etc.) to track ordering.
- **Removes duplicate citations**, ensuring a concise bibliography.
- **Preserves unused entries**, appending them at the end for later use.

### Double-Checker (`checker.py`)

- **Automatically searches IEEE Xplore** for a given BibTeX title.
- **Fetches the latest BibTeX citation**, ensuring accurate metadata.
- **Maintains original BibTeX keys**, replacing only outdated information.
- **Processes a configurable number of entries** (default: 60) with a progress bar.

## Installation

Ensure you have Python installed, install dependencies:

```bash
pip install -r requirements.txt
```

You also need to install the appropriate WebDriver (e.g., ChromeDriver for Google Chrome) if using automated web scraping.

## Usage

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

---

## Contributing & Support

Feel free to open issues or pull requests if you encounter any problems or have suggestions for improvement. If you find this project useful, consider giving it a ⭐ on GitHub!