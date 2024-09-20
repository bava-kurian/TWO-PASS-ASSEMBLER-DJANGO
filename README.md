# TWO-PASS-ASSEMBLER-PYTHON-TKINTER-GUI

Here’s a sample `README.md` file for your GitHub repository based on the two-pass assembler program implemented in Python with a Tkinter-based GUI:

---

# Two-Pass Assembler with Tkinter GUI

This project implements a **Two-Pass Assembler** for a hypothetical assembly language using Python. It provides a GUI (built with Tkinter) for users to load assembly files and an operation table (OPTAB), and generate an **intermediate file**, a **symbol table**, and **machine code**.

## Features

- **Pass 1**: Generates an intermediate file and a symbol table (SYMTAB) by parsing the assembly file.
- **Pass 2**: Produces machine code from the intermediate file and symbol table.
- **Graphical User Interface (GUI)**: Built with Tkinter, allowing users to:
  - Load an OPTAB file.
  - Load an assembly code input file.
  - Generate and view the intermediate file, symbol table, and machine code.

## Requirements

- **Python 3.x**
- **Tkinter** (Included with most Python installations)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/two-pass-assembler.git
   ```

2. Navigate into the project directory:

   ```bash
   cd two-pass-assembler
   ```

3. Install dependencies (if needed):
   - Tkinter should already be installed with Python, but if not, you can install it using:
     ```bash
     sudo apt-get install python3-tk  # On Ubuntu/Debian
     ```

## Usage

1. Run the Python program:

   ```bash
   python assembler.py
   ```

2. Load an **OPTAB file** (a text file that maps mnemonics to opcodes, one per line) by clicking the "Browse" button under "Load OPTAB file".

3. Load an **assembly input file** (your assembly code in a text file) by clicking the "Browse" button under "Load Assembly Input file".

4. Click the **"Assemble"** button to start the assembly process. The results (intermediate file and machine code) will be displayed in the GUI.

## File Formats

### OPTAB file

The OPTAB (Operation Table) file should contain mnemonic-opcode mappings in the following format (one mnemonic per line):

```
LDA 00
STA 0C
ADD 18
SUB 1C
```

### Assembly Input File

The input assembly file should contain assembly instructions. A simple example might look like:

```
COPY    START  1000
FIRST   LDA    ALPHA
        ADD    BETA
        STA    GAMMA
ALPHA   WORD   1
BETA    WORD   2
GAMMA   RESW   1
        END    FIRST
```

### Intermediate File and Machine Code

The **intermediate file** and **machine code** will be generated after assembly and displayed in the GUI.

## Screenshots

### Main Window

![Main Window](path_to_screenshot.png)

## Future Enhancements

- Add support for more complex assembly directives and pseudo-operations.
- Improve error handling for unsupported mnemonics and invalid operands.
- Add a feature to save the output to a file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin feature/my-new-feature`.
5. Submit a pull request!

---

Feel free to replace `"yourusername"` with your actual GitHub username and update the image path if you add screenshots to your repository.
