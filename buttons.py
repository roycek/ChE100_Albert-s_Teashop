import pygame

"""
Written by Bruce Roy Harold Legge
"""

# Creating a Button 
def create_button(x, y, w, h, text):
    """
    (float, float, float, float, str) -> dict
    """
    return {"rect": pygame.Rect(x, y, w, h), "text": text}  # Returns the dictionary with button setting.

# Drawing the button on screen 
def draw_button(button, screen, font, color):
    """
    (dict, Surface, Font, tuple) -> None
    """
    pygame.draw.rect(screen, color, button["rect"])  # drawing a rectangular button on the screen.
    text = font.render(button["text"], True, (0, 0, 0))  # Render text.
    buttonText = text.get_rect(center=button["rect"].center)  # Centering the text inside the button.
    screen.blit(text, buttonText)  # Draws the text on screen.

def button_clicked(button, event):  # Returns true when left mouse button is clicked.
    """
    (dict, Event) -> bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Mouse left click.
            if button["rect"].collidepoint(event.pos):
                return True
    return False
