class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
    self.isHidden = False
  
  #Flip this card face-down hiding it from one or more players
  def flip(self):
    self.isHidden = not self.isHidden

  def printCard(self):
    if self.isHidden:
      print("??")
    else:
      print(self.toString())

  def toString(self):
    val = self.value
    if val == 1:
      val = "A"
    elif val == 11:
      val = "J"
    elif val == 12:
      val = "Q"
    elif val == 13:
      val = "K"
    else:
      val = (str)(val)
    return val + self.suit

  '''
  * @param c: The card we are comparing to 'self'
  * @return: 1 if self > c, -1 if c > self, 0 if self = c
  * Take 2 cards and evaluate which is a higher card
  '''
  def compareTo(self, c):
    if c.type != Card:
      raise ValueError("The passed object is not a card")
    elif c.getValue > self.getValue():
      return -1
    elif c.getValue < self.getValue():
      return 1
    else: 
      return 0
      
class Deck:
  DEBUG = False
  def __init__(self):
    self.deck = []
    self.size = 52
    self.isEmpty = False
    self.fillDeck()

  '''
  def __init__(self, size):
    self.deck = []
    self.size = size
    self.isEmpty = False
    self.fillDeck()
  '''

  '''
  * Start with a blank deck
  * Fill the deck and place it in new deck order
  '''
  def fillDeck(self):
    self.isEmpty = False
    self.size = 52
    suits = ["H", "C", "D", "S"]
    values = 13
    deck = []
    for s in suits:
      if s == "H" or s == "C":
        for v in range(1, values+1):
          c = Card(v, s)
          deck.append(c)
      else:
        for v in range (values,0, -1):
          c = Card(v, s)
          deck.append(c)
    self.deck = deck
  #End fillDeck

  def shuffle(self):
    self.deck = self.randMerge(self.deck)
  
  '''
  * Much like a regular merge sort, 
  * break down the problem as much as possible using recursion.
  * On the way up, however, use random numbers to choose sorting,
  * rather than using compareTo() or similar
  '''
  def randMerge(self, d):
    if len(d) <= 1:
      return d
    left = self.randMerge(d[:len(d)//2])
    if self.DEBUG:
      print("Left")
      print(left)
    right = self.randMerge(d[(len(d)//2):])
    if self.DEBUG:
      print("Right")
      print(right)
    mixedDeck = []
    while len(left) > 0 and len(right) > 0:
      which = random.randint(1,3)
      if which == 1:
        mixedDeck.append(left.pop(0))
      else:
        mixedDeck.append(right.pop(0))
    if self.DEBUG:
      print("Halfway through, one stack left")
    if len(right) == 0:
      if self.DEBUG:
        print("Adding left stack")
      for c in left:
        mixedDeck.append(c)
    else:
      if self.DEBUG:
        print("Adding right stack")
      for c in right:
        mixedDeck.append(c)
    return mixedDeck
  
  #Print each card in an array-like format for readability
  def printDeck(self):
    pDeck = "["
    for c in self.deck:
      pDeck += " " + c.toString() + " |"
    pDeck = pDeck[:len(pDeck) - 1] + "]"
    print(pDeck)

  #If the deck is not empty, remove the top card from the deck
  def dealCard(self):
    if not self.isEmpty:
      self.size -= 1
      if self.size == 0:
        self.isEmpty = True
      return self.deck.pop(0)
    else:
      print("No cards in the deck to deal")
      return None
      
class BJHand:
    def __init__(self):
        self.reset()
        self.busted = False

    '''
    * @param c: The Card being added to the hand
    * First, tack the card on the hand list
    * Then, update all current hand values
    * Also, if the card is an ace,
    * Add a new value where the ace is treated as an 11
    '''
    def addCard(self, c):
        self.hand.append(c)
        size = len(self.handValue)
        for pos in range(size):
            if c.value == 1: #deal with Aces counting as 11 first
                self.handValue.append(self.handValue[pos] + 11)
            if c.value <= 10:
                self.handValue[pos] += c.value
            else:
                self.handValue[pos] += 10
        self.numOfCards += 1
    
    '''
    * Set the player's best score, 
    * and pull him out of the dealing process
    '''
    def stand(self):
        best = 0
        for v in self.handValue:
            if v >= best:
                best = v
        del(v)
        self.handValue = best

    #Return a hand to its default state
    def reset(self):
        self.hand = []
        self.handValue = [0]
        self.numOfCards = 0
        self.stillIn = True

    '''
    * Iterate through each possible hand value in the player's hand
    * If a particular value is greater than 21, 
    * remove it from the list
    '''
    def areBusted(self):
        for val in self.handValue:
            if val > 21:
                self.handValue.remove(val)
        del(val)
        if len(self.handValue) <= 0:
            return True
        return False 

    def toString(self):
        currentHand = "| "
        for c in self.hand:
            currentHand += c.toString() + ", "
        currentHand = currentHand[:len(currentHand) - 2] + "|" 
        return currentHand
    
    '''
    * @param altHand: The other player's hand we are comparing 'self' to
    * @return 1: If self's value > altHand's value
    * @return 0: If self's value == altHand's value
    * @return -1: If self's value < altHand's value
    '''
    def compareTo(self, altHand):
        if self.handValue > altHand.handValue:
            return 1
        elif self.handValue == altHand.handValue:
            return 0
        else:
            return -1
    

class BJPlayer:
    def __init__(self, name):
        self.money = 100
        self.hand = BJHand()
        self.name = name
        self.bet = 0

    '''
    * @param m: The amount of money a player is betting on his hand
    * If the player cannot pay 'm' dollars, return false to show this inability
    * Otherwise, subtract that amount of money from the player's account
    '''
    def placeBet(self, m):
        if m > self.money:
            print("You do not have that much money. Try again")
            return False
        elif m <= 0:
            print("Please place a bet greater than $0.")
            return False
        else:
            self.money -= m
            self.bet = m
            return True
    
    '''
    * @param m: The amount of money a player wins from a particular hand
    * Player 'self' adds 'm' money to his account
    '''
    def receiveWinnings(self, m):
        self.money += m
    
    #Player is dealt a card and adds it to his hand
    def dealCard(self, c):
        self.hand.addCard(c)
    
class Dealer:
    def __init__(self):
        self.hand = BJHand()

    '''
    * If a hand has a value that leaves it between 17 and 21
    * The dealer must stay
    * Otherwise, the dealer must hit
    '''    
    def decideToHit(self):
        for val in self.hand.handValue:
            if val >= 17 and val <= 21:
                return False
        del(val)
        return True

playerNumber = -1
playerList = []
dealer = Dealer()

def startGame():
    playerNumber = -1
    while playerNumber <= 0:
        playerNumber = (int)(input("How many players would like a chair at the table?"+
                                    "\nMax 5 "))
    for i in range(playerNumber):
        pName = input("Player " + (str)(i + 1) + ", choose a name: ")
        print(pName + " is your name")
        playerList.append(BJPlayer(pName))
    del(i)

def acceptBets():
    for player in playerList:
        valid = False
        while not valid:
            print(player.name + ": You have $" + str(player.money) + "." )
            amount = int(input("How much would you like to bet on this hand?"))
            valid = player.placeBet(amount)


def dealHands(deck):
    for round in range(2):
        for player in playerList:
            player.dealCard(deck.dealCard())
        dealer.hand.addCard(deck.dealCard())
    dealer.hand.hand[1].flip()
    del(round, player)

def playerLoop(player):
    while player.hand.stillIn:
        if len(player.hand.handValue) == 2 and player.hand.handValue[1] == 21:
            print("Blackjack! You win!")
            return
        isValid = False
        print("Dealer is showing " + dealer.hand.hand[0].toString())
        while not isValid:
            print(player.name + ": Your Hand is " + player.hand.toString())
            decision = input("Would you like to hit (\'h\') or stand (\'s\')? ")
            if decision == "h":
                player.dealCard(deck.dealCard())
                if player.hand.areBusted():
                    player.hand.stillIn = False
                    print("You busted with " + player.hand.toString())
                    return
                isValid = True
            elif decision == "s":
                player.hand.stand()
                return
            else:
                print("Excuse me, sir. This is not a valid move. Try again.")

def dealerLoop():
    print("Dealer is showing " + dealer.hand.hand[0].toString())
    dealer.hand.hand[1].flip()
    print("Dealer reveals his face-down card: " + dealer.hand.hand[1].toString())
    if len(dealer.hand.handValue) == 2 and dealer.hand.handValue[1] == 21:
        print("Dealer has blackjack!")
        return -1
    playing = True
    while playing:
        playing = dealer.decideToHit()
        if playing:
            dealer.hand.addCard(deck.dealCard())
            print("Dealer now has " + dealer.hand.toString())
            if dealer.hand.areBusted():
                print("Dealer busted with " + dealer.hand.toString() + "!")
                return 0
    dealer.hand.stand()
    print("Dealer stands at " + str(dealer.hand.handValue))
    return dealer.hand.handValue

def checkWinner(player, dealer, dealerStatus):
    if dealerStatus == 0:
        player.receiveWinnings(player.bet * 2)
        print(player.name + " wins!")
    elif dealerStatus == -1:
    #Dealer hit blackjack, all players lose except those with BJ    
        print("Sorry, " + player.name + ": dealer's blackjack means you lose.")
    else:
        #Calculate who wins between dealers and players that are still in
        winner = player.hand.compareTo(dealer.hand)
        if winner == 1:
            player.receiveWinnings(player.bet * 2)
            print("Congrats, " + player.name + ", you win $" + (str)(player.bet))
        elif winner == 0:
            player.receiveWinnings(player.bet)
            print(player.name + ": You pushed and have received your bet back.")
        else:
            print("Dealer beats " + player.name + "\'s " + 
                    str(player.hand.handValue) + " with " + 
                    str(dealer.hand.handValue) + ". Better luck next time.")
    
   
deck = Deck()
deck.shuffle()
startGame()
acceptBets()
dealHands(deck)
for player in playerList:
    playerLoop(player)
dealerStatus = dealerLoop()
for player in playerList:
    if player.hand.stillIn:
        checkWinner(player, dealer, dealerStatus)
