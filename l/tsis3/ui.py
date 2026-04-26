import pygame

FONT = None


def init():
    global FONT
    pygame.font.init()
    FONT = pygame.font.SysFont("Arial", 20)


def draw_text(screen, text, x, y):
    img = FONT.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))


def main_menu(screen):
    screen.fill((0, 0, 0))
    draw_text(screen, "MAIN MENU", 120, 100)
    draw_text(screen, "Play", 140, 200)
    draw_text(screen, "Leaderboard", 140, 250)
    draw_text(screen, "Settings", 140, 300)
    draw_text(screen, "Quit", 140, 350)


def game_over(screen, score, distance):
    screen.fill((0, 0, 0))
    draw_text(screen, "GAME OVER", 120, 100)
    draw_text(screen, f"Score: {score}", 120, 200)
    draw_text(screen, f"Distance: {distance}", 120, 230)


def leaderboard_screen(screen, data):
    screen.fill((0, 0, 0))
    draw_text(screen, "LEADERBOARD", 120, 50)

    y = 120
    for i, entry in enumerate(data):
        draw_text(screen, f"{i+1}. {entry['name']} - {entry['score']}", 80, y)
        y += 30