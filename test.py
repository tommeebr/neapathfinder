def load_from_file(file_path):
    with open(file_path, 'r') as file:
        data = [[int(num) for num in line.split(',')] for line in file]
    return data

print(load_from_file("assets\grids\grid.txt"))