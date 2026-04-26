import pygame
import random
import json
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 RACER FINAL")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

LANES = [80, 180, 280]

# ---------------- LOAD / SAVE ----------------
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

settings = load_json("settings.json", {
    "sound": True,
    "difficulty": "normal",
    "car_color": "green"
})

leaderboard = load_json("leaderboard.json", [])

# ---------------- INVENTORY ----------------
inventory = {
    "shield": 0,
    "repair": 0
}

nitro_timer = 0
NITRO_DURATION = 180  # 3 seconds

# ---------------- BUTTON ----------------
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)

        color = (
            min(self.color[0] + 40, 255),
            min(self.color[1] + 40, 255),
            min(self.color[2] + 40, 255)
        ) if hover else self.color

        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        text_surf = font.render(self.text, True, (255,255,255))
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------- RESET ----------------
def reset_game():
    global enemies, powerups, score, distance, player_lane, enemy_timer, power_timer, nitro_timer

    enemies = []
    powerups = []
    score = 0
    distance = 0
    player_lane = 1
    enemy_timer = 0
    power_timer = 0
    nitro_timer = 0

# ---------------- STATE ----------------
state = "menu"
name = ""

player_lane = 1
player_y = 500

score = 0
distance = 0

enemies = []
enemy_timer = 0

powerups = []
power_timer = 0

game_over_score = 0
game_over_distance = 0

# ---------------- ENEMY ----------------
class Enemy:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.y = -100

    def update(self, speed):
        self.y += speed

# ---------------- POWERUP ----------------
class PowerUp:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.y = -100
        self.type = random.choice(["nitro", "shield", "repair"])

    def update(self, speed):
        self.y += speed

# ---------------- SETTINGS ----------------
def get_speed():
    if settings["difficulty"] == "easy":
        return 4
    if settings["difficulty"] == "hard":
        return 7
    return 5

def get_interval():
    if settings["difficulty"] == "easy":
        return 70
    if settings["difficulty"] == "hard":
        return 40
    return 55

def get_car_color():
    if settings["car_color"] == "red":
        return (255,0,0)
    if settings["car_color"] == "blue":
        return (0,0,255)
    return (0,255,0)

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.5)


# ---------------- SPAWN ----------------
def spawn_enemy():
    global enemy_timer

    enemy_timer += 1
    interval = max(20, get_interval() - distance // 300)

    if enemy_timer >= interval:
        e = Enemy()
        if e.lane == player_lane and random.random() < 0.6:
            e.lane = random.choice([0,1,2])
        enemies.append(e)
        enemy_timer = 0

def spawn_powerup():
    global power_timer

    power_timer += 1
    if power_timer >= 180:
        powerups.append(PowerUp())
        power_timer = 0

# ---------------- BUTTONS ----------------
play_btn = Button(120, 180, 160, 50, "PLAY", (0, 180, 0))
lb_btn = Button(120, 250, 160, 50, "LEADERBOARD", (0, 120, 255))
set_btn = Button(120, 320, 160, 50, "SETTINGS", (255, 165, 0))
quit_btn = Button(120, 390, 160, 50, "QUIT", (200, 0, 0))

confirm_btn = Button(140, 320, 120, 50, "CONFIRM", (0, 200, 200))
back_btn = Button(120, 500, 160, 50, "BACK", (120, 120, 120))

sound_btn = Button(120, 170, 160, 50, "", (80, 80, 80))

easy_btn = Button(80, 240, 80, 40, "EASY", (0, 200, 0))
normal_btn = Button(160, 240, 100, 40, "NORMAL", (255, 165, 0))
hard_btn = Button(280, 240, 80, 40, "HARD", (200, 0, 0))

red_btn = Button(80, 320, 80, 40, "RED", (255, 0, 0))
blue_btn = Button(160, 320, 100, 40, "BLUE", (0, 0, 255))
green_btn = Button(280, 320, 80, 40, "GREEN", (0, 255, 0))

# ---------------- LOOP ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU
        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_btn.clicked(pos):
                    reset_game()
                    state = "name"
                elif lb_btn.clicked(pos):
                    state = "leaderboard"
                elif set_btn.clicked(pos):
                    state = "settings"
                elif quit_btn.clicked(pos):
                    running = False

        # NAME
        elif state == "name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_btn.clicked(pygame.mouse.get_pos()) and name != "":
                    state = "game"

        # GAME
        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_lane = max(0, player_lane - 1)
                if event.key == pygame.K_RIGHT:
                    player_lane = min(2, player_lane + 1)

        # SETTINGS
        elif state == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if sound_btn.clicked(pos):
                    settings["sound"] = not settings["sound"]

                    if settings["sound"]:
                        pygame.mixer.music.play(-1)

                    else:
                        pygame.mixer.music.stop()

                elif easy_btn.clicked(pos):
                    settings["difficulty"] = "easy"
                elif normal_btn.clicked(pos):
                    settings["difficulty"] = "normal"
                elif hard_btn.clicked(pos):
                    settings["difficulty"] = "hard"

                elif red_btn.clicked(pos):
                    settings["car_color"] = "red"
                elif blue_btn.clicked(pos):
                    settings["car_color"] = "blue"
                elif green_btn.clicked(pos):
                    settings["car_color"] = "green"

                save_json("settings.json", settings)

        if state in ["leaderboard", "settings"]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.clicked(pygame.mouse.get_pos()):
                    state = "menu"

        elif state == "gameover":
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = "menu"

    # ---------------- GAME ----------------
    if state == "game":
        screen.fill((20,20,20))

        distance += 1
        score += 1

        spawn_enemy()
        spawn_powerup()

        base_speed = get_speed() + distance // 1000

        if nitro_timer > 0:
            speed = base_speed + 6
            nitro_timer -= 1
        else:
            speed = base_speed

        pygame.draw.rect(screen, (50,50,50), (50,0,300,600))

        # ENEMIES
        for e in enemies[:]:
            e.update(speed)

            if e.y > HEIGHT + 50:
                enemies.remove(e)

            player_rect = pygame.Rect(LANES[player_lane], player_y, 30, 50)
            enemy_rect = pygame.Rect(LANES[e.lane], e.y, 30, 50)

            if player_rect.colliderect(enemy_rect):

                if inventory["shield"] > 0:
                    inventory["shield"] -= 1
                    enemies.remove(e)
                    continue

                if inventory["repair"] > 0:
                    inventory["repair"] -= 1
                    enemies.clear()
                    player_lane = 1
                    continue

                game_over_score = score
                game_over_distance = distance

                leaderboard.append({
                    "name": name,
                    "score": score,
                    "distance": distance
                })

                leaderboard.sort(key=lambda x: x["score"], reverse=True)
                leaderboard[:] = leaderboard[:10]
                save_json("leaderboard.json", leaderboard)

                state = "gameover"

        # POWERUPS
        for p in powerups[:]:
            p.update(speed)

            if p.y > HEIGHT + 50:
                powerups.remove(p)

            player_rect = pygame.Rect(LANES[player_lane], player_y, 30, 50)
            p_rect = pygame.Rect(LANES[p.lane], p.y, 25, 25)

            if player_rect.colliderect(p_rect):

                if p.type == "nitro":
                    nitro_timer = NITRO_DURATION
                else:
                    inventory[p.type] += 1

                powerups.remove(p)

        # DRAW
        pygame.draw.rect(screen, get_car_color(),
                         (LANES[player_lane], player_y, 30, 50))

        for e in enemies:
            pygame.draw.rect(screen, (255,0,0),
                             (LANES[e.lane], e.y, 30, 50))

        for p in powerups:
            color = (255,255,0)
            if p.type == "shield":
                color = (0,255,255)
            if p.type == "repair":
                color = (255,0,255)

            pygame.draw.rect(screen, color,
                             (LANES[p.lane], p.y, 25, 25))

        # UI
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        screen.blit(font.render(f"Shield: {inventory['shield']}", True, (0,255,255)), (10,40))
        screen.blit(font.render(f"Repair: {inventory['repair']}", True, (255,0,255)), (10,60))

        if nitro_timer > 0:
            screen.blit(font.render("NITRO ACTIVE", True, (255,255,0)), (10, 80))

    # ---------------- OTHER STATES ----------------
    elif state == "menu":
        screen.fill((30,30,30))
        play_btn.draw()
        lb_btn.draw()
        set_btn.draw()
        quit_btn.draw()
        screen.blit(font.render("TSIS 3 RACER", True, (255,255,255)), (140, 100))

    elif state == "name":
        screen.fill((30,30,30))
        screen.blit(font.render("ENTER NAME", True, (255,255,255)), (140, 150))
        pygame.draw.rect(screen, (255,255,255), (100, 250, 200, 40), 2)
        screen.blit(font.render(name, True, (0,255,0)), (110, 260))
        confirm_btn.draw()

    elif state == "leaderboard":
        screen.fill((30,30,30))
        screen.blit(font.render("LEADERBOARD", True, (255,255,255)), (120, 50))

        y = 120
        for i, item in enumerate(leaderboard):
            screen.blit(font.render(f"{i+1}. {item['name']} - {item['score']}",
                                    True, (255,255,255)), (80, y))
            y += 30

        back_btn.draw()

    elif state == "settings":
        screen.fill((30,30,30))
        screen.blit(font.render("SETTINGS", True, (255,255,255)), (150, 80))

        sound_btn.text = "SOUND: ON" if settings["sound"] else "SOUND: OFF"
        sound_btn.draw()

        screen.blit(font.render("DIFFICULTY", True, (255,255,255)), (150, 210))
        easy_btn.draw()
        normal_btn.draw()
        hard_btn.draw()

        screen.blit(font.render("CAR COLOR", True, (255,255,255)), (150, 290))
        red_btn.draw()
        blue_btn.draw()
        green_btn.draw()

        back_btn.draw()

    elif state == "gameover":
        screen.fill((0,0,0))
        screen.blit(font.render("GAME OVER", True, (255,0,0)), (140, 120))
        screen.blit(font.render(f"Player: {name}", True, (255,255,255)), (120, 200))
        screen.blit(font.render(f"Score: {game_over_score}", True, (255,255,255)), (120, 240))
        screen.blit(font.render(f"Distance: {game_over_distance}", True, (255,255,255)), (110, 280))
        screen.blit(font.render("Click to MENU", True, (200,200,200)), (120, 340))

    pygame.display.flip()

pygame.quit()