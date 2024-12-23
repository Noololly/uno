import pygame
import random

class Player:
    def __init__(self, deck, player_number):
        self.hand = {}
        self.deal_hand(deck)
        self.player_number = player_number


    def deal_hand(self, deck):
        for i in range(7):
            card = deck.pop()
            self.hand[i] = card

pygame.init()

screen = pygame.display.set_mode((1080,500))
pygame.display.set_caption("UNO")
clock = pygame.time.Clock()
colours = ["red", "blue", "green", "yellow"]
numbers = ["_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9", "_skip", "_reverse", "_+2"]
players = []
deck = []
discard = []
player_turn = 0

def create_game(player_number):
    create_deck()
    for i in range(player_number):
        players.append(Player(deck, i))

def create_deck():
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


def end_of_deck():
    for card in discard:
        deck.append(card)
        discard.remove(card)
    random.shuffle(deck)


def main():
    players = 0
    while players < 2:
        players = int(input("Player number: "))
        if players < 2:
            print("You can't play alone, loner!")
    create_game(players)
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

pygame.quit()
