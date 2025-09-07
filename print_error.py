import sys

def print_error_line(file_path, line_number, column_number):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    print(f"Error is in line {line_number}:")
    print(lines[line_number-1])
    print(" " * (column_number - 1) + "^")

if __name__ == '__main__':
    file_path = sys.argv[1]
    line_number = int(sys.argv[2])
    column_number = int(sys.argv[3])
    print_error_line(file_path, line_number, column_number)
