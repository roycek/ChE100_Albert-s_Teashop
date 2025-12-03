import pygame
import sys
import math
import random

"""
Written by Royce Malikov
ID: 21180984
"""

# The Spell class is a helper class which contains a bunch of information related to each spell
class Spell:
    def __init__(self, name, aspects, words, icon, node_positions):
        """
        :param name: A string containing the name of the spell
        :param aspects: A stripng containing the aspects of the spell
        :param words: A list containing magic words corresponding to the spell
        :param icon: A pygame image, converted by alpha to keep transparent, and scaledc to 160 pixels
        :param node_positions: A list of screen coordinates for the nodes of the spell
        """
        self.name = name
        self.aspects = aspects
        self.words = words
        self.icon = icon
        self.node_positions = node_positions


class SpellNode:
    def __init__(self, pos, index, radius=20):
        """
        The SpellNode class contains information about a specific node, along with two methods:
        draw() which draws it onto a given pygame Screen
        is_hover() which returns a boolean of if a given pygame mouse object is hovering over the node

        :param pos: A set of screen coordinates to draw the node at
        :param index: An index corresponding to the node for use in hover_interaction
        :param radius: The radius of the circle representing the node
        """
        self.pos = pos
        self.index = index
        self.radius = radius
        self.traced = False

    def draw(self, screen, font):
        """
        The draw() function takes a pygame Screen and pygame Font and draws a circle onto the screen, representing the node
        The function colors the circle depending on whether or not it has been traced already, and draws it at self.pos
        It adds the number corresponding to the node onto the circle in the correct font

        :param screen:
        :param font:
        :return: None
        """
        x, y = self.pos

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
        """
        The is_hover() method checks whether or not a pygame mouse pointer is currently hovering over the node

        :param mouse_pos: coordinates of mouse pointer
        :return: result of the boolean evaluation
        """
        return math.dist(self.pos, mouse_pos) <= self.radius


def cast_spell(screen, clock, spell, background_image):
    """
    The cast_spell method takes a pygame Screen object, a pygame Clock object, and a Spell object.
    It performs all user interaction and handling for tracing the nodes, casting the spell, playing sound effects,
    and checking for success or failure.

    :param screen: The pygame Screen to draw the spell onto
    :param clock: The pygame Clock for ticking the game
    :param spell: The Spell object containing the info of the spell currently being cast
    :param background_image: The background image of the game
    :return: a booolean value corresponding to whether or not the spell succeeded.
    """

    # Width and height of the screen
    WIDTH, HEIGHT = screen.get_size()

    # Font for node numbering
    node_font = pygame.font.Font("Spell_Assets/MagicSchoolOne.ttf", 28)

    # generating list of SpellNodes() from the list of coordinates in the spell
    nodes = [SpellNode(pos, i) for i, pos in enumerate(spell.node_positions)]

    # booleans for spell handling
    next_required = 0
    hovered_prev = None
    running_cast = True
    result = None  # None while in progress, True success, False fail

    # Loading images for the game and scaling
    teacup_img = pygame.image.load("Spell_Assets/Teacup.png").convert_alpha()
    teacup_img = pygame.transform.scale(teacup_img, (120, 120))
    star_img = pygame.image.load("Spell_Assets/GoldStar.png").convert_alpha()
    star_img = pygame.transform.scale(star_img, (24, 24))
    x_img = pygame.image.load("Spell_Assets/RedX.png").convert_alpha()
    x_img = pygame.transform.scale(x_img, (32, 32))

    # loading sounds for the game
    ding = pygame.mixer.Sound("Spell_Assets/ding.mp3")
    error = pygame.mixer.Sound("Spell_Assets/error.mp3")

    # position the teacup in the center of the screen for the post-cast effects
    teacup_pos = (WIDTH // 2 - 60, HEIGHT // 2 - 60)
    effects = []
    effect_timer = 120  # 3 seconds

    def draw_pattern_guides():
        """
        The draw_pattern_guides() function draws lines connecting the centers of each node.
        The nodes will be drawn on top of these lines at the vertices. This creates a visual path between the nodes.
        :return: None
        """
        if len(nodes) > 1:
            pts = [n.pos for n in nodes]
            pygame.draw.lines(screen, (120, 180, 200), False, pts, 4)

    # Main loop of the spell cast
    while running_cast:
        # handling game quitout
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # current mouse coordinates
        mouse = pygame.mouse.get_pos()

        # checking if mouse is currently hovering over node
        hovered_now = None
        for n in nodes:
            if n.is_hover(mouse):
                hovered_now = n.index
                break

        # draw background
        screen.blit(background_image, (0, 0))

        # draw spell if it has not resolved yet(not failed or succeeded)
        if result is None:
            # draw the connecing lines
            draw_pattern_guides()
            # draw each node using SpellNode.draw()
            for n in nodes:
                n.draw(screen, node_font)

            # check if the node hovered currently is new, to prevent errors for the cursor remaining in a node
            if hovered_now is not None and hovered_now != hovered_prev:
                node = nodes[hovered_now]
                # if the node was already traced, play the error sound and fail the spell
                if node.traced:
                    error.play()
                    result = False
                else:
                    # if the node traced is the next required index, play the ding sound and increment the next requried node!
                    if node.index == next_required:
                        ding.play()
                        node.traced = True
                        next_required += 1
                        # if the next required node is out of the list, the spell is successful!
                        if next_required >= len(nodes):
                            result = True
                    # if the node is out of order, play the error sound and fail the spell
                    else:
                        error.play()
                        result = False

            # update the previously hovered node
            hovered_prev = hovered_now

            # as long as the spell is not yet complete, draw a circle around the next required node that has a
            # radius of 6 more pixels
            if next_required < len(nodes):
                nx = nodes[next_required]
                pygame.draw.circle(screen, (80, 200, 230), nx.pos, nx.radius + 6, 3)

        # if the spell has a result, begin drawing the effects
        else:
            # check if the effects list has not been generated yet
            if not effects:
                # center of teacup
                teacup_center = (teacup_pos[0] + teacup_img.get_width() // 2,
                                 teacup_pos[1] + teacup_img.get_height() // 2)
                # 25 gold stars if successful, 15 x images if failed
                num_effects = 25 if result else 15

                # generate the effects list to be a list of dicitonaries
                # each dictionary contains:
                # the position of the effect spread out by 80 pixels around the center of the teacup
                # the delay in spawning which is a random number beetween 0 and 0.5s
                # the state of the effect
                # the oppacity of the effect
                # the velocity of the effect (negative if it is a gold star, making it go up the screen, 0 if it is an x keep it stagnant)
                for i in range(num_effects):
                    dx = random.randint(-80, 80)
                    dy = random.randint(-60, 60)
                    spawn_delay = random.randint(0, 30)
                    effects.append({
                        'pos': [teacup_center[0] + dx, teacup_center[1] + dy],
                        'spawn_delay': spawn_delay,
                        'spawned': False,
                        'alpha': 255,
                        'vy': -random.uniform(0.5, 1.5) if result else 0
                    })

            # Draw the teacup
            screen.blit(teacup_img, teacup_pos)

            # Draw the effects
            for e in effects:
                # decrease the spawn delay by 1 game tick if it is above 0
                if e['spawn_delay'] > 0:
                    e['spawn_delay'] -= 1
                    continue

                # if the effect has reached 0 spawn delay, set the spawned flag to true
                if not e['spawned']:
                    e['spawned'] = True

                # position of effect
                x, y = e['pos']

                # draw gold stars if successful
                if result:
                    # y position of the stars decreases, making them raise up the screen by vy every tick
                    y += e['vy']
                    e['pos'][1] = y
                    # opacity decreases by 3 units up to a limit of 0
                    e['alpha'] = max(e['alpha'] - 3, 0)
                    if e['alpha'] <= 0:
                        continue

                    # draw the star image at the coordinates with the provided opacity
                    star_surf = star_img.copy()
                    star_surf.fill((255, 255, 255, e['alpha']), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(star_surf, (x - star_surf.get_width() // 2, y - star_surf.get_height() // 2))

                else:
                    # Draw static red X at the coordinates of the effect
                    screen.blit(x_img, (x - x_img.get_width() // 2, y - x_img.get_height() // 2))

            # decrement effect timer. The timer starts at 120 ticks, so the effect lasts 2 seconds
            effect_timer -= 1
            # if the effect is done, stop the cast
            if effect_timer <= 0:
                running_cast = False

        # render the display and tick the game by 1 game tick (60 ticks per second)
        pygame.display.flip()
        clock.tick(60)

    # return the result of the spell
    return bool(result)