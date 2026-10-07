import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window Setup
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors - Best of 3")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (30, 32, 44)
CARD_BG = (45, 49, 66)
TEXT_COLOR = (240, 240, 240)
MUTED_TEXT = (160, 160, 170)
ACCENT_BLUE = (74, 144, 226)
ACCENT_GREEN = (72, 187, 120)
ACCENT_RED = (229, 62, 62)
ACCENT_YELLOW = (236, 201, 75)
HOVER_COLOR = (90, 160, 240)
RESET_BTN_COLOR = (220, 80, 80)
RESET_HOVER_COLOR = (240, 100, 100)
PLAY_AGAIN_COLOR = (72, 187, 120)
PLAY_AGAIN_HOVER = (92, 207, 140)

# Fonts
font_title = pygame.font.SysFont("Arial", 40, bold=True)
font_large = pygame.font.SysFont("Arial", 32, bold=True)
font_medium = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 16)

# Game Rules
WINNING_SCORE = 3
choices = ["Rock", "Paper", "Scissors"]

# Game State Variables
player_score = 0
computer_score = 0
player_choice = None
computer_choice = None
result_text = "First to 3 points wins! Make your move."
result_color = TEXT_COLOR
game_over = False

# Buttons setup
button_width, button_height = 180, 55
move_button_y = 480

move_buttons = [
    {"name": "Rock", "rect": pygame.Rect(100, move_button_y, button_width, button_height)},
    {"name": "Paper", "rect": pygame.Rect(310, move_button_y, button_width, button_height)},
    {"name": "Scissors", "rect": pygame.Rect(520, move_button_y, button_width, button_height)},
]

reset_button = {"rect": pygame.Rect(310, 560, button_width, 45)}


def determine_winner(player, computer):
    if player == computer:
        return "It's a Tie!", ACCENT_YELLOW, 0, 0
    elif (
        (player == "Rock" and computer == "Scissors") or
        (player == "Paper" and computer == "Rock") or
        (player == "Scissors" and computer == "Paper")
    ):
        return "You Win the Round!", ACCENT_GREEN, 1, 0
    else:
        return "Computer Wins the Round!", ACCENT_RED, 0, 1


def reset_game():
    global player_score, computer_score, player_choice, computer_choice
    global result_text, result_color, game_over
    player_score = 0
    computer_score = 0
    player_choice = None
    computer_choice = None
    result_text = "New match! First to 3 points wins."
    result_color = TEXT_COLOR
    game_over = False


def draw_icon(name, center, color):
    """Draw a simple rock / paper / scissors icon using shapes."""
    cx, cy = center

    if name == "Rock":
        pygame.draw.circle(screen, color, (cx, cy), 32)
        pygame.draw.circle(screen, CARD_BG, (cx - 10, cy - 10), 6)
        pygame.draw.circle(screen, CARD_BG, (cx + 12, cy + 8), 4)

    elif name == "Paper":
        page = pygame.Rect(0, 0, 54, 66)
        page.center = (cx, cy)
        pygame.draw.rect(screen, color, page, border_radius=5)
        for i in range(4):
            y = page.top + 14 + i * 13
            pygame.draw.line(screen, CARD_BG, (page.left + 10, y), (page.right - 10, y), 3)

    elif name == "Scissors":
        # two blades crossing
        pygame.draw.line(screen, color, (cx - 24, cy - 30), (cx + 14, cy + 14), 6)
        pygame.draw.line(screen, color, (cx + 24, cy - 30), (cx - 14, cy + 14), 6)
        # two finger loops
        pygame.draw.circle(screen, color, (cx - 14, cy + 24), 11, 5)
        pygame.draw.circle(screen, color, (cx + 14, cy + 24), 11, 5)


# Main Game Loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Handle Reset / Play Again Button
            if reset_button["rect"].collidepoint(mouse_pos):
                reset_game()

            # Handle Move Buttons (only active if game is ongoing)
            elif not game_over:
                for btn in move_buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        player_choice = btn["name"]
                        computer_choice = random.choice(choices)

                        res_msg, color, p_pts, c_pts = determine_winner(player_choice, computer_choice)
                        player_score += p_pts
                        computer_score += c_pts

                        # Check Match Winner
                        if player_score == WINNING_SCORE:
                            result_text = "YOU WON THE MATCH!"
                            result_color = ACCENT_GREEN
                            game_over = True
                        elif computer_score == WINNING_SCORE:
                            result_text = "COMPUTER WON THE MATCH!"
                            result_color = ACCENT_RED
                            game_over = True
                        else:
                            result_text = res_msg
                            result_color = color

    # Drawing
    screen.fill(BG_COLOR)

    # Title Banner
    title_surface = font_title.render("Rock Paper Scissors (Best to 3)", True, TEXT_COLOR)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 45)))

    # Scoreboard
    score_rect = pygame.Rect(150, 95, 500, 70)
    pygame.draw.rect(screen, CARD_BG, score_rect, border_radius=12)

    p_score_txt = font_medium.render(f"Player: {player_score} / {WINNING_SCORE}", True, ACCENT_BLUE)
    c_score_txt = font_medium.render(f"Computer: {computer_score} / {WINNING_SCORE}", True, ACCENT_RED)
    vs_txt = font_medium.render("VS", True, TEXT_COLOR)

    screen.blit(p_score_txt, (score_rect.left + 30, score_rect.centery - p_score_txt.get_height() // 2))
    screen.blit(vs_txt, (score_rect.centerx - vs_txt.get_width() // 2, score_rect.centery - vs_txt.get_height() // 2))
    screen.blit(c_score_txt, (score_rect.right - c_score_txt.get_width() - 30, score_rect.centery - c_score_txt.get_height() // 2))

    # Matchup Display Cards
    card_p = pygame.Rect(150, 190, 220, 180)
    card_c = pygame.Rect(430, 190, 220, 180)
    pygame.draw.rect(screen, CARD_BG, card_p, border_radius=15)
    pygame.draw.rect(screen, CARD_BG, card_c, border_radius=15)

    lbl_p = font_small.render("YOUR CHOICE", True, MUTED_TEXT)
    lbl_c = font_small.render("COMPUTER CHOICE", True, MUTED_TEXT)
    screen.blit(lbl_p, (card_p.centerx - lbl_p.get_width() // 2, card_p.top + 15))
    screen.blit(lbl_c, (card_c.centerx - lbl_c.get_width() // 2, card_c.top + 15))

    # Icons (only once a choice has been made)
    if player_choice:
        draw_icon(player_choice, (card_p.centerx, card_p.top + 85), ACCENT_BLUE)
    if computer_choice:
        draw_icon(computer_choice, (card_c.centerx, card_c.top + 85), ACCENT_RED)

    val_p = player_choice if player_choice else "-"
    val_c = computer_choice if computer_choice else "-"

    txt_p = font_large.render(val_p, True, ACCENT_BLUE)
    txt_c = font_large.render(val_c, True, ACCENT_RED)
    screen.blit(txt_p, txt_p.get_rect(center=(card_p.centerx, card_p.bottom - 38)))
    screen.blit(txt_c, txt_c.get_rect(center=(card_c.centerx, card_c.bottom - 38)))

    # Result Banner
    res_surface = font_large.render(result_text, True, result_color)
    screen.blit(res_surface, res_surface.get_rect(center=(WIDTH // 2, 410)))

    # Play-again hint when the match is over
    if game_over:
        hint = font_medium.render("Click 'Play Again' to start a new match.", True, MUTED_TEXT)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 445)))

    # Move Action Buttons
    for btn in move_buttons:
        is_hovered = btn["rect"].collidepoint(mouse_pos) and not game_over

        # Dim buttons when match is over
        if game_over:
            btn_color = (60, 65, 80)
        else:
            btn_color = HOVER_COLOR if is_hovered else ACCENT_BLUE

        pygame.draw.rect(screen, btn_color, btn["rect"], border_radius=10)
        btn_text = font_medium.render(btn["name"], True, (255, 255, 255) if not game_over else (120, 120, 120))
        screen.blit(btn_text, btn_text.get_rect(center=btn["rect"].center))

    # Reset / Play Again Button
    reset_hovered = reset_button["rect"].collidepoint(mouse_pos)
    if game_over:
        reset_color = PLAY_AGAIN_HOVER if reset_hovered else PLAY_AGAIN_COLOR
        reset_label = "Play Again"
    else:
        reset_color = RESET_HOVER_COLOR if reset_hovered else RESET_BTN_COLOR
        reset_label = "Reset Game"

    pygame.draw.rect(screen, reset_color, reset_button["rect"], border_radius=10)
    reset_text = font_medium.render(reset_label, True, (255, 255, 255))
    screen.blit(reset_text, reset_text.get_rect(center=reset_button["rect"].center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
