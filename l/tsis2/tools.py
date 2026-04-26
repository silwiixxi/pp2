import pygame

WIDTH, HEIGHT = 1000, 700


def flood_fill(surface, x, y, new_color):
    target = surface.get_at((x, y))

    if target == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or py < 0 or px >= WIDTH or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px+1, py))
        stack.append((px-1, py))
        stack.append((px, py+1))
        stack.append((px, py-1))


def draw_line(surface, color, start, end, size):
    if start is None or end is None:
        return
    pygame.draw.line(surface, color, start, end, size)


def draw_rect(surface, color, start, end, size):
    if start is None or end is None:
        return
    rect = pygame.Rect(start, (end[0]-start[0], end[1]-start[1]))
    pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, color, start, end, size):
    if start is None or end is None:
        return
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5)
    pygame.draw.circle(surface, color, start, radius, size)