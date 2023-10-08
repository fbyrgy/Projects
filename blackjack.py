import random

class Card():
    #class that holds the data for each card in the deck
    def __init__(self,suit,rank,faceDown = False):
        self.suit = suit
        self.rank = rank
        self.faceDown = faceDown
        
    def getValue(self):
        #determines the value of each card in the deck
        if self.faceDown:
            return 0
        elif self.rank == "A":
            return 11
        elif self.rank.isalpha():
            return 10
        return int(self.rank)

    def __repr__(self):
        #returns propper string formatting for the card
        if self.faceDown:
            return "face down card"
        elif self.rank.isalpha():
            if self.rank == "A":
                return f"Ace of {self.suit}"
            if self.rank == "J":
                return f"Jack of {self.suit}"
            if self.rank == "Q":
                return f"Queen of {self.suit}"
            if self.rank == "K":
                return f"King of {self.suit}"
        else:
            return f"{self.rank} of {self.suit}"

    def flipCard(self):
        #function makes the cards visibile/invisible to the player
        self.faceDown = not self.faceDown


class Deck():
    #class that deals with the deck

    def __init__(self):
        self.cards = self.generateDeck()

    def generateDeck(self):
        #generates the deck with suits and ranks
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        cards = []
        for suit in suits:
            for rank in ranks:
                cards.append(Card(suit,rank))
        
        return cards


    def dealCard(self):
        #deals a random card from the deck
        return self.cards.pop(random.randint(0,len(self.cards)-1))

class Player():
    #class that holds the player's data
    def __init__(self,name):
        self.hand = []
        self.name = name
        self.account = 0

    def handValue(self):
        #determines the value of each hand
        count = 0
        aces = 0
        """
        This method gets the value of a hand with aces in it. It works by first taking note of
        how many aces are in the hand, and then giving them a value which is dependant on the hand value.
        If the hand value would be above 21 if the ace is valued at 11, its value is then changed to 1.
        """
        for card in self.hand:
            count += card.getValue()
            if card.getValue() == 11:
                aces += 1
        while count > 21 and aces > 0:
            count -= 10
            aces -= 1
        return count

    def addCard(self,card,faceDown = False):
        #adds a card to the hand
        if faceDown:
            card.flipCard()
        self.hand.append(card)
        
        print(f"Dealer dealt a {card} to {self.name}\n")
        

    def showHand(self):
        #prints out the player's hand
        return self.hand
            

    def deposit(self):
        #function that deals with the users initial deposit and handles storing it in a file
        """
        This method determines if a file with the given name already exsists, and if it does prompts the user
        to either add more money or continue with their balance from previous games
        """
        try:
            with open(f"{self.name}_account_balance.txt","r") as file:
                self.account = float(file.read())
                print(f"Welcome back {self.name}, your current account balance is {self.account}.")
                if input("Would you like to deposit more money (y/n)?\n").lower() not in ["yes","y"]:
                    return

        except:
            pass         
                

        """
        This method will run either if the already existing user wants to deposit money, or if someone is
        playing for the first time
        """
        while True:
            deposit = input(f"How much money would you like to deposit, {self.name}? (You will use this money to bet on hands)\n")
            if not deposit.isnumeric() or float(deposit) < 0:
                print("Please input a valid number")
                continue
            break
        
        
        self.updateAccount(round(float(deposit),2))

       
            
                
    def getBalance(self):
        #function that returns the player's balance
        return self.account

    def updateAccount(self,delta):
        #function that updates the account with the "delta," which is how much they won or lost
        self.account += delta

        #updating the file with the change in balance 
        with open (f"{self.name}_account_balance.txt","w") as file:
            file.write(str(self.account))

    def getName(self):
        #function that returns the player's name
        return self.name

     
    def resetHand(self):
        #resets the player's hand to empty
        self.hand = []
        
class Game():
    #class that deals with the game logic

    def __init__(self):
        #creating the deck of cards
        self.deck = Deck()
        #asking the user for their name
        name = input("What is your name?\n")
        self.player = Player(name)
        #initializing the dealer by calling them "themselves"
        self.dealer = Player('themselves')
        self.player.deposit()
        

    def startingHand(self):
        #function that deals out the starting hand to the dealer and the player
        self.player.addCard(self.deck.dealCard())
        self.dealer.addCard(self.deck.dealCard())
        
        self.player.addCard(self.deck.dealCard())
        #this card must be added "face down" because, the player is not allowed to see the dealer's second card
        self.dealer.addCard(self.deck.dealCard(),True)
        

    def findWinners(self,bet):
        #function that determines the player's payout relative to their bet
        payout = self.getPayout()
        #updating the account with their payout
        self.player.updateAccount(round(payout * bet,2))
        if self.getPayout() == 0:
            print("You pushed. You won no money")
            
        elif self.getPayout() == -1:
            print(f"You lost ${bet}")
            
        elif self.getPayout() == 1:
            print(f"You won ${bet}!")
                  
        else:
            print(f"Blackjack! You won ${round(payout * bet,2)}")
            
        print(f"{self.player.getName()}'s current account balance is ${self.player.getBalance()}")    

        
                
    def showHands(self):
        #prints the card and value of each person's hand
        
        
        print(f"{self.player.getName()}'s cards are {self.player.showHand()} and their hand value is {self.player.handValue()}\n")
        
        
        print(f"Dealer is showing a {self.dealer.showHand()}, with a value of {self.dealer.handValue()}\n")

    def dealerDrawing(self):
        #sets the rules for when a dealer can draw a card
        """
        The dealer must stand on a soft 17 and does not draw cards if the player's hand value has already
        exceeded the dealer's starting hand.
        """
        while self.dealer.handValue() < 17 and self.dealer.handValue() < self.player.handValue() and self.player.handValue() < 22:
            self.dealer.addCard(self.deck.dealCard())
        
    def getPayout(self):
        #determines the payout that the player should receive relative to their bet
        player = self.player.handValue()
        dealer = self.dealer.handValue()
        #logic that determines how much money the player has won or lost by analyzing the hand values
        if player == 21 and dealer != 21:
            #you get a 3/2 return on your bet if you get a blackjack
            return 3/2
        elif player == dealer:
            return 0
        elif player > 21:
            return -1
        elif player > dealer:
            return 1
        elif player < dealer and dealer < 22:
            return -1
        elif player < dealer and dealer > 21:
            return 1

    def hit(self):
        #adds a card to the player's hand
        self.player.addCard(self.deck.dealCard())

    def resetGame(self):
        #resets the deck and hands, should the player choose to play again
        self.player.resetHand()
        self.dealer.resetHand()
        self.deck = Deck()

    def playGame(self):
        #main game logic

        #resets game to ensure every game is starting on a blank slate
        self.resetGame()

        #asking for the user's bet on the hand. The logic ensures that the player's bet is within their account limits
        while True:
            bet = input("How much would you like to bet?\n")
            if not bet.isnumeric():
                print("Please input a valid bet\n")
                continue
            bet = float(bet)    
            if bet > self.player.getBalance():
                print("Your bet is greater than your account balance. Please choose a smaller bet\n")
                continue
            elif bet == 0:
                print("Please choose a greater bet ammount\n")
                continue
            break
            
        #dealing the starting hand and showing the hands to the table
        self.startingHand()
        self.showHands()

        """
        If the dealer's face up card is an ace, or has a value of 10, they must check
        their other card to see if they have a blackjack. If the dealer gets a blackjack
        the game is over, and the player is not allowed to get more cards. If it is not a blackjack,
        the game continues as normal, but the player is still not allowed to be privy of the face down
        card yet. This works by "flipping" the card to obtain its value, and then flipping it back over
        to ensure that its value is not printed.
        """
        if self.dealer.handValue() == 10 or self.dealer.handValue() == 11:

            self.dealer.showHand()[1].flipCard()
            if self.dealer.handValue() != 21:
                print("Dealer is checking their other card and it is not a blackjack\n")

            else:
                print("Dealer is checking their other card and it is a blackjack\n")
                self.findWinners(bet)   
                return  
            self.dealer.showHand()[1].flipCard()

        
        
        
        #sets the conditions for when the player is asked what they would like to do. They cannot do anything if they have gone bust
        while self.player.handValue() < 21:
            """
            The first time the player gets asked for their input, there is an option to double down.
            The question is only asked if the player has 2 cards in their hand, ensuring it only gets
            asked the first time. The player must also have enough money in their account to double their bet.
            """
            
            if len(self.player.showHand()) == 2 and 2 * bet <= self.player.getBalance():
                questionString = "What would you like to do?\nType '1' to hit\nType '2' to stand\nType '3' to double down\n"
                validAnswers = ['1','2','3']

            #if the above criteria is not met, this statement runs only allowing the player to hit or stand
            else:
                questionString = "What would you like to do?\nType '1' to hit\nType '2' to stand\n"
                validAnswers = ['1','2']

            #deals with error handling the user's input
            question = input(questionString)
            if question not in validAnswers:
                print("That is not a valid response. Please enter a valid response")
                continue
                      
            if question == "1":
                #adds a card to the player's hand and then shows the table their new card
                self.hit()
                self.showHands()

            elif question == "2":
                #there is nothing left to be done when the player chooses to stand
                break

            elif question == "3":
                """
                When doubling down you are only allowed to get one card.
                Your bet is doubled, and your new hand is printed out.
                """
                self.hit()
                self.showHands()
                bet *= 2
                break
                
        #if you go bust the game is over and findWinners() is called which updates your account
        if self.player.handValue() > 21:
            print("You went bust\n")
            self.findWinners(bet)
            return

        #dealer flips over their other card, allowing the table to see it
        self.dealer.showHand()[1].flipCard()
        #dealer begins their process of drawing which does not require any player input, as it is based on method
        self.dealerDrawing()
        #dealer shows their hand to the table
        self.showHands()
        #findWinners() is called which determines how much the player won or lost
        self.findWinners(bet)

        
#calling the class, starting the game loop        
startGame = Game()
#asks the player if they want to play again
while True:
    startGame.playGame()
    playAgain = input ("Do you want to play again? (y/n)\n").lower()
    if playAgain == "y" or playAgain == "yes":
        continue
    break

        


