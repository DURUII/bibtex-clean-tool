import regex as re  # Requires installation: pip install regex

def remove_textcolor(input_path, output_path, color="red"):
    """
    Processes a LaTeX file by replacing all occurrences of \textcolor{red}{...}
    with the inner content, correctly handling nested braces.

    Args:
        input_path (str): Path to the input .tex file.
        output_path (str): Path to the output .tex file.
    """
    # Read file content
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Loaded content from {input_path} (length: {len(content)} characters)")

    # Define a recursive pattern to match balanced braces.
    # (?P<braced>\{(?:[^{}]+|(?P>braced))*\}) matches nested curly braces.
    pattern = r'\\textcolor\{' + color+ r'\}(?P<braced>\{(?:[^{}]+|(?P>braced))*\})'

    def repl(match):
        """Replacement function that removes the outermost braces."""
        braced = match.group('braced')
        return braced[1:-1]  # Remove the outermost braces

    total_subs = 0
    # Loop replacements until no further substitutions are made.
    while True:
        content, num_subs = re.subn(pattern, repl, content)
        total_subs += num_subs
        print(f"Iteration substitution count: {num_subs}")
        if num_subs == 0:
            break

    print(f"Total substitutions performed: {total_subs}")

    # Write the processed content to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed content written to {output_path}")