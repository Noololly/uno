import sys
import pygame
import random
from time import sleep

class Player: #Player class
    def __init__(self, deck, player_number):
        self.hand = {}
        self.deal_hand(deck)
        self.player_number = player_number


    def deal_hand(self, deck): #Deals the player's hand
        for i in range(7): #number of cards dealt at the start of an uno game
            card = deck.pop()
            self.hand[i] = card

#Initialise EVERYTHING
pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("UNO")

clock = pygame.time.Clock()
screen.fill("black")
colours = ["red", "blue", "green", "yellow"]
numbers = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9", "_skip", "_reverse", "_+2"] #lists of the colours and numbers of the cards
cards = {} #a dict to store all instances of the card images
players = [] #list of instances of players
deck = [] #list of cards in the draw pile
discard = [] #list of cards in the discard pile
player_turn = 0 #Number of player whose turn it currently is
reverse = False #bool storing direction of play

card_back = pygame.image.load("back.png")

font = pygame.font.Font(None, 32) #loads the font


def calculate_x_increment():
    card_quantity = len(players[player_turn].hand)
    screen_width = pygame.display.get_window_size()[0]

    # Constants
    CARD_WIDTH = 200  # Width of each card
    BORDER_WIDTH = 50  # Left and right borders

    # Calculate usable width
    usable_width = screen_width - 2 * BORDER_WIDTH

    x_increment = (usable_width - CARD_WIDTH) / (card_quantity - 1)

    return x_increment

def load_cards(): #loads all the card image files into the cards dict
    for colour in colours:
        for number in numbers:
            name = colour + number
            cards[name] = pygame.image.load(f"uno_cards\\{colour}{number}.png") #loads most of the cards
    cards["wild_wild"] = pygame.image.load("uno_cards/wild_wild.png")
    cards["wild_+4"] = pygame.image.load("uno_cards/wild_+4.png") #loads the two wild cards

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
    while True:
        discard.append(deck.pop()) #add first card to the discard pile to allow gameplay to start
        _ , number = discard[-1]
        if isinstance(number, int):
            break

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

def top_discard(): #gets the top card from the discard pile and turns it into the image object
    colour, number = discard[-1]
    card = colour + "_" +str(number)
    return cards[card]
#TODO get this function working
def detect_clicked_card(): #Detects which card the user clicks on and returns its index in the player.hand list
                           #Returns -1 if no card was clicked on
    CARD_WIDTH = 200
    BORDER_WIDTH = 50

    x_increment = calculate_x_increment()
    card_quantity = len(players[player_turn].hand)

    current_x = BORDER_WIDTH
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i in range(card_quantity):
        if current_x <= mouse_x < current_x + CARD_WIDTH:
            return i
        current_x += x_increment
    return -1

def turn():
    screen.fill("black")
    player_turn_text = font.render(f"Player {player_turn+1}'s turn", True, (255,255,255))
    screen.blit(player_turn_text, (0,0)) #Creats and displays the text showing the current player
    x = 50 #x coordinate for first card allowing 50px buffer
    y = 700 #y coordinate for all cards
    for card in players[player_turn].hand:
        to_blit_colour, to_blit_number = players[player_turn].hand[card]
        to_blit = to_blit_colour + "_" + str(to_blit_number)
        to_blit = cards[to_blit]
        screen.blit(to_blit, (x,y)) #displays all cards in the current player's hand
        x += calculate_x_increment() #calculates the increment for x with the number of cards in their hand
    screen.blit(card_back, (400, 300))
    screen.blit(top_discard(), (600, 300)) #displays the top card in the discard pile to allow players to know what they can place down.
    pygame.display.update()
    clock.tick(60)

def main(): #The main game rendering loop
    global player_turn
    create_game()
    running = True
    screen.fill("black")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update()
        clock.tick(60)
        turn()
        #TODO fix broken player counters
        if reverse:
            player_turn -= 1
        else:
            player_turn += 1

        if player_turn < 0: #checks to see if the player counter goes out of range and corrects if it does
            player_turn = len(players)
        elif player_turn > len(players):
            player_turn = 0

        sleep(3)
        card_hider()

if __name__ == "__main__": #Ctrl-C error handling and initialisation of the game
    try:
        load_cards()
        main()
    except KeyboardInterrupt:
        pass

pygame.quit() #Kills the pygame library
