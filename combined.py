import heapq
import math
import random
import numpy as np
import pygame
from pygame.locals import *
import sys
import tkinter as tk
from tkinter import filedialog


class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent # Parent node
        self.pos = pos # (x, y) coordinates
        self.g = 0 # Cost to start node
        self.h = 0 # Heuristic cost
        self.f = 0 # Total cost of the node

    def __eq__(self, other):
        return self.pos == other.pos

class PathFinder:
    def __init__(self, *args, structure = None):
        self.path = []
        self.fileInit = False
        self.structure = structure
        if len(args) == 1 and isinstance(args[0], str):
            self.loadFile(args[0])
            self.fileInit = True
        elif len(args) == 4 and all(isinstance(arg, tuple) for arg in args[:2]) and all(isinstance(arg, int) for arg in args[2:]):
            self.start, self.end, self.height, self.width = args
            self.validateInputs()
            self.structInstance = GeneratorStructure(self.start, self.end, self.height, self.width)
        elif len(args) == 5:
            self.start, self.end, self.height, self.width, self.structure = args
        else:
            raise ValueError("Must provide either a file path or height and width")


    def validateInputs(self):
        if self.width % 2 == 0:
            self.width -= 1
            self.end = (self.end[0] - 1, self.end[1]) # Tuples are immutable, so have to assign it to a new one
            print(f'EVEN Width not permitted. Adjusting width to {self.width}')
        if self.height % 2 == 0:
            self.height -= 1
            self.end = (self.end[0], self.end[1] - 1) # ^^^
            print(f'EVEN Height not permitted. Adjusting height to {self.height}')
        if self.end[0] >= self.width or self.end[1] >= self.height:
            raise ValueError("End position must be within the bounds of the maze")
        if self.start[0] < 0 or self.start[1] < 0 or self.end[0] < 0 or self.end[1] < 0:
            raise ValueError("Start and end positions must be non-negative")

    def manhattanDist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def displayStructure(self):
        for row in self.structure:
            print(' '.join(str(cell) for cell in row))

    def displayPathOnStructure(self):
        for i in range(len(self.structure)):
            for j in range(len(self.structure[0])):
                if (i, j) in self.path:
                    print(' X', end='')
                else:
                    print(' -', end='')
            print()  # Newline after each row

    def solvableStructure(self):
        if self.fileInit == True:
            self.aStar()
        else:
            if self.structure is None:
                while True:
                    self.generateStructure()
                    if self.aStar():
                        break
            else:
                self.aStar()

    def aStar(self):
        startNode = Node(None, self.start)
        endNode = Node(None, self.end)

        openList = []
        closedList = []

        count = 0  # Counter for tie-breaking
        heapq.heappush(openList, (startNode.f, count, startNode))  # Add the start node

        while len(openList) > 0:
            currentNode = heapq.heappop(openList)[2]  # Node with the lowest f values
            closedList.append(currentNode)

            if currentNode == endNode:  # Found the goal
                path = []
                while currentNode is not None:
                    path.append(currentNode.pos)
                    currentNode = currentNode.parent
                self.path = path[::-1]  # Reverse the path

                # Calculate the Manhattan distances for the final path
                manhattanDistTotal = sum(self.manhattanDist(path[i], path[i + 1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)
                return self.path

            children = self.getNeighbour(currentNode)
            for child in children:
                if child in closedList:
                    continue  # Child is already in the closed list
                child.g = currentNode.g + 1
                child.h = self.manhattanDist(child.pos, endNode.pos)
                child.f = child.g + child.h

                # Check if child is in open list and if it has a lower g value
                inOpenList = False
                for openNode in openList:
                    if child == openNode[2] and child.g >= openNode[2].g:
                        inOpenList = True
                        break

                if inOpenList:
                    continue  # Child is already in the open list and has a higher g value

                count += 1  # Increment counter
                heapq.heappush(openList, (child.f, count, child))  # Add the child to the open list
        return []

    def getNeighbour(self, node):
        raise NotImplementedError("This method should be overridden in a subclass")

    def findPath(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    def loadFile(self, filePath):
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()

            # Parse start and end positions
            self.start = tuple(map(int, lines[0].strip().split(',')))
            self.end = tuple(map(int, lines[1].strip().split(',')))

            # Construct the 2D array
            self.structure = [list(map(int, line.strip().split(','))) for line in lines[2:]]

            self.height, self.width = len(self.structure), len(self.structure[0])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filePath} not found.")
        except ValueError:
            print("Could not parse the file. Make sure it is in the correct format.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def generateStructure(self):
        raise NotImplementedError("This method should be overridden in a subclass")

class PathFinderGrid(PathFinder):
    def __init__(self, *args):
        super().__init__(*args)

    def getNeighbour(self, node):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= self.width or nodePos[1] < 0 or nodePos[1] >= self.height:
                continue  # Node is out of bounds
            if self.structure[nodePos[0]][nodePos[1]] != 0:
                continue  # Node is not walkable
            neighbors.append(Node(node, nodePos))
        return neighbors

    def generateStructure(self):
        if self.structure is None:
            self.structInstance = GeneratorStructure(self.start, self.end, self.height, self.width)
            structure, self.width, self.height, self.end = self.structInstance.generateStructure()
            self.structure = structure

class PathFinderMaze(PathFinder):
    def getNeighbour(self, node):
        neighbors = []
        for newPos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            nodePos = (node.pos[0] + newPos[0], node.pos[1] + newPos[1])
            if nodePos[0] < 0 or nodePos[0] >= len(self.structure) or nodePos[1] < 0 or nodePos[1] >= len(self.structure[0]):
                continue  # Node is out of bounds

            # Check for walls
            #* Bitwise AND operation to check for walls
            if newPos == (0, -1):  # Moving left
                if self.structure[node.pos[0]][node.pos[1]] & 1:  # There's a left wall
                    continue
            elif newPos == (0, 1):  # Moving right
                if nodePos[0] < len(self.structure) and self.structure[nodePos[0]][nodePos[1]] & 1:  # There's a left wall in the next cell
                    continue
            elif newPos == (-1, 0):  # Moving up
                if self.structure[node.pos[0]][node.pos[1]] & 2:  # There's a top wall
                    continue
            elif newPos == (1, 0):  # Moving down
                if nodePos[0] < len(self.structure) and self.structure[nodePos[0]][nodePos[1]] & 2:  # There's a top wall in the next cell
                    continue

            neighbors.append(Node(node, nodePos))
        return neighbors

    def generateStructure(self):
        self.structInstance = GeneratorMaze(self.start, self.end, self.height, self.width)
        structure, self.width, self.height, self.end = self.structInstance.generateStructure()
        self.structure = structure



class GeneratorStructure():
    def __init__(self, start, end, width,height):
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.array = np.ones((height, width), dtype=np.int8)
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up

    def _dfs(self, x, y):
        #! Cannot use even numbers for width and height for some reason
        self.array[y][x] = 0
        np.random.shuffle(self.directions)
        for dx, dy in self.directions:
            nextX, nextY = x + 2*dx, y + 2*dy
            if (0 <= nextX < self.width) and (0 <= nextY < self.height) and self.array[nextY][nextX] == 1:
                self.array[nextY-dy][nextX-dx] = 0
                self._dfs(nextX, nextY)

    def generateStructure(self):
        raise NotImplementedError("This method should be overridden in a subclass")


class GeneratorGrid(GeneratorStructure):
    def generateStructure(self):
        #! Ensure dimensions are odd - for some reason it makes the final row and column full of walls? could do with fixing this
        if self.width % 2 == 0:
            self.width -= 1
        if self.height % 2 == 0:
            self.height -= 1

        # Adjust end position if it falls outside the adjusted grid size
        if self.end[0] >= self.width:
            self.end = (self.width - 1, self.end[1])
        if self.end[1] >= self.height:
            self.end = (self.end[0], self.height - 1)

        self._dfs(self.start[0], self.start[1])
        self.array[self.start[1]][self.start[0]] = 0  # Ensure start is traversable
        self.array[self.end[1]][self.end[0]] = 0  # Ensure end is traversable
        return self.array.tolist(), self.width, self.height, self.end  # Return adjusted width, height and end

class GeneratorMaze(GeneratorStructure):
    def generateStructure(self):
        raise NotImplementedError("This method has not yet been implemented")


# def main():
#     gridPF = PathFinderGrid((0,0),(9,9),10,10)
#     gridPF.solvableStructure()
#     gridPF.displayStructure()
#     gridPF.displayPathOnStructure()
#
# if __name__ == '__main__':
#     main()
# ! ///////////////////////////// PYGAME ///////////////////////////////
# Define some colour variables
RED = (200, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (1, 50, 32)
BLUE = (0, 0, 200)
START = (0, 0, 255)
END = (75,0,130)
CONTRAST = (255, 255, 255)
MAIN = (18, 18, 18)
DARK_GRAY = (24,24,24)
LIGHT_GRAY = (211, 211, 211)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
class UI:
    @staticmethod
    def init(app):
        UI.font = pygame.font.Font(None, 30)
        UI.sfont = pygame.font.Font(None, 20)
        UI.lfont = pygame.font.Font(None, 40)
        UI.xlfont = pygame.font.Font(None, 50)
        UI.center = (app.screen.get_size()[0]//2, app.screen.get_size()[1]//2)
        UI.half_width = app.screen.get_size()[0]//2
        UI.half_height = app.screen.get_size()[1]//2

        UI.fonts = {
            'sm':UI.sfont,
            'm':UI.font,
            'l':UI.lfont,
            'xl':UI.xlfont
        }
class TextUtils:
    @staticmethod
    def wrap_to_pixels(font, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line
            if test_line != '':
                test_line += ' '
            test_line += word
            text_width, _ = font.size(test_line)
            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line != '':
            lines.append(current_line)
        return lines
class Button:
    def __init__(self, text, x, y, width, height, inactive_colour, active_colour):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_colour = inactive_colour
        self.active_colour = active_colour

    def draw(self, screen, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_colour, (self.x, self.y, self.width, self.height))

            if click[0] == 1 and action is not None:
                print("Button action called")
                pygame.time.delay(100) # ! Stop double click input - could be improved
                action()
        else:
            pygame.draw.rect(screen, self.inactive_colour, (self.x, self.y, self.width, self.height))


        small_text = UI.fonts['sm']
        text_surf, text_rect = self.text_objects(self.text, small_text)
        text_rect.center = ((self.x+(self.width/2)), (self.y+(self.height/2)))
        screen.blit(text_surf, text_rect)

    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, CONTRAST)
        return text_surface, text_surface.get_rect()

class Slider:
    def __init__(self, x, y, width, min_val, max_val, default_val):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.val = default_val
        self.slider_pos = (self.x + (default_val - min_val) * self.width / (max_val - min_val), self.y)

    def draw(self, screen):
        pygame.draw.line(screen, CONTRAST, (self.x, self.y), (self.x + self.width, self.y), 3)
        pygame.draw.circle(screen, CONTRAST, (int(self.slider_pos[0]), int(self.slider_pos[1])), 10)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] in range(self.x, self.x + self.width) and abs(pygame.mouse.get_pos()[1] - self.y) < 10:
                self.val = round((pygame.mouse.get_pos()[0] - self.x) * (self.max_val - self.min_val) / self.width + self.min_val)
                self.slider_pos = (pygame.mouse.get_pos()[0], self.y)

class InputBox:
    def __init__(self, x, y, w, h, page, placeholder=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour_inactive = LIGHT_GRAY
        self.colour_active = GREEN  # Define the active colour as green
        self.colour = self.colour_inactive
        self.text = ''
        self.placeholder = placeholder
        self.font = UI.fonts['m']
        self.error_font = pygame.font.Font(None, 20)  # Smaller font for error message
        self.txt_surface = self.font.render(self.placeholder, True, self.colour)
        self.active = False
        self.error_message = ''
        self.page = page

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = self.colour_active if self.active else self.colour_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.page.generateBlank()  # Generate the grid when enter is pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.colour)

    def draw(self, screen):
        if self.text == '':
            self.txt_surface = self.font.render(self.placeholder, True, LIGHT_GRAY)
        else:
            self.txt_surface = self.font.render(self.text, True, CONTRAST)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)

        # Wrap the error message to fit within 200px
        error_lines = TextUtils.wrap_to_pixels(self.error_font, self.error_message, 200)
        for i, line in enumerate(error_lines):
            error_text_surface = self.error_font.render(line, True, RED)
            screen.blit(error_text_surface,
                        (self.rect.x, self.rect.y + self.rect.height + 5 + i * self.error_font.get_linesize()))

    def validate(self):
        if self.text.isdigit():
            val = int(self.text)
            if 5 <= val <= 80:
                self.error_message = ''
                return True
        self.error_message = 'Error: Input should be a number between 5 and 80'
        return False

class CheckBox:
    def __init__(self, x, y, width, height, checked=True, label=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.checked = checked
        self.active_colour = GREEN
        self.inactive_colour = LIGHT_GRAY
        self.label = UI.fonts['sm'].render(label, True, CONTRAST)
    def draw(self, screen):
        if self.checked:
            pygame.draw.rect(screen, self.active_colour, self.rect)
        else:
            pygame.draw.rect(screen, self.inactive_colour, self.rect, 2)
        screen.blit(self.label, (self.rect.x + self.rect.width + 5, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.maze_button = Button("Maze", UI.half_width - 50, UI.half_height, 100, 50, GREEN, LIGHT_GRAY)
        self.grid_button = Button("Grid", UI.half_width - 50, UI.half_height - 75, 100, 50, GREEN, LIGHT_GRAY)
        self.draw_button = Button("Draw", UI.half_width - 50, UI.half_height + 75, 100, 50, GREEN,
                                  LIGHT_GRAY)  # New button

    def game_intro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(MAIN)
            large_text = UI.fonts['xl']
            TextSurf1, TextRect1 = self.text_objects("Pathfinding", large_text)
            TextRect1.center = ((SCREEN_WIDTH / 2), (150))
            self.screen.blit(TextSurf1, TextRect1)

            TextSurf2, TextRect2 = self.text_objects("Showcase", large_text)
            TextRect2.center = ((SCREEN_WIDTH / 2), (200))
            self.screen.blit(TextSurf2, TextRect2)

            self.maze_button.draw(self.screen, self.maze_page)
            self.grid_button.draw(self.screen, self.grid_page)
            self.draw_button.draw(self.screen, self.draw_page)  # New button

            pygame.display.update()
            self.clock.tick(15)
    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, CONTRAST)
        return text_surface, text_surface.get_rect()

    def maze_page(self):
        page = MazePage(self.screen)
        page.display_page()

    def grid_page(self):
        page = GridPage(self.screen)
        page.display_page()

    def draw_page(self):
        page = DrawPage(self.screen)
        page.display_page()

class Page:
    def __init__(self, screen, page_name):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.page_name = page_name
        self.back_button = Button("Back", 50, 50, 100, 50, RED, LIGHT_GRAY)

    def display_page(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, CONTRAST)
        return text_surface, text_surface.get_rect()

    def useFile(self):
        root = tk.Tk()  # * Used tkinter to open file dialog, not possible in pygame
        root.withdraw()  # Hide the main window
        filePath = filedialog.askopenfilename()  # Open the file dialog

        try:
            # Create a PathFinder instance and use its loadFile method
            pathfinder = PathFinder(filePath)
            self.grid = pathfinder.structure
            self.start = pathfinder.start
            self.end = pathfinder.end
            self.width = pathfinder.width
            self.height = pathfinder.height

        except FileNotFoundError:
            self.error_message = f"File {filePath} not found."
        except ValueError:
            self.error_message = "Could not parse the file. Make sure it is in the correct format."
        except Exception as e:
            self.error_message = f"An error occurred: {e}"

    def back(self):
        menu = Menu(self.screen)
        menu.game_intro()

class GridPage(Page, PathFinder):
    def __init__(self, screen):
        super().__init__(screen, "Grid")
        self.width = None
        self.generate_button = Button("Generate", 50, 300, 100, 50, GREEN, LIGHT_GRAY)
        self.use_file_button = Button("Use File", 50, 400, 100, 50, GREEN, LIGHT_GRAY)
        self.solve_button = Button("Solve", 50, 500, 100, 50, GREEN, LIGHT_GRAY)
        self.help_button = Button("Help", 50, 600, 100, 50, BLUE, LIGHT_GRAY)
        self.show_grid_checkbox = CheckBox(50, 675, 20, 20, True, 'Grid Lines')
        self.visualise_generation_checkbox = CheckBox(50, 700, 20, 20, False, 'Visualise DFS')
        self.visualise_solver_checkbox = CheckBox(50, 725, 20, 20, False, 'Visualise A*')
        self.width_input = InputBox(50, 150, 100, 32, self, 'Width')  # Pass self as the page argument
        self.height_input = InputBox(50, 225, 100, 32, self, 'Height')  # Pass self as the page argument
        self.grid = []
        self.start = None
        self.end = None
        self.error_message = ''
        self.path = []
        self.cell_size = 0

    def display_page(self):
        page = True
        small_text = UI.fonts['sm']

        while page:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                self.width_input.handle_event(event)
                self.height_input.handle_event(event)
                self.show_grid_checkbox.handle_event(event)
                self.visualise_generation_checkbox.handle_event(event)
                self.visualise_solver_checkbox.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and self.grid:
                    self.cell_size = 800 // max(len(self.grid[0]), len(self.grid))  # Calculate cell size here
                    x, y = event.pos
                    grid_x = (x - (1000 - len(self.grid[0]) * self.cell_size)) // self.cell_size
                    grid_y = y // self.cell_size

                    # Check if the click is within the grid
                    if 0 <= grid_x < len(self.grid[0]) and 0 <= grid_y < len(self.grid):
                        if event.button == 1:  # Left mouse button
                            if self.end is not None and (grid_y, grid_x) == self.end:
                                continue  # Skip if the start position is the same as the end position
                            self.start = (grid_y, grid_x)
                        elif event.button == 3:  # Right mouse button
                            if self.start is not None and (grid_y, grid_x) == self.start:
                                continue  # Skip if the end position is the same as the start position
                            self.end = (grid_y, grid_x)

            self.screen.fill(MAIN)

            self.back_button.draw(self.screen, self.back)
            self.generate_button.draw(self.screen, self.generate)
            self.use_file_button.draw(self.screen, self.useFile)
            self.solve_button.draw(self.screen, self.solve)
            self.help_button.draw(self.screen, self.show_help)
            self.show_grid_checkbox.draw(self.screen)
            self.visualise_generation_checkbox.draw(self.screen)
            self.visualise_solver_checkbox.draw(self.screen)
            self.width_input.draw(self.screen)
            self.height_input.draw(self.screen)

            self.draw_grid()

            if self.start:
                start_text = small_text.render(f'Start: {self.start}', True, CONTRAST)
                self.screen.blit(start_text, (10, SCREEN_HEIGHT - 40))

            if self.end:
                end_text = small_text.render(f'End: {self.end}', True, CONTRAST)
                self.screen.blit(end_text, (10, SCREEN_HEIGHT - 20))

            # Add these lines
            if self.error_message:
                # Wrap the error message to fit within 200px
                error_lines = TextUtils.wrap_to_pixels(small_text, self.error_message, 150)
                for i, line in enumerate(error_lines):
                    error_text_surface = small_text.render(line, True, RED)
                    self.screen.blit(error_text_surface,
                                     (50, 350 + i * small_text.get_linesize()))

            if self.path:
                self.display_manhattan_distance()

            pygame.display.update()
            self.clock.tick(15)

    def generateBlank(self):
        if self.width_input.validate() and self.height_input.validate():
            width = int(self.width_input.text)
            height = int(self.height_input.text)

            # Ensure the dimensions are odd
            if width % 2 == 0:
                width -= 1
            if height % 2 == 0:
                height -= 1

            self.cell_size = 800 // max(width, height)
            self.grid = [[0 for _ in range(width)] for _ in range(height)]
        else:
            print("Error: Width and height should be numbers between 5 and 100")

    def draw_grid(self):
        if self.grid:
            self.cell_size = 800 // max(len(self.grid[0]), len(self.grid))
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    if cell == 1:  # If the cell is a wall
                        colour = CONTRAST  # Full white colour
                    elif self.start is not None and (i, j) == self.start:
                        colour = START  # Start position colour
                    elif self.end is not None and (i, j) == self.end:
                        colour = END  # End position colour
                    elif cell == 2:  # If the cell is part of the path
                        colour = GREEN  # Path colour
                    else:
                        colour = MAIN  # Default colour
                    pygame.draw.rect(self.screen, colour,
                                     pygame.Rect(1000 - len(self.grid[0]) * self.cell_size + j * self.cell_size,
                                                 i * self.cell_size, self.cell_size, self.cell_size))
            # Draw grid lines
            if self.show_grid_checkbox.checked:
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[0])):
                        pygame.draw.rect(self.screen, CONTRAST,
                                         pygame.Rect(1000 - len(self.grid[0]) * self.cell_size + j * self.cell_size,
                                                     i * self.cell_size, self.cell_size, self.cell_size), 1)

    def generate(self):
        if self.start is not None and self.end is not None and self.width_input.validate() and self.height_input.validate():
            width = int(self.width_input.text)
            height = int(self.height_input.text)

            # Ensure the dimensions are odd
            if width % 2 == 0:
                width -= 1
            if height % 2 == 0:
                height -= 1

            self.width = width
            self.height = height

            if self.visualise_generation_checkbox.checked:
                generator = VisualGeneratorGrid(self.start, self.end, self.width, self.height, self.screen)
            else:
                generator = GeneratorGrid(self.start, self.end, self.width, self.height)
            self.grid, _, _, _ = generator.generateStructure()
            self.error_message = ''
        else:
            self.error_message = 'Error: Start, end positions and dimensions must be set before generation'

    def solve(self):
        if self.grid and self.start and self.end and self.width and self.height:
            if self.visualise_solver_checkbox.checked:
                pathfinder = VisualAStar(self.start, self.end, self.width, self.height, self.screen, self.cell_size,
                                         structure=self.grid)
            else:
                pathfinder = PathFinderGrid(self.start, self.end, self.width, self.height, self.grid)
            pathfinder.path = pathfinder.aStar()
            self.path = pathfinder.path
            self.update_grid_with_path()
        else:
            self.error_message = 'Error: Grid must be generated before solving'

    def update_grid_with_path(self):
        if self.path:
            for cell in self.path:
                if cell[0] < len(self.grid) and cell[1] < len(self.grid[0]):
                    self.grid[cell[0]][cell[1]] = 2  # Use a different number to represent the path
                else:
                    print(f"Error: Cell {cell} is out of grid bounds.")
        else:
            print("Error: No path to update.")

    def display_manhattan_distance(self):
        manhattan_distance = sum(self.manhattanDist(self.path[i], self.path[i + 1]) for i in range(len(self.path) - 1))
        text1 = UI.fonts['sm'].render(f'Distance:\n{manhattan_distance}', True, CONTRAST)
        self.screen.blit(text1 , (100, SCREEN_HEIGHT - 40))

    def show_help(self):
        print("GridPage show_help method called")
        help_page = GridHelpPage(self.screen)
        help_page.display_page()

class MazePage(Page):
    def __init__(self, screen):
        super().__init__(screen, "Maze")
        self.use_file_button = Button("Use File", 50, 400, 100, 50, GREEN, LIGHT_GRAY)
        self.solve_button = Button("Solve", 50, 500, 100, 50, GREEN, LIGHT_GRAY)
        self.show_grid_checkbox = CheckBox(50, 675, 20, 20, True, 'Grid Lines')
        self.help_button = Button("Help", 50, 600, 100, 50, BLUE, LIGHT_GRAY)
        self.grid = []
        self.start = None
        self.end = None
        self.error_message = ''
        self.path = []
        self.cell_size = 0
        self.pathfinder = None
        
    def display_page(self):
        page = True
        small_text = UI.fonts['sm']

        while page:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                self.show_grid_checkbox.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and self.grid:
                    self.cell_size = 800 // max(len(self.grid[0]), len(self.grid))  # Calculate cell size here
                    x, y = event.pos
                    grid_x = (x - (1000 - len(self.grid[0]) * self.cell_size)) // self.cell_size
                    grid_y = y // self.cell_size

                    # Check if the click is within the grid
                    if 0 <= grid_x < len(self.grid[0]) and 0 <= grid_y < len(self.grid):
                        if event.button == 1:  # Left mouse button
                            pass
                        elif event.button == 3:  # Right mouse button
                            pass

            self.screen.fill(MAIN)

            self.back_button.draw(self.screen, self.back)
            self.use_file_button.draw(self.screen, self.useFile)
            self.solve_button.draw(self.screen, self.solve)
            self.help_button.draw(self.screen, self.show_help)
            self.show_grid_checkbox.draw(self.screen)


            self.draw_grid()

            if self.start:
                start_text = small_text.render(f'Start: {self.start}', True, CONTRAST)
                self.screen.blit(start_text, (10, SCREEN_HEIGHT - 40))

            if self.end:
                end_text = small_text.render(f'End: {self.end}', True, CONTRAST)
                self.screen.blit(end_text, (10, SCREEN_HEIGHT - 20))

            if self.error_message:
                error_lines = TextUtils.wrap_to_pixels(small_text, self.error_message, 150)
                for i, line in enumerate(error_lines):
                    error_text_surface = small_text.render(line, True, RED)
                    self.screen.blit(error_text_surface,
                                     (50, 350 + i * small_text.get_linesize()))

            if self.path:
                self.display_manhattan_distance()

            pygame.display.update()
            self.clock.tick(15)

    def draw_grid(self):
        if self.grid:
            self.cell_size = 800 // max(len(self.grid[0]), len(self.grid))
            wall_thickness = self.cell_size // 10  # Adjust this value to change the wall thickness

            # Draw start and end positions
            if self.start:
                start_x = 1000 - len(self.grid[0]) * self.cell_size + self.start[1] * self.cell_size
                start_y = self.start[0] * self.cell_size
                pygame.draw.rect(self.screen, START, pygame.Rect(start_x, start_y, self.cell_size, self.cell_size))
            if self.end:
                end_x = 1000 - len(self.grid[0]) * self.cell_size + self.end[1] * self.cell_size
                end_y = self.end[0] * self.cell_size
                pygame.draw.rect(self.screen, END, pygame.Rect(end_x, end_y, self.cell_size, self.cell_size))

            if self.path:
                self.cell_size = 800 // max(len(self.grid[0]), len(self.grid))
                for i in range(len(self.path) - 1):
                    current_cell = self.path[i]
                    next_cell = self.path[i + 1]
                    x = 1000 - len(self.grid[0]) * self.cell_size + current_cell[1] * self.cell_size
                    y = current_cell[0] * self.cell_size
                    start = (x, y)
                    end = (x + self.cell_size, y + self.cell_size)
                    # Calculate the direction of the arrow based on the current cell and the next cell in the path
                    if next_cell[1] > current_cell[1]:
                        direction = 'right'
                    elif next_cell[1] < current_cell[1]:
                        direction = 'left'
                    elif next_cell[0] > current_cell[0]:
                        direction = 'down'
                    elif next_cell[0] < current_cell[0]:
                        direction = 'up'
                    self.draw_arrow(start, end, GREEN, direction)

            # Draw the walls after drawing the path
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    x = 1000 - len(self.grid[0]) * self.cell_size + j * self.cell_size
                    y = i * self.cell_size
                    if cell == 1 or cell == 3:  # Draw a wall on the left side of the cell
                        pygame.draw.line(self.screen, CONTRAST, (x, y), (x, y + self.cell_size), wall_thickness)
                    if cell == 2 or cell == 3:  # Draw a wall on the top side of the cell
                        pygame.draw.line(self.screen, CONTRAST, (x, y), (x + self.cell_size, y), wall_thickness)
                    if j == len(row) - 1:  # Draw a wall on the right side of the rightmost cells
                        pygame.draw.line(self.screen, CONTRAST, (x + self.cell_size, y),
                                         (x + self.cell_size, y + self.cell_size), wall_thickness)
                    if i == len(self.grid) - 1:  # Draw a wall on the bottom side of the bottommost cells
                        pygame.draw.line(self.screen, CONTRAST, (x, y + self.cell_size),
                                         (x + self.cell_size, y + self.cell_size), wall_thickness)
                    if self.show_grid_checkbox.checked:  # Draw the grid lines
                        pygame.draw.rect(self.screen, CONTRAST, pygame.Rect(x, y, self.cell_size, self.cell_size), 1)

    def draw_arrow(self, start, end, color, direction):
        offset = self.cell_size // 4  # Adjust this value to change the size of the arrow
        if direction == 'right':
            points = [(start[0] + offset, start[1] + offset), (end[0] - offset, (start[1] + end[1]) / 2),
                      (start[0] + offset, end[1] - offset)]
        elif direction == 'left':
            points = [(end[0] - offset, start[1] + offset), (start[0] + offset, (start[1] + end[1]) / 2),
                      (end[0] - offset, end[1] - offset)]
        elif direction == 'up':
            points = [(start[0] + offset, end[1] - offset), ((start[0] + end[0]) / 2, start[1] + offset),
                      (end[0] - offset, end[1] - offset)]
        elif direction == 'down':
            points = [(start[0] + offset, start[1] + offset), ((start[0] + end[0]) / 2, end[1] - offset),
                      (end[0] - offset, start[1] + offset)]
        pygame.draw.polygon(self.screen, color, points)

    def solve(self):
        if self.grid and self.start and self.end:
            self.pathfinder = PathFinderMaze(self.start, self.end, len(self.grid[0]), len(self.grid), self.grid)
            self.pathfinder.path = self.pathfinder.aStar()
            self.path = self.pathfinder.path
            self.display_manhattan_distance()
            




    def display_manhattan_distance(self):
        if self.path and self.pathfinder:
            manhattan_distance = sum(
                self.pathfinder.manhattanDist(self.path[i], self.path[i + 1]) for i in range(len(self.path) - 1))
            text1 = UI.fonts['sm'].render(f'Distance:\n{manhattan_distance}', True, CONTRAST)
            self.screen.blit(text1 , (100, SCREEN_HEIGHT - 40))


    def show_help(self):
        print("MazePage show_help method called")
        help_page = MazeHelpPage(self.screen)
        help_page.display_page()

class DrawPage(Page):
    def __init__(self, screen):
        super().__init__(screen, "Draw")
        self.width_input = InputBox(50, 150, 100, 32, self, 'Width')  # Pass self as the page argument
        self.height_input = InputBox(50, 225, 100, 32, self, 'Height')  # Pass self as the page argument
        self.solve_button = Button("Solve", 50, 300, 100, 50, GREEN, LIGHT_GRAY)
        self.help_button = Button("Help", 50, 400, 100, 50, BLUE, LIGHT_GRAY)
        self.draw_checkbox = CheckBox(50, 650, 20, 20, False, 'Draw')  # Changed to CheckBox
        self.visualise_solver_checkbox = CheckBox(50, 700, 20, 20, False, 'Visualise A*')
        self.show_grid_checkbox = CheckBox(50, 675, 20, 20, True, 'Grid Lines')
        self.start = None
        self.end = None
        self.grid = []
        self.cell_size = 0

      # Quit pygame when the loop is exited

    def generateBlank(self):
        if self.width_input.validate() and self.height_input.validate():
            width = int(self.width_input.text)
            height = int(self.height_input.text)

            # Ensure the dimensions are odd
            if width % 2 == 0:
                width -= 1
            if height % 2 == 0:
                height -= 1

            self.cell_size = 800 // max(width, height)
            self.grid = [[0 for _ in range(width)] for _ in range(height)]
        else:
            print("Error: Width and height should be numbers between 5 and 100")

    def draw_grid(self):
        # ! Right hand side column goes off the screen
        if self.grid:
            self.cell_size = 800 // max(len(self.grid[0]), len(self.grid))
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    rect = pygame.Rect(1000 - len(self.grid[0]) * self.cell_size + j * self.cell_size,
                                       i * self.cell_size, self.cell_size, self.cell_size)
                    if not self.draw_checkbox.checked:
                        if (i, j) == self.start:
                            pygame.draw.rect(self.screen, START, rect)
                        elif (i, j) == self.end:
                            pygame.draw.rect(self.screen, END, rect)
                        else:
                            pygame.draw.rect(self.screen, MAIN if cell == 0 else GREEN, rect)
                    else:
                        pygame.draw.rect(self.screen, MAIN if cell == 0 else GREEN, rect)

            # Draw grid lines
            if self.show_grid_checkbox.checked:
                for i in range(len(self.grid[0])):  # Adjusted to iterate over the width of the grid
                    pygame.draw.line(self.screen, CONTRAST,
                                     (1000 - len(self.grid[0]) * self.cell_size + i * self.cell_size, 0),
                                     (1000 - len(self.grid[0]) * self.cell_size + i * self.cell_size,
                                      (len(self.grid) - 1) * self.cell_size), 2)  # Adjusted to stop at the last cell
                for i in range(len(self.grid)):  # Adjusted to iterate over the height of the grid
                    pygame.draw.line(self.screen, CONTRAST,
                                     (1000 - len(self.grid[0]) * self.cell_size, i * self.cell_size),
                                     (1000, i * self.cell_size), 2)

    def solve(self):
        pass
    def draw(self):
        pass

    def show_help(self):
        print("DrawPage show_help method called")
        help_page = DrawHelpPage(self.screen)
        help_page.display_page()

class GridHelpPage(GridPage):
    def __init__(self, screen):
        super().__init__(screen)
        self.back_button = Button("Back", 50, 50, 100, 50, RED, LIGHT_GRAY)

    def display_page(self):
        page = True

        while page:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(MAIN)
            self.back_button.draw(self.screen, self.back)
            small_text = UI.fonts['sm']
            text_surf1, text_rect1 = self.text_objects('Left click to place Start Position', small_text)
            text_rect1.center = (UI.half_width, UI.half_height - 100)
            self.screen.blit(text_surf1, text_rect1)
            text_surf2, text_rect2 = self.text_objects('Right click to place End Position', small_text)
            text_rect2.center = (UI.half_width, UI.half_height - 70)
            self.screen.blit(text_surf2, text_rect2)
            text_surf3, text_rect3 = self.text_objects('The input boxes only accept dimensions 5-100', small_text)
            text_rect3.center = (UI.half_width, UI.half_height)
            self.screen.blit(text_surf3, text_rect3)
            text_surf4, text_rect4 = self.text_objects('Only odd numbers are implemented, but even numbers are accepted', small_text)
            text_rect4.center = (UI.half_width, UI.half_height + 30)
            self.screen.blit(text_surf4, text_rect4)
            text_surf5, text_rect5 = self.text_objects('Press enter to generate blank grid', small_text)
            text_rect5.center = (UI.half_width, UI.half_height + 60)
            self.screen.blit(text_surf5, text_rect5)

            pygame.display.update()
            self.clock.tick(15)

    def back(self):
        print("Back method called")
        grid_page = GridPage(self.screen)
        grid_page.display_page()

class MazeHelpPage(MazePage):
    def __init__(self, screen):
        super().__init__(screen)
        self.back_button = Button("Back", 50, 50, 100, 50, RED, LIGHT_GRAY)

    def display_page(self):
        page = True

        while page:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(MAIN)
            self.back_button.draw(self.screen, self.back)
            small_text = UI.fonts['sm']
            text_surf1, text_rect1 = self.text_objects('Load a maze by pressing Use File button', small_text)
            text_rect1.center = (UI.half_width, UI.half_height - 100)
            self.screen.blit(text_surf1, text_rect1)
            text_surf2, text_rect2 = self.text_objects('File must be in correct format', small_text)
            text_rect2.center = (UI.half_width, UI.half_height - 70)
            self.screen.blit(text_surf2, text_rect2)
            text_surf3, text_rect3 = self.text_objects('Arrows after solve correspond to direction the path is travelling', small_text)
            text_rect3.center = (UI.half_width, UI.half_height)
            self.screen.blit(text_surf3, text_rect3)


            pygame.display.update()
            self.clock.tick(15)

    def back(self):
        print("Back method called")
        grid_page = MazePage(self.screen)
        grid_page.display_page()

class VisualGeneratorGrid(GeneratorGrid):
    def __init__(self, start, end, width, height, screen):
        super().__init__(start, end, width, height)
        self.screen = screen
        self.stack = []  # Stack to keep track of the path

    def generateStructure(self):
        # Draw a white rectangle as the background of the grid
        self.cell_size = 800 // max(self.width, self.height)
        pygame.draw.rect(self.screen, CONTRAST,
                         pygame.Rect(1000 - self.width * self.cell_size, 0,
                                     self.width * self.cell_size, self.height * self.cell_size))
        pygame.display.update()

        # Call the parent class's generateStructure method
        return super().generateStructure()
    def _dfs(self, x, y):
        self.array[y][x] = 0
        self.draw_cell(x, y, GREEN)  # Draw the current cell
        self.stack.append((x, y))  # Add the current cell to the stack
        np.random.shuffle(self.directions)
        for dx, dy in self.directions:
            nextX, nextY = x + 2*dx, y + 2*dy
            if (0 <= nextX < self.width) and (0 <= nextY < self.height) and self.array[nextY][nextX] == 1:
                self.array[nextY-dy][nextX-dx] = 0
                self.draw_cell(x + dx, y + dy, GREEN)  # Draw the cell in between
                self._dfs(nextX, nextY)
        if len(self.stack) > 1:  # If there are at least two cells in the stack
            prevX, prevY = self.stack[-2]  # Get the previous cell
            self.draw_cell((x + prevX) // 2, (y + prevY) // 2, MAIN)  # Draw the cell in between
            self.draw_cell(x, y, MAIN)  # Draw the cell after backtracking
        self.stack.pop()  # Remove the current cell from the stack

    def draw_cell(self, x, y, colour):
        self.cell_size = 800 // max(self.width, self.height)
        pygame.draw.rect(self.screen, colour,
                         pygame.Rect(1000 - self.width * self.cell_size + x * self.cell_size,
                                     y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()
        pygame.time.delay(40)

class VisualAStar(PathFinderGrid):
    def __init__(self, start, end, width, height, screen, cell_size, structure=None):
        super().__init__(start, end, width, height, structure)
        self.screen = screen
        self.cell_size = cell_size

    def aStar(self):
        startNode = Node(None, self.start)
        endNode = Node(None, self.end)

        openList = []
        closedList = []

        count = 0  # Counter for tie-breaking
        heapq.heappush(openList, (startNode.f, count, startNode))  # Add the start node

        while len(openList) > 0:
            currentNode = heapq.heappop(openList)[2]  # Node with the lowest f values
            closedList.append(currentNode)

            if currentNode == endNode:
                # Found the goal
                path = []
                while currentNode is not None:
                    path.append(currentNode.pos)
                    currentNode = currentNode.parent
                self.path = path[::-1]  # Reverse the path

                # Calculate the Manhattan distances for the final path
                manhattanDistTotal = sum(self.manhattanDist(path[i], path[i + 1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)
                return self.path

            children = self.getNeighbour(currentNode)
            for child in children:
                if child in closedList:
                    continue  # Child is already in the closed list
                child.g = currentNode.g + 1
                child.h = self.manhattanDist(child.pos, endNode.pos)
                child.f = child.g + child.h

                # Check if child is in open list and if it has a lower g value
                inOpenList = False
                for openNode in openList:
                    if child == openNode[2] and child.g >= openNode[2].g:
                        inOpenList = True
                        break

                if inOpenList:
                    continue  # Child is already in the open list and has a higher g value

                count += 1  # Increment counter
                heapq.heappush(openList, (child.f, count, child))  # Add the child to the open list

            self.draw(openList, closedList, currentNode)  # Draw the current state of the algorithm
        return []

    # ! Different dimensions does not align correctly.
    def draw(self, openList, closedList, currentNode):
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Calculate the remaining space on the left of the grid
        remaining_space_left = 1000 - (self.width * self.cell_size)

        # Draw the grid and walls here
        for i, row in enumerate(self.structure):
            for j, cell in enumerate(row):
                if cell == 1:  # If the cell is a wall
                    pygame.draw.rect(self.screen, (255, 255, 255),  # Draw the wall in white
                                     (remaining_space_left + j * self.cell_size,
                                      i * self.cell_size,
                                      self.cell_size, self.cell_size))

        for node in openList:
            pygame.draw.rect(self.screen, GREEN,
                             (remaining_space_left + node[2].pos[1] * self.cell_size,
                              node[2].pos[0] * self.cell_size,
                              self.cell_size, self.cell_size))  # Draw open nodes in green

        for node in closedList:
            pygame.draw.rect(self.screen, RED,
                             (remaining_space_left + node.pos[1] * self.cell_size,
                              node.pos[0] * self.cell_size,
                              self.cell_size, self.cell_size))  # Draw closed nodes in red

        pygame.draw.rect(self.screen, RED,
                         (remaining_space_left + currentNode.pos[1] * self.cell_size,
                          currentNode.pos[0] * self.cell_size,
                          self.cell_size, self.cell_size))  # Draw current node in blue

        pygame.display.update()  # Update the display
        pygame.time.delay(30)  # Delay to slow down the animation




def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Change screen size here
    pygame.display.set_caption('Main Menu')

    # Define your app here. For example:
    app = type('', (), {})()  # Create a simple empty object
    app.screen = screen

    # Initialize UI
    UI.init(app)

    menu = Menu(screen)
    menu.game_intro()


if __name__ == "__main__":
    main()
