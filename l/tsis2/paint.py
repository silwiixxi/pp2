import pygame
from datetime import datetime
from tools import flood_fill, draw_line, draw_rect, draw_circle

pygame.init()

# =========================
# SCREEN
# =========================
W, H = 1000, 700
TOOLBAR_H = 60
COLORBAR_Y = 650

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint Final")

canvas = pygame.Surface((W, H))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# =========================
# STATE
# =========================
tool = "pencil"
color = (0, 0, 0)
brush_size = 2

drawing = False
start_pos = None

typing = False
text = ""
text_pos = (0, 0)

# =========================
# COLORS
# =========================
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
]

# =========================
# TOOL SELECT
# =========================
def select_tool(pos):
    global tool

    tools = ["pencil", "line", "rect", "circle", "fill", "text"]
    x = 10

    for t in tools:
        rect = pygame.Rect(x, 10, 90, 40)

        if rect.collidepoint(pos):
            tool = t

        x += 100


# =========================
# COLOR SELECT
# =========================
def select_color(pos):
    global color

    x = 10

    for c in colors:
        rect = pygame.Rect(x, COLORBAR_Y, 30, 30)

        if rect.collidepoint(pos):
            color = c

        x += 40


# =========================
# MAIN LOOP
# =========================
running = True

while running:
    screen.fill((210, 210, 210))
    screen.blit(canvas, (0, TOOLBAR_H))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ================= MOUSE =================
        if event.type == pygame.MOUSEBUTTONDOWN:

            # toolbar
            if my < TOOLBAR_H:
                select_tool(event.pos)

            # colors
            elif my > COLORBAR_Y:
                select_color(event.pos)

            else:

                if tool == "pencil":
                    drawing = True

                elif tool == "line":
                    start_pos = event.pos
                    drawing = True

                elif tool == "rect":
                    start_pos = event.pos
                    drawing = True

                elif tool == "circle":
                    start_pos = event.pos
                    drawing = True

                elif tool == "fill":
                    flood_fill(canvas, mx, my-TOOLBAR_H, color)

                elif tool == "text":
                    typing = True
                    text_pos = event.pos
                    text = ""

        if event.type == pygame.MOUSEBUTTONUP:

            if tool == "pencil":
                drawing = False

            elif tool == "line":
                draw_line(canvas, color, start_pos, event.pos, brush_size)

            elif tool == "rect":
                draw_rect(canvas, color, start_pos, event.pos, brush_size)

            elif tool == "circle":
                draw_circle(canvas, color, start_pos, event.pos, brush_size)

            drawing = False
            start_pos = None

        # ================= KEYBOARD =================
        if event.type == pygame.KEYDOWN:

            # BRUSH SIZE
            if event.key == pygame.K_1:
                brush_size = 2
            if event.key == pygame.K_2:
                brush_size = 5
            if event.key == pygame.K_3:
                brush_size = 10

            # SAVE
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = f"paint_{datetime.now().strftime('%H-%M-%S')}.png"
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            # TEXT INPUT
            if typing:
                if event.key == pygame.K_RETURN:
                    img = font.render(text, True, color)
                    canvas.blit(img, (text_pos[0], text_pos[1] - TOOLBAR_H))
                    typing = False
                    text = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text = ""

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                else:
                    text += event.unicode

    # =========================
    # TOOLBAR DRAW
    # =========================
    pygame.draw.rect(screen, (180, 180, 180), (0, 0, W, TOOLBAR_H))

    tools = ["P", "L", "R", "C", "F", "T"]
    x = 10

    for t in tools:
        pygame.draw.rect(screen, (255, 255, 255), (x, 10, 90, 40))
        txt = font.render(t, True, (0, 0, 0))
        screen.blit(txt, (x + 35, 20))
        x += 100

    # =========================
    # COLOR BAR
    # =========================
    x = 10
    for c in colors:
        pygame.draw.rect(screen, c, (x, COLORBAR_Y, 30, 30))
        x += 40

    # =========================
    # PENCIL
    # =========================
    if tool == "pencil" and pygame.mouse.get_pressed()[0]:
        pygame.draw.circle(canvas, color, (mx, my - TOOLBAR_H), brush_size)

    # =========================
    # LINE PREVIEW
    # =========================
    if tool == "line" and drawing and start_pos:
        pygame.draw.line(screen, color, start_pos, pygame.mouse.get_pos(), brush_size)

    # =========================
    # TEXT PREVIEW
    # =========================
    if typing:
        preview = font.render(text, True, color)
        screen.blit(preview, text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()