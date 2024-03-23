def main():
    gridPF = PathFinderMaze("assets/mazes/maze1.txt")
    gridPF.solvableStructure()
    gridPF.displayStructure()
    gridPF.displayPathOnStructure()

if __name__ == '__main__':
    main()