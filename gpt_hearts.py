import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hearts")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define card dimensions
card_width = 50
card_height = 70

# Create the deck of cards
suits = ["H", "D", "C", "S"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = [(rank, suit) for suit in suits for rank in ranks]

# Shuffle the deck
random.shuffle(deck)

# Initialize the players' hands
player_hand = []
opponent_hand = []
played_cards = []

# Deal the cards to the players
for i in range(13):
    player_hand.append(deck.pop())
    opponent_hand.append(deck.pop())

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill(WHITE)

    # Draw the player's hand
    for i, card in enumerate(player_hand):
        card_x = i * (card_width + 10) + 50
        card_y = window_height - card_height - 50
        pygame.draw.rect(window, RED, (card_x, card_y, card_width, card_height))
        pygame.draw.rect(
            window, WHITE, (card_x + 2, card_y + 2, card_width - 4, card_height - 4)
        )
        font = pygame.font.Font(None, 24)
        text = font.render(card[0], True, BLACK)
        window.blit(text, (card_x + 10, card_y + 10))

    # Draw the opponent's hand (as covered cards)
    for i in range(len(opponent_hand)):
        card_x = i * (card_width + 10) + 50
        card_y = 50
        pygame.draw.rect(window, GREEN, (card_x, card_y, card_width, card_height))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
