import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Global variables
optab = {}
input_content = ""
symtab = {}
intermediate_file_content = ""

# Function to load OPTAB from file
def load_optab():
    global optab
    file_path = filedialog.askopenfilename(title="Select OPTAB file", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            optab.clear()
            for line in f:
                opcode, machine_code = line.strip().split()
                optab[opcode] = machine_code
        optab_display.delete(1.0, tk.END)
        optab_display.insert(tk.END, f"Loaded OPTAB:\n{optab}")
        messagebox.showinfo("Success", "OPTAB loaded successfully!")

# Function to load input assembly file
def load_input_file():
    global input_content
    file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            input_content = f.read()
        input_file_display.delete(1.0, tk.END)
        input_file_display.insert(tk.END, input_content)
        messagebox.showinfo("Success", "Input file loaded successfully!")

# Function to perform Pass 1
def pass_one():
    global intermediate_file_content, symtab
    if not optab or not input_content:
        messagebox.showerror("Error", "Please load the input file and OPTAB first.")
        return
    
    lines = input_content.strip().splitlines()
    locctr = 0
    intermediate_file_content = ""
    symtab = {}

    output_content = []
    starting_address = 0

    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            label, opcode, operand = parts
        else:
            label = ""
            opcode, operand = parts
        
        # Process START directive
        if opcode == "START":
            locctr = int(operand, 16)
            starting_address = locctr
            output_content.append(f"{locctr:04X} {label} {opcode} {operand}")
            continue

        # Add to SYMTAB if label exists
        if label:
            if label in symtab:
                messagebox.showerror("Error", f"Duplicate symbol {label} found.")
                return
            symtab[label] = f"{locctr:04X}"

        # Handle different directives and opcodes
        if opcode in optab:
            locctr += 3
        elif opcode == "WORD":
            locctr += 3
        elif opcode == "RESW":
            locctr += 3 * int(operand)
        elif opcode == "RESB":
            locctr += int(operand)
        elif opcode == "BYTE":
            if operand.startswith("C'"):
                locctr += len(operand) - 3
            elif operand.startswith("X'"):
                locctr += (len(operand) - 3) // 2
        elif opcode == "END":
            output_content.append(f"{locctr:04X} {label} {opcode} {operand}")
            break
        else:
            messagebox.showerror("Error", f"Invalid opcode {opcode} on line {line}.")
            return
        
        # Append line to intermediate content
        output_content.append(f"{locctr:04X} {label} {opcode} {operand}")
    
    # Store intermediate content and display it
    intermediate_file_content = "\n".join(output_content)
    intermediate_file_display.delete(1.0, tk.END)
    intermediate_file_display.insert(tk.END, intermediate_file_content)

    # Display SYMTAB
    symtab_display.delete(1.0, tk.END)
    symtab_display.insert(tk.END, f"Generated SYMTAB:\n{symtab}")
    
    messagebox.showinfo("Success", "Pass 1 completed. Intermediate file and SYMTAB generated.")

# Function to perform Pass 2
def pass_two():
    if not intermediate_file_content or not symtab or not optab:
        messagebox.showerror("Error", "Please run Pass 1 to generate the intermediate file and SYMTAB.")
        return

    output_content = ""
    lines = intermediate_file_content.strip().splitlines()[1:]  # Skip START line
    starting_address = None
    program_length = 0
    object_code = []
    object_count = 0

    # Process the intermediate file line by line
    for line in lines:
        locctr, label, opcode, operand = line.split()

        if opcode == "START":
            starting_address = int(operand, 16)
            continue
        elif opcode == "END":
            break

        # Generate object code
        if opcode in optab:
            machine_code = optab[opcode]
            address = symtab.get(operand, "0000")
            object_code.append(f"{machine_code}{address}")
            object_count += 1
        elif opcode == "WORD":
            object_code.append(f"{int(operand):06X}")
        elif opcode == "BYTE":
            if operand.startswith("C'"):
                value = ''.join(f"{ord(c):02X}" for c in operand[2:-1])
                object_code.append(value)
            elif operand.startswith("X'"):
                object_code.append(operand[2:-1])

    program_length = int(locctr, 16) - starting_address

    # Generate header record
    header_record = f"H {label} {starting_address:06X} {program_length:06X}"
    output_content += f"{header_record}\n"

    # Generate text record
    text_record = f"T {starting_address:06X} {len(object_code) * 3:02X} " + ' '.join(object_code)
    output_content += f"{text_record}\n"

    # Generate end record
    end_record = f"E {starting_address:06X}"
    output_content += f"{end_record}\n"

    # Display output in GUI
    output_display.delete(1.0, tk.END)
    output_display.insert(tk.END, output_content)

    # Save to output.txt
    with open("output.txt", "w") as f:
        f.write(output_content)

    messagebox.showinfo("Success", "Pass 2 completed. Output file generated.")

# Initialize Tkinter GUI
root = tk.Tk()
root.title("Two-Pass Assembler")

# Load OPTAB Button
load_optab_btn = tk.Button(root, text="Load OPTAB", command=load_optab)
load_optab_btn.grid(row=0, column=0, padx=10, pady=10)

# Load Input File Button
load_input_btn = tk.Button(root, text="Load Input File", command=load_input_file)
load_input_btn.grid(row=0, column=1, padx=10, pady=10)

# Run Pass 1 Button
pass_one_btn = tk.Button(root, text="Run Pass 1", command=pass_one)
pass_one_btn.grid(row=0, column=2, padx=10, pady=10)

# Run Pass 2 Button
pass_two_btn = tk.Button(root, text="Run Pass 2", command=pass_two)
pass_two_btn.grid(row=0, column=3, padx=10, pady=10)

# Display for optab
optab_display = scrolledtext.ScrolledText(root, height=10, width=40)
optab_display.grid(row=1, column=0, padx=10, pady=10)

# Display for input file
input_file_display = scrolledtext.ScrolledText(root, height=10, width=40)
input_file_display.grid(row=1, column=1, padx=10, pady=10)

# Display for intermediate file
intermediate_file_display = scrolledtext.ScrolledText(root, height=10, width=40)
intermediate_file_display.grid(row=1, column=2, padx=10, pady=10)

# Display for SYMTAB
symtab_display = scrolledtext.ScrolledText(root, height=10, width=40)
symtab_display.grid(row=1, column=3, padx=10, pady=10)

# Display for output (Pass 2 result)
output_display = scrolledtext.ScrolledText(root, height=10, width=40)
output_display.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
