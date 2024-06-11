import sys

# Initialize the symbol table with predefined symbols
symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576,
}
for i in range(16):
    symbol_table[f'R{i}'] = i
    
# Predefined dictionaries for C-instruction parts
comp_dict = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "-D": "0001111", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010",
    "D-A": "0010011", "A-D": "0000111", "D&A": "0000000",
    "D|A": "0010101", "M": "1110000", "!M": "1110001",
    "-M": "1110011", "M+1": "1110111", "M-1": "1110010",
    "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}
dest_dict = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}
jump_dict = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def assemble(input_file):
    output_file = input_file.replace('.asm', '.hack')
    next_address = 0  # Next instruction address
    next_variable_address = 16  # Next available RAM address for variables

    # First pass: build the symbol table for label symbols
    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.split('//')[0].strip()
            if line.startswith('('):
                label = line[1:-1]
                symbol_table[label] = next_address
                continue
            if line:
                next_address += 1

    # Second pass: translate to machine code
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.split('//')[0].strip()
            if line == '' or line.startswith('('):
                continue
            if line.startswith('@'):  # A-instruction
                symbol = line[1:]
                if symbol.isdigit():
                    value = int(symbol)
                else:
                    if symbol not in symbol_table:
                        symbol_table[symbol] = next_variable_address
                        next_variable_address += 1
                    value = symbol_table[symbol]
                outfile.write('0' + format(value, '015b') + '\n')
            else:  # C-instruction
                dest, comp, jump = '', '', ''
                if '=' in line:
                    dest, line = line.split('=')
                if ';' in line:
                    comp, jump = line.split(';')
                else:
                    comp = line
                binary_code = '111' + comp_dict[comp] + dest_dict[dest] + jump_dict[jump]
                outfile.write(binary_code + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: Assembler fileName.asm")
        sys.exit(1)
    assemble(sys.argv[1])