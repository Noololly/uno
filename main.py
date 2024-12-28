import sys
import pygame
import random



class Player: #Player class
    def __init__(self, deck, player_number):
        self.hand = {}
        self.deal_hand(deck)
        self.player_number = player_number


    def deal_hand(self, deck): #Deals the player's hand
        for i in range(7):
            card = deck.pop()
            self.hand[i] = card

#Initialise EVERYTHING
pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("UNO")

clock = pygame.time.Clock()

colours = ["red", "blue", "green", "yellow"]
numbers = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9", "_skip", "_reverse", "_+2"]
players = []
deck = []
discard = []
player_turn = 0 #Number of player whose turn it currently is
reverse = False

card_back = pygame.image.load("back.png")

font = pygame.font.Font(None, 32)


def create_game(): #Function to create the game and display a nice GUI to enter the number of players
    input_rect = pygame.Rect(400, 250, 250, 35)
    user_text = ""
    player_number = 0
    while not player_number: #Render player number selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.isdigit():
                        user_number = int(user_text)
                        if 0 < user_number <= 10:
                            player_number = user_number
                            print(f"Number of players: {player_number}")
                            break
                        else:
                            user_text = ''
                    else:
                        user_text = ''
                elif event.unicode.isprintable():
                    user_text += event.unicode

        user_instruction_rect = pygame.Rect(375, 215, 250, 35)
        instruction_text = font.render("Enter the number of players:", True, (255,255,255))
        screen.blit(instruction_text, (user_instruction_rect.x, user_instruction_rect.y))

        pygame.draw.rect(screen, "white", input_rect)

        text_surface = font.render(user_text, True, (0,0,0))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        pygame.display.flip()
        clock.tick(60)

    create_deck() #Make the deck to draw from
    for i in range(player_number):
        players.append(Player(deck, i)) #Create the players. Gives each player a number in which order of turn they will be in


def create_deck(): #Makes the deck with all the appropriate cards
    for i in range(3):
        deck.append(("wild", "wild"))
        deck.append(("wild", "+4"))
    for colour in colours:
        deck.append((colour, 0))
        deck.append((colour, "skip"))
        deck.append((colour, "skip"))
        deck.append((colour, "reverse"))
        deck.append((colour, "reverse"))
        deck.append((colour, "+2"))
        deck.append((colour, "+2"))
        for j in range(1,10):
            deck.append((colour, j))
    random.shuffle(deck)


def end_of_deck(): #If all the cards in the deck have been used, take all the cards in the discard pile and shuffle
    for card in discard:
        deck.append(card)
        discard.remove(card)
    random.shuffle(deck)

def card_hider(): #A function to blank the screen to hide a player's cards from other players when passing the device around
    button = pygame.Rect(350, 440, 360, 30)
    player_turn_rect = pygame.Rect(350, 10, 360, 30)
    hidden = True
    while hidden:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos): #Detects if the button is pushed to start the turn of the next player
                    hidden = False

        screen.fill("black")

        player_turn_text = font.render(f"It is player {player_turn}'s turn", True, (255,255,255))
        screen.blit(player_turn_text, (player_turn_rect.x, player_turn_rect.y))

        pygame.draw.rect(screen, "white", button)
        above_button_text = font.render("Click to start the next player's turn", True, (255,255,255))
        screen.blit(above_button_text, (button.x, button.y-40))

        button_text = font.render("Next Player!", True, (0,0,0))
        screen.blit(button_text, ((button.x+(button.w-250)), button.y+5))

        pygame.display.flip()
        clock.tick(60)
    return

def turn():
    x = 0
    y = 0
    for card in players[0].hand:
        to_blit_colour, to_blit_number = players[0].hand[card]
        to_blit = pygame.image.load(f"uno_cards\\{to_blit_colour}_{to_blit_number}.png")
        screen.blit(to_blit, (x,y))
        pygame.display.flip()
        clock.tick(60)
        x += 50


def main(): #The main game rendering loop
    create_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                turn()
        screen.fill("black")

        pygame.display.update()
        clock.tick(60)
        turn()
        #card_hider()


if __name__ == "__main__": #Ctrl-C error handling and initialisation of the game
    try:
        main()
    except KeyboardInterrupt:
        pass

pygame.quit() #Kills the pygame library
