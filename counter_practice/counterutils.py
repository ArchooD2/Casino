def getcount(deck):
    #reverse the counting stats to get the running count (without looking at discarded cards, so inverse)
    count = 0
    for card in deck:
        if card["Rank"] in ["10", "J", "Q", "K", "A"]:
            count += 1
        elif card["Rank"] in ["2", "3", "4", "5", "6"]:
            count -= 1
    return count
def truecount(count, deck):
    #calculate the true count
    return count / (len(deck) / 52)
