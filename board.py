import random
import card

#what is the difference between class.object vs class.object()?
kingdomCards = [
                #Base
                    #Actions
                    card.Cellar(), card.Chapel(), card.Chancellor(), card.Festival(), card.Laboratory(), card.Market(),
                    card.Moat(), card.Moneylender(), card.Smithy(), card.Village(), card.Witch(), card.Woodcutter(),
                    card.Workshop()

                ]


class Board:
    def __init__(self, players):
        self.supply = []
        self.trash = []
        self.players = players

    def makeKingdom(self):

        #generate 10 kingdom cards
        x = 0
        while x < 10:
            addCard = kingdomCards[random.randint(0, len(kingdomCards) - 1)]
            if len(self.supply) == 0:
                self.supply.append(Pile(addCard, 10))
            else:
                canAdd = True
                for i in range(len(self.supply)):
                    if self.supply[i].card == addCard:
                        canAdd = False
                if canAdd:
                    self.supply.append(Pile(addCard, 10))
                else:
                    x -= 1
            x += 1

        #fill the estates and duchies
        vp = 8
        if self.players > 2:
            vp = 12

        self.supply.append(Pile(card.Estate(), vp))
        self.supply.append(Pile(card.Duchy(), vp))

        #fill provinces for 5 and 6 player games
        if self.players == 4:
            vp = 15
        if self.players > 4:
            vp = 18
        self.supply.append(Pile(card.Province(), vp))

        #fill curses
        self.supply.append(Pile(card.Curse(), (self.players - 1) * 10))

        #fill money
        self.supply.append(Pile(card.Copper(), 60 - 7 * self.players))
        self.supply.append(Pile(card.Silver(), 40))
        self.supply.append(Pile(card.Gold(), 30))


class Pile():
    def __init__(self, card, amount):
        self.card = card
        self.amount = amount

    def isEmpty(self):
        if self.amount <= 0:
            return True
        else:
            return False