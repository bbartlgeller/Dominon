import card
import handler
import random
import player
import board

def play():
    #Initiate game

    events = handler.Handler()

    print("---Dominion---\n")
    players = setupPlayers()
    while True:

        #setup this game instance
        playboard = board.Board(len(players))
        playboard.makeKingdom()
        random.shuffle(players)

        for i in range(len(players)):
            dude = players[i]
            dude.shuffleDeck()
            dude.drawHand(events)

        '''for dude in players:
            dude.shuffleDeck()
            #dude.drawHand(events)

        for dude in players:
            print(dude.deck)'''

        turn = 0
        gameOver = False #this variable is actually not necessary.

        #start gameplay
        while not gameOver:
            turn += 1
            print('_______Turn ' + str(turn) + '_______')
            for player in players:
                #os.system('clear')
                print('----{}\'s turn!----\n'.format(player.name))
                print('\nSupply: ')
                for pile in playboard.supply:
                    print(pile.card.name + ' (' + str(pile.amount) + '), ')

                #action phase
                print("\n-ACTION PHASE-")
                while player.action > 0:
                    print('\nActions: ' + str(player.action) + '. Buys: ' + str(player.buy) + '. Money: ' +
                          str(player.money) + '.')
                    print('\nYour hand: ')
                    for cardchoice in player.hand:
                        print(cardchoice.name + ', ')
                    print('\nCommands: actionName, endPhase')
                    command = input('\nCommand? ')
                    if command == 'endPhase':
                        break
                    else:
                        validPlay = False
                        for cardChoice in player.hand:
                            if command == cardChoice.name and isinstance(cardChoice, card.Action):
                                player.playCard(events, cardChoice, playboard)
                                validPlay = True
                                break
                        if not validPlay:
                            print('Command not recognized, misspelled, or card is not in hand.')

                #buy phase part 1
                print('\n-BUY PHASE-')
                print('\nBuys: ' + str(player.buy) + '. Money: $' + str(player.money) + '.')
                while True:
                    print('\nYour hand: ')
                    for cardChoice in player.hand:
                        print(cardChoice.name + ', ')
                    print('\nCommands: treasureName, playAll, buy')
                    command = input('\nPlay treasures. ')
                    if command == 'buy':
                        break
                    elif command == 'playAll':
                        print('\nYou play all your treasures:')

                        for i in range(len(player.hand) - 1, -1, -1):
                            cardChoice = player.hand[i]
                            if isinstance(cardChoice, card.Treasure):
                                player.playCard(events, players, cardChoice, playboard)

                        '''
                        OLD CODE THAT USES INDICES
                        handIndices = list(range(len(players[i].hand))).reverse()
                        for j in handIndices:
                            if isinstance(players[i].hand[0], card.Treasure):
                                players[i].playCard(events, j, playboard)
                            else:
                                players[i].hand.append(players[i].hand.pop(1))'''
                    else:
                        validPlay = False
                        for cardChoice in player.hand:
                            if command == cardChoice.name and isinstance(cardChoice, card.Treasure):
                                player.playCard(events, players, cardChoice, playboard)
                                validPlay = True
                                break
                        if not validPlay:
                            print('Command not recognized, misspelled, or card is not in hand.')

                #buy phase part 2
                print('\nBuy cards.')
                while True:
                    if player.buy > 0:
                        print('\nBuys: ' + str(player.buy) + '. Money: $' + str(player.money) + '.')
                        print('\nSupply:')
                        for pile in playboard.supply:
                            print('\n\t' + pile.card.name + ' (' + str(pile.amount) + ')')
                        print('\nCommands: supplyCard, endPhase')
                        command = input('\nCommand? ')
                        if command == 'endPhase':
                            break
                        else:
                            validPlay = False
                            for pile in playboard.supply:
                                if command == pile.card.name and not pile.isEmpty() and player.money >= pile.card.cost:
                                    players[i].gainCard(pile)
                                    players[i].buy -= 1
                                    validPlay = True
                                    break
                            if not validPlay:
                                print('Command not recognized, misspelled, not enough money, or card is not in supply/ empty pile.')
                    else:
                        print('\nNo more buys.')
                        break

                #Clean-up phase
                player.action = 1
                player.money = 0
                player.buy = 1
                for i in range(len(player.hand) - 1, -1, -1):
                    cardChoice = player.hand[i]
                    player.discardCard(cardChoice)
                for j in range(len(players[i].inPlay)):
                    player.discard.append(player.inPlay.pop(-1))
                player.drawHand(events)

                #Is the game over?
                pileCounter = 0
                if playboard.supply[12].isEmpty():
                    gameOver = True
                for pile in playboard.supply:
                    if pile.isEmpty():
                        pileCounter += 1
                if pileCounter >= 3:
                    gameOver = True

                if gameOver:
                    break

        #Post Game Report
        print('\n------GAME OVER!------')

        #Count VP and determine a winner!

        #Play again?
        command = input('\nPlay again? (y/n)')
        if command == 'y':
            pass
        elif command == 'n':
            break
        else:
            print('\nCommand unrecognized you are playing again, buddy')
            #find a way to actually not recognize the command

def setupPlayers():
    players = []
    deck = []
    for x in range(7):
        deck.append(card.Copper())
    for x in range(3):
        deck.append(card.Estate())
    numPlayers = input('Number of players? ')
    for i in range(int(numPlayers)):
        playerName = input("Player {} name? ".format(i+1))
        players.append(player.Player(playerName, deck))
    return players

if __name__ == "__main__":
    play()
