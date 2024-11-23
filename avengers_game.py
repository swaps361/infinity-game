import pygame
import random
import sys
import cv2

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avengers Puzzle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (180, 180, 180)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 153, 0)

# Load and resize images
stone_image = pygame.image.load("stone.png")
stone_image = pygame.transform.scale(stone_image, (400, 400))

ironman_image = pygame.image.load("ironman.png")
captainamerica_image = pygame.image.load("captainamerica.png")
hulk_image = pygame.image.load("hulk.png")
thanos_image = pygame.image.load("thanos.png")

character_images = [ironman_image, captainamerica_image, hulk_image, thanos_image]
character_images = [pygame.transform.scale(img, (80, 80)) for img in character_images]

# Divide stone image into 4 pieces
piece_size = 200
pieces = [stone_image.subsurface((x, y, piece_size, piece_size)) for y in range(0, 400, piece_size) for x in range(0, 400, piece_size)]

# Puzzle state
puzzle_positions = [(500, 50), (700, 50), (500, 250), (700, 250)]
solved = [False] * 4

# Questions and answers
missions = [
    {"question": "Who defeated Thanos in the end?", "answer": "ironman", "piece": 0},
    {"question": "Who is the First Avenger?", "answer": "captainamerica", "piece": 1},
    {"question": "Who turns green when angry?", "answer": "hulk", "piece": 2},
    {"question": "Who wanted to eliminate half of life?", "answer": "thanos", "piece": 3},
]

# Shuffle missions
random.shuffle(missions)

# Font
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)

# Infinity Stones Quiz questions
infinity_stones_questions = [
    {"question": "Which stone is red in color?", "answer": "reality"},
    {"question": "Which stone manipulates time?", "answer": "time"},
    {"question": "Which stone controls minds?", "answer": "mind"},
]

def display_question(question):
    """Display the question at the top."""
    pygame.draw.rect(screen, DARK_GRAY, (50, 20, 700, 80), border_radius=10)
    text = font_large.render(question, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(text, text_rect)

def display_options(images):
    """Display the clickable options without text labels."""
    for idx, img in enumerate(images):
        x = 100 + idx * 150
        y = 450
        pygame.draw.rect(screen, GRAY, (x, y, 120, 120), border_radius=10)
        pygame.draw.rect(screen, BLUE, (x, y, 120, 120), 3, border_radius=10)
        screen.blit(img, (x + 20, y + 20))

def display_end_screen(message):
    """Display the solved puzzle and a custom congratulations message."""
    screen.fill(WHITE)
    screen.blit(stone_image, (200, 100))
    text = font_large.render(message, True, GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

def play_video(video_path):
    """Play a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame)

        screen.blit(pygame.transform.rotate(frame_surface, -90), (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

    cap.release()

def card_selection_animation(selected_card_rect):
    """Display an animation on the selected card."""
    for i in range(5):  # Simple pulsing effect
        pygame.draw.rect(screen, GREEN if i % 2 == 0 else WHITE, selected_card_rect.inflate(10, 10), border_radius=10)
        pygame.display.flip()
        pygame.time.delay(200)

def card_selection_game():
    """Display four cards and give 2 attempts to select the correct card."""
    hidden_star_index = random.randint(0, 3)  # Randomly choose the card with the star
    attempts = 2
    correct_card_selected = False

    while attempts > 0:
        screen.fill(WHITE)

        # Display the cards
        card_positions = []
        for idx, img in enumerate(character_images):
            x = 150 + idx * 150
            y = 300
            card_rect = pygame.Rect(x, y, 100, 150)
            card_positions.append(card_rect)

            pygame.draw.rect(screen, GRAY, card_rect, border_radius=10)
            pygame.draw.rect(screen, BLUE, card_rect, 3, border_radius=10)
            screen.blit(img, (x + 10, y + 20))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for idx, card_rect in enumerate(card_positions):
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        if idx == hidden_star_index:
                            card_selection_animation(card_rect)
                            correct_card_selected = True
                            break
                        else:
                            attempts -= 1
                            text = font_medium.render("Incorrect card. Try again.", True, RED)
                            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
                            screen.blit(text, text_rect)
                            pygame.display.flip()
                            pygame.time.delay(1500)

        if correct_card_selected:
            break

    if correct_card_selected:
        text = font_large.render("Correct card! Infinity Stones Quiz begins!", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        infinity_stones_quiz()
    else:
        text = font_large.render("Attempts over! Better luck next time.", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

def infinity_stones_quiz():
    """Ask 3 questions about Infinity Stones with selectable options."""
    stone_options = ["reality", "time", "mind"]  # Predefined options for answers

    for question_data in infinity_stones_questions:
        correct = False
        while not correct:
            screen.fill(WHITE)
            display_question(question_data["question"])

            # Display answer options
            for idx, option in enumerate(stone_options):
                x = 200 + idx * 200
                y = 300
                option_rect = pygame.Rect(x, y, 150, 100)
                pygame.draw.rect(screen, GRAY, option_rect, border_radius=10)
                pygame.draw.rect(screen, BLUE, option_rect, 3, border_radius=10)
                text = font_medium.render(option.capitalize(), True, BLACK)
                text_rect = text.get_rect(center=(x + 75, y + 50))
                screen.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    for idx, option in enumerate(stone_options):
                        x = 200 + idx * 200
                        y = 300
                        if x <= mouse_x <= x + 150 and y <= mouse_y <= y + 100:
                            if option == question_data["answer"]:
                                correct = True
                                text = font_medium.render("Correct!", True, GREEN)
                                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
                                screen.blit(text, text_rect)
                                pygame.display.flip()
                                pygame.time.delay(1000)
                            else:
                                text = font_medium.render("Incorrect! Try again.", True, RED)
                                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
                                screen.blit(text, text_rect)
                                pygame.display.flip()
                                pygame.time.delay(1000)

    display_end_screen("Congratulations! Wait for upcoming missions soon!")

def game_loop():
    running = True
    current_mission = 0

    while running:
        screen.fill(WHITE)

        # Draw the background grid for the puzzle area
        for pos in puzzle_positions:
            pygame.draw.rect(screen, GRAY, (*pos, piece_size, piece_size), border_radius=10)

        # Draw only solved puzzle pieces
        for i, pos in enumerate(puzzle_positions):
            if solved[i]:
                screen.blit(pieces[i], pos)

        # Display current question and options
        mission = missions[current_mission]
        display_question(mission["question"])
        display_options(character_images)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for idx, option in enumerate(["ironman", "captainamerica", "hulk", "thanos"]):
                    x = 100 + idx * 150
                    y = 450
                    if x <= mouse_x <= x + 120 and y <= y + 120:
                        if option == mission["answer"]:
                            solved[mission["piece"]] = True
                            current_mission += 1
                            if current_mission == len(missions):
                                running = False  # All questions answered
                        else:
                            text = font_medium.render("Incorrect! Try again.", True, RED)
                            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
                            screen.blit(text, text_rect)
                            pygame.display.flip()
                            pygame.time.delay(1000)

    display_end_screen("Puzzle Complete!")
    play_video("infinity.mp4")  # Play video after completing the puzzle
    card_selection_game()

# Run the game
play_video("welcome.mp4")
game_loop()
pygame.quit()
