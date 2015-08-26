def translator():
    with open('Converted32to64.asm','w') as new_file:
        with open('32_bit.asm') as old_file:
            for line in old_file:
                line = line.replace('pushl','pushq')
                line = line.replace('ebp','rbp')
                line = line.replace('.cfi_def_cfa_offset 8','.cfi_def_cfa_offset 16')
                line = line.replace('.cfi_offset 5, -8','.cfi_offset 6, -16')
                line = line.replace('.cfi_def_cfa_register 5','.cfi_def_cfa_register 6')
                line = line.replace('leave','popq	%rbp')
                line = line.replace('.cfi_restore 5','.cfi_def_cfa 7, 8')
                if "esp" in line and "subl" not in line:
                    new_file.write("	movq	%rsp, %rbp\n")
                elif "subl" not in line and ".cfi_def_cfa 4, 4" not in line:
                    new_file.write(line)
translator()
