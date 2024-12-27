import sys

import pygame
import random



class Player: #Player class
    def __init__(self, deck, player_number):
        self.hand = {}
        self.deal_hand(deck)
        self.player_number = player_number


    def deal_hand(self, deck):
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
player_turn = 0

card_back = pygame.image.load("back.png")


def create_game(): #Function to create the game and display a nice GUI to enter the number of players
    input_rect = pygame.Rect(400, 250, 250, 35)
    user_text = ""
    font = pygame.font.Font(None, 32)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        user_instruction_rect = pygame.Rect(400, 215, 250, 35)
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

def turn():
    for player in players:
        print(player.hand)


def end_of_deck(): #If all the cards in the deck have been used, take all the cards in the discard pile and shuffle
    for card in discard:
        deck.append(card)
        discard.remove(card)
    random.shuffle(deck)


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

        screen.blit(card_back, (0,0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__": #Ctrl-C error handling and initialisation of the game
    try:
        main()
    except KeyboardInterrupt:
        pass

pygame.quit() #Kills the pygame library
