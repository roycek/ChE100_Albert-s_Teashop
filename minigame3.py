import pygame
import sys

from spellcaster import Spell
from spellcaster import cast_spell

"""
Written by Royce Malikov
ID: 21180984
"""

def run_minigame3(screen, clock):
    """
    This is the main function of the minigame. It takes a pygame Screen and Clock and draws the entirety of the minigame.
    This includes the spellbook, all buttons, and the spell itself as it is being cast using the cast_spell() function

    :param screen: The pygasme Screen that the minigame is drawn onto
    :param clock: The pygame Clock for ticking the game
    :return: a dictionary containing the aspects created by the tea and the amount of each aspect
    """

    # load background image to fit the screen
    background_image = pygame.transform.scale(pygame.image.load("Spell_Assets/Magic_Bg.jpg").convert(), screen.get_size())

    # load spellbook image and set the scale
    spellbook_image = pygame.image.load("Spell_Assets/Spellbook_Transparent.png").convert_alpha()
    spellbook_image = pygame.transform.scale(spellbook_image, (800, 500))

    # load the page flip cound effect
    page_flip = pygame.mixer.Sound("Spell_Assets/page_flip.mp3")

    # load and begin the background music, set loops to -1 to keep it always looping
    pygame.mixer.music.load("Spell_Assets/spell_background.mp3")
    pygame.mixer.music.play(loops=-1)

    # width and height of the screen
    WIDTH, HEIGHT = screen.get_size()

    # setting the font size for every font type, different texts in the game all need different fonts
    title_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 70)
    aspects_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 30)
    words_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 60)
    button_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 32)
    arrow_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 22)
    result_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 52)
    casts_remaining_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 90)
    formulation_f = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 35)


    # setting book position and boundaries of the pages
    book_w, book_h = 800, 500
    book_x = (WIDTH - book_w) // 2
    book_y = (HEIGHT - book_h) // 2
    left_page_x = book_x + 140
    left_page_y = book_y + 60
    right_page_x = book_x + 430
    right_page_y = book_y + 10

    # navigation buttons and casting buttons
    button_rect = pygame.Rect(right_page_x, right_page_y + 350, 220, 55)
    left_btn = pygame.Rect(book_x + 20, book_y + 20, 50, 35)
    right_btn = pygame.Rect(book_x + book_w - 70, book_y + 20, 50, 35)

    # center of screen
    center = (WIDTH // 2, HEIGHT // 2)
    cx, cy = center

    # small helper function for the nodes; given an integer offset dx and dy, multiply it by 20 add it to the center coords
    # this keeps all spell nodes centered on the screen
    def rel(dx, dy):
        return cx + dx*20, cy + dy*20

    # creating the list of spells
    spells = [
        Spell(
            "Honeywisp", # set the name of the spell
            "Aspects: Sweet +2", # set the aspects of the spell
            ["Mellino", "Honstar", "Cortegen","Unfluxia"], # set the magic words of the spell
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/HoneyWhisper.png").convert_alpha(),
                                   (160, 160)), # set the glyph of the spell
            [
                rel(-5,5), rel(0,-8), rel(5,5), rel(-6,-5), rel(6, -5), rel(-3,3)
            ] # set the coordinates of each node, in order. The numbers are multiples of 20 pixels offset from the center of the screen.
            # all spells were first hand drawn on grid paper and then transferred into the game
        ),

        Spell(
            "Sugar Sigil",
            "Aspects: Sweet +1",
            ["Astralis", "Penthera", "Lumistar", "Sucrama"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/SugarSigil.png").convert_alpha(), (160, 160)),
            [
                rel(-7, -5), rel(0,5), rel(7,-5), rel(7, 5), rel(0,-5), rel(-7,5)
            ]
        ),

        Spell(
            "Citrus Pulse",
            "Aspects: Citrus +2",
            ["Lemoana", "Spiraflux", "Helixor", "Fluxia"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/CitrusPulse.png").convert_alpha(), (160, 160)),
            [
                rel(6,-3), rel(3,-5), rel(0,-6), rel(-3,-5), rel(-6,-3),
                rel(-6,0), rel(6,0), rel(6,3), rel(3,5), rel(0,6), rel(-3,5),
                rel(-6,3)
            ]
        ),

        Spell(
            "Lemonflare",
            "Aspects: Citrus +1, Sweet +1",
            ["Ragamorg", "Ravelis", "Skratcha", "Citraline"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/Lemonflare.png").convert_alpha(), (160, 160)),
            [
                rel(-8,0), rel(-4,6), rel(4,6), rel(8,0), rel(2,2),
                rel(0,-9), rel(-2,2), rel(-6,1)
            ]
        ),

        Spell(
            "Tealeaf Rite",
            "Aspects: Tea +2",
            ["Seraphae", "Sinuara", "Silvena", "Invoka"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/TealeafInvocation.png").convert_alpha(), (160, 160)),
            [
                rel(-5,7), rel(-9,-4), rel(-3,-7), rel(-7,1), rel(3,-2), rel(0,7), rel(-3,-2),
                rel(7,1), rel(3,-7), rel(9,-4), rel(5,7)
            ]
        ),

        Spell(
            "Earl Echo",
            "Aspects: Tea +1, Citrus +1",
            ["Earlis", "Resona", "Citralux", "Echovera"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/EarlgreyEcho.png").convert_alpha(), (160, 160)),
            [
                rel(-7,-10), rel(7,-10), rel(-7,-5), rel(7,-5), rel(-7,0), rel(7,0),
                rel(0,7), rel(0,-14)
            ]
        ),

        Spell(
            "Chai Ember",
            "Aspects: Spice +2, Tea +1",
            ["Chalon", "Emberyx", "Masalir", "Flaretea"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/ChaiEmber.png").convert_alpha(), (160, 160)),
            [
                rel(0,-10), rel(-6,-4), rel(4,-4), rel(9,3), rel(-6,3), rel(9,-4),
                rel(0,7), rel(0,-7), rel(9,-7)
            ]
        ),

        Spell(
            "Cinnamon",
            "Aspects: Spice +1",
            ["Cinnaar", "Spiralux", "Brashava", "Scorchine"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/CinnamonWeave.png").convert_alpha(), (160, 160)),
            [
                rel(0, -10), rel(-2, -4), rel(-8, -10), rel(-4, -2),
                rel(0, 6), rel(4, -2), rel(8, -10), rel(2, -4)
            ]
        ),

        Spell(
            "Herb Bloom",
            "Aspects: Herbal +2",
            ["Herbalis", "Florien", "Sprouthex", "Budmora"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/HerbalBloom.png").convert_alpha(), (160, 160)),
            [
                rel(0, -8), rel(6, 0), rel(0, 8), rel(-6, 0),
                rel(3, -3), rel(-3, -3), rel(3, 3), rel(-3, 3),
            ]
        ),

        Spell(
            "Ley Garden",
            "Aspects: Herbal +1, Tea +1",
            ["Leyward", "Gardenis", "Verdalux", "Infusara"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/GardenDraught.png").convert_alpha(), (160, 160)),
            [
                rel(-8, 6), rel(-4, -10), rel(-1, -4),
                rel(1, -4), rel(4, -10), rel(8, 6),
                rel(0, -2), rel(0, 4)
            ]
        ),

        Spell(
            "Mintwhirl",
            "Aspects: Mint +2",
            ["Freskal", "Whirleaf", "Mentara", "Gustine"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/Mintwhirl.png").convert_alpha(), (160, 160)),
            [
                rel(6, -2), rel(4, -6), rel(0, -8), rel(-4, -6), rel(-6, -2), rel(-4, 4),
                rel(0, 6), rel(4, 4), rel(6, 0)
            ]
        ),

        Spell(
            "Frost Snap",
            "Aspects: Mint +1, Citrus +1",
            ["Frigidis", "Zintrix", "Snaplemon", "Chillara"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/FrostmintSnap.png").convert_alpha(), (160, 160)),
            [
                rel(0, -8), rel(0, 8), rel(-8, 0), rel(8, 0), rel(-4, -4), rel(4, -4),
                rel(4, 4), rel(-4, 4)
            ]
        ),

        Spell(
            "Creamweave",
            "Aspects: Creamy +2",
            ["Creamora", "Velastrid", "Silkalux", "Bindara"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/CreamyWeave.png").convert_alpha(), (160, 160)),
            [
                rel(-10, 0), rel(-8, -4), rel(-4, -7), rel(0, -8),
                rel(4, -7), rel(8, -4), rel(10, 0),
                rel(6, 2), rel(3, 4), rel(0, 6), rel(-3, 4), rel(-6, 2)
            ]
        ),

        Spell(
            "Velvetfoam",
            "Aspects: Creamy +1, Sweet +1",
            ["Velveta", "Suavine", "Foamara", "Sugrith"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/Velvetfoam.png").convert_alpha(), (160, 160)),
            [
                rel(-10, -8), rel(-6, -4), rel(-2, 0),
                rel(2, -4), rel(6, -8),
                rel(0, 2), rel(0, 6)
            ]
        ),

        Spell(
            "Dark Surge",
            "Aspects: Bitter +2",
            ["Darkara", "Survex", "Ravenero", "Nightbrew"],
            pygame.transform.scale(pygame.image.load("Spell_Assets/Spell Glyphs/DarkroastSurge.png").convert_alpha(), (160, 160)),
            [
                rel(0, -16), rel(-4, -10), rel(-2, -5), rel(0, -1), rel(2, -5), rel(4, -10),
                rel(0, -12), rel(0, -6), rel(0, 4), rel(0, 10)
            ]
        ),
    ]

    # current page of the book
    current_page = 0

    # dictionary for storing the prepared formulation
    tea_formulation = {}

    # spells remaining
    spells_remaining = 3

    # message after succeeding or failing a spell
    post_result_text = ""
    post_result_timer = 0

    running = True

    while running:
        # handling game exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Navigation (only when not casting)
                if post_result_timer <= 0:  #  normal interaction allowed only when not showing post-result
                    if left_btn.collidepoint(mouse):
                        page_flip.play() # play page flip sound effect
                        current_page = (current_page - 1) % len(spells) # flipping through the pages and wrapping around the left side of the list
                    elif right_btn.collidepoint(mouse):
                        page_flip.play() # play page flip sound effect
                        current_page = (current_page + 1) % len(spells) # flipping through the pages and wrapping around the right side of the list
                    elif button_rect.collidepoint(mouse):
                        # if the user presses the cast button, get the spell index of the current page and run cast_spell()
                        # save the output of the spell cast to success and decrement spells remaining
                        active_spell = spells[current_page]
                        pygame.mouse.set_pos(cx+200, cy+200)# move mouse away from spell to avoid acidentally failing
                        success = cast_spell(screen, clock, active_spell, background_image)
                        spells_remaining -= 1
                        if success:
                            post_result_text = "Spell Cast Successfully!" # set post result text to successful option
                            parsed_aspects = active_spell.aspects.replace("Aspects: ","").replace("+", "").replace(",", "").split(" ") # parse the aspect text of the spell
                            spell_dict = {parsed_aspects[i]:parsed_aspects[i+1] for i in range(0, len(parsed_aspects), 2)} # create a dictionary out of the aspect text
                            # update the tea formulation with the parsed aspects from the spell
                            for aspect in spell_dict.keys():
                                if aspect in tea_formulation.keys():
                                    tea_formulation[aspect] += int(spell_dict[aspect])
                                else:
                                    tea_formulation[aspect] = int(spell_dict[aspect])
                        else:
                            post_result_text = "Spell Cast Failed." # set post ressult text to failed option
                        post_result_timer = 90  # show end screen for 1.5 seconds

        mouse = pygame.mouse.get_pos()  # mouse coordinates

        # Draw background
        screen.blit(background_image, (0, 0))

        screen.blit(spellbook_image, (book_x, book_y)) # draw the spellbook

        spell = spells[current_page] # select the current spell for drawing

        # draw the casts remaining text
        casts_remaining  = casts_remaining_f.render(f"{spells_remaining} casts remaining", True, (0, 0, 0))
        screen.blit(casts_remaining, (book_x + 200, book_y - 80))

        # draw tea formulation caption
        tea_formulation_test = formulation_f.render("Tea Formulation:", True, (255, 255, 255))
        screen.blit(tea_formulation_test, (book_x - 150, book_y + 100))

        # draw each aspect within the formulation
        for index, (aspect, amount) in enumerate(tea_formulation.items(), start=1):
            aspect_text = formulation_f.render(f"{aspect}: {amount}", True, (255, 255, 255))
            screen.blit(aspect_text, (book_x - 150, book_y + 120 + index * 30))

        # draw the title of the spell on the left page
        title_surface = title_f.render(spell.name, True, (0, 0, 0))
        screen.blit(title_surface, (left_page_x-15, left_page_y))

        # draw the icon of the spell on the left page
        screen.blit(spell.icon, (left_page_x + 20, left_page_y + 100))

        # draw the aspects of the spell on the left page
        aspects_surface = aspects_f.render(spell.aspects, True, (0, 0, 0))
        screen.blit(aspects_surface, (left_page_x, left_page_y + 270))

        # draw the magic words of the spell on the right page
        for i, word in enumerate(spell.words):
            wsurf = words_f.render(word, True, (0, 0, 0))
            screen.blit(wsurf, (right_page_x, right_page_y + 60 + i * 60))

        # draw the spell cast button on the right page
        hovered = button_rect.collidepoint(mouse)
        color = (215, 200, 255) if hovered else (190, 175, 235)
        pygame.draw.rect(screen, color, button_rect, border_radius=12)
        btn_text = button_f.render("Cast Spell", True, (0, 0, 0))
        screen.blit(btn_text, btn_text.get_rect(center=button_rect.center))

        # draw the page navigation buttons
        pygame.draw.rect(screen, (255, 220, 180), left_btn, border_radius=8)
        pygame.draw.rect(screen, (255, 220, 180), right_btn, border_radius=8)
        screen.blit(arrow_f.render("<", True, (80, 30, 10)), left_btn.move(4, 0))
        screen.blit(arrow_f.render(">", True, (80, 30, 10)), right_btn.move(8, 0))

        # if we are in a post spell result state, show the post-result text
        if post_result_timer > 0:
            post_result_timer -= 1
            txt = result_f.render(post_result_text, True, (255, 245, 200) if "Successfully" in post_result_text else (255, 180, 180))
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2-20, HEIGHT // 2+250)))
            #  if there are no spells remaining, stop the music and return the formulation
            if post_result_timer == 0 and spells_remaining == 0:
                pygame.mixer.music.stop()
                return tea_formulation

        # update the display and tick the clock
        pygame.display.flip()
        clock.tick(60)
