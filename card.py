#Card superclass
class Card:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description

    def __str__(self):
        return "{}\n=====\n{}\nCost: {}\n".format(self.name, self.description, self.cost)

    def __eq__(self, other):
        return self.name == other.name


#-----Card subclasses-----
class Action(Card):
    def __init__(self, name, cost, description, draw, action, money, buy):
        self.draw = draw
        self.action = action
        self. money = money
        self. buy = buy
        super().__init__(name, cost, description)

    #yes need player parameter here?
    def special(self, currentPlayer, playBoard):
        pass


class Victory(Card):
    def __init__(self, name, cost, description, points):
        self.points = points
        super().__init__(name, cost, description)


#Is this proper or best way to do this?????
class Curse(Card):
    def __init__(self):
        self.points = -1
        super().__init__(name = "Curse",
                         cost = 0,
                         description = "Curse card worth -1 VP")


class Treasure(Card):
    def __init__(self, name, cost, description, value):
        self.value = value
        super().__init__(name, cost, description)


#--------More specific subclasses--------
class Attack(Card):
    def attack(self):
        pass


class Reaction(Card):
    def reaction(self):
        pass


class Duration(Card):
    def duration(self):
        pass


class Prize(Card):
    #is this method even neccessary?
    def prize(self):
        pass


class Knight(Card):
    def knight(self):
        pass


class Reserve(Card):
    def reserve(self):
        pass


class Ruins(Card):
    def ruins(self):
        pass


class Event(Card):
    #this will definitely need def __init__

    def event(self):
        pass

'''------- BASIC SUPPLY ----'''


#Victory points
class Estate(Victory):
    def __init__(self):
        super().__init__(name = "Estate",
                         cost = 2,
                         description = "Victory card worth 1 VP",
                         points = 1)


class Duchy(Victory):
    def __init__(self):
        super().__init__(name = "Duchy",
                         cost = 5,
                         description = "Victory card worth 3 VP",
                         points = 3)


class Province(Victory):
    def __init__(self):
        super().__init__(name = "Province",
                         cost = 8,
                         description = "Victory card worth 6 VP",
                         points = 6)

#curses are their own subclass.


#Treasures
class Copper(Treasure):
    def __init__(self):
        super().__init__(name = "Copper",
                         cost = 0,
                         description = "Treasure card worth $1",
                         value = 1)


class Silver(Treasure):
    def __init__(self):
        super().__init__(name = "Silver",
                         cost = 3,
                         description = "Treasure card worth $2",
                         value = 2)


class Gold(Treasure):
    def __init__(self):
        super().__init__(name = "Gold",
                         cost = 6,
                         description = "Treasure card worth $3",
                         value = 3)

'''----------------------- CARDS BY SET --------------------'''

'''---BASE---'''

#Actions


class Cellar(Action):
    def __init__(self):
        super().__init__(name = "Cellar",
                         cost = 2,
                         description = "Action: +1 Actions, Discard any number of cards, + card for each card discarded",
                         draw = 0,
                         action = 1,
                         money = 0,
                         buy = 0)

    def special(self, currentPlayer, playBoard):
        numDiscarded = 0
        print('\nDiscard any number of cards:')
        currentPlayer.printHand()
        print('\nCommands: cardName, done.')
        while True:
            command = input('\n\tCommand? ')
            if command == 'done':
                break
            else:
                validPlay = False
                for i in currentPlayer.hand:
                    if command == i.name:
                        currentPlayer.discardCard(i)
                        numDiscarded += 1
                        validPlay = True
                        break
                if not validPlay:
                    print('Command not recognized, misspelled, or card is not in hand.')
        for i in range(numDiscarded):
            currentPlayer.drawCard()


class Chapel(Action):
    def __init__(self):
        super().__init__(name = "Chapel",
                         cost = 2,
                         description = "Action: Trash up to 4 cards from your hand",
                         draw = 0,
                         action = 0,
                         money = 0,
                         buy = 0)

    def special(self, currentPlayer, playBoard):
        numTrashed = 0
        print('\nTrash up to 4 cards from your hand:')
        currentPlayer.printHand()
        print('\nCommands: cardName, done.')
        while numTrashed < 4:
            command = input('\n\tCommand? ')
            if command == 'done':
                break
            else:
                validPlay = False
                for i in currentPlayer.hand:
                    if command == i.name:
                        currentPlayer.trashCard(i, playBoard)
                        numTrashed += 1
                        validPlay = True
                        break
                if not validPlay:
                    print('Command not recognized, misspelled, or card is not in hand.')


class Chancellor(Action):
    def __init__(self):
        super().__init__(name = "Chancellor",
                         cost = 3,
                         description = "Action: +$2, you may put your deck into your discard pile.",
                         draw = 0,
                         action = 0,
                         money = 2,
                         buy = 0)

    def special(self, currentPlayer, playBoard):
        print('\nDo you want to discard your deck?')
        command = input('\n(y\\n)?')
        if command == 'y':
            for i in range(len(currentPlayer.deck)):
                currentPlayer.discard.append(currentPlayer.deck.pop(0))
            print('You put your deck in your discard pile.')


class Festival(Action):
    def __init__(self):
        super().__init__(name = "Festival",
                         cost = 5,
                         description = "Action: +2 Actions, +1 Buy, +$2",
                         draw = 0,
                         action = 2,
                         money = 2,
                         buy = 1)


class Laboratory(Action):
    def __init__(self):
        super().__init__(name = "Laboratory",
                         cost = 5,
                         description = "Action: +2 Cards, +1 Action",
                         draw = 2,
                         action = 1,
                         money = 0,
                         buy = 0)


class Market(Action):
    def __init__(self):
        super().__init__(name = "Market",
                         cost = 5,
                         description = "Action: +1 Card, +1 Action, +1 Buy, +$1",
                         draw = 1,
                         action = 1,
                         money = 1,
                         buy = 1)


class Moat(Action, Reaction):
    def __init__(self):
        super().__init__(name = "Moat",
                         cost = 2,
                         description = "Action: +2 cards | Reaction: When another player plays an attack card, you may"
                                       " reveal this from your hand.  If you do your are unnaffected by the attack",
                         draw = 2,
                         action = 0,
                         money = 0,
                         buy = 0)

    def reaction(self, event, player):
        if event == 0:
            print("\n{} would you like to reveal {}?").format(player.name, self.name)
            command = input("\ny/n")
            while True:
                if command == 'y':
                    print("\n{} reveals a {}?").format(player.name, self.name)
                    player.immune = True
                    break
                elif command == 'n':
                    break
                else:
                    print('\nCommand misspelled or unrecognized.')


class Moneylender(Action):
    def __init__(self):
        super().__init__(name = "Moneylender",
                         cost = 4,
                         description = 'Action: Trash a copper from your hand.  If you do +$3',
                         draw = 0,
                         action = 0,
                         money = 0,
                         buy = 0)

    #place holder needs special() METHOD.


class Smithy(Action):
    def __init__(self):
        super().__init__(name = "Smithy",
                         cost = 4,
                         description = "Action: +3 Cards",
                         draw = 3,
                         action = 0,
                         money = 0,
                         buy = 0)


class Village(Action):
    def __init__(self):
        super().__init__(name = "Village",
                         cost = 3,
                         description = "Action: +1 Card, +2 Ations",
                         draw = 1,
                         action = 2,
                         money = 0,
                         buy = 0)



class Woodcutter(Action):
    def __init__(self):
        super().__init__(name = "Woodcutter",
                         cost = 3,
                         description = "Action: +1 Buy, +$2",
                         draw = 0,
                         action = 0,
                         money = 2,
                         buy = 1)


class Workshop(Action):
    def __init__(self):
        super().__init__(name = 'Workshop',
                         cost = 3,
                         description = "Action: Gain a card costing up to $4.",
                         draw = 0,
                         action = 0,
                         money = 0,
                         buy = 0)

    def special(self, currentPlayer, playBoard):
        print("Gain a card costing up to $4")


class Witch(Action, Attack):
    def __init__(self):
        super().__init__(name = 'Witch',
                         cost = 5,
                         description = "Action: +2 cards.  Each other player gains a curse card.",
                         draw = 2,
                         action = 0,
                         money = 0,
                         buy = 0)

    def attack(self, events, players, currentPlayer, playBoard):
        events.notify(0)
        playerIndex = 0
        for i in range(len(players)):
            player = players[i]
            if player.name == currentPlayer.name:
                playerIndex = i

        for i in range(playerIndex + 1, len(players)):
            player = players[i]
            if not player.immune:
                for pile in playBoard:
                    if isinstance(pile.card, Curse) and not pile.isEmpty():
                        player.discard.append(pile.card)
                        pile.amount -= 1

        for i in range(playerIndex):
            player = players[i]
            if not player.immune:
                for pile in playBoard:
                    if isinstance(pile.card, Curse) and not pile.isEmpty():
                        player.discard.append(pile.card)
                        pile.amount -= 1
