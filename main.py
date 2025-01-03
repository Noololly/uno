import os
import sys
from time import sleep
import pygame
import random

#Initialise EVERYTHING
pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("UNO")

clock = pygame.time.Clock()
screen.fill("black")
colours = ["red", "blue", "green", "yellow"]
numbers = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9", "_skip", "_reverse", "_+2"]  #lists of the colours and numbers of the cards

"""
Global Variables:
"""
cards = {}  #a dict to store all instances of the card images
players = []  #list of instances of players
deck = []  #list of cards in the draw pile
discard = []  #list of cards in the discard pile
player_turn = 0  #Number of player whose turn it currently is
reverse = False  #bool storing direction of play
WILD = "wild"
PLUS_FOUR = "+4"
DISCARD_POSITION = (600, 300)
DRAW_POSITION = (400, 300)
DRAW_RECT = pygame.Rect(DRAW_POSITION[0], DRAW_POSITION[1], 200, 300)  #rect for the draw pile to allow users to draw more cards if they cannot play
STATUS_TEXT_RECT = pygame.Rect(0, 50, 100, 34)  #Rectangle to place the status text

card_back = pygame.image.load("back.png")  #loads the card back

font = pygame.font.Font(None, 32)  #loads the font


class Player:  #Player class
    def __init__(self, deck, player_number):
        self.hand = []
        self.deal_hand(deck)
        self.player_number = player_number

    def deal_hand(self, deck):  #Deals the player's hand
        for i in range(7):  #number of cards dealt at the start of an uno game
            card = deck.pop()
            self.hand.append(card)


def restart_program():
    """Restarts the program to allow users to play again."""
    python = sys.executable
    os.execl(python, python, *sys.argv)


def calculate_x_increment():
    """Calculates the amount to increment x by for each card in the player's hand."""
    card_quantity = len(players[player_turn].hand)
    screen_width = pygame.display.get_window_size()[0]

    # Constants
    CARD_WIDTH = 200  # Width of each card
    BORDER_WIDTH = 50  # Left and right borders

    # Calculate usable width
    usable_width = screen_width - 2 * BORDER_WIDTH
    if card_quantity > 1:
        return (usable_width - CARD_WIDTH) / (card_quantity - 1)
    else:
        return 50


def load_cards():
    """loads all the card image files into the cards dict"""
    for colour in colours:
        for number in numbers:
            name = colour + number
            cards[name] = pygame.image.load(f"uno_cards\\{colour}{number}.png")  #loads most of the cards
    cards["wild_wild"] = pygame.image.load("uno_cards/wild_wild.png")
    cards["wild_+4"] = pygame.image.load("uno_cards/wild_+4.png")  #loads the two wild cards


def create_game():
    """Function to create the game and display a nice GUI to enter the number of players"""
    input_rect = pygame.Rect(400, 250, 250, 35)
    user_text = ""
    player_number = 0
    while not player_number:  #Render player number selection
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
        instruction_text = font.render("Enter the number of players:", True, (255, 255, 255))
        screen.blit(instruction_text, (user_instruction_rect.x, user_instruction_rect.y))

        pygame.draw.rect(screen, "white", input_rect)

        text_surface = font.render(user_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()
        clock.tick(60)

    create_deck()  #Make the deck to draw from
    for i in range(player_number):
        players.append(
            Player(deck, i))  #Create the players. Gives each player a number in which order of turn they will be in


def create_deck():
    """Makes the deck with all the appropriate cards"""
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
        for j in range(1, 10):
            deck.append((colour, j))
    random.shuffle(deck)
    while True:
        discard.append(deck.pop())  #add first card to the discard pile to allow gameplay to start
        _, number = discard[-1]
        if isinstance(number, int):
            break


def end_of_deck():
    """If all the cards in the deck have been used, take all the cards in the discard pile and shuffle"""
    status_text = font.render("All cards in the deck have been used. Shuffling discard pile", True, (255, 255, 255))
    screen.blit(status_text, (STATUS_TEXT_RECT.x, STATUS_TEXT_RECT.y))
    pygame.display.flip()
    sleep(3)
    for card in discard:
        deck.append(card)
        discard.remove(card)
    random.shuffle(deck)


def card_hider():
    """A function to blank the screen to hide a player's cards from other players when passing the device around"""
    button = pygame.Rect(350, 440, 360, 30)
    player_turn_rect = pygame.Rect(350, 10, 360, 30)
    hidden = True
    while hidden:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(
                        event.pos):  #Detects if the button is pushed to start the turn of the next player
                    hidden = False

        screen.fill("black")

        player_turn_text = font.render(f"It is player {player_turn + 1}'s turn", True, (255, 255, 255))
        screen.blit(player_turn_text, (player_turn_rect.x, player_turn_rect.y))

        pygame.draw.rect(screen, "white", button)
        above_button_text = font.render("Click to start the next player's turn", True, (255, 255, 255))
        screen.blit(above_button_text, (button.x, button.y - 40))

        button_text = font.render("Next Player!", True, (0, 0, 0))
        screen.blit(button_text, ((button.x + (button.w - 250)), button.y + 5))

        pygame.display.flip()
        clock.tick(60)
    return


def top_discard():
    """gets the top card from the discard pile and turns it into the image object"""
    colour, number = discard[-1]
    card = colour + "_" + str(number)
    return cards[card]


def detect_clicked_card():
    """Detects which card the user clicks on and returns its index in the player.hand list
    #Returns -1 if no card was clicked on"""
    CARD_WIDTH = 200
    BORDER_WIDTH = 50

    x_increment = calculate_x_increment()
    card_quantity = len(players[player_turn].hand)

    mouse_x, _ = pygame.mouse.get_pos()

    for i in range(card_quantity - 1, -1, -1):
        card_x_start = BORDER_WIDTH + i * x_increment
        card_x_end = card_x_start + CARD_WIDTH

        if card_x_start <= mouse_x < card_x_end:
            return i


def update_discard(card_colour, card_number):
    """updates top card of the discard pile"""
    discard.append((card_colour, card_number))


def render_discard():
    """renders top card of the discard pile"""
    discard_card = top_discard()
    screen.blit(discard_card, DISCARD_POSITION)
    pygame.display.update()
    clock.tick(60)


def is_card_placeable(card_colour, card_number):
    """checks if card is placeable"""
    top_card_colour, top_card_number = discard[-1]
    return (
            card_colour == WILD or
            top_card_colour == card_colour or
            top_card_number == card_number or
            top_card_colour == WILD
    )


def check_placeable(card_colour,
                    card_number):
    """calls is_card_placeable, if it is, then the discard pile is rendered again with the placed card on top"""
    if is_card_placeable(card_colour, card_number):
        update_discard(card_colour, card_number)
        render_discard()
        return True
    else:
        return False


def turn():
    """The main gameplay loop"""
    screen.fill("black")
    player_turn_text = font.render(f"Player {player_turn + 1}'s turn", True, (255, 255, 255))
    screen.blit(player_turn_text, (0, 0))  #Creats and displays the text showing the current player
    x = 50  #x coordinate for first card allowing 50px buffer
    y = 700  #y coordinate for all cards
    for index, card in enumerate(players[player_turn].hand):
        to_blit_colour, to_blit_number = card
        to_blit = to_blit_colour + "_" + str(to_blit_number)
        to_blit = cards[to_blit]
        screen.blit(to_blit, (x, y))  #displays all cards in the current player's hand
        x += calculate_x_increment()  #calculates the increment for x with the number of cards in their hand

    #Render draw and discard pile
    screen.blit(card_back, (400, 300))
    screen.blit(top_discard(), (
        600, 300))  #displays the top card in the discard pile to allow players to know what they can place down.
    pygame.display.update()
    clock.tick(60)
    taking_turn = True
    while taking_turn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    if pos_y > 700:
                        card_index = detect_clicked_card()
                        if card_index is not None:
                            card_colour, card_number = players[player_turn].hand[card_index]
                            if check_placeable(card_colour, card_number):
                                players[player_turn].hand.pop(card_index)
                                taking_turn = False
                    elif DRAW_RECT.collidepoint(pos_x, pos_y):
                        if len(deck) > 0:
                            card = deck.pop()
                            players[player_turn].hand.append(card)
                            render_discard()
                            taking_turn = False
                        else:
                            end_of_deck()
                            render_discard()


def main():
    """Main program loop"""
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
        if not players[player_turn].hand:
            win(player_turn)
        #Adjusts player_turn based on direction of play
        if reverse:
            player_turn = (player_turn - 1) % len(
                players)  #the mod handles the wrap around to allow the players to go around in a circle like in a normal game
        else:
            player_turn = (player_turn + 1) % len(players)

        if player_turn < 0:  #checks to see if the player counter goes out of range and corrects if it does
            player_turn = len(players) - 1
        elif player_turn > len(players):
            player_turn = 0
        if len(deck) <= 1:
            end_of_deck()
        card_hider()


def win(player):
    """Screen at the end of the game to allow players to play again or quit."""
    play_again_button_rect = pygame.Rect(350, 440, 360, 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button_rect.collidepoint(event.pos):
                    restart_program()
        screen.fill("black")
        play_again_text = font.render("Play Again?", True, (255, 255, 255))
        screen.blit(play_again_text, play_again_button_rect)
        status_text = font.render(f"Player {player + 1} wins!", True, (255, 255, 255))
        screen.blit(status_text, STATUS_TEXT_RECT)
        pygame.display.flip()



if __name__ == "__main__":  #Ctrl-C error handling and initialisation of the game
    try:
        load_cards()
        main()
    except KeyboardInterrupt:
        pass

pygame.quit()  #Kills the pygame library
