import pygame
import sys
import buttons

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

#Sounds
dialogueSound = pygame.mixer.Sound("sounds/talking.mp3")
dialogueSound.set_volume(0.5)

professors = [
    [pygame.image.load("images/zhao0.png")],      # 0 - Zhao
    [pygame.image.load("images/hamilton0.png")],  # 1 - Hamilton
    [pygame.image.load("images/mintah0.png")],    # 2 - Mintah
    [pygame.image.load("images/pendar0.png")]     # 3 - Pendar
]

# Where to draw the bubble
bubbleX = 430
bubbleY = 0

# For mapping gameState -> professor index
customerIndexMap = {
    "Zhao": 0,
    "Hamilton": 1,
    "Mintah": 2,
    "Pendar": 3
}

# Game State
gameState = "startScreen"
dialogueNum = 0
currentCustomer = "Zhao"
minigame = False 
# Dialogue
dialogue = {
    "Zhao": [
        "Hello, hello.",
        "My order: simple!",
        "Just black tea. Strong. \nTea:2, Bitter: 1 ",
        "Wow, wonderful.",
        "It's okay.",
        "No, not good."
    ],
    "Pendar": [
        "Good mornin'",
        "I would like a honey citrus mint tea.",
        "And use that 'TEA-O-MATIC',\nI like how consistent it is.",
        "That's right! Good job!",
        "Not quite...",
        "Hmmmm, that's not it."
    ],
    "Hamilton": [
        "Hey barista!",
        "Give me an orange juice for my son,",
        "Squeeze it 6 or 7 times.",
        "Cool!",
        "You're almost there...",
        "No, that's not it."
    ],
    "Mintah": [
        "Hello CHEMICAL, \nI have not ordered anything yet.",
        "I would like a green tea \nwith no caffeine,",
        "I don't care \nif you have to do any magic.",
        "Thank you colleague, that is correct!",
        "Those in the back might like this, not me...",
        "I could've made tea better \nthan this when I was two years old."
    ]
}

def enterReleased(event):
    return (
        event.type == pygame.KEYUP and
        (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER)
    )
def valueCheck(order: dict, result: dict):
    for key in order:
        if key not in result:
            return "Bad"
    perfect = True
    for key in order:
        if result[key] < order[key]:
            perfect =False
    if(perfect):
        return "Perfect"
    return "Good"
def drawCustomerDialogue(customerName):
    global dialogueNum

    mainScreen.blit(inGameImage, (0, 0))

    customerIndex = customerIndexMap[customerName]
    mainScreen.blit(professors[customerIndex][0], (0, -10))

    currentLines = dialogue[customerName]

    if dialogueNum >= 1:
        mainScreen.blit(textBubble, (bubbleX, bubbleY))

        lineIndex = dialogueNum - 1
        if lineIndex > 2:
            lineIndex = 2

        if 0 <= lineIndex < len(currentLines):  # Making sure the index is valid
            text = currentLines[lineIndex]

            # Support "\n" by drawing each line separately
            lines = text.split("\n")
            baseY = bubbleY + 60  # a bit higher
            lineSpacing = 35

            for i, line in enumerate(lines):
                textSurface = dialogueFont.render(line, True, (0, 0, 0))
                textX = bubbleX + (textBubble.get_width() - textSurface.get_width()) // 2
                textY = baseY + i * lineSpacing + 30
                mainScreen.blit(textSurface, (textX, textY))

def main():
    global gameState
    global dialogueNum
    global currentCustomer
    global minigame
    clock = pygame.time.Clock()

    if (gameState == "startScreen"):
        mainScreen.blit(startImage, (0, 0))
        pygame.mixer.music.load("sounds/startBGM.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        startButton = buttons.create_button(554, 582, 193, 48, "")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (gameState == "startScreen"):
                if (buttons.button_clicked(startButton, event)):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/doorBell.mp3")
                    pygame.mixer.music.set_volume(0.25)
                    gameState = "inGame"

            elif (gameState == "inGame"):
                if (enterReleased(event)):
                    pygame.mixer.music.play()
                    gameState = currentCustomer
                    dialogueNum = 0

            elif (gameState in ["Zhao", "Hamilton", "Mintah", "Pendar"]):
                if (enterReleased(event) and minigame == False ):
                    oldNum = dialogueNum

                    dialogueNum += 1
                    if dialogueNum > 3:
                        dialogueNum = 3
                        minigame = True
                    if dialogueNum != oldNum and (dialogueNum - 1) <= 2:
                        dialogueSound.play()
                    

        if (gameState == "startScreen"):
            mainScreen.blit(startImage, (0, 0))

        elif (gameState == "inGame"):
            mainScreen.blit(inGameImage, (0, 0))

        elif (gameState in ["Zhao", "Hamilton", "Mintah", "Pendar"]):
            drawCustomerDialogue(gameState)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
