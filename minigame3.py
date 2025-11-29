# minigame3.py
import pygame
import math
import random

# -------------------------
# Spell + Pattern Classes
# -------------------------
class Spell:
    def __init__(self, name, aspects, words, icon_color, node_positions):
        """
        node_positions: list of (x, y) positions in screen coordinates (absolute)
        """
        self.name = name
        self.aspects = aspects
        self.words = words
        self.icon_color = icon_color
        self.node_positions = node_positions


class PatternNode:
    def __init__(self, pos, index, radius=22):
        self.pos = pos
        self.index = index  # 0-based ordering
        self.radius = radius
        self.traced = False

    def draw(self, screen, font):
        x, y = self.pos
        # inner color: traced green, next target cyan, default gold
        if self.traced:
            fill = (90, 200, 120)
            border = (40, 120, 60)
        else:
            fill = (255, 210, 100)
            border = (160, 110, 40)

        pygame.draw.circle(screen, fill, (x, y), self.radius)
        pygame.draw.circle(screen, border, (x, y), self.radius, 3)
        # Draw index number
        num_surf = font.render(str(self.index + 1), True, (10, 10, 10))
        screen.blit(num_surf, num_surf.get_rect(center=(x, y)))

    def is_hover(self, mouse_pos):
        return math.dist(self.pos, mouse_pos) <= self.radius


def cast_spell(screen, clock, spell, background_image):
    """
    Runs the casting minigame for a single spell.
    Returns True on success, False on failure.
    While this is running the spellbook is NOT drawn by caller.
    The background_image is still drawn (user requested).
    """

    WIDTH, HEIGHT = screen.get_size()

    # Fonts for casting UI
    node_font = pygame.font.Font("Assets/MagicSchoolOne.ttf", 28)
    result_font = pygame.font.Font("Assets/MagicSchoolOne.ttf", 60)

    # Create PatternNodes from spell.node_positions
    nodes = [PatternNode(pos, i) for i, pos in enumerate(spell.node_positions)]
    next_required = 0
    hovered_prev = None
    running_cast = True
    result = None  # None while in progress, True success, False fail

    # Load images
    teacup_img = pygame.image.load("Assets/Teacup.png").convert_alpha()
    teacup_img = pygame.transform.scale(teacup_img, (120, 120))
    star_img = pygame.image.load("Assets/GoldStar.png").convert_alpha()
    star_img = pygame.transform.scale(star_img, (24, 24))
    x_img = pygame.image.load("Assets/RedX.png").convert_alpha()
    x_img = pygame.transform.scale(x_img, (32, 32))

    ding = pygame.mixer.Sound("Assets/ding.mp3")
    error = pygame.mixer.Sound("Assets/error.mp3")

    teacup_pos = (WIDTH // 2 - 60, HEIGHT // 2 - 60)
    effects = []
    effect_timer = 120  # 3 seconds

    def draw_pattern_guides():
        if len(nodes) > 1:
            pts = [n.pos for n in nodes]
            pygame.draw.lines(screen, (120, 180, 200), False, pts, 4)

    while running_cast:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

        hovered_now = None
        for n in nodes:
            if n.is_hover(mouse):
                hovered_now = n.index
                break

        screen.blit(background_image, (0, 0))

        if result is None:
            draw_pattern_guides()
            for n in nodes:
                n.draw(screen, node_font)

            if hovered_now is not None and hovered_now != hovered_prev:
                node = nodes[hovered_now]
                if node.traced:
                    error.play()
                    result = False
                else:
                    if node.index == next_required:
                        ding.play()
                        node.traced = True
                        next_required += 1
                        if next_required >= len(nodes):
                            result = True
                    else:
                        error.play()
                        result = False

            hovered_prev = hovered_now

            if next_required < len(nodes):
                nx = nodes[next_required]
                pygame.draw.circle(screen, (80, 200, 230), nx.pos, nx.radius + 6, 3)

        else:
            # --- TEACUP + IMAGE EFFECTS ---
            # Generate effects once
            if not effects:
                teacup_center = (teacup_pos[0] + teacup_img.get_width()//2,
                                 teacup_pos[1] + teacup_img.get_height()//2)
                num_effects = 25 if result else 15
                for _ in range(num_effects):
                    dx = random.randint(-80, 80)
                    dy = random.randint(-60, 60)
                    spawn_delay = random.randint(0, 30)
                    effects.append({
                        'pos': [teacup_center[0] + dx, teacup_center[1] + dy],
                        'spawn_delay': spawn_delay,
                        'spawned': False,
                        'alpha': 255,
                        'vy': -random.uniform(0.5, 1.5) if result else 0  # floating
                    })

            # Draw teacup
            screen.blit(teacup_img, teacup_pos)

            # Draw effects
            for e in effects:
                if e['spawn_delay'] > 0:
                    e['spawn_delay'] -= 1
                    continue
                if not e['spawned']:
                    e['spawned'] = True

                x, y = e['pos']

                if result:
                    # floating/fading star
                    y += e['vy']
                    e['pos'][1] = y
                    e['alpha'] = max(e['alpha'] - 3, 0)
                    if e['alpha'] <= 0:
                        continue

                    # Draw star image with alpha
                    star_surf = star_img.copy()
                    star_surf.fill((255, 255, 255, e['alpha']), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(star_surf, (x - star_surf.get_width()//2, y - star_surf.get_height()//2))

                else:
                    # Draw static red X
                    screen.blit(x_img, (x - x_img.get_width()//2, y - x_img.get_height()//2))

            effect_timer -= 1
            if effect_timer <= 0:
                running_cast = False

        pygame.display.flip()
        clock.tick(60)

    return bool(result)




# -------------------------
# Main minigame function
# -------------------------
def run_minigame3(screen, clock):
    pygame.init()
    pygame.mixer.init()

    # Load images (background kept visible during casting)
    background_image = pygame.transform.scale(
        pygame.image.load("Assets/Magic_Bg.jpg").convert(),
        screen.get_size()
    )

    spellbook_image = pygame.image.load("Assets/Spellbook_Transparent.png").convert_alpha()
    spellbook_image = pygame.transform.scale(spellbook_image, (800, 500))

    page_flip = pygame.mixer.Sound("Assets/page_flip.mp3")

    pygame.mixer.music.load("Assets/spell_background.mp3")
    pygame.mixer.music.play(loops=-1)

    WIDTH, HEIGHT = screen.get_size()

    # Fonts
    title_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 80)
    aspects_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 30)
    words_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 60)
    button_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 32)
    arrow_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 22)
    result_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 52)

    # Book position & page layout
    book_w, book_h = 800, 500
    book_x = (WIDTH - book_w) // 2
    book_y = (HEIGHT - book_h) // 2
    left_page_x = book_x + 140
    left_page_y = book_y + 60
    right_page_x = book_x + 430
    right_page_y = book_y + 10

    # Cast button + nav buttons
    button_rect = pygame.Rect(right_page_x, right_page_y + 350, 220, 55)
    left_btn = pygame.Rect(book_x + 20, book_y + 20, 50, 35)
    right_btn = pygame.Rect(book_x + book_w - 70, book_y + 20, 50, 35)

    # -- define node patterns for each spell (absolute screen coords) --
    center = (WIDTH // 2, HEIGHT // 2)
    cx, cy = center

    # Helper to place relative to center
    def rel(dx, dy):
        return (cx + dx, cy + dy)

    spells = [
        Spell(
            "Cappuccino",
            "Aspects: 2 Caffeine",
            ["Frotharis", "Cafienox", "Baristarum"],
            (200, 160, 100),
            # little triangle swirl
            [rel(-120, 0), rel(0, -110), rel(120, 10), rel(20, 120)]
        ),
        Spell(
            "Milk",
            "Aspects: 1 Sweet, 1 Neutral",
            ["Dairiana", "Calcisweet", "Melliflux"],
            (240, 240, 255),
            # horizontal line of nodes
            [rel(-150, 0), rel(-50, 0), rel(50, 0), rel(150, 0)]
        ),
        Spell(
            "Honey",
            "Aspects: 2 Sweet",
            ["Nectarion", "Zymflora", "Ambrosium"],
            (255, 220, 90),
            # diamond
            [rel(0, -140), rel(120, 0), rel(0, 140), rel(-120, 0)]
        ),
        Spell(
            "Black Tea",
            "Aspects: 2 Neutral",
            ["Infusara", "Tannorin", "Obscurleaf"],
            (150, 90, 40),
            # zigzag vertical
            [rel(-80, -120), rel(80, -60), rel(-80, 0), rel(80, 60), rel(-80, 120)]
        ),
        Spell(
            "Fruit Punch",
            "Aspects: 2 Fruit",
            ["Berrimorph", "Citrinova", "Tropiflux"],
            (255, 100, 120),
            # star-ish
            [rel(-120, -30), rel(-20, -120), rel(100, -10), rel(-10, 100), rel(120, 50)]
        ),
    ]

    current_page = 0
    running = True

    # State for showing a message (after cast success/fail)
    post_result_text = ""
    post_result_timer = 0

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Navigation (only when not casting)
                if post_result_timer <= 0:  # normal interaction allowed only when not showing post-result
                    if left_btn.collidepoint(mouse):
                        page_flip.play()
                        current_page = (current_page - 1) % len(spells)
                    elif right_btn.collidepoint(mouse):
                        page_flip.play()
                        current_page = (current_page + 1) % len(spells)
                    elif button_rect.collidepoint(mouse):
                        # Start casting: hide the book and run cast_spell()
                        active_spell = spells[current_page]
                        success = cast_spell(screen, clock, active_spell, background_image)
                        if success:
                            post_result_text = "Spell Cast Successfully!"
                        else:
                            post_result_text = "Spell Cast Failed."
                        post_result_timer = 90  # show for 1.5 seconds

        # Draw background (always)
        screen.blit(background_image, (0, 0))

        # If we're showing a post-result (after casting), show result text centered
        # Draw the spellbook (normal mode)
        screen.blit(spellbook_image, (book_x, book_y))
        spell = spells[current_page]

        # LEFT PAGE: title, icon, aspects
        title_surface = title_f.render(spell.name, True, (255, 240, 200))
        screen.blit(title_surface, (left_page_x-20, left_page_y))

        icon_surface = pygame.Surface((160, 160))
        icon_surface.fill(spell.icon_color)
        screen.blit(icon_surface, (left_page_x + 20, left_page_y + 100))

        aspects_surface = aspects_f.render(spell.aspects, True, (255, 240, 200))
        screen.blit(aspects_surface, (left_page_x, left_page_y + 270))

        # RIGHT PAGE: magical words
        for i, word in enumerate(spell.words):
            wsurf = words_f.render(word, True, (220, 255, 255))
            screen.blit(wsurf, (right_page_x, right_page_y + 60 + i * 60))

        # Cast button
        hovered = button_rect.collidepoint(mouse)
        color = (215, 200, 255) if hovered else (190, 175, 235)
        pygame.draw.rect(screen, color, button_rect, border_radius=12)
        btn_text = button_f.render("Cast Spell", True, (40, 20, 80))
        screen.blit(btn_text, btn_text.get_rect(center=button_rect.center))

        # Page nav buttons
        pygame.draw.rect(screen, (255, 220, 180), left_btn, border_radius=8)
        pygame.draw.rect(screen, (255, 220, 180), right_btn, border_radius=8)
        screen.blit(arrow_f.render("<", True, (80, 30, 10)), left_btn.move(4, 0))
        screen.blit(arrow_f.render(">", True, (80, 30, 10)), right_btn.move(8, 0))

        if post_result_timer > 0:
            post_result_timer -= 1
            txt = result_f.render(post_result_text, True, (255, 245, 200) if "Successfully" in post_result_text else (255, 180, 180))
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2-20, HEIGHT // 2+250)))
            if post_result_timer == 0:
                pygame.mixer.music.stop()
                return {"Tea": 10, "Bitter": 10}


        pygame.display.flip()
        clock.tick(60)
