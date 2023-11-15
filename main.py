import sys
import os
import argparse


def extract_variables(equation):
    variables = []
    current_var = ''
    negate = False

    for char in equation:
        if char.isalnum() or char == '+':
            if char == '+':
                if current_var:
                    variables.append([current_var, int(negate)])
                    variables.append(['#', 0])  # Add '#' directly after '+' as a separate variable
                    current_var = ''
                    negate = False
                else:
                    variables.append(['#', 0])  # Handle standalone '#' as a variable
            else:
                current_var += char
        elif char == "'":
            negate = True
        else:
            if current_var:
                variables.append([current_var, int(negate)])
            current_var = ''
            negate = False

    if current_var:
        variables.append([current_var, int(negate)])

    return variables


def print_variables_with_format(variables, file):
    print_flag = False
    for index, (var, negate) in enumerate(variables):
        if index == 0:
            print(var, end=' = ', file=file)
        else:
            if index > 1 and var not in ['#', '+']:
                if variables[index - 1][0] != '#':
                    print('&', end=' ', file=file)

            if negate:
                print('!' + var, end=' ', file=file)
            else:
                print(var, end=' ', file=file)

    print(';', file=file)


def main():
    parser = argparse.ArgumentParser(description="Convert equations into a specified format.")
    parser.add_argument('input_file', metavar='input_file', type=str, nargs='?', help='Input file name')
    args = parser.parse_args()

    if args.input_file:
        input_file_name = args.input_file
    else:
        input_file_name = input("Enter the filename: ")

    if not os.path.exists(input_file_name):
        print(f"File '{input_file_name}' not found.")
        sys.exit(1)

    input_file_path = os.path.abspath(input_file_name)
    output_file_name = os.path.splitext(input_file_path)[0] + '_converted.txt'

    try:
        with open(input_file_path, 'r') as input_file, open(output_file_name, 'w') as output_file:
            lines = input_file.readlines()
            for line in lines:
                result = extract_variables(line)
                print_variables_with_format(result, output_file)
        print(f"Conversion successful. Converted equations saved in '{output_file_name}'.")
    except FileNotFoundError:
        print(f"Error while processing the file.")


if __name__ == "__main__":
    main()
