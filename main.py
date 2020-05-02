# BY : Mohamed Ashraf Gaber

# This is a Snake Game.
# It made by PYGAME.
# You can play using the arrows in your keyboard.
# You die when you hit yourself.
# When you die there will be a message that tell you your score and the option to play again.

# Importing our libraries we need.
import pygame
import random
import tkinter as tk
from tkinter import messagebox


pygame.init()  # Initializing the game.
pygame.display.set_caption("Snake Game")  # To set a title to the game.

# The global variables we will use
run = True  # For run the game and end it when you die.
width = 500  # The width and the height of the screen.
rows = 20  # The number of rows we want to make grid.
score = 1  # The score of the player.

# The Colors we will use.
background_color = (75, 75, 75)
snake_color = (48, 175, 153)
grid_lines_color = (222, 222, 222)
food_color = (0, 100, 0)


# Creating the Cube class that will be the main thing in the game.
class Cube:
    def __init__(self, start, direction_x=1, direction_y=0, color=snake_color):
        # Declare the variables we need to control the cube.
        self.pos = start  # The start position that the player will start playing from it.
        self.direction_x = direction_x  # The x direction of the snake.
        self.direction_y = direction_y  # The y direction of the snake.
        self.color = color  # The color of the snake.

    # This method make the cube moves.
    def move(self, direction_x, direction_y):
        self.direction_x = direction_x  # Set the new x direction
        self.direction_y = direction_y  # Set the new y direction

        # Change the position to a new one.
        # noinspection PyUnresolvedReferences
        self.pos = (self.pos[0] + self.direction_x, self.pos[1] + self.direction_y)

    def draw(self, surface):
        size = width // rows  # The size of the cube

        i, j = self.pos[0], self.pos[1]  # Set the x and y axes of the cube.

        # Drawing the cube in the screen.
        pygame.draw.rect(surface, self.color, (i*size+2, j*size+2, size-4, size-4))


# Creating the Snake class that will be the snake and will contain the Cube class.
class Snake:
    body = []  # The body list will contain all the cubes of the snake.
    turns = {}  # The turns dictionary will contain all turns the user will make.

    def __init__(self, pos, color):
        self.head = Cube(pos)  # Creating a head for the snake.
        self.color = color  # The color of the snake.
        self.body.append(self.head)  # Append the head inside the body list.

        # The first directions the snake has.
        self.direction_x = 1
        self.direction_y = 0

    def move(self):
        global run  # Making the run variable global to can change it.

        # Loop for every event user do.
        for event in pygame.event.get():
            # If the player quit the quit button, the game close.
            if event.type == pygame.QUIT:
                run = False

            keys = pygame.key.get_pressed()  # Get all keys player pressed.

            # Loop for every key user pressed.
            for _ in keys:
                # Checking if the player wants to go to RIGHT direction and he isn't in the LEFT direction.
                if keys[pygame.K_RIGHT] and self.direction_x != -1:
                    self.direction_x, self.direction_y = 1, 0

                # Checking if the player wants to go to LEFT direction and he isn't in the RIGHT direction.
                elif keys[pygame.K_LEFT] and self.direction_x != 1:
                    self.direction_x, self.direction_y = -1, 0

                # Checking if the player wants to go to UP direction and he isn't in the DOWN direction.
                elif keys[pygame.K_UP] and self.direction_y != 1:
                    self.direction_x, self.direction_y = 0, -1

                # Checking if the player wants to go to DOWN direction and he isn't in the UP direction.
                elif keys[pygame.K_DOWN] and self.direction_y != -1:
                    self.direction_x, self.direction_y = 0, 1

                # Append the new direction in the turns dictionary.
                self.turns[self.head.pos[:]] = (self.direction_x, self.direction_y)

        # Loop for every cube in the Snake.
        for i, c in enumerate(self.body):
            p = c.pos[:]  # Set the position of the current cube in (p) variable.

            # Checking if the position in the turns dictionary.
            # If the position is in the turns dictionary.
            if p in self.turns:
                turn = self.turns[p]  # Set the new direction in (turn) variable.
                c.move(turn[0], turn[1])  # And call (move) method for this turn.
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            # If the position isn't in the turns dictionary.
            else:
                # Checking if the snake reaches the end of the screen.
                # If the snake reaches the LEFT side, it will appear the RIGHT side.
                if c.direction_x == -1 and c.pos[0] <= 0:
                    c.pos = (rows-1, c.pos[1])
                # If the snake reaches the RIGHT side, it will appear the LEFT side.
                elif c.direction_x == 1 and c.pos[0] >= rows - 1:
                    c.pos = (0, c.pos[1])
                # If the snake reaches the TOP side, it will appear the BOTTOM side.
                elif c.direction_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows-1)
                # If the snake reaches the BOTTOM side, it will appear the TOP side.
                elif c.direction_y == 1 and c.pos[1] >= rows - 1:
                    c.pos = (c.pos[0], 0)
                # If not, move the snake in the same direction.
                else:
                    c.move(c.direction_x, c.direction_y)

    # Drawing the snake.
    def draw(self, surface):
        # For every element inside the body list, call the draw method that's inside the Cube class.
        for i, c in enumerate(self.body):
            c.draw(surface)

    # Adding a new cube when snake eats food.
    def add_cube(self):
        # Get the last cube of the snake.
        tail = self.body[-1]
        # Get the last cube position.
        dx, dy = tail.direction_x, tail.direction_y

        # Checking what is the direction of the snake.
        # If the snake walk RIGHT, add cube to the LEFT.
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))

        # If the snake walk LEFT, add cube to the RIGHT.
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))

        # If the snake walk DOWN, add cube to the UP.
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))

        # If the snake walk UP, add cube to the DOWN.
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        # Set the direction of the last cube to the previous one.
        self.body[-1].direction_x, self.body[-1].direction_y = dx, dy

    # The reset method reset everything when the snake die and begins a new game.
    def reset(self, pos):
        global score

        self.body = []
        self.turns = {}
        self.head = Cube(pos)
        self.body.append(self.head)
        self.direction_x = 1
        self.direction_y = 0
        score = 0


# The main function that will contain everything will happen.
# noinspection PyGlobalUndefined
def main():
    # making the player, food, score global to be able to use the methods that's inside it anywhere.
    global player, food, score

    # This is the surface that will draw inside it and every thing will work in it.
    win = pygame.display.set_mode((width, width))
    clock = pygame.time.Clock()  # The clock object to be able to change the FPS to make sure that the game isn't fast.

    # Creating The snake object in (10, 10) position and this color
    player = Snake((10, 10), (48, 175, 153))

    # Creating The food object in random position and this color
    food = Cube(random_food(player), color=food_color)

    # This loop will make the game run and will stop when game ended
    while run:
        pygame.time.delay(50)  # Making a 50 milliseconds delay.
        clock.tick(10)  # Set the FPS to 10.

        if player.body[0].pos == food.pos:
            player.add_cube()
            food = Cube(random_food(player), color=food_color)
            score += 1

        player.move()  # Calling the move method that move the snake.

        # Checking if the snake hits itself.
        for x in range(len(player.body)):
            if player.body[x].pos in list(map(lambda z: z.pos, player.body[x + 1:])):
                print('Score: ', len(player.body))
                message_box('You Lost!', f'Your score is {score}. Play again...')
                player.reset((10, 10))
                break

        draw_window(win)  # Drawing all things in the screen.


# This function will draw everything in the window.
def draw_window(surface):
    surface.fill(background_color)  # fill the screen with black
    draw_grid(surface)  # Drawing grid
    food.draw(surface)  # Calling the draw method to draw the food.
    player.draw(surface)  # Calling the draw method to draw every cube in the snake.
    print_score(surface)  # Print the score in the screen.

    pygame.display.update()  # Update the screen.


# This function will draw the grid in the window.
def draw_grid(surface):
    size_between = width // rows  # The size between rows

    x = y = 0  # Starting drawing the lines from the top left.

    # To draw the grid in all the window.
    for i in range(size_between):
        x += size_between
        y += size_between

        pygame.draw.line(surface, grid_lines_color, (x, 0), (x, width))  # Drawing the horizontal lines.
        pygame.draw.line(surface, grid_lines_color, (0, y), (width, y))  # Drawing the vertical lines.


# This function will make random food.
def random_food(s):
    pos = s.body  # Get the body of the snake.

    while True:
        # Get random x and y axes
        x, y = random.randrange(rows), random.randrange(rows)

        # Check if the random position is in the position snake.
        if len(list(filter(lambda z: z.pos == (x, y), pos))):
            continue
        else:
            # Return the first position that isn't in the snake's body.
            return x, y


# This function prints the score in the screen.
def print_score(surface):
    font = pygame.font.SysFont('Arial', 40, True)  # The settings of the font
    text = font.render('SCORE: ' + str(score), 1, (255, 255, 255))  # make the text able to be on the screen
    surface.blit(text, (width - 180, 5))


# The message that will appear when the snake die.
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()


# Calling the main loop to run the game
main()

# If reaches here the game will stop
pygame.quit()
