import random
import card
import handler


class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.discard = []
        self.inPlay = []
        self.action = 1
        self.money = 0
        self.buy = 1
        self.immune = False

    def __str__(self):
        return "{}\n=========\nDeck: {}".format(self.name, self.deck)

    def __eq__(self, other):
        return self.name == other.name

    def shuffleDeck(self):
        random.shuffle(self.deck)
        print('\t{} shuffles their library.\n'.format(self.name))

    def drawHand(self, events):
        for i in range(5):
            self.drawCard(events)

    def drawCard(self, events):
        if len(self.deck) == 0:
            for i in range(len(self.discard)):
                self.deck.append(self.discard.pop(-1))
            self.shuffleDeck()
        self.hand.append(self.deck.pop(0))
        if isinstance(self.hand[-1], card.Reaction):
            events.subscribers.append(self.react)
        print('\n\t{} draws {}.'.format(self.name, self.hand[-1].name))

    # pass in players so we can check for reaction cards?
    def playCard(self, events, players, cardChoice, playBoard):
        if isinstance(cardChoice, card.Action):
            print('\n' + self.name + ' plays a ' + cardChoice.name + '...')
            for j in range(cardChoice.draw):
                self.drawCard()
            self.action = self.action - 1 + cardChoice.action
            self.buy += cardChoice.buy
            self.money += cardChoice.money
            print('\n\t...receiving...\n\t+' +
                  str(cardChoice.action) + ' action(s)\n\t+' + str(cardChoice.buy) + ' buy(s)\n\t+$' +
                  str(cardChoice.money))
            # is this the best place to put the card into play?
            self.inPlay.append(cardChoice)
            self.hand.remove(cardChoice)
            self.inPlay[-1].special(self, playBoard)
            if isinstance(cardChoice, card.Attack):
                self.inPlay[-1].attack(events, players, self, playBoard)
        elif isinstance(cardChoice, card.Treasure):
            self.money += cardChoice.value
            print('\n' + self.name + ' plays a ' + cardChoice.name + ' receiving +$' + str(cardChoice.value) +
                  '.')
            self.inPlay.append(cardChoice)
            self.hand.remove(cardChoice)

    def gainCard(self, pile):
        if not pile.isEmpty():
            self.discard.append(pile.card)
            pile.amount -= 1
            print('\n' + self.name + ' gains a ' + pile.card.name + '.')
        else:
            print('\n' + self.name + ' gains nothing because the pile is empty.')

    def discardCard(self, playCard):
        print('\n' + self.name + ' discards a ' + playCard.name)
        self.discard.append(playCard)
        self.hand.remove(playCard)

    def trashCard(self, playCard, playBoard):
        playBoard.trash.append(playCard)
        self.hand.remove(playCard)
        print('\n' + self.name + ' trashes ' + playBoard.trash[-1])

    def printHand(self):
        print('\nYour hand: ')
        for card in self.hand:
            print(card.name + ', ')

    def react(self, event, events):
        events.subscirbers.remove(self)
        for choice in self.hand:
            if isinstance(choice, card.Reaction):
                choice.reaction(event, self)
