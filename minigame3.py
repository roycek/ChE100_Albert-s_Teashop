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
        self.icon = icon_color
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
    Runs the casting minigame for a single spell.
    Returns True on success, False on failure.
    While this is running the spellbook is NOT drawn by caller.
    The background_image is still drawn (user requested).
    """

    WIDTH, HEIGHT = screen.get_size()

    # Fonts for casting UI
    node_font = pygame.font.Font("Assets/MagicSchoolOne.ttf", 28)

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
    title_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 70)
    aspects_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 30)
    words_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 60)
    button_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 32)
    arrow_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 22)
    result_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 52)
    casts_remaining_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 90)
    formulation_f = pygame.font.Font("Assets/MagicSchoolOne.ttf", 35)


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
        return cx + dx*20, cy + dy*20

    spells = [
        # 1 — angular 'B' shape (top-left)
        Spell(
            "Honeywisp",
            "Aspects: Sweet +2",
            ["Bramaris", "Thornvox", "Cortegen"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/HoneyWhisper.png").convert_alpha(),
                                   (160, 160)),
            # angular zigzag / folded L
            [
                rel(-5,5), rel(0,-8), rel(5,5), rel(-6,-5), rel(6, -5), rel(-3,3)
            ]
        ),

        # 2 — star (pentagram / star)
        Spell(
            "Sugar Sigil",
            "Aspects: Sweet +1",
            ["Astralis", "Penthera", "Lumistar"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/SugarSigil.png").convert_alpha(), (160,160)),
            # star pentagon crossing nodes
            [
                rel(-7, -5), rel(0,5), rel(7,-5), rel(7, 5), rel(0,-5), rel(-7,5)
            ]
        ),

        # 3 — spiral (large smooth inward spiral)
        Spell(
            "Citrus Pulse",
            "Aspects: Citrus +2",
            ["Gyrevex", "Spiraflux", "Helixor"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/CitrusPulse.png").convert_alpha(), (160,160)),
            # smooth inward spiral (approximated by ring of nodes)
            [
                rel(6,-3), rel(3,-5), rel(0,-6), rel(-3,-5), rel(-6,-3),
                rel(-6,0), rel(6,0), rel(6,3), rel(3,5), rel(0,6), rel(-3,5),
                rel(-6,3)
            ]
        ),

        # 4 — dense scribble / hatch (chaotic block)
        Spell(
            "Lemonflare",
            "Aspects: Citrus +1, Sweet +1",
            ["Ragamorg", "Ravelis", "Skratcha"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/Lemonflare.png").convert_alpha(), (160,160)),
            # dense crossed hatch: several short zig nodes forming the block
            [
                rel(-8,0), rel(-4,6), rel(4,6), rel(8,0), rel(2,2),
                rel(0,-9), rel(-2,2), rel(-6,1)
            ]
        ),

        # 5 — smooth 'S' curve
        Spell(
            "Tealeaf Rite",
            "Aspects: Tea +2",
            ["Seraphae", "Sinuara", "Silvena"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/TealeafInvocation.png").convert_alpha(), (160,160)),
            # long S-curve with 8 nodes
            [
                rel(-5,7), rel(-9,-4), rel(-3,-7), rel(-7,1), rel(3,-2), rel(0,7), rel(-3,-2),
                rel(7,1), rel(3,-7), rel(9,-4), rel(5,7)
            ]
        ),

        # 6 — lightning slash with long tail
        Spell(
            "Earl Echo",
            "Aspects: Tea +1, Citrus +1",
            ["Voltaris", "Zapkern", "Thundrix"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/EarlgreyEcho.png").convert_alpha(), (160,160)),
            # sharp zig then long diagonal tail
            [
                rel(-7,-10), rel(7,-10), rel(-7,-5), rel(7,-5), rel(-7,0), rel(7,0),
                rel(0,7), rel(0,-14)
            ]
        ),

        # 7 — loop with diagonal tick (circle+slash)
        Spell(
            "Chai Ember",
            "Aspects: Spice +2, Tea +1",
            ["Loopent", "Crovis", "Torsha"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/ChaiEmber.png").convert_alpha(), (160,160)),
            # circle-ish loop with a diagonal tick crossing
            [
                rel(0,-10), rel(-6,-4), rel(4,-4), rel(9,3), rel(-6,3), rel(9,-4),
                rel(0,7), rel(0,-7), rel(9,-7)
            ]
        ),

        # 8 — 'D' with rectangle inside (boxy)
        Spell(
            "Cinnamon",
            "Aspects: Spice +1",
            ["Rectalus", "Plaxion", "Vaulten"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/CinnamonWeave.png").convert_alpha(), (160,160)),
            # rounded D-outline plus inner rectangular nodes
            [
                rel(0, -10), rel(-2, -4), rel(-8, -10), rel(-4, -2),
                rel(0, 6), rel(4, -2), rel(8, -10), rel(2, -4)
            ]
        ),

        # 9 — crossed M / diamond zigzag
        Spell(
            "Herb Bloom",
            "Aspects: Herbal +2",
            ["Diacrit", "Zemmar", "Crestor"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/HerbalBloom.png").convert_alpha(), (160,160)),
            # sharp zigzags forming a double-peak diamond
            [
                rel(0, -8), rel(6, 0), rel(0, 8), rel(-6, 0),
                rel(3, -3), rel(-3, -3), rel(3, 3), rel(-3, 3),
            ]
        ),

        # 10 — U-turn with downward hook
        Spell(
            "Ley Garden",
            "Aspects: Herbal +1, Tea +1",
            ["Hookrun", "Trogla", "Pendrix"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/GardenDraught.png").convert_alpha(), (160,160)),
            # U shape turning down then a short hook
            [
                rel(-8, 6), rel(-4, -10), rel(-1, -4),
                rel(1, -4), rel(4, -10), rel(8, 6),
                rel(0, -2), rel(0, 4)
            ]
        ),

        # 11 — spiral arrow / curl-to-arrow
        Spell(
            "Mintwhirl",
            "Aspects: Mint +2",
            ["Spiralux", "Orien", "Gyralon"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/Mintwhirl.png").convert_alpha(), (160,160)),
            # small inward spiral then an outward arrow point
            [
                rel(6, -2), rel(4, -6), rel(0, -8), rel(-4, -6),
                rel(-6, -2), rel(-4, 4), rel(0, 6), rel(4, 4),
                rel(6, 0)
            ]
        ),

        # 12 — three diagonal slashes (parallel)
        Spell(
            "Frost Snap",
            "Aspects: Mint +1, Citrus +1",
            ["Clavix", "Tremor", "Rendrix"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/FrostmintSnap.png").convert_alpha(), (160,160)),
            # three near-parallel slashes approximated by staggered nodes
            [
                rel(0, -8), rel(0, 8),  # vertical ray
                rel(-8, 0), rel(8, 0),  # horizontal ray
                rel(-4, -4), rel(4, -4),  # inner diamond
                rel(4, 4), rel(-4, 4)
            ]
        ),

        # 13 — tall U / cup-hold (boxy cup)
        Spell(
            "Creamweave",
            "Aspects: Creamy +2",
            ["Caffara", "Urbina", "Lacton"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/CreamyWeave.png").convert_alpha(), (160,160)),
            # tall U with squared base
            [
                rel(-10, 0), rel(-8, -4), rel(-4, -7), rel(0, -8),
                rel(4, -7), rel(8, -4), rel(10, 0),
                rel(6, 2), rel(3, 4), rel(0, 6), rel(-3, 4), rel(-6, 2)
            ]
        ),

        # 14 — pointed boat / sail spikes
        Spell(
            "Velvetfoam",
            "Aspects: Creamy +1, Sweet +1",
            ["Keelion", "Trianta", "Sailorix"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/Velvetfoam.png").convert_alpha(), (160,160)),
            # three-point sail-like spikes rising from a base
            [
                rel(-10, -8), rel(-6, -4), rel(-2, 0),
                rel(2, -4), rel(6, -8),
                rel(0, 2), rel(0, 6)
            ]
        ),

        # 15 — concentric spiral / heart-like looping circle (bottom-right)
        Spell(
            "Dark Surge",
            "Aspects: Bitter +2",
            ["Cordalis", "Orbheart", "Amorix", "Bittera"],
            pygame.transform.scale(pygame.image.load("Assets/Spell Glyphs/DarkroastSurge.png").convert_alpha(), (160,160)),
            # outer loop + inner curl approximated with nodes
            [
                rel(0, -16), rel(-4, -10), rel(-2, -5), rel(0, -1), rel(2, -5), rel(4, -10),
                rel(0, -12), rel(0, -6), rel(0, 4), rel(0, 10)
            ]
        ),
    ]

    current_page = 0
    running = True

    tea_formulation = {}
    spells_remaining = 3

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
                        spells_remaining -= 1
                        if success:
                            post_result_text = "Spell Cast Successfully!"
                            print(type(active_spell.aspects))
                            parsed_aspects = active_spell.aspects.replace("Aspects: ","").replace("+", "").replace(",", "").split(" ")
                            spell_dict = {parsed_aspects[i]:parsed_aspects[i+1] for i in range(0, len(parsed_aspects), 2)}
                            for aspect in spell_dict.keys():
                                if aspect in tea_formulation.keys():
                                    tea_formulation[aspect] += int(spell_dict[aspect])
                                else:
                                    tea_formulation[aspect] = int(spell_dict[aspect])
                        else:
                            post_result_text = "Spell Cast Failed."
                        post_result_timer = 90  # show for 1.5 seconds

        # Draw background (always)
        screen.blit(background_image, (0, 0))

        # If we're showing a post-result (after casting), show result text centered
        # Draw the spellbook (normal mode)
        screen.blit(spellbook_image, (book_x, book_y))
        spell = spells[current_page]

        casts_remaining  = casts_remaining_f.render(f"{spells_remaining} casts remaining", True, (0, 0, 0))
        screen.blit(casts_remaining, (book_x + 200, book_y - 80))

        tea_formulation_test = formulation_f.render("Tea Formulation:", True, (255, 255, 255))
        screen.blit(tea_formulation_test, (book_x - 150, book_y + 100))

        for index, (aspect, amount) in enumerate(tea_formulation.items(), start=1):
            aspect_text = formulation_f.render(f"{aspect}: {amount}", True, (255, 255, 255))
            screen.blit(aspect_text, (book_x - 150, book_y + 120 + index * 30))

        # LEFT PAGE: title, icon, aspects
        title_surface = title_f.render(spell.name, True, (0, 0, 0))
        screen.blit(title_surface, (left_page_x-15, left_page_y))

        screen.blit(spell.icon, (left_page_x + 20, left_page_y + 100))

        aspects_surface = aspects_f.render(spell.aspects, True, (0, 0, 0))
        screen.blit(aspects_surface, (left_page_x, left_page_y + 270))

        # RIGHT PAGE: magical words
        for i, word in enumerate(spell.words):
            wsurf = words_f.render(word, True, (0, 0, 0))
            screen.blit(wsurf, (right_page_x, right_page_y + 60 + i * 60))

        # Cast button
        hovered = button_rect.collidepoint(mouse)
        color = (215, 200, 255) if hovered else (190, 175, 235)
        pygame.draw.rect(screen, color, button_rect, border_radius=12)
        btn_text = button_f.render("Cast Spell", True, (0, 0, 0))
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
            if post_result_timer == 0 and spells_remaining == 0:
                return tea_formulation


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_minigame3(pygame.display.set_mode((1280, 720)), pygame.time.Clock())
