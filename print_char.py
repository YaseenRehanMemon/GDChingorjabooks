import sys

def print_char_at_pos(file_path, pos):
    with open(file_path, 'r') as f:
        content = f.read()
    
    print(f"Character at position {pos} is: {content[pos]}")
    print(f"Context: {content[pos-20:pos+20]}")

if __name__ == '__main__':
    file_path = sys.argv[1]
    pos = int(sys.argv[2])
    print_char_at_pos(file_path, pos)
