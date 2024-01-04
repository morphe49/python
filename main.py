import random
from operator import attrgetter
"""Constant values"""
card_values = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
               11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
card_colors = {"♠": "Spades", "♣": "Clubs", "♦": "Diamonds", "♥": "Hearts"}

class card:
    def __init__(self, value , color):
        self.value = value
        self.color = color
        if self.value in card_values:
            value_str = card_values[self.value]
        else:
            value_str = str(self.value)
        self.name = f"{value_str}{self.color}"
    def __repr__(self):
        return '{' + self.name + '}'
"""Constats lists"""
royals = [[card("10", "♠"), card("Jack", "♠"), card("Queen", "♠"),card("King", "♠"), card("Ace", "♠")],
              [card("10", "♣"), card("Jack", "♣"),card("Queen", "♣"), card("King", "♣"),card("Ace", "♣")]
        , [card("10", "♦"), card("Jack", "♦"), card("Queen", "♦"),card("King", "♦"), card("Ace", "♦")]
        , [card("10", "♥"), card("Jack", "♥"), card("Queen", "♥"),card("King", "♥"), card("Ace", "♥")]]
"""Main Functions"""
def shuffle(card_values, card_colors):
    deck = []
    for value in card_values.keys():
        for color in card_colors:
            deck.append(card(value,color))
    return deck
def deal():
    deck = shuffle(card_values,card_colors)
    dealt_cards = []
    player_hand1 = random.choice(deck)
    deck.remove(player_hand1)
    player_hand2 = random.choice(deck)
    deck.remove(player_hand2)
    comp_hand1 = random.choice(deck)
    deck.remove(comp_hand1)
    comp_hand2 = random.choice(deck)
    deck.remove(comp_hand2)
    flop1 = random.choice(deck)
    deck.remove(flop1)
    flop2 = random.choice(deck)
    deck.remove(flop2)
    flop3 = random.choice(deck)
    deck.remove(flop3)
    turn = random.choice(deck)
    deck.remove(turn)
    river = random.choice(deck)
    dealt_cards.append(player_hand1)
    dealt_cards.append(player_hand2)
    dealt_cards.append(comp_hand1)
    dealt_cards.append(comp_hand2)
    dealt_cards.append(flop1)
    dealt_cards.append(flop2)
    dealt_cards.append(flop3)
    dealt_cards.append(turn)
    dealt_cards.append(river)
    return dealt_cards
def deposit() :
    while True:
        balance = input("Mennyit szeretnél váltani? $ ")
        if balance.isdigit() :
            balance = int(balance)
            if balance > 0 :
                break
            else:
                print("0-nál magasabb összeggel tudsz csak játszani! ")
        else:
            print("Pozitív egész számmal add meg a váltásod! ")
    return balance
def bet() :
    while True:
        bet = input("Add meg a téted $ , vagy check c-vel: ")
        if bet.isdigit() :
            bet = int(bet)
            if bet > 0 :
                break
            else:
                print("0-nál magasabb tétet tudsz csak megadni! ")
        elif bet == "c" or "C":
            bet = 0
            break
        else:
            print("Pozitív egész számmal add meg a téted , vagy c-vel check! ")
    return bet
"""Check functions"""
def royalcheckp(royals,cardsp):
    for cards_5 in royals:
        matching_count = 0
        for card_5 in cards_5:
            for card_7 in cardsp:
                if card_5.value == card_7.value and card_5.color == card_7.color:
                    matching_count += 1
                    break
        if matching_count == len(cards_5):
            return True
    return False
def pokercheckp(cardsp):
    value_count = {}
    for cards in cardsp:
        value = cards.value
        if value in value_count:
            value_count[value] +=  1
        else:
            value_count[value] = 1
        if value_count[value] >= 4 :
            value_v = value
            return True , value_v
    return False , 0
def flushcheckp(cardsp):
    color_counts = {}
    color_highest_card = {}
    for card in cardsp:
        cc = card.color
        value = card.value
        if cc in color_counts:
            color_counts[cc] += 1
        else:
            color_counts[cc] = 1
        if cc in color_highest_card:
            if value > color_highest_card[cc]:
                color_highest_card[cc] = value
        else:
            color_highest_card[cc] = value
    for cc, count in color_counts.items():
        if count >= 5:
            return True, color_highest_card[cc]

    return False, None
def strflushcheckp(cardsp):
    color_counts = {}
    value_sequences = {}
    for card in cardsp:
        color = card.color
        value = card.value
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1
        if color in value_sequences:
            value_sequences[color].append(value)
        else:
            value_sequences[color] = [value]
    for color, count in color_counts.items():
        if count >= 5:
            values = value_sequences[color]
            values.sort()
            for i in range(len(values) - 4):
                if values[i:i + 5] == list(range(values[i], values[i] + 5)):

                    return True, max(values[i:i + 5])

    return False, 0
def straightcheckp(cardsp):
    cardsp.sort(key=lambda card: card.value)
    consecutive_count = 1
    for i in range(1, len(cardsp)):
        if cardsp[i].value == cardsp[i - 1].value + 1:
            consecutive_count += 1
            if consecutive_count >= 5:
                hc = cardsp[i].value
                return True , hc
        else:
            consecutive_count = 1
    return False , 0
def triplescheckp(cardsp):
    value_count = {}
    for cards in cardsp:
        value = cards.value
        if value in value_count:
            value_count[value] += 1
        else:
            value_count[value] = 1
        if value_count[value] == 3:
            tv=value
            return True , tv
    return False , 0
def paircheckp(cardsp):
    sorted_cards = sorted(cardsp, key=lambda card: card.value, reverse=True)
    value_count = {}
    pairs = []
    remaining_cards = []
    for card in sorted_cards:
        value = card.value
        if value in value_count:
            value_count[value] += 1
            if value_count[value] == 2:
                pairs.append(card)
                firstp = value
                if len(pairs) == 1:
                    secondp = value
        else:
            value_count[value] = 1
            remaining_cards.append(card)
    if len(pairs) == 1:
        return 1 , firstp , 0
    elif len(pairs) == 2:
        return 2 , firstp , secondp
    elif len(pairs) == 3:
        return 2 ,firstp , secondp
    else:
        return 0 , 0 ,0

"""Main"""
def main(royals,balance):
    balance_init = balance
    dealt_cards = deal()
    player_hand1 = random.choice(dealt_cards)
    dealt_cards.remove(player_hand1)
    player_hand2 = random.choice(dealt_cards)
    dealt_cards.remove(player_hand2)
    comp_hand1 = random.choice(dealt_cards)
    dealt_cards.remove(comp_hand1)
    comp_hand2 = random.choice(dealt_cards)
    dealt_cards.remove(comp_hand2)
    flop1 = random.choice(dealt_cards)
    dealt_cards.remove(flop1)
    flop2 = random.choice(dealt_cards)
    dealt_cards.remove(flop2)
    flop3 = random.choice(dealt_cards)
    dealt_cards.remove(flop3)
    turn = random.choice(dealt_cards)
    dealt_cards.remove(turn)
    river = random.choice(dealt_cards)
    player_cards = []
    comp_cards = []
    player_cards.append(player_hand1)
    player_cards.append(player_hand2)
    player_cards.append(flop1)
    player_cards.append(flop2)
    player_cards.append(flop3)
    player_cards.append(turn)
    player_cards.append(river)
    comp_cards.append(comp_hand1)
    comp_cards.append(comp_hand2)
    comp_cards.append(flop1)
    comp_cards.append(flop2)
    comp_cards.append(flop3)
    comp_cards.append(turn)
    comp_cards.append(river)
    print(f"Bank total: {balance_init}\nLapjaid: |{player_hand1}| |{player_hand2}|")
    while True:
        tet = bet()
        if tet > balance_init:
            print(f"Nincs elég pénzed! {balance_init} zsetonod van.Add meg a téted!")
        else:
            break
    balance = int(balance_init - tet)
    print(f"Bank total: {balance}\nLapjaid: |{player_hand1}| |{player_hand2}|\n"
          f"Flop: |{flop1}| |{flop2}| |{flop3}|")
    if balance == 0:
        print(f"Bank total: {balance}\nLapjaid: |{player_hand1}| |{player_hand2}|\n"
              f"River: |{flop1}| |{flop2}| |{flop3}| |{turn}| |{river}|\nComputer lapjai: |{comp_hand1}| |{comp_hand2}|")
        pass
    else:
        while True:
            tet = bet()
            if tet > balance:
                print(f"Nincs elég pénzed! {balance} zsetonod van.Add meg a téted!")
            else:
                break
        balance = int(balance - tet)
        print(f"Bank total: {balance}\nLapjaid: |{player_hand1}| |{player_hand2}|\n"
              f"Turn: |{flop1}| |{flop2}| |{flop3}| |{turn}|")
        if balance == 0:
            print(f"Bank total: {balance}\nLapjaid: |{player_hand1}| |{player_hand2}|\n"
                  f"River: |{flop1}| |{flop2}| |{flop3}| |{turn}| |{river}|\nComputer lapjai: |{comp_hand1}| |{comp_hand2}|")
            pass
        else:

            while True:
                tet = bet()
                if tet > balance:
                    print(f"Nincs elég pénzed! {balance} zsetonod van.Add meg a téted!")
                else:
                    break
            balance = int(balance - tet)
            print(f"Bank total: {balance}\nLapjaid: |{player_hand1}| |{player_hand2}|\n"
                  f"River: |{flop1}| |{flop2}| |{flop3}| |{turn}| |{river}| \nComputer lapjai: |{comp_hand1}| |{comp_hand2}|")
    total_bet = balance_init - balance
    royal_player = royalcheckp(royals,player_cards)   # True/False
    poker_player, pokervaluep = pokercheckp(player_cards)          # True/False , value
    flush_player, flushlistp = flushcheckp(player_cards)          # True/False , list of same color cards?
    strflush_player, strflush_highp = strflushcheckp(player_cards)       # True/False , highcardvalue
    straight_player, strhp = straightcheckp(player_cards)       # True/False , highcardvalue
    triples_player, triplesvaluep = triplescheckp(player_cards)        # True/False , triplesvalue
    pair_player, firstpvp, secondpvp = paircheckp(player_cards)           # paircount , firs pair value , second pair value
    royal_comp = royalcheckp(royals, comp_cards)  # True/False
    poker_comp, pokervaluec = pokercheckp(comp_cards)  # True/False , value
    flush_comp, flushlistc = flushcheckp(comp_cards)  # True/False , list of same color cards?
    strflush_comp, strflush_highc = strflushcheckp(comp_cards)  # True/False , highcardvalue
    straight_comp, strhc = straightcheckp(comp_cards)  # True/False , highcardvalue
    triples_comp, triplesvaluec = triplescheckp(comp_cards)  # True/False , triplesvalue
    pair_comp, firstpvc, secondpvc = paircheckp(comp_cards)  # paircount , firs pair value , second pair value

    player_cards.sort(key=attrgetter('value'), reverse=True)
    comp_cards.sort(key=attrgetter('value'), reverse=True)

    if triples_player or triples_comp :
        thp = sorted(set(player_cards), key=lambda card: card.value, reverse=True)
        thc = sorted(set(comp_cards), key=lambda card: card.value, reverse=True)
        for cards in thp :
            if cards.value == triplesvaluep :
                thp.remove(cards)
        for cards in thc :
            if cards.value == triplesvaluec :
                thc.remove(cards)
        tripleshighp1 = thp[0].value
        tripleshighp2 = thp[1].value
        tripleshighc1 = thc[0].value
        tripleshighc2 = thc[1].value
    phplist = sorted(set(player_cards), key=lambda card: card.value, reverse=True)
    phclist = sorted(set(comp_cards), key=lambda card: card.value, reverse=True)
    for cards in phplist :
        if cards.value == firstpvp or secondpvp :
            phplist.remove(cards)
    for cards in phclist :
        if cards.value == firstpvc or secondpvc :
            phclist.remove(cards)
    php1 = phplist[0].value
    php2 = phplist[1].value
    php3 = phplist[2].value
    phc1 = phclist[0].value
    phc2 = phclist[1].value
    phc3 = phclist[2].value
    if triples_player  and (pair_player == 1 or 2):
        fullhp = True
    else:
        fullhp = False
    if triples_comp  and (pair_comp == 1 or 2):
        fullhc = True
    else:
        fullhc = False
    highhandp = sorted(set(player_cards), key=lambda card: card.value, reverse=True)
    highhandc = sorted(set(comp_cards), key=lambda card: card.value, reverse=True)
    phh1 = highhandp[0].value
    phh2 = highhandp[1].value
    phh3 = highhandp[2].value
    phh4 = highhandp[3].value
    phh5 = highhandp[4].value
    chh1 = highhandc[0].value
    chh2 = highhandc[1].value
    chh3 = highhandc[2].value
    chh4 = highhandc[3].value
    chh5 = highhandc[4].value
    if royal_player == True and royal_comp == False:
        print("Nyertél! Royal Flush!!!")
        win = True
        split = False
        return win , split, total_bet
    elif royal_comp == True and royal_player == False:
        print("Computer nyert, Royal Flush!!")
        win = False
        split = False
        return win , split, total_bet
    elif royal_player == True and royal_comp == True:
        print("Split!Royal flush mindkét játékosnak!")
        win = False
        split = True
        return win , split, total_bet
    else:
        if strflush_player == True and strflush_comp == False:
            print("Nyertél! Straight Flush!!!")
            win = True
            split = False
            return win, split, total_bet
        elif strflush_player == False and strflush_comp == True:
            print("Computer nyert, Straight Flush!!")
            win = False
            split = False
            return win, split, total_bet
        elif strflush_player == True and strflush_comp == True:
            if strflush_highp > strflush_highc :
                print("Nyertél! Straight Flush!!!")
                win = True
                split = False
                return win, split, total_bet
            elif strflush_highp < strflush_highc :
                print("Computer nyert, Straight Flush!!")
                win = False
                split = False
                return win, split, total_bet
            else:
                print("Split!! Straight Flush!!")
                win = False
                split = True
                return win,split, total_bet
        else :
            if poker_player == True and poker_comp == False :
                print("Nyertél! Poker!!!")
                win = True
                split = False
                return win, split, total_bet
            elif poker_player == False and poker_comp == True :
                print("Computer nyert! Poker!!!")
                win = True
                split = False
                return win, split, total_bet
            elif poker_player == True and poker_comp == True:
                if int(pokervaluep) > int(pokervaluec) :
                    print("Nyertél! Poker!!!")
                    win = True
                    split = False
                    return win, split, total_bet
                elif int(pokervaluep) < int(pokervaluec) :
                    print("Computer nyert! Poker!!!")
                    win = True
                    split = False
                    return win, split, total_bet
                elif int(pokervaluep) == int(pokervaluec):
                    fifthp = set(player_cards)
                    fifthc = set(comp_cards)
                    for cardvalue in fifthp :
                        cv = cardvalue.value
                        if cv == pokervaluep :
                            fifthp.remove(cardvalue)
                            php = fifthp[0].value
                        else:
                            php = 0
                    for cardvalue in fifthc:
                        cv = cardvalue.value
                        if cv == pokervaluep:
                            fifthc.remove(cardvalue)
                            phc = fifthc[0].value
                        else:
                            phc = 0
                    if int(php) > int(phc) :
                        print("Nyertél! Poker!!!")
                        win = True
                        split = False
                        return win, split, total_bet
                    elif int(php) < int(phc) :
                        print("Computer nyert! Poker!!!")
                        win = False
                        split = False
                        return win, split, total_bet
                    else :
                        print("Split! Poker!!")
                        win = False
                        split = True
                        return win , split, total_bet
            else:
                if fullhp == True and fullhc == False :
                    print("Nyertél! Fullhouse!!!")
                    win = True
                    split = False
                    return win, split, total_bet
                elif fullhc == True and fullhp == False :
                    print("Computer nyert! Fullhouse!!!")
                    win = False
                    split = False
                    return win, split, total_bet
                elif fullhp == True and fullhc == True :
                    if triplesvaluep > triplesvaluec:
                        print("Nyertél! Fullhouse!!!")
                        win = True
                        split = False
                        return win, split, total_bet
                    elif triplesvaluec > triplesvaluep:
                        print("Computer nyert! Fullhouse!!!")
                        win = False
                        split = False
                        return win, split, total_bet
                    else :
                        if firstpvp > firstpvc:
                            print("Nyertél! Fullhouse!!!")
                            win = True
                            split = False
                            return win, split, total_bet
                        elif firstpvc > firstpvp:
                            print("Computer nyert! Fullhouse!!!")
                            win = False
                            split = False
                            return win, split, total_bet
                        else :
                            print("Split! Fullhouse!!")
                            win = False
                            split = True
                            return win, split, total_bet
                else:
                    if flush_player == True and flush_comp == False :
                        print("Nyertél! Flush!!!")
                        win = True
                        split = False
                        return win, split, total_bet
                    elif flush_player == False and flush_comp == True :
                        print("Computer nyert! Flush!!!")
                        win = False
                        split = False
                        return win, split, total_bet
                    elif flush_player == True and flush_comp == True :
                        if flushlistp > flushlistc :
                            print("Nyertél! Flush!!!")
                            win = True
                            split = False
                            return win, split, total_bet
                        elif flushlistp < flushlistc :
                            print("Computer nyert! Flush!!!")
                            win = False
                            split = False
                            return win, split, total_bet
                        else :
                            print("Split! Flush !!!")
                            win = False
                            split = True
                            return win, split, total_bet
                    else:
                        if straight_player == True and straight_comp == False:
                            print("Nyertél! Sor!!!")
                            win = True
                            split = False
                            return win, split, total_bet
                        elif straight_player == False and straight_comp == True:
                            print("Computer nyert! Sor!!!")
                            win = False
                            split = False
                            return win, split, total_bet
                        elif straight_player == True and straight_comp == True:
                            if strhp > strhc:
                                print("Nyertél! Sor!!!")
                                win = True
                                split = False
                                return win, split, total_bet
                            elif strhp < strhc:
                                print("Computer nyert! Sor!!!")
                                win = False
                                split = False
                                return win, split, total_bet
                            else:
                                print("Split! Sor !!!")
                                win = False
                                split = True
                                return win, split, total_bet
                        else:
                            if triples_player == True and triples_comp == False:
                                print("Nyertél! Drill!!!")
                                win = True
                                split = False
                                return win, split, total_bet
                            elif triples_player == False and triples_comp == True:
                                print("Computer nyert! Drill!!!")
                                win = False
                                split = False
                                return win, split, total_bet
                            elif triples_player == True and triples_comp == True:
                                if triplesvaluep > triplesvaluec:
                                    print("Nyertél! Drill!!!")
                                    win = True
                                    split = False
                                    return win, split, total_bet
                                elif triplesvaluep < triplesvaluec:
                                    print("Computer nyert! Drill!!!")
                                    win = False
                                    split = False
                                    return win, split, total_bet
                                elif triplesvaluep == triplesvaluec:
                                    if int(tripleshighp1+tripleshighp2) > int(tripleshighc1+tripleshighc2):
                                        print("Nyertél! Drill!!!")
                                        win = True
                                        split = False
                                        return win, split, total_bet
                                    elif int(tripleshighp1+tripleshighp2) < int(tripleshighc1+tripleshighc2):
                                        print("Computer nyert! Drill!!!")
                                        win = False
                                        split = False
                                        return win, split, total_bet
                                    else:
                                        print("Split! Drill !!!")
                                        win = False
                                        split = True
                                        return win, split, total_bet
                            else:
                                if pair_player > pair_comp :
                                    print(f"Nyertél!{pair_player} pár!!!")
                                    win = True
                                    split = False
                                    return win, split, total_bet
                                elif pair_player < pair_comp :
                                    print(f"Computer nyert! {pair_comp} pár!!!")
                                    win = False
                                    split = False
                                    return win, split, total_bet
                                elif pair_player == pair_comp:
                                    ppsum = int(firstpvp+secondpvp)
                                    cpsum = int(firstpvc+secondpvc)
                                    if ppsum > cpsum:
                                        print(f"Nyertél!Nagyobb {pair_player} pár!!!")
                                        win = True
                                        split = False
                                        return win, split, total_bet
                                    elif ppsum < cpsum :
                                        print(f"Computer nyert!Nagyobb {pair_comp} pár!!!")
                                        win = False
                                        split = False
                                        return win, split, total_bet
                                    else:
                                        if pair_player == 1:
                                            phpsum = int(php1+php2+php3)
                                            phcsum = int(phc1+phc2+phc3)
                                            if phpsum > phcsum :
                                                print(f"Nyertél!Nagyobb {pair_player} pár!!!")
                                                win = True
                                                split = False
                                                return win, split, total_bet
                                            elif phpsum < phcsum :
                                                print(f"Computer nyert!Nagyobb {pair_comp} pár!!!")
                                                win = False
                                                split = False
                                                return win, split, total_bet
                                            else:
                                                print(f"Split!  {pair_comp} pár!!!")
                                                win = False
                                                split = True
                                                return win, split, total_bet
                                        else:
                                            if php1 > phc1 :
                                                print(f"Nyertél!Nagyobb {pair_player} pár!!!")
                                                win = True
                                                split = False
                                                return win, split, total_bet
                                            elif php1 < phc1 :
                                                print(f"Computer nyert!Nagyobb {pair_comp} pár!!!")
                                                win = False
                                                split = False
                                                return win, split, total_bet
                                            else:
                                                print(f"Split!  {pair_comp} pár!!!")
                                                win = False
                                                split = True
                                                return win, split, total_bet
                                else:
                                    phhsum = int(phh1+phh2+phh3+phh4+phh5)
                                    chhsum = int(chh1+chh2+chh3+chh4+chh5)
                                    if phhsum > chhsum :
                                        print(f"Nyertél!Magasabb kéz!!!")
                                        win = True
                                        split = False
                                        return win, split, total_bet
                                    elif phhsum < chhsum :
                                        print(f"Computer nyert!Magasabb kéz!!!")
                                        win = False
                                        split = False
                                        return win, split, total_bet
                                    else :
                                        print(f"Split!!!")
                                        win = False
                                        split = True
                                        return win, split, total_bet
balance_init = deposit()
while balance_init != 0 :
    x = input("Következő leosztás? I / N ").lower()
    if x == "i":
        win , split, total_bet = main(royals,balance_init)
        if win:
            balance_init -= total_bet
            balance_init = (total_bet*2)+balance_init
        elif split:
            balance_init = balance_init
        else:
            balance_init = balance_init-total_bet
    elif x == "n":
        print(f"Kiléptél a játékból {balance_init} zsetonnal")
        break
    else:
        print("Érvénytelen parancs.Új leosztás: I , kilépés : N. ")
