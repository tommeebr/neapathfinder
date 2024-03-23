
import heapq
import math
import random
import numpy as np
import pygame
from pygame.locals import *
import sys


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
    def __init__(self, *args): 
        self.path = [] 
        self.fileInit = False
        if len(args) == 1 and isinstance(args[0], str): 
            self.loadFile(args[0])
            self.fileInit = True
        elif len(args) == 4 and all(isinstance(arg, tuple) for arg in args[:2]) and all(isinstance(arg, int) for arg in args[2:]): 
            self.start, self.end, self.height, self.width = args
            self.validateInputs()
            self.structInstance = GeneratorStructure(self.start, self.end, self.height, self.width) 
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
            while True:
                self.generateStructure()
                if self.aStar():
                    break

    def aStar(self):
        startNode = Node(None, (self.start[1], self.start[0]))  
        endNode = Node(None, (self.end[1], self.end[0]))  

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
                manhattanDistTotal = sum(self.manhattanDist(path[i], path[i+1]) for i in range(len(path) - 1))

                print("Total Manhattan distance for path:", manhattanDistTotal)
                return True

            children = self.getNeighbour(currentNode)
            for child in children:
                if child in closedList:
                    continue  # Child is already in the closed list
                child.g = currentNode.g + 1
                child.h = self.manhattanDist(child.pos, endNode.pos)
                child.f = child.g + child.h

                if any(openNode for openNode in openList if child == openNode[2] and child.g > openNode[2].g):
                    continue  # Child is already in the open list and has a higher g value

                count += 1  # Increment counter
                heapq.heappush(openList, (child.f, count, child))  # Add the child to the open list          
        return False

    def getNeighbour(self, node, grid):
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
            if nodePos[0] < 0 or nodePos[0] >= self.height or nodePos[1] < 0 or nodePos[1] >= self.width:
                continue  # Node is out of bounds
            if self.structure[nodePos[0]][nodePos[1]] != 0:
                continue  # Node is not walkable
            neighbors.append(Node(node, nodePos))
        return neighbors
    
    def generateStructure(self):
        self.structInstance = GeneratorGrid(self.start, self.end, self.height, self.width)
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
        self.colour_active = GREEN  # Define the active color as green
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
            if 5 <= val <= 100:
                self.error_message = ''
                return True
        self.error_message = 'Error: Input should be a number between 5 and 100'
        return False

class Menu:
    def __init__(self,screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.maze_button = Button("Maze", UI.half_width - 50, UI.half_height + 50, 100, 50, GREEN, LIGHT_GRAY)
        self.grid_button = Button("Grid", UI.half_width - 50, UI.half_height - 50, 100, 50, GREEN, LIGHT_GRAY)

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
            TextRect1.center = ((SCREEN_WIDTH/2),(150))
            self.screen.blit(TextSurf1, TextRect1)

            TextSurf2, TextRect2 = self.text_objects("Showcase", large_text)
            TextRect2.center = ((SCREEN_WIDTH/2),(200))
            self.screen.blit(TextSurf2, TextRect2)

            self.maze_button.draw(self.screen, self.maze_page)
            self.grid_button.draw(self.screen, self.grid_page)

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

    def back(self):
        menu = Menu(self.screen)
        menu.game_intro()

class GridPage(Page):
    def __init__(self, screen):
        super().__init__(screen, "Grid")
        self.generate_button = Button("Generate", 50, 300, 100, 50, GREEN, LIGHT_GRAY)
        self.use_file_button = Button("Use File", 50, 375, 100, 50, GREEN, LIGHT_GRAY)
        self.help_button = Button("Help", 50, 450, 100, 50, BLUE, LIGHT_GRAY)
        self.width_input = InputBox(50, 150, 100, 32, self, 'Width')  # Pass self as the page argument
        self.height_input = InputBox(50, 225, 100, 32, self, 'Height')  # Pass self as the page argument
        self.grid = []
        self.start = None
        self.end = None

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

                if event.type == pygame.MOUSEBUTTONDOWN and self.grid:
                    cell_size = 800 // max(len(self.grid[0]), len(self.grid))  # Calculate cell size here
                    x, y = event.pos
                    grid_x = (x - (1000 - len(self.grid[0]) * cell_size)) // cell_size
                    grid_y = y // cell_size

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
            self.use_file_button.draw(self.screen, lambda: None)
            self.help_button.draw(self.screen, self.show_help)
            self.width_input.draw(self.screen)
            self.height_input.draw(self.screen)

            self.draw_grid()

            if self.start:
                start_text = small_text.render(f'Start: {self.start}', True, CONTRAST)
                self.screen.blit(start_text, (10, SCREEN_HEIGHT - 40))

            if self.end:
                end_text = small_text.render(f'End: {self.end}', True, CONTRAST)
                self.screen.blit(end_text, (10, SCREEN_HEIGHT - 20))

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

            cell_size = 800 // max(width, height)
            self.grid = [[0 for _ in range(width)] for _ in range(height)]
        else:
            print("Error: Width and height should be numbers between 5 and 100")

    def draw_grid(self):
        if self.grid:
            cell_size = 800 // max(len(self.grid[0]), len(self.grid))
            for i, row in enumerate(self.grid):
                for j, cell in enumerate(row):
                    if self.start is not None and (i, j) == self.start:
                        colour = START  # Start position colour
                    elif self.end is not None and (i, j) == self.end:
                        colour = END  # End position colour
                    else:
                        colour = MAIN  # Default colour
                    pygame.draw.rect(self.screen, colour,
                                     pygame.Rect(1000 - len(self.grid[0]) * cell_size + j * cell_size,
                                                 i * cell_size, cell_size, cell_size))

            # Draw grid lines
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    pygame.draw.rect(self.screen, CONTRAST,
                                     pygame.Rect(1000 - len(self.grid[0]) * cell_size + j * cell_size,
                                                 i * cell_size, cell_size, cell_size), 1)
    def generate(self):
        pass

    def show_help(self):
        print("GridPage show_help method called")
        help_page = GridHelpPage(self.screen)
        help_page.display_page()

class MazePage(Page):
    def __init__(self, screen):
        super().__init__(screen, "Maze")
        self.help_button = Button("Help", 50, 450, 100, 50, BLUE, LIGHT_GRAY)

        # Add any specific buttons or functionality for the Maze page

    def display_page(self):
        # Implement the display_page method for the Maze page
        pass

    def show_help(self):
        print("GridPage show_help method called")
        help_page = GridHelpPage(self.screen)
        help_page.display_page()

class GridHelpPage(GridPage):
    def __init__(self, screen):
        super().__init__(screen)
        self.back_button = Button("Back", 50, 50, 100, 50, RED, LIGHT_GRAY)

    def display_page(self):
        print("GridHelpPage display_page method called")
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

    def display_page(self):
        # Implement the method to display help content for the Maze page
        pass

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