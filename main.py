import pygame
import random
import sys

# ─────────────────────────────────────────
#  INIT
# ─────────────────────────────────────────
pygame.init()

SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Strawberry Cafe")
clock = pygame.time.Clock()
FPS = 60

# ─────────────────────────────────────────
#  COLOURS
# ─────────────────────────────────────────
PINK_LIGHT   = (255, 228, 235)
PINK_MED     = (255, 200, 215)
PINK_DEEP    = (255, 150, 180)
PINK_DARK    = (200, 100, 130)
WHITE        = (255, 255, 255)
CREAM        = (255, 248, 240)
RED_SOFT     = (255, 120, 120)
GREEN_SOFT   = (140, 210, 140)
YELLOW_SOFT  = (255, 235, 140)
PURPLE_SOFT  = (200, 170, 255)
TEXT_DARK    = (80, 50, 60)
BUBBLE_COL   = (255, 248, 250)
TIMER_BG     = (230, 200, 210)

# ─────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────
font_title  = pygame.font.Font(None, 48)
font_big    = pygame.font.Font(None, 36)
font_med    = pygame.font.Font(None, 28)
font_small  = pygame.font.Font(None, 20)
font_tiny   = pygame.font.Font(None, 16)

# ─────────────────────────────────────────
#  ASSET LOADER
# ─────────────────────────────────────────
def load_img(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            return pygame.transform.smoothscale(img, size)
        return img
    except Exception:
        return None

ASSET = "assets/"

bg_img       = load_img(ASSET + "bg.png", (SCREEN_W, SCREEN_H))
wait_img     = load_img(ASSET + "wait1.png", (120, 150))
happy_img    = load_img(ASSET + "happy1.png", (120, 150))
angry_img    = load_img(ASSET + "angry1.png", (120, 150))
bubble_img   = load_img(ASSET + "bubble.png", (90, 90))

FOOD_NAMES  = ["Strawberry Cake", "Vanilla Cupcake", "Caramel Latte", "Milk Tea", "Macaron Set"]
FOOD_FILES  = ["cake.png", "cupcake.png", "latte.png", "boba.png", "macaron.png"]
FOOD_COLORS = [RED_SOFT, PINK_DEEP, YELLOW_SOFT, PURPLE_SOFT, GREEN_SOFT]

food_imgs = []
for fname in FOOD_FILES:
    food_imgs.append(load_img(ASSET + fname, (70, 70)))

# ─────────────────────────────────────────
#  DRAWING HELPERS
# ─────────────────────────────────────────
def draw_rounded_rect(surf, color, rect, radius=12, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def draw_text_centered(surf, text, font, color, cx, cy):
    s = font.render(text, True, color)
    surf.blit(s, (cx - s.get_width() // 2, cy - s.get_height() // 2))

def draw_text(surf, text, font, color, x, y):
    s = font.render(text, True, color)
    surf.blit(s, (x, y))

# ─────────────────────────────────────────
#  BACKGROUND
# ─────────────────────────────────────────
def draw_fallback_bg(surf):
    # Gradient background
    for i in range(SCREEN_H):
        color_ratio = i / SCREEN_H
        r = int(255 - color_ratio * 20)
        g = int(228 - color_ratio * 30)
        b = int(235 - color_ratio * 40)
        pygame.draw.line(surf, (r, g, b), (0, i), (SCREEN_W, i))
    
    # Floor
    floor_y = 400
    tile = 50
    for row in range((SCREEN_H - floor_y) // tile + 1):
        for col in range(SCREEN_W // tile + 1):
            if (row + col) % 2 == 0:
                pygame.draw.rect(surf, (245, 220, 230),
                                 (col * tile, floor_y + row * tile, tile, tile))
    
    # Decorative hearts
    heart_positions = [(100, 80), (200, 50), (350, 70), (500, 55), (650, 80)]
    for hx, hy in heart_positions:
        pygame.draw.circle(surf, PINK_MED, (hx, hy), 8)
        pygame.draw.polygon(surf, PINK_MED, [(hx, hy-5), (hx-5, hy+3), (hx+5, hy+3)])
    
    # Counter
    pygame.draw.rect(surf, (220, 170, 180), (30, 430, 740, 170), border_radius=20)
    pygame.draw.rect(surf, (240, 190, 200), (30, 430, 740, 35), border_radius=20)
    pygame.draw.rect(surf, PINK_DARK, (30, 430, 740, 170), 4, border_radius=20)

# ─────────────────────────────────────────
#  FALLBACK CUSTOMER
# ─────────────────────────────────────────
def draw_fallback_customer(surf, x, y, state, width, height):
    center_x = x + width // 2
    body_y = y + height // 2
    
    # Body
    col = PINK_MED if state == "wait" else (GREEN_SOFT if state == "happy" else RED_SOFT)
    pygame.draw.ellipse(surf, col, (center_x - 30, body_y - 15, 60, 50))
    
    # Head
    pygame.draw.circle(surf, CREAM, (center_x, body_y - 40), 35)
    pygame.draw.circle(surf, PINK_DARK, (center_x, body_y - 40), 35, 2)
    
    # Eyes
    pygame.draw.circle(surf, TEXT_DARK, (center_x - 14, body_y - 47), 5)
    pygame.draw.circle(surf, TEXT_DARK, (center_x + 14, body_y - 47), 5)
    pygame.draw.circle(surf, WHITE, (center_x - 16, body_y - 49), 2)
    pygame.draw.circle(surf, WHITE, (center_x + 12, body_y - 49), 2)
    
    # Mouth
    if state == "happy":
        pygame.draw.arc(surf, PINK_DARK, (center_x - 12, body_y - 42, 24, 15), 3.14, 0, 3)
    elif state == "angry":
        pygame.draw.arc(surf, RED_SOFT, (center_x - 12, body_y - 38, 24, 15), 0, 3.14, 3)
        pygame.draw.line(surf, RED_SOFT, (center_x - 20, body_y - 55), (center_x - 8, body_y - 52), 3)
        pygame.draw.line(surf, RED_SOFT, (center_x + 20, body_y - 55), (center_x + 8, body_y - 52), 3)
    else:
        pygame.draw.line(surf, PINK_DARK, (center_x - 10, body_y - 35), (center_x + 10, body_y - 35), 3)
    
    # Blush
    pygame.draw.circle(surf, PINK_DEEP, (center_x - 22, body_y - 40), 5)
    pygame.draw.circle(surf, PINK_DEEP, (center_x + 22, body_y - 40), 5)

# ─────────────────────────────────────────
#  DRAW CUSTOMER
# ─────────────────────────────────────────
def draw_customer(surf, customer, x, y):
    if customer.state == "wait" and wait_img:
        surf.blit(wait_img, (x, y))
    elif customer.state == "happy" and happy_img:
        surf.blit(happy_img, (x, y))
    elif customer.state == "angry" and angry_img:
        surf.blit(angry_img, (x, y))
    else:
        draw_fallback_customer(surf, x, y, customer.state, 120, 150)

# ─────────────────────────────────────────
#  DRAW FOOD
# ─────────────────────────────────────────
def draw_food(surf, idx, x, y, size=70):
    if food_imgs[idx]:
        img = pygame.transform.smoothscale(food_imgs[idx], (size, size))
        surf.blit(img, (x, y))
    else:
        col = FOOD_COLORS[idx]
        pygame.draw.circle(surf, col, (x + size//2, y + size//2), size//2 - 3)
        pygame.draw.circle(surf, WHITE, (x + size//2, y + size//2), size//2 - 3, 2)

# ─────────────────────────────────────────
#  PARTICLES
# ─────────────────────────────────────────
particles = []

def spawn_particles(x, y):
    for _ in range(15):
        particles.append({
            "x": x, "y": y,
            "vx": random.uniform(-3, 3),
            "vy": random.uniform(-5, -1),
            "life": 1.0,
        })

def update_draw_particles(surf):
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.15
        p["life"] -= 0.02
        if p["life"] <= 0:
            particles.remove(p)
            continue
        
        heart_x, heart_y = int(p["x"]), int(p["y"])
        heart_color = (255, 100, 150)
        pygame.draw.circle(surf, heart_color, (heart_x, heart_y), 4)
        pygame.draw.circle(surf, heart_color, (heart_x - 4, heart_y), 4)

# ─────────────────────────────────────────
#  CUSTOMER CLASS
# ─────────────────────────────────────────
CUSTOMER_SLOTS = [120, 340, 560]
CUSTOMER_Y = 330
ORDER_TIME = 12.0

class Customer:
    def __init__(self, slot_idx):
        self.slot = slot_idx
        self.x = CUSTOMER_SLOTS[slot_idx] - 60
        self.y = CUSTOMER_Y
        self.order = random.randint(0, len(FOOD_NAMES) - 1)
        self.timer = ORDER_TIME
        self.state = "wait"
        self.leave_timer = 0.0

    def update(self, dt):
        if self.state == "wait":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "angry"
                self.leave_timer = 1.5

        if self.state in ("happy", "angry"):
            self.leave_timer -= dt
            if self.leave_timer <= 0:
                self.state = "leaving"

    def draw(self, surf):
        draw_customer(surf, self, self.x, self.y)
        
        if self.state == "wait":
            bubble_x = self.x + 80
            bubble_y = self.y - 50
            
            if bubble_img:
                surf.blit(bubble_img, (bubble_x, bubble_y))
            else:
                draw_rounded_rect(surf, BUBBLE_COL, (bubble_x, bubble_y, 80, 80), 
                                 radius=15, border=2, border_color=PINK_DEEP)
            
            draw_food(surf, self.order, bubble_x + 10, bubble_y + 10, size=60)
            
            # Timer bar
            bar_w = 100
            bar_h = 6
            bar_x = self.x + 10
            bar_y = self.y - 15
            frac = max(0, self.timer / ORDER_TIME)
            bar_color = GREEN_SOFT if frac > 0.5 else YELLOW_SOFT if frac > 0.25 else RED_SOFT
            draw_rounded_rect(surf, TIMER_BG, (bar_x, bar_y, bar_w, bar_h), radius=3)
            if frac > 0:
                draw_rounded_rect(surf, bar_color, (bar_x, bar_y, int(bar_w * frac), bar_h), radius=3)

    @property
    def done(self):
        return self.state == "leaving"

# ─────────────────────────────────────────
#  MENU PANEL
# ─────────────────────────────────────────
MENU_X = 630
MENU_Y = 100
ITEM_H = 80
ITEM_W = 150

def draw_menu(surf, hovered):
    draw_rounded_rect(surf, (255, 240, 245),
                      (MENU_X - 8, MENU_Y - 8, ITEM_W + 16, ITEM_H * 5 + 16),
                      radius=15, border=2, border_color=PINK_DEEP)
    
    draw_text_centered(surf, "Menu", font_big, PINK_DARK, 
                      MENU_X + ITEM_W // 2, MENU_Y - 20)

    rects = []
    for i, name in enumerate(FOOD_NAMES):
        iy = MENU_Y + i * ITEM_H
        rect = pygame.Rect(MENU_X, iy, ITEM_W, ITEM_H - 4)
        bg = PINK_MED if hovered == i else WHITE
        draw_rounded_rect(surf, bg, rect, radius=10, border=1, border_color=PINK_DEEP)
        draw_food(surf, i, MENU_X + 8, iy + 10, size=55)
        
        display_name = name if len(name) < 14 else name[:11] + "..."
        txt = font_small.render(display_name, True, TEXT_DARK)
        surf.blit(txt, (MENU_X + 72, iy + ITEM_H // 2 - txt.get_height() // 2))
        rects.append(rect)
    return rects

# ─────────────────────────────────────────
#  HUD
# ─────────────────────────────────────────
def draw_hud(surf, score, combo, lives, level):
    draw_rounded_rect(surf, PINK_DEEP, (10, 10, 150, 40), radius=20)
    draw_text(surf, f"Score: {score}", font_med, WHITE, 20, 16)
    
    draw_rounded_rect(surf, PURPLE_SOFT, (170, 10, 100, 40), radius=20)
    draw_text(surf, f"Level {level}", font_med, WHITE, 182, 16)
    
    if combo > 1:
        draw_rounded_rect(surf, YELLOW_SOFT, (280, 10, 110, 40), radius=20)
        draw_text(surf, f"Combo x{combo}", font_med, TEXT_DARK, 292, 16)
    
    # Lives as hearts
    for i in range(lives):
        heart_x = SCREEN_W - 25 - (i * 22)
        heart_y = 22
        pygame.draw.circle(surf, RED_SOFT, (heart_x, heart_y), 7)
        pygame.draw.circle(surf, RED_SOFT, (heart_x - 5, heart_y), 7)

# ─────────────────────────────────────────
#  TITLE SCREEN
# ─────────────────────────────────────────
def title_screen():
    t = 0.0
    while True:
        dt = clock.tick(FPS) / 1000
        t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            draw_fallback_bg(screen)

        draw_rounded_rect(screen, (255, 220, 235), (100, 120, 600, 200), 
                         radius=25, border=3, border_color=PINK_DARK)
        
        draw_text_centered(screen, "Strawberry Cafe", font_title, PINK_DARK, 400, 170)
        draw_text_centered(screen, "Serve customers before their timer runs out", 
                          font_small, TEXT_DARK, 400, 220)
        draw_text_centered(screen, "Click on desserts to match their orders", 
                          font_small, TEXT_DARK, 400, 250)
        
        if int(t * 1.5) % 2 == 0:
            draw_text_centered(screen, "Click anywhere to start", font_med, PINK_DEEP, 400, 300)

        pygame.display.flip()

# ─────────────────────────────────────────
#  GAME OVER SCREEN
# ─────────────────────────────────────────
def game_over_screen(score, level):
    t = 0.0
    while True:
        dt = clock.tick(FPS) / 1000
        t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            draw_fallback_bg(screen)

        draw_rounded_rect(screen, (255, 220, 235), (150, 120, 500, 260), 
                         radius=25, border=3, border_color=PINK_DARK)
        
        draw_text_centered(screen, "Cafe Closed", font_title, PINK_DARK, 400, 180)
        draw_text_centered(screen, f"Final Score: {score}", font_big, TEXT_DARK, 400, 240)
        draw_text_centered(screen, f"Highest Level: {level}", font_med, PINK_DEEP, 400, 280)
        
        if int(t * 1.5) % 2 == 0:
            draw_text_centered(screen, "Click to try again", font_med, PINK_DEEP, 400, 350)

        pygame.display.flip()

# ─────────────────────────────────────────
#  MAIN GAME
# ─────────────────────────────────────────
def game():
    customers = []
    occupied_slots = set()
    score = 0
    combo = 0
    lives = 5
    level = 1
    spawn_timer = 0.0
    spawn_interval = 3.5
    served_count = 0
    level_target = 8
    
    hovered_item = -1
    menu_rects = []
    
    flash_msg = ""
    flash_timer = 0.0
    flash_color = PINK_DEEP

    def add_customer():
        free = [s for s in range(3) if s not in occupied_slots]
        if free:
            slot = random.choice(free)
            occupied_slots.add(slot)
            customers.append(Customer(slot))

    add_customer()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for fi, rect in enumerate(menu_rects):
                    if rect.collidepoint(mouse_pos):
                        matched = False
                        for c in customers:
                            if c.state == "wait" and c.order == fi:
                                c.state = "happy"
                                c.leave_timer = 1.2
                                combo += 1
                                pts = 10 * combo
                                score += pts
                                served_count += 1
                                
                                if served_count >= level_target:
                                    level += 1
                                    served_count = 0
                                    level_target = int(level_target * 1.2)
                                    flash_msg = f"Level {level} Up!"
                                    flash_color = PURPLE_SOFT
                                    flash_timer = 1.5
                                    lives = min(lives + 1, 8)
                                    spawn_interval = max(2.0, spawn_interval - 0.1)
                                else:
                                    flash_msg = f"+{pts}" if combo < 2 else f"+{pts}  Combo x{combo}!"
                                    flash_color = GREEN_SOFT if combo < 3 else YELLOW_SOFT
                                    flash_timer = 1.2
                                
                                spawn_particles(c.x + 60, c.y + 75)
                                matched = True
                                break
                        if not matched:
                            combo = 0
                            flash_msg = "Wrong Order!"
                            flash_color = RED_SOFT
                            flash_timer = 1.0

        hovered_item = -1
        for fi, rect in enumerate(menu_rects):
            if rect.collidepoint(mouse_pos):
                hovered_item = fi

        spawn_timer += dt
        if spawn_timer >= spawn_interval and len(occupied_slots) < 3:
            spawn_timer = 0.0
            add_customer()

        for c in customers[:]:
            c.update(dt)
            if c.done:
                occupied_slots.discard(c.slot)
                customers.remove(c)
                if c.state == "leaving":
                    combo = 0
                    lives -= 1
                    flash_msg = "Customer left!"
                    flash_color = RED_SOFT
                    flash_timer = 1.2

        if lives <= 0:
            return score, level

        # Draw
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            draw_fallback_bg(screen)

        for c in customers:
            c.draw(screen)

        menu_rects = draw_menu(screen, hovered_item)
        update_draw_particles(screen)

        if flash_timer > 0:
            flash_timer -= dt
            alpha = min(1.0, flash_timer / 0.3)
            fs = font_med.render(flash_msg, True, flash_color)
            fs.set_alpha(int(alpha * 255))
            screen.blit(fs, (400 - fs.get_width() // 2, 520))

        draw_hud(screen, score, combo, lives, level)
        
        # Progress bar
        progress_w = 400
        progress_h = 8
        progress_x = SCREEN_W // 2 - progress_w // 2
        progress_y = 70
        draw_rounded_rect(screen, TIMER_BG, (progress_x, progress_y, progress_w, progress_h), radius=4)
        progress_fill = (served_count / level_target) * progress_w
        draw_rounded_rect(screen, PURPLE_SOFT, (progress_x, progress_y, progress_fill, progress_h), radius=4)
        draw_text_centered(screen, f"Next Level: {served_count}/{level_target}", 
                          font_tiny, PINK_DARK, SCREEN_W // 2, progress_y - 10)

        pygame.display.flip()

    return score, level

# ─────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────
if __name__ == "__main__":
    while True:
        title_screen()
        final_score, final_level = game()
        game_over_screen(final_score, final_level)