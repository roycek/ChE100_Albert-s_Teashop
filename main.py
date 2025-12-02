import pygame
import sys
import buttons

import minigame3
from minigame3 import run_minigame3

pygame.init()

# Window 
width = 1280
height = 720
mainScreen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame GUI")

# Font
defaultFont = pygame.font.SysFont("arial", 30)
dialogueFont = pygame.font.SysFont("timesnewroman", 28)

# Images
startImage = pygame.image.load("images/startScreen.png")
inGameImage = pygame.image.load("images/ingame.png")
textBubble = pygame.image.load("images/textBubble.png")
textBubble = pygame.transform.scale(textBubble, (600, 350))

professors = [
    [pygame.image.load("images/zhao0.png")],      # 0 - Zhao (neutral)
    [pygame.image.load("images/hamilton0.png")],  # 1 - Hamilton (neutral)
    [pygame.image.load("images/mintah0.png")],    # 2 - Mintah (neutral)
    [pygame.image.load("images/pendar0.png")]     # 3 - Pendar (neutral)
]

# Reaction images
angry = [
    pygame.image.load("images/zhao2.png"),
    pygame.image.load("images/hamilton2.png"),
    pygame.image.load("images/mintah2.png"),
    pygame.image.load("images/pendar2.png")
]

happy = [
    pygame.image.load("images/zhao1.png"),
    pygame.image.load("images/hamilton1.png"),
    pygame.image.load("images/mintah1.png"),
    pygame.image.load("images/pendar1.png")
]

# Sounds
dialogueSound = pygame.mixer.Sound("sounds/talking.mp3")
dialogueSound.set_volume(0.5)

# Where to draw the bubble
bubbleX = 430
bubbleY = 0

# For mapping gameState -> professor index for images
customerIndexMap = {
    "Zhao": 0,
    "Hamilton": 1,
    "Mintah": 2,
    "Pendar": 3
}

# Customer order
customerOrder = ["Zhao", "Hamilton", "Mintah", "Pendar"]

# Game State
gameState = "startScreen"
dialogueNum = 0
currentCustomerIndex = 0
currentCustomer = customerOrder[currentCustomerIndex]
minigame = False
waitingForNextCustomer = False
output = None

# "neutral", "happy", "angry"
currentExpression = "neutral"

# Dialogue
dialogue = {
    "Zhao": [
        "Hello, hello.",
        "My order: simple!",
        "Just black tea. Strong. \nSweet: 1, Bitter: 1 ",
        "Wow, wonderful.",
        "It's okay.",
        "No, not good."
    ],
    "Pendar": [
        "Good mornin'",
        "I would like a honey citrus mint tea.",
        "And use that 'TEA-O-MATIC',\nMint: 2, Spice: 1, Citrus: 1, Sweet: 1",
        "That's right! Good job!",
        "Not quite...",
        "Hmmmm, that's not it."
    ],
    "Hamilton": [
        "Hey barista!",
        "Give me a tea with a \nhint of spicy sweetness,",
        "Squeeze it 6 or 7 times\nBitter: 2, Spice: 1, Sweet: 1.",
        "Cool!",
        "You're almost there...",
        "No, that's not it."
    ],
    "Mintah": [
        "Hello CHEMICAL, \nI have not ordered anything yet.",
        "I would like a medium creamy \ncoffee, make it extra sweet!",
        "I don't care \nif you have to do any magic.\nCreamy: 1, Sweet: 2, Tea: 2",
        "Thank you colleague, that is correct!",
        "Those in the back might like this, not me...",
        "I could've made tea better \nthan this when I was two years old."
    ]
}
# Target ingredient amounts for each customer
orderList = {
    "Zhao": {"Sweet": 1, "Bitter": 1},
    "Hamilton": {"Bitter": 2, "Spice": 1, "Sweet": 1},
    "Mintah": {"Creamy": 1, "Sweet": 2, "Tea": 2},
    "Pendar": {"Mint": 2, "Spice": 1, "Citrus": 1, "Sweet": 1}
}

def enterReleased(event):#AH
    '''
    (Event) -> bool
    Returns true when enter key is released. 
    '''
    return (
        event.type == pygame.KEYUP and
        (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER)
    )

def valueCheck(order: dict, result: dict):#AH
    """
    (dict, dict) -> str
    Compare the required order with the minigame result.
    """
    for key in order:
        if key not in result:
            return "Bad"
    perfect = True
    for key in order:
        if result[key] < order[key]:
            perfect = False
    if (perfect):
        return "Perfect"
    return "Good"

def drawCustomerDialogue(customerName):#AH
    """
    (str) -> None
    Draw the customer's sprite and dialogue text.
    """
    global dialogueNum  
    global currentExpression

    mainScreen.blit(inGameImage, (0, 0))

    customerIndex = customerIndexMap[customerName]

    # Choose image based on expression
    if (currentExpression == "happy"):
        profImage = happy[customerIndex]
    elif (currentExpression == "angry"):
        profImage = angry[customerIndex]
    else:
        profImage = professors[customerIndex][0]

    mainScreen.blit(profImage, (0, -10))

    currentLines = dialogue[customerName]

    if (dialogueNum >= 1):
        mainScreen.blit(textBubble, (bubbleX, bubbleY))

        lineIndex = dialogueNum - 1

        if (0 <= lineIndex < len(currentLines)):
            text = currentLines[lineIndex]

            lines = text.split("\n")
            baseY = bubbleY + 60
            lineSpacing = 35

            for i, line in enumerate(lines):
                textSurface = dialogueFont.render(line, True, (0, 0, 0))
                textX = bubbleX + (textBubble.get_width() - textSurface.get_width()) // 2
                textY = baseY + i * lineSpacing + 30
                mainScreen.blit(textSurface, (textX, textY))

def goToNextCustomer():
    """
    () -> None
    Move to the next customer and reset dialogue state.
    """
    global currentCustomerIndex
    global currentCustomer
    global gameState
    global dialogueNum
    global currentExpression

    pygame.mixer.music.load("sounds/doorBell.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play()

    currentCustomerIndex += 1

    if (currentCustomerIndex >= len(customerOrder)):
        gameState = "gameComplete"
        currentCustomerIndex = 0
        currentCustomer = customerOrder[currentCustomerIndex]
        dialogueNum = 0
        currentExpression = "neutral"
    else:
        currentCustomer = customerOrder[currentCustomerIndex]
        gameState = currentCustomer
        dialogueNum = 0
        currentExpression = "neutral"

def main():
    """
    () -> None
    Main game loop controlling menus, dialogue, and minigames.
    """
    global gameState
    global dialogueNum
    global currentCustomer
    global minigame
    global output
    global waitingForNextCustomer
    global currentExpression
    clock = pygame.time.Clock()

    if (gameState == "startScreen"):
        mainScreen.blit(startImage, (0, 0))
        pygame.mixer.music.load("sounds/startBGM.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        startButton = buttons.create_button(554, 582, 193, 48, "")
        howtoPlayButton = buttons.create_button(554,641,193,48, "")

    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (gameState == "startScreen"):
                if (buttons.button_clicked(startButton, event)):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/doorBell.mp3")
                    pygame.mixer.music.set_volume(0.25)
                    gameState = "inGame"
                if(buttons.button_clicked(howtoPlayButton,event)):
                    gameState = "howToPlay"
            elif (gameState == "howToPlay"):
                mainScreen.fill((0, 0, 0))

                instructions = [#Explanation of how to play
                    "HOW TO PLAY",
                    "",
                    "Press ENTER to advance dialogue.",
                    "Your goal is to prepare each customer's drink",
                    "by matching their order using the minigame.",
                    "",
                    "The minigame works like an Euler Trail:",
                    "you must trace edges exactly once",
                    "to choose the ingredients.",
                    "",
                    "Match their order perfectly to earn a Perfect score!",
                    "",
                    "Press ENTER to begin."
                ]

                base_y = 100
                spacing = 40

                for i, line in enumerate(instructions):
                    textSurface = dialogueFont.render(line, True, (255, 255, 255))
                    textX = (width - textSurface.get_width()) // 2
                    textY = base_y + i * spacing
                    mainScreen.blit(textSurface, (textX, textY))
                if(enterReleased(event)):
                    gameState = "inGame"
                
            elif (gameState == "inGame"):
                if (enterReleased(event)):
                    pygame.mixer.music.play()
                    gameState = currentCustomer
                    dialogueNum = 0
                    currentExpression = "neutral"

            elif (gameState in ["Zhao", "Hamilton", "Mintah", "Pendar"]):

                if (waitingForNextCustomer): #AH: After result line, wait for Enter to go to next customer
                    if (enterReleased(event)):
                        waitingForNextCustomer = False
                        goToNextCustomer()

                else:
                    if (enterReleased(event) and (minigame == False)):
                        oldNum = dialogueNum

                        dialogueNum += 1
                        if (dialogueNum > 3):#AH: Starting minigame 
                            dialogueNum = 3
                            minigame = True
                            output = run_minigame3(mainScreen, clock)

                        if (dialogueNum != oldNum and (dialogueNum - 1) <= 2):
                            dialogueSound.play()

                    if ((gameState in orderList) and minigame and (output is not None)):#AH: Result checking 
                        prof = gameState
                        result = valueCheck(orderList[prof], output)
                        print(result)

                        if (result == "Perfect"):
                            dialogueNum = 4
                            currentExpression = "happy"
                        elif (result == "Good"):
                            dialogueNum = 5
                            currentExpression = "neutral"
                        else:  #Bad
                            dialogueNum = 6
                            currentExpression = "angry"

                        dialogueSound.play()
                        minigame = False
                        waitingForNextCustomer = True
                        output = None

        if (gameState == "startScreen"):
            mainScreen.blit(startImage, (0, 0))

        elif (gameState == "inGame"):
            mainScreen.blit(inGameImage, (0, 0))

        elif (gameState in ["Zhao", "Hamilton", "Mintah", "Pendar"]):
            drawCustomerDialogue(gameState)

        elif (gameState == "gameComplete"):
            mainScreen.fill((0, 0, 0))
            textSurface = dialogueFont.render("Thank you for playing!", True, (255, 255, 255))
            textX = (width - textSurface.get_width()) // 2
            textY = (height - textSurface.get_height()) // 2
            mainScreen.blit(textSurface, (textX, textY))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
