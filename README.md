

# Two-Pass Assembler GUI Documentation

## Overview

This program simulates a two-pass assembler using a graphical user interface (GUI) built with the Tkinter library. The assembler reads a source program (input file) and an opcode table, processes the program in two passes, and generates machine code and symbol tables. The GUI allows the user to upload input and opcode files, view the intermediate results and machine code, and save the machine code to a file.

---

## Features

- **Upload Input File**: Select a source assembly program file.
- **Upload Opcode Table**: Select an opcode table file containing opcodes and their corresponding hex codes.
- **Start Assembling**: Once both files are uploaded, this button becomes active. It runs the assembler logic to generate intermediate code (Pass 1) and machine code (Pass 2).
- **View Results**: The GUI provides four text areas displaying:
  1. **Input File Content**: The original content of the uploaded input file.
  2. **Intermediate Code (Pass 1)**: The intermediate output after Pass 1, including the label, opcode, operand, and LOCCTR (location counter) values.
  3. **Machine Code (Pass 2)**: The final machine code generated after Pass 2, including object codes and records.
  4. **Symbol Table**: The generated symbol table containing labels and their associated addresses.
- **Save Output**: Save the final machine code to a file for future use.
- **Progress Bar**: Provides visual feedback for the progress of the assembly process.

---

## GUI Components

### 1. **Top Frame**

This section contains the buttons for uploading files and labels showing the names of the uploaded files.
- **Input File Label**: Displays the name of the uploaded input file.
- **Opcode Table Label**: Displays the name of the uploaded opcode table.
- **Upload Input File Button**: Opens a file dialog for selecting the input file.
- **Upload Opcode Table Button**: Opens a file dialog for selecting the opcode table file.

### 2. **Middle Frame**

This section contains the buttons to start the assembly process and save the output, as well as a progress bar.
- **Start Button**: Starts the assembly process, enabling the generation of the intermediate code and machine code.
- **Save Output Button**: Enables after the assembly process is complete, allowing the user to save the final machine code to a file.
- **Progress Bar**: Displays the progress of the assembly process.

### 3. **Bottom Frame**

This section contains four labeled text boxes for viewing different parts of the assembly process.
- **Input File Content Text Box**: Displays the raw content of the uploaded input file.
- **Intermediate Code (Pass 1) Text Box**: Displays the intermediate code after Pass 1 (label, opcode, operand, and LOCCTR values).
- **Machine Code (Pass 2) Text Box**: Displays the final machine code after Pass 2.
- **Symbol Table Text Box**: Displays the symbol table with labels and their associated addresses.

---

## Assembly Process

### 1. **Pass 1 (Intermediate Code Generation)**
The first pass of the assembler generates intermediate code by reading each line of the source program, calculating the location counter (LOCCTR), and updating the symbol table with labels and their addresses. It also identifies the starting address and processes directives like `START`, `WORD`, `RESW`, `RESB`, and `BYTE`.

### 2. **Pass 2 (Machine Code Generation)**
The second pass generates machine code by converting each opcode to its corresponding object code using the opcode table, resolving symbol addresses for operands, and generating text records, header records, and the end record.

### 3. **Symbol Table Generation**
The symbol table is created during Pass 1. Each label encountered in the source program is added to the symbol table along with its address (calculated by the LOCCTR).

---

## Code Documentation

### 1. **Class `AssemblerGUI`**

The main class responsible for the GUI and the functionality of the two-pass assembler.

### 2. **Initialization (`__init__`)**
Initializes the GUI components and member variables used in the assembly process.

- **self.master**: The root window of the Tkinter application.
- **self.input_file_content**: Stores the content of the uploaded input file.
- **self.optab_file_content**: Stores the content of the uploaded opcode table.
- **self.opcode_list**: List of opcodes extracted from the opcode table.
- **self.opcode_hex**: Dictionary that maps opcodes to their hexadecimal equivalents.
- **self.sym_list**: List of labels encountered during assembly.
- **self.sym_addresses**: List of corresponding addresses for the labels.
- **self.locctr**: Location counter, used to track the address of each instruction.
- **self.starting_address**: Stores the starting address of the program.
- **self.end_address**: Stores the ending address of the program after Pass 2.

### 3. **Creating Widgets (`create_widgets`)**
Defines the structure of the GUI, including labels, buttons, and text areas for displaying output.

### 4. **File Upload Functions**
- **`upload_input_file`**: Opens a file dialog to select the input file and displays its content in the Input File Content text box.
- **`upload_optab_file`**: Opens a file dialog to select the opcode table and processes the opcode contents.

### 5. **Process Files**
- **`check_files_and_enable_button`**: Ensures both files are uploaded before enabling the Start button.
- **`process_file_content`**: Processes the input file content during Pass 1 to generate intermediate code and symbol table. Updates the progress bar as it processes each line.
- **`pass2`**: Executes the second pass of the assembler to generate the machine code based on the intermediate code and symbol table.

### 6. **Generate Object Code**
- **`generate_records`**: Generates the header, text, and end records of the machine code and displays them in the machine code text box.

### 7. **Save Output**
- **`save_output_file`**: Allows the user to save the machine code output to a file.

---

## How to Use

1. **Upload Files**: 
   - Click "Upload Input File" to select the assembly program file.
   - Click "Upload Opcode Table File" to select the opcode table file.
2. **Start Assembling**: 
   - Once both files are uploaded, click "Start" to process the input file. The intermediate code, machine code, and symbol table will be displayed in the respective text boxes.
3. **Save Machine Code**: 
   - Click "Save Output" to save the generated machine code to a file.
4. **View Progress**: 
   - The progress bar will indicate the progress during file processing.

---

## File Format Requirements

### Input File Format
The input file must follow standard assembly program syntax, where each line contains:
- Label
- Opcode
- Operand

### Opcode Table Format
The opcode table file must contain opcodes and their corresponding hexadecimal values in the format:
```
<opcode> <hexcode>
```

---

## Conclusion

This GUI-based two-pass assembler provides an interactive way for users to assemble programs, view intermediate results, and save the final machine code. By separating the input file, intermediate code, machine code, and symbol table into distinct sections, the program makes the assembly process easy to follow and debug.

