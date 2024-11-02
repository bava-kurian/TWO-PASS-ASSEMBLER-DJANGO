# views.py
from django.shortcuts import render, redirect
from .models import AssemblerFile
from django.utils import timezone
import os

def two_pass_assembler(request):
    context = {}

    # Retrieve all previous uploads, ordered by the most recent
    previous_uploads = AssemblerFile.objects.order_by('-upload_date')
    context['previous_uploads'] = previous_uploads

    if request.method == 'POST':
        # Check if a previous upload is selected
        selected_file_id = request.POST.get('selected_file')
        if selected_file_id:
            # Reuse selected previous files
            selected_file = AssemblerFile.objects.get(id=selected_file_id)
            input_file_path = selected_file.input_file.path
            optab_file_path = selected_file.optab_file.path
        else:
            # Handle new file upload
            input_file = request.FILES.get('input_file')
            optab_file = request.FILES.get('optab_file')
            
            # Save files to the model
            if input_file and optab_file:
                assembler_file = AssemblerFile.objects.create(
                    input_file=input_file,
                    optab_file=optab_file,
                    upload_date=timezone.now()
                )
                input_file_path = assembler_file.input_file.path
                optab_file_path = assembler_file.optab_file.path
            else:
                context['error'] = "Please upload both input and optab files or select a previous upload."
                return render(request, 'index.html', context)

        # Process the assembler logic using the selected files
        try:
            with open(input_file_path, 'r') as input_file, open(optab_file_path, 'r') as optab_file:
                # Parse OPTAB (Opcode Table)
                optab = {}
                for line in optab_file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        optab[parts[0]] = parts[1]

                # Initialize tables
                symtab = {}
                intermediate_code = []
                location_counter = 0
                start_address = 0
                program_name = "COPY"

                # Pass 1 - Generate Intermediate File and Symbol Table
                for line in input_file:
                    line_parts = line.strip().split()
                    label = line_parts[0] if len(line_parts) == 3 else None
                    opcode = line_parts[1] if len(line_parts) == 3 else line_parts[0]
                    operand = line_parts[2] if len(line_parts) == 3 else line_parts[1]

                    if opcode == 'START':
                        start_address = int(operand, 16)
                        location_counter = start_address
                        intermediate_code.append(f'{label}\t{opcode}\t{operand}')
                    else:
                        if label:
                            symtab[label] = format(location_counter, 'X')
                        if opcode in optab:
                            location_counter += 3
                        elif opcode == 'WORD':
                            location_counter += 3
                        elif opcode == 'RESW':
                            location_counter += 3 * int(operand)
                        elif opcode == 'RESB':
                            location_counter += int(operand)
                        elif opcode == 'BYTE':
                            location_counter += len(operand) - 3  # assuming format C'...' for character constant

                        intermediate_code.append(f'{format(location_counter, "X")}\t{label}\t{opcode}\t{operand}')

                # Pass 2 - Generate Machine Code in specified format
                program_length = format(location_counter - start_address, 'X')
                machine_code = []

                # Header Record
                header_record = f'H^{program_name.ljust(6, "_")}^{format(start_address, "06X")}^{program_length.zfill(6)}'
                machine_code.append(header_record)

                # Text Records
                text_records = []
                for line in intermediate_code[1:]:
                    parts = line.split()
                    if len(parts) >= 3:
                        addr = parts[0]
                        opcode = parts[2]
                        operand = parts[3] if len(parts) > 3 else None

                        if opcode in optab:
                            code = optab[opcode]
                            operand_address = symtab.get(operand, "0000")
                            text_records.append(f'{code}{operand_address}')

                # Combine Text Records into a single line with format
                start_addr = format(start_address, "06X")
                text_record_line = f'T^{start_addr}^' + '^'.join(text_records)
                machine_code.append(text_record_line)

                # End Record
                end_record = f'E^{format(start_address, "06X")}'
                machine_code.append(end_record)

                # Prepare context with final outputs
                context['intermediate_code'] = '\n'.join(intermediate_code)
                context['symtab'] = '\n'.join([f'{key}\t{value}' for key, value in symtab.items()])
                context['machine_code'] = '\n'.join(machine_code)

        except Exception as e:
            context['error'] = f"An error occurred while processing the files: {str(e)}"
            return render(request, 'index.html', context)

    return render(request, 'index.html', context)
