# Description: A simple snake game using Pygame
# Imports
import pygame
import time
import random
import json
import os
import math

# Initialize Pygame 
pygame.init() # Initialize Pygame

# Path to the high scores file
high_scores_path = os.path.join(os.path.expanduser("~"), "high_scores.json")

# Constants
WIDTH, HEIGHT = 800, 600 # The width and height of the window
TOP_BAR_HEIGHT = 50 # The height of the top bar
FRUIT_PADDING = 40
GRID_SIZE = 10  # Size of the grid cells

# Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Fonts
LABEL_FONT = pygame.font.SysFont("comicsans", 26)
TITLE_FONT = pygame.font.SysFont("comicsans", 48)
H1_FONT = pygame.font.SysFont("comicsans", 36)

# Colors
BG_COLOR = (225, 225, 225)
TOP_BAR_COLOR = ("#13780A")
TEXT_COLOR = ("#1DB30E")

USER_EVENT = pygame.USEREVENT

# Global variables
player_name = ""
high_scores = {}

snake_speed = 15 # The speed of the snake
snake_pos = [100, 50]
snake_body = [
                [100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
            ]

# Fruit class
class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE))

    def collide(self, x, y):
        return self.x == x and self.y == y

# Setting default snake direction towards the right
direction = 'RIGHT'
change_to = direction

# Function to format time in minutes, seconds and milliseconds
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000 / 100)) # Calculate milliseconds
    seconds = int(round(secs % 60, 1))  # Calculate seconds
    minutes = int(secs // 60) # Calculate minutes

    return f"{minutes:02d}:{seconds:02d}:{milli}" # Return the formatted time

score = 0 # Initialize the score

# Function to draw the top bar
def draw_top_bar(win, elapsed_time, score):
    # Draw the top bar
    pygame.draw.rect(win, TOP_BAR_COLOR, (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    #Labels
    score_label = LABEL_FONT.render(f"Score: {score}", 1, "white")

    # Draw the labels
    win.blit(time_label, (10, 5))
    win.blit(score_label, ((780 - score_label.get_width() // 2) - (score_label.get_width() - score_label.get_width() // 2), 5))

# Function for the home screen
def home_screen(win):
    # Global variables
    global player_name
    run = True
    user_input = ""
    is_displayed_name = False

    # Main loop
    while run:
        win.fill(BG_COLOR)

        # Title
        title_label = TITLE_FONT.render("Snake Game", 1, ("#1DB30E"))
        win.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 100))

        # Start Button
        start_button_width, start_button_height = 200, 50
        start_button_x = WIDTH // 2 - start_button_width // 2
        start_button_y = 300
        pygame.draw.rect(win, ("#1DB30E"), (start_button_x, start_button_y, start_button_width, start_button_height))
        start_button_text = LABEL_FONT.render("Start", 1, "white")
        win.blit(start_button_text, (start_button_x + start_button_width // 2 - start_button_text.get_width() // 2, 
                               start_button_y + start_button_height // 2 - start_button_text.get_height() // 2))

        # Ask for player's name
        name_label = LABEL_FONT.render("Enter your name:", 1, ("#1DB30E"))
        win.blit(name_label, (WIDTH // 2 - 100, 375))

        # Input Box
        input_box_width, input_box_height = start_button_width, start_button_height
        input_box_x = start_button_x
        input_box_y = 425
        input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(win, ("#1DB30E"), input_box, 2)

        # Calculate the maximum number of characters that can fit in the input box
        max_chars = input_box_width // LABEL_FONT.size('O')[0]

        # Trim the user input if it exceeds the maximum number of characters
        trimmed_user_input = user_input[:max_chars]

        # Render the user input
        text_surface = LABEL_FONT.render(trimmed_user_input, True, ("#1DB30E"))
        win.blit(text_surface, (input_box.x + 10, input_box.y + 5))

        
        # Render error messages
        if is_displayed_name:
            error_message_name = LABEL_FONT.render("Please enter your name.", 1, "red")
            win.blit(error_message_name, (WIDTH // 2 - error_message_name.get_width() // 2, 465))


        # Update the display
        pygame.display.update()

        # Event Handling
        for event in pygame.event.get():
            # Handle window close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get the mouse position
                if start_button_x <= mouse_x <= start_button_x + start_button_width and start_button_y <= mouse_y <= start_button_y + start_button_height:
                    is_displayed_name = not user_input.strip() # Check if the player's name is entered
                    if not is_displayed_name:
                        player_name = user_input.strip() # Set the player's name
                        run = False  # Exit the loop
            
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_input = user_input[:-1]    # Remove the last character
                else:
                    user_input += event.unicode # Add the character to the user input

# Function to display the end screen
def end_screen(win, elapsed_time, score, player_name, high_scores, high_scores_dic):
    win.fill(BG_COLOR)

    # Update high score for the current player
    if player_name in high_scores_dic:
        if score > high_scores_dic[player_name]:
            high_scores[player_name] = (score) # Update the high score
    else:
        high_scores[player_name] = (score) # Add the player to the high scores

    # Save the updated high scores
    save_high_scores()

    # Render the end screen
    title_label = TITLE_FONT.render("Game Over", 1, TEXT_COLOR)
    stats_label = H1_FONT.render("Stats", 1, TEXT_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, TEXT_COLOR)
    score_label = LABEL_FONT.render(f"Score: {score}", 1, TEXT_COLOR)

    # Render the labels
    win.blit(title_label, (get_middle(title_label), 25))
    win.blit(stats_label, (100, 100))
    win.blit(time_label, (stats_label.get_width() // 2, win.get_height() // 2 - 100))
    win.blit(score_label, (stats_label.get_width() // 2, win.get_height() // 2 - 50))

    # Render high scores
    high_scores_label = H1_FONT.render("High Scores", 1, TEXT_COLOR)
    sorted_scores = sorted(high_scores_dic.items(), key=lambda x: x[1], reverse=True)  # Sort by score
    win.blit(high_scores_label, ((750 - high_scores_label.get_width() // 2) - (high_scores_label.get_width() - high_scores_label.get_width() // 2), 100))
    for idx, (player_name, high_scores) in enumerate(sorted_scores):
        score_label = LABEL_FONT.render(f"{idx + 1}. {player_name}: {high_scores}", 1, TEXT_COLOR)  # Render the high scores
        win.blit(score_label, ((700 - high_scores_label.get_width() // 2) - (high_scores_label.get_width() - high_scores_label.get_width() // 2), win.get_height() // 2 - 100 + idx * 30))  # Position the high scores
        if idx + 1 == 5:
            win.blit(LABEL_FONT.render("", 1, TEXT_COLOR), (850, 200 + (idx + 1) * 30))  # Render the ellipsis
            break

    # Main Button
    main_button_width, main_button_height = 200, 50
    main_button_x = get_middle(high_scores_label)
    main_button_y = 500
    pygame.draw.rect(win, TEXT_COLOR, (main_button_x, main_button_y, main_button_width, main_button_height))  # Draw the button
    main_button_text = LABEL_FONT.render("Main Menu", 1, "white")
    win.blit(main_button_text, (main_button_x + main_button_width // 2 - main_button_text.get_width() // 2, 
                               main_button_y + main_button_height // 2 - main_button_text.get_height() // 2))  # Position the button

    # Reset High Score Button
    reset_high_score_button_width, reset_high_score_button_height = 225, 50
    reset_high_score_button_x = (750 - high_scores_label.get_width() // 2) - (high_scores_label.get_width() - high_scores_label.get_width() // 2)
    reset_high_score_button_y = 500
    pygame.draw.rect(win, TEXT_COLOR, (reset_high_score_button_x, reset_high_score_button_y, reset_high_score_button_width, reset_high_score_button_height)) # Draw the button
    reset_high_score_button_text = LABEL_FONT.render("Reset High Score", 1, "white")
    win.blit(reset_high_score_button_text, (reset_high_score_button_x + reset_high_score_button_width // 2 - reset_high_score_button_text.get_width() // 2, 
                               reset_high_score_button_y + reset_high_score_button_height // 2 - reset_high_score_button_text.get_height() // 2)) # Position the button

    # Restart High Score Button
    restart_button_width, restart_button_height = 150, 50
    restart_button_x = 50
    restart_button_y = 500
    pygame.draw.rect(win, TEXT_COLOR, (restart_button_x, restart_button_y, restart_button_width, restart_button_height)) # Draw the button
    restart_button_text = LABEL_FONT.render("Restart", 1, "white")
    win.blit(restart_button_text, (restart_button_x + restart_button_width // 2 - restart_button_text.get_width() // 2, 
                               restart_button_y + restart_button_height // 2 - restart_button_text.get_height() // 2)) # Position the button


    pygame.display.update()  # Update the display

    run_end = True  # Run the end screen

    # Main loop
    while run_end:
        # Event Handling
        for event in pygame.event.get():
            # Handle window close button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position
                if main_button_x <= mouse_x <= main_button_x + main_button_width and main_button_y <= mouse_y <= main_button_y + main_button_height:
                    run_end = False  # Exit the loop
                    start_game()  # Goes back to home screen
                    
                if restart_button_x <= mouse_x <= restart_button_x + restart_button_width and restart_button_y <= mouse_y <= restart_button_y + restart_button_height:
                    run_end = False  # Exit the loop
                    main(WIN)  # Goes back to home screen

                # Reset High Score Button
                if reset_high_score_button_x <= mouse_x <= reset_high_score_button_x + reset_high_score_button_width and reset_high_score_button_y <= mouse_y <= reset_high_score_button_y + reset_high_score_button_height:
                    win.fill(BG_COLOR)  # Clear the screen

                    # Render the reset high score screen
                    title_text = "Are you sure you want to reset your high scores?"
                    title_lines = title_text.split(" ")  # Split the text into words
                    line1 = " ".join(title_lines[:6])  # First line
                    line2 = " ".join(title_lines[6:])  # Second line

                    title_label1 = H1_FONT.render(line1, 1, TEXT_COLOR)
                    title_label2 = H1_FONT.render(line2, 1, TEXT_COLOR)

                    win.blit(title_label1, (get_middle(title_label1), 150))
                    win.blit(title_label2, (get_middle(title_label2), 200))

                    # Yes Button
                    yes_button_width, yes_button_height = 200, 50
                    yes_button_x = 100
                    yes_button_y = 400
                    pygame.draw.rect(win, TEXT_COLOR, (yes_button_x, yes_button_y, yes_button_width, yes_button_height))  # Draw the button
                    yes_button_text = LABEL_FONT.render("Yes", 1, "white")
                    win.blit(yes_button_text, (yes_button_x + yes_button_width // 2 - yes_button_text.get_width() // 2, 
                                               yes_button_y + yes_button_height // 2 - yes_button_text.get_height() // 2))  # Position the button

                    # No Button
                    no_button_width, no_button_height = 200, 50
                    no_button_x = (700 - no_button_width // 2) - (no_button_width - no_button_width // 2)
                    no_button_y = 400
                    pygame.draw.rect(win, TEXT_COLOR, (no_button_x, no_button_y, no_button_width, no_button_height))  # Draw the button
                    no_button_text = LABEL_FONT.render("No", 1, "white")
                    win.blit(no_button_text, (no_button_x + no_button_width // 2 - no_button_text.get_width() // 2, 
                                              no_button_y + no_button_height // 2 - no_button_text.get_height() // 2))  # Position the button
                    pygame.display.update()  # Update the display

                    confirm_reset = True  # Confirm the reset

                    # Main loop
                    while confirm_reset:
                        # Handle window close button
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            # Handle mouse clicks
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position
                                if yes_button_x <= mouse_x <= yes_button_x + yes_button_width and yes_button_y <= mouse_y <= yes_button_y + yes_button_height:
                                    high_scores_dic.clear()  # Clear the high scores
                                    save_high_scores()  # Save the empty high scores
                                    confirm_reset = False  # Confirms the reset
                                    run_end = False  # Exit the loop
                                    start_game()  # Restart the game

                                # No Button
                                if no_button_x <= mouse_x <= no_button_x + no_button_width and no_button_y <= mouse_y <= no_button_y + no_button_height:
                                    confirm_reset = False  # Doesn't confirm the reset
                                    end_screen(win, elapsed_time, score, player_name, high_scores, high_scores_dic)  # Display the end screen

# Function to get the middle of the screen
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2 # Return the middle of the screen

# Function to load high scores from a JSON file
def load_high_scores():
    # Global variables
    global high_scores 
    try:
        with open(high_scores_path, "r") as file:
            high_scores = json.load(file) # Load the high scores from the file
            high_scores = {player: int(data[0]) if isinstance(data, list) else int(data) for player, data in high_scores.items()}
    except FileNotFoundError:
        high_scores = {} # Create an empty dictionary if the file does not exist

# Function to save high scores to a JSON file
def save_high_scores():
    with open(high_scores_path, "w") as file:
        json.dump(high_scores, file) # Save the high scores to the file

# Game function
def main(win):
    load_high_scores() # Load the high scores

    global snake_speed
    global change_to
    global direction
    global snake_pos
    global snake_body
    global fruits_pos
    global Fruit

    # Function to spawn a new fruit
    def spawn_fruit():
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(TOP_BAR_HEIGHT // GRID_SIZE, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return Fruit(x, y)

    # Initialize game variables
    score = 0
    start_time = time.time()
    direction = 'RIGHT'
    change_to = direction
    snake_speed = 15  # Set a reasonable initial speed
    snake_pos = [100, 50]
    snake_body = [
        [100, 50],
        [90, 50],
        [80, 50],
        [70, 50]
    ]
    fruits_pos = [spawn_fruit()]

    clock = pygame.time.Clock()

    run = True

    while run:
        elapsed_time = time.time() - start_time
        clock.tick(snake_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        if direction == "UP":
            snake_pos[1] -= GRID_SIZE
        if direction == "DOWN":
            snake_pos[1] += GRID_SIZE
        if direction == "LEFT":
            snake_pos[0] -= GRID_SIZE
        if direction == "RIGHT":
            snake_pos[0] += GRID_SIZE

        snake_body.insert(0, list(snake_pos))

        for fruit_pos in fruits_pos:
            if fruit_pos.collide(*snake_pos):
                fruits_pos.remove(fruit_pos)
                score += 10
                snake_speed += 1
                fruits_pos.append(spawn_fruit())
                if score % 50 == 0:
                    fruits_pos.append(spawn_fruit())
                break
        else:
            snake_body.pop()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                end_screen(WIN, elapsed_time, score, player_name, high_scores, high_scores)
                run = False
                break

        if snake_pos[0] >= WIDTH or snake_pos[0] < 0 or snake_pos[1] >= HEIGHT or snake_pos[1] < TOP_BAR_HEIGHT:
            end_screen(WIN, elapsed_time, score, player_name, high_scores, high_scores)
            run = False
            break

        win.fill(BG_COLOR)
        for pos in snake_body:
            pygame.draw.rect(win, TEXT_COLOR, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))

        # Draw eyes on the head of the snake
        head_pos = snake_body[0]
        eye_radius = 2
        eye_offset_x = 3
        eye_offset_y = 3

        # Left eye
        pygame.draw.circle(win, (0, 0, 0), (head_pos[0] + eye_offset_x, head_pos[1] + eye_offset_y), eye_radius)
        # Right eye
        pygame.draw.circle(win, (0, 0, 0), (head_pos[0] + GRID_SIZE - eye_offset_x, head_pos[1] + eye_offset_y), eye_radius)

        for fruit in fruits_pos:
            fruit.draw(win)

        draw_top_bar(win, elapsed_time, score)
        pygame.display.update()

    pygame.quit()
# Function to start the game
def start_game():
    home_screen(WIN)
    main(WIN)

# Start the game
start_game()
