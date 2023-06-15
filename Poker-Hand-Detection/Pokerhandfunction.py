def findPokerHand(hand):
    ranks = []
    suits = []
    possibleRanks = []
    pokerHandRanks = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of a Kind", 7: "Full House", 6: "Flush",
                      5: "Straight", 4: "Three of a Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}

    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]

        if rank=="A":
            rank = 14
        elif rank=="K":
            rank=13
        elif rank=="Q":
            rank=12
        elif rank=="J":
            rank=11

        ranks.append(int(rank))
        suits.append(suit)

    sortedRanks = sorted(ranks)

    #Flush
    if suits.count(suits[0]) == 5:
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks and 10 in sortedRanks:
            possibleRanks.append(10)
        elif all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
            possibleRanks.append(9)
        else:
            possibleRanks.append(6)


    #Straight
    if all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range (1, len(sortedRanks))):
        possibleRanks.append(5)

    #Four of an kind
    handUniqueVals = list(set(sortedRanks))

    if len(handUniqueVals) == 2:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 4:
                possibleRanks.append(8)
            if sortedRanks.count(val) == 3:
                possibleRanks.append(7)

    #Three of a kind
    if len(handUniqueVals) == 3:
        for val in handUniqueVals:
            if sortedRanks.count(val) == 3:  
                possibleRanks.append(4)
            if sortedRanks.count(val) == 2:  
                possibleRanks.append(3)

    #Pair
    if len(handUniqueVals) == 4:
        possibleRanks.append(2)

    if not possibleRanks:
        possibleRanks.append(1)

    output  = pokerHandRanks[max(possibleRanks)]
    return output


if __name__ == "__main__":
    findPokerHand(["KH", "AH", "QH", "JH", "10H"])  # Royal Flush