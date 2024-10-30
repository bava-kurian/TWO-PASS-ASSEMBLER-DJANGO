# views.py
import os
from django.shortcuts import render
from django.http import HttpResponse
from .models import UploadedFile
from .forms import FileUploadForm

def pass1_logic(input_data_path):
    # Sample Pass 1 logic
    symtab = {}
    intermediate_content = ""
    locctr = 0

    with open(input_data_path, 'r') as input_file:
        for line in input_file:
            label, opcode, operand = line.strip().split()
            if opcode == 'START':
                locctr = int(operand)
            elif opcode == 'END':
                break
            else:
                intermediate_content += f"{locctr}\t{label}\t{opcode}\t{operand}\n"
                symtab[label] = locctr
                locctr += 3

    return intermediate_content, symtab

def pass2_logic(intermediate_content, symtab, optab_data_path):
    output_content = ""
    machine_code = []

    with open(optab_data_path, 'r') as optab_file:
        optab = {line.split()[0]: line.split()[1] for line in optab_file}

    for line in intermediate_content.splitlines():
        locctr, label, opcode, operand = line.split()
        if opcode in optab:
            machine_code.append(f"{optab[opcode]}{symtab.get(operand, '0000')}")
        elif opcode == 'WORD':
            machine_code.append(f"{int(operand):06}")

    output_content = "\n".join(machine_code)
    return output_content, machine_code

def assembler_view(request):
    intermediate_content = None
    symtab = None
    pass1_result = None
    pass2_result = None
    machine_code = None

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            input_file = UploadedFile.objects.filter(file_type="input").last()
            optab_file = UploadedFile.objects.filter(file_type="optab").last()

            if input_file and optab_file:
                try:
                    # Run Pass 1
                    intermediate_content, symtab = pass1_logic(input_file.file.path)
                    pass1_result = {
                        'intermediate': intermediate_content,
                        'symtab': symtab,
                    }

                    # Run Pass 2
                    output_content, machine_code = pass2_logic(intermediate_content, symtab, optab_file.file.path)
                    pass2_result = {
                        'output_content': output_content,
                        'machine_code': machine_code,
                    }
                except Exception as e:
                    return HttpResponse(f"Error in processing: {str(e)}", status=500)
    else:
        form = FileUploadForm()

    return render(request, 'index.html', {
        'form': form,
        'pass1_result': pass1_result,
        'pass2_result': pass2_result,
        'machine_code': machine_code,
    })
