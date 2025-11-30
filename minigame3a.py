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
    def __init__(self, pos, index, radius=20):
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
    New version:
    Instead of drawing nodes and detecting a pattern,
    this version draws a grid centered on the screen and a center dot.

    Always returns True (or you can change logic later).
    """

    WIDTH, HEIGHT = screen.get_size()
    cx, cy = WIDTH // 2, HEIGHT // 2

    running = True
    duration = 12000  # Show grid for ~2 seconds (60 FPS)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

        # Draw background
        screen.blit(background_image, (0, 0))

        # -----------------------------
        # Draw grid (every 20 px)
        # -----------------------------
        step = 20
        grid_color = (255, 255, 255, 60)

        # Vertical lines (center → outwards)
        for x in range(cx, WIDTH, step):
            pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
        for x in range(cx, 0, -step):
            pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))

        # Horizontal lines
        for y in range(cy, HEIGHT, step):
            pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))
        for y in range(cy, 0, -step):
            pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))

        # -----------------------------
        # Draw center dot
        # -----------------------------
        pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 3)

        # -----------------------------
        # Exit after short delay
        # -----------------------------
        duration -= 1
        if duration <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    return True


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
        return cx + dx, cy + dy

    spells = [
        # 1 — angular 'B' shape (top-left)
        Spell(
            "Bramble Bend",
            "Aspects: Earthy +1, Bitter +1",
            ["Bramaris", "Thornvox", "Cortegen"],
            (110, 90, 70),
            # angular zigzag / folded L
            [
                rel(-120, -60), rel(-40, -20), rel(-100, 20),
                rel(-20, 40), rel(-80, 80), rel(0, 100),
                rel(80, 80), rel(40, 20), rel(120, -20),
                rel(40, -80)
            ]
        ),

        # 2 — star (pentagram / star)
        Spell(
            "Starpoint",
            "Aspects: Sweet +1, Floral +1",
            ["Astralis", "Penthera", "Lumistar"],
            (240, 210, 220),
            # star pentagon crossing nodes
            [
                rel(0, -130), rel(40, -10), rel(130, -30),
                rel(60, 40), rel(100, 120), rel(0, 70),
                rel(-100, 120), rel(-60, 40), rel(-130, -30),
                rel(-40, -10)
            ]
        ),

        # 3 — spiral (large smooth inward spiral)
        Spell(
            "Gyrecoil",
            "Aspects: Tea +2",
            ["Gyrevex", "Spiraflux", "Helixor"],
            (180, 160, 120),
            # smooth inward spiral (approximated by ring of nodes)
            [
                rel(0, -140), rel(50, -120), rel(100, -70),
                rel(110, -10), rel(90, 50), rel(40, 90),
                rel(-20, 110), rel(-80, 90), rel(-110, 20),
                rel(-70, -40)
            ]
        ),

        # 4 — dense scribble / hatch (chaotic block)
        Spell(
            "Scrib Quell",
            "Aspects: Spice +1, Bitter +1",
            ["Ragamorg", "Ravelis", "Skratcha"],
            (90, 90, 110),
            # dense crossed hatch: several short zig nodes forming the block
            [
                rel(-80, -120), rel(-40, -80), rel(10, -110),
                rel(50, -70), rel(80, -100), rel(60, -40),
                rel(0, -10), rel(-40, 10), rel(-10, 60),
                rel(40, 80)
            ]
        ),

        # 5 — smooth 'S' curve
        Spell(
            "Serpent Sway",
            "Aspects: Creamy +1, Tea +1",
            ["Seraphae", "Sinuara", "Silvena"],
            (200, 180, 170),
            # long S-curve with 8 nodes
            [
                rel(-100, -90), rel(-40, -120), rel(20, -80),
                rel(60, -20), rel(40, 40), rel(-10, 80),
                rel(-60, 100), rel(-90, 60)
            ]
        ),

        # 6 — lightning slash with long tail
        Spell(
            "Voltline",
            "Aspects: Citrus +1, Spice +1",
            ["Voltaris", "Zapkern", "Thundrix"],
            (220, 200, 80),
            # sharp zig then long diagonal tail
            [
                rel(-40, -120), rel(20, -80), rel(-10, -40),
                rel(60, -10), rel(20, 40), rel(100, 80),
                rel(140, 100), rel(120, 40), rel(100, 0),
                rel(40, -40)
            ]
        ),

        # 7 — loop with diagonal tick (circle+slash)
        Spell(
            "Hookturn",
            "Aspects: Mint +1, Citrus +1",
            ["Loopent", "Crovis", "Torsha"],
            (160, 230, 200),
            # circle-ish loop with a diagonal tick crossing
            [
                rel(-80, 0), rel(-40, -80), rel(20, -110),
                rel(80, -80), rel(110, -10), rel(80, 60),
                rel(20, 100), rel(-40, 100), rel(-80, 60),
                rel(-20, 20)
            ]
        ),

        # 8 — 'D' with rectangle inside (boxy)
        Spell(
            "Lockplate",
            "Aspects: Tea +1, Creamy +1",
            ["Rectalus", "Plaxion", "Vaulten"],
            (140, 150, 170),
            # rounded D-outline plus inner rectangular nodes
            [
                rel(-80, -80), rel(20, -120), rel(100, -60),
                rel(100, 20), rel(40, 80), rel(-20, 100),
                rel(-60, 80), rel(-80, 20), rel(-60, -10),
                rel(-20, -40)
            ]
        ),

        # 9 — crossed M / diamond zigzag
        Spell(
            "Twincrest",
            "Aspects: Bitter +1, Spice +1",
            ["Diacrit", "Zemmar", "Crestor"],
            (190, 160, 140),
            # sharp zigzags forming a double-peak diamond
            [
                rel(-120, 0), rel(-40, -90), rel(10, 0),
                rel(60, -90), rel(120, 10), rel(60, 70),
                rel(0, 20), rel(-60, 90), rel(-110, 40),
                rel(-70, -10)
            ]
        ),

        # 10 — U-turn with downward hook
        Spell(
            "Downpivot",
            "Aspects: Herbal +1, Tea +1",
            ["Hookrun", "Trogla", "Pendrix"],
            (120, 180, 150),
            # U shape turning down then a short hook
            [
                rel(-60, -80), rel(-40, 0), rel(-20, 80),
                rel(20, 120), rel(80, 80), rel(80, 20),
                rel(40, -20), rel(0, -40), rel(-20, -60),
                rel(-40, -40)
            ]
        ),

        # 11 — spiral arrow / curl-to-arrow
        Spell(
            "Gyroarrow",
            "Aspects: Citrus +1, Sweet +1",
            ["Spiralux", "Orien", "Gyralon"],
            (220, 200, 160),
            # small inward spiral then an outward arrow point
            [
                rel(-20, -80), rel(20, -120), rel(70, -80),
                rel(90, -20), rel(80, 30), rel(40, 70),
                rel(0, 110), rel(-40, 80), rel(-80, 40),
                rel(-40, 10)
            ]
        ),

        # 12 — three diagonal slashes (parallel)
        Spell(
            "Triscratch",
            "Aspects: Spice +2",
            ["Clavix", "Tremor", "Rendrix"],
            (210, 120, 100),
            # three near-parallel slashes approximated by staggered nodes
            [
                rel(-100, -120), rel(-60, -60), rel(-20, -20),
                rel(20, 20), rel(60, 60), rel(100, 120),
                rel(60, 80), rel(20, 40), rel(-20, -40),
                rel(-60, -80)
            ]
        ),

        # 13 — tall U / cup-hold (boxy cup)
        Spell(
            "Cuphold",
            "Aspects: Creamy +2, Sweet +1",
            ["Caffara", "Urbina", "Lacton"],
            (255, 240, 220),
            # tall U with squared base
            [
                rel(-80, -120), rel(-80, -20), rel(-80, 60),
                rel(-20, 120), rel(40, 120), rel(100, 60),
                rel(100, -20), rel(40, -80), rel(-20, -90),
                rel(-40, -60)
            ]
        ),

        # 14 — pointed boat / sail spikes
        Spell(
            "Keelflare",
            "Aspects: Herbal +1, Floral +1",
            ["Keelion", "Trianta", "Sailorix"],
            (170, 200, 180),
            # three-point sail-like spikes rising from a base
            [
                rel(-110, 40), rel(-40, 100), rel(20, 30),
                rel(60, -80), rel(100, 10), rel(60, 90),
                rel(10, 120), rel(-40, 100), rel(-80, 80),
                rel(-100, 40)
            ]
        ),

        # 15 — concentric spiral / heart-like looping circle (bottom-right)
        Spell(
            "Coreheart",
            "Aspects: Sweet +2, Floral +1",
            ["Cordalis", "Orbheart", "Amorix"],
            (255, 200, 210),
            # outer loop + inner curl approximated with nodes
            [
                rel(0, -120), rel(60, -100), rel(110, -40),
                rel(120, 20), rel(100, 80), rel(40, 110),
                rel(-20, 110), rel(-80, 80), rel(-110, 20),
                rel(-40, -20)
            ]
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


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_minigame3(pygame.display.set_mode((1280, 720)), pygame.time.Clock())
