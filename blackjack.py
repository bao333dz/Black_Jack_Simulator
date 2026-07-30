import random
import matplotlib.pyplot as plt

# Black Jack

base = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # 0 is A and the 3 10s stand for JQK
deck = base * 4 * 6

player = []
house = []

# Split
def split(player, deck, hands):
    pending = 0

    for i in range(0,4):
        if len(player[i]) == 0 and pending > 0:
            player[i].append(player[i-1][0])
            p = random.choice(deck)
            player[i].append(p)
            pending -= 1

        while player[i][0] == player[i][0] and hands < 4 and pending < 3:
            player[i].pop(1)
            p = random.choice(deck)
            player[i].append(p)
            hands += 1
            pending += 1

    return hands, player


# Calculate the value of the cards
def handval(lists):
    hard = False
    soft = False
    i = lists.count(0)

    suml = sum(lists)
    
    # If no A
    if i == 0:
        hard = True
        return suml, hard, soft
    
    # If only 1 A
    elif i == 1:

        # Hard
        if suml + 11 > 21:
            suml += 1
            hard = True
            return suml, hard, soft
        
        # Soft
        else:
            suml += 11
            soft = True
            return suml, hard, soft
        
    # If more than 1 A
    else:

        # Soft
        if suml + 11 + (i - 1) <= 21:
            suml += 11 + (i - 1)
            soft = True
            return suml, hard, soft
        
        # Hard
        else:
            suml += i
            hard = True
            return suml, hard, soft
        
# Take one card
def one(player, deck, run_count):
    p = random.choice(deck)
    deck.remove(p)
    player.append(p)
    if p in range(2,7):
        run_count += 1
    if p in (0,10):
        run_count -= 1
    return run_count
 
# Illustrious 18 (excluding the insurance case)
def specstrat(player, house, deck, double, stand, run_count, remain_deck):
    

    # Calculate the ace
    if 0 in player:
        numA = player.count(0)
        sumpl = sum(player) + 1 * numA

    # If no ace
    else:
        sumpl = sum(player)
    # Calculate true count
    remain_deck = len(deck) / 52
    true_count = run_count / remain_deck

    # Player 10 and House 10 or House A (double)
    if sumpl == 10 and true_count >= 4 and (house[0] in (0,10)) and len(player) == 2:
        run_count = one(player, deck, run_count)
        double = True
        return double, stand, run_count

    # Player 16
    if sumpl == 16:

        # 10 - 6
        if 10 in player and len(player) == 2:

            # House 10 (stand)
            if house[0] == 10 and true_count >= 0:
                stand = True
                return double, stand, run_count

        # House 9 (stand)
        if house[0] == 9 and true_count >= 5:
            stand = True
            return double, stand, run_count
                
    # Player 15
    if sumpl == 15:

        # House 10 (stand)
        if house[0] == 10 and true_count >= 4:
            stand = True
            return double, stand, run_count
            
        # House 9 (stand)
        if house[0] == 9 and true_count >= 2:
            stand = True
            return double, stand, run_count
    
    # Player 14 and House 10 (stand)
    if sumpl == 14 and house[0] == 10 and true_count >= 3:
        stand = True
        return double, stand, run_count
        
    # Player 13
    if sumpl == 13:

        # House 2 (hit)
        if house[0] == 2 and true_count < -1:
            run_count = one(player, deck, run_count)
            return double, stand, run_count

        # House 3 (hit)
        if house[0] == 3 and true_count < -2:
            run_count = one(player, deck, run_count)
            return double, stand, run_count
    
    # Player 12
    if sumpl == 12:

        # House 3 (stand)
        if house[0] == 3 and true_count >= 2:
            stand = True
            return double, stand, run_count
            
        # House 2 (stand)
        if house[0] == 2 and true_count >= 3:
            stand = True
            return double, stand, run_count
        
        # House 4 (hit)
        if house[0] == 4 and true_count < 0:
            run_count = one(player, deck, run_count)
            return double, stand, run_count
            
        # House 5 (hit)
        if house[0] == 5 and true_count < -2:
            run_count = one(player, deck, run_count)
            return double, stand, run_count

        # House 6 (hit)
        if house[0] == 6 and true_count < -1:
            run_count = one(player, deck, run_count)
            return double, stand, run_count

    # Player 11 and House A (double)
    if sumpl == 11 and house[0] == 0 and len(player) == 2:
        if true_count >= 1:
            run_count = one(player, deck, run_count)
            double = True
            return double, stand, run_count

    # Player 9
    if sumpl == 9:

        # House 2 (double)
        if house[0] == 2 and true_count >= 1 and len(player) == 2:
            run_count = one(player, deck, run_count)
            double = True
            return double, stand, run_count

        # House 7 (double)
        if house[0] == 7 and true_count >= 3 and len(player) == 2:
            run_count = one(player, deck, run_count)
            double = True
            return double, stand, run_count

    return double, stand, run_count

# Basic Strategy 
def basicstrat(player, deck, house, run_count, stand, double, remain_deck):

    busted = False

    # Player
    while True:
        
        # Calculate the hand and determine if it hard or soft
        suml, hard, soft = handval(player)

        # Cases for hard hands
        if hard == True:

            # Player over 22
            if suml > 21:
                busted = True
                return busted, double, stand, run_count

            # Player 17 - 21 (stand)
            if suml in range(17,22):
                stand = True
                return busted, double, stand, run_count
            
            # Player 13 - 16
            if suml in range(13,17):

                # House 2 - 6
                if house[0] in range(2,7):

                    # Store the len 
                    bf = len(player)

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Hit
                    if len(player) != bf:
                        continue

                    # Nothing happen case (stand)
                    else:
                        stand = True
                        return busted, double, stand, run_count
                
            
                
                # House 7 - A
                else:

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Stand
                    if stand == True:
                        return busted, double, stand, run_count

                    # Nothing happen case (hit)
                    else:
                        run_count = one(player, deck, run_count)
                        continue
                
            # Player 12
            if suml == 12:

                # House 4,5,6
                if house[0] in range(4,7):
                    # Store the len 
                    bf = len(player)

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Hit
                    if len(player) != bf:
                        continue

                    # Nothing happen case (stand)
                    else:
                        stand = True
                        return busted, double, stand, run_count
            
                # House 2 - 3 or 7 - A (hit)
                else:

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Stand
                    if stand == True:
                        return busted, double, stand, run_count

                    # Nothing happen case (hit)
                    else:
                        run_count = one(player, deck, run_count)
                        continue


            # Player 11
            if suml == 11:

                # House 2 - 10 (double)
                if house[0] in range(2,11) and len(player) == 2:
                    run_count = one(player,deck, run_count)
                    double = True
                    return busted, double, stand, run_count
                
                # House A
                else:

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Double
                    if double == True:
                        return busted, double, stand, run_count

                    # Nothing happedn (hit)
                    else:
                        run_count = one(player, deck, run_count)
                        continue
            
            # Player 10
            if suml == 10:
                
                # House 2 - 9 (double)
                if house[0] in range(2,10) and len(player) == 2:
                    run_count = one(player,deck, run_count)
                    double = True
                    return busted, double, stand, run_count

                # House 10 or A
                else:

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Double
                    if double == True:
                        return busted, double, stand, run_count

                    # Nothing happedn (hit)
                    else:
                        run_count = one(player, deck, run_count)
                        continue
            
            # Player 9
            if suml == 9:

                # House 3 - 6 (double)
                if house[0] in range(3,7) and len(player) == 2:
                    run_count = one(player,deck, run_count)
                    double = True
                    return busted, double, stand, run_count
                
                # House 2 or 7 - A
                else:

                    # Checking illustrious
                    double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

                    # Double
                    if double == True:
                        return busted, double, stand, run_count

                    # Nothing happen case (hit)
                    else:
                        run_count = one(player, deck, run_count)
                        continue
            
            # Player 5 - 8 (hit)
            if suml in range(5,9):
                run_count = one(player, deck, run_count)
                continue

            # Player 4 (hit)
            if suml == 4:
                run_count = one(player, deck, run_count)
                continue

        # Cases for soft hands     
        if soft == True:

            # Player 19 - 21 (stand)
            if suml in range(19,22):
                stand = True
                return busted, double, stand, run_count
            
            # Player 18
            if suml == 18:

                # House 2 - 6 (double)
                if house[0] in range(2,7) and len(player) == 2:
                    run_count = one(player,deck, run_count)
                    double = True
                    return busted, double, stand, run_count
                
                # House 7, 8 (stand)
                if house[0] in (7,8):
                    stand = True
                    return busted, double, stand, run_count
                
                # House 9 to A (hit)
                if house[0] in (0,9,10):
                    run_count = one(player, deck, run_count)
                    continue
            
            # Player 16, 17
            if suml in (16,17):

                # House 4,5,6 (double)
                if house[0] in range (4,7) and len(player) == 2:
                    run_count = one(player,deck, run_count)
                    double = True
                    return busted, double, stand, run_count

                # House 2,3 or 7 - A (hit)
                else:
                    run_count = one(player, deck, run_count)
                    continue
            
            # Player 13 - 15
            if suml in range(13,16):

                # House 5,6 (double)
                if house[0] in (5,6) and len(player) == 2:
                    run_count = one(player,deck, run_count)
                    double = True
                    return busted, double, stand, run_count
                
                # House 2 - 4 or 7 - A (hit)
                else:
                    run_count = one(player, deck, run_count)
                    continue
             
# Deciding win or lose
def wl(finpoint, sumh, capital, wager):

    # Tie
    if finpoint[0] == sumh and finpoint[0] <= 21 and sumh <= 21:
        wager.pop(0)
        finpoint.pop(0)
        return capital, finpoint, wager

    # House win
    elif (sumh <= 21 and finpoint[0] > 21) or (sumh < 21 and sumh > finpoint[0]):
        capital -= wager[0]
        wager.pop(0)
        finpoint.pop(0)
        return capital, finpoint, wager

    # Player win
    else:
        capital += wager[0]
        wager.pop(0)
        finpoint.pop(0)
        return capital, finpoint, wager

# House turn
def hoturn(house, deck, run_count):

    # Count revealed card
    if house[1] in range (2,7):
        run_count += 1
    elif house[1] in (0,10):
        run_count -= 1

    while True:
        suml, _, _ = handval(house)

        if suml >= 17:
            return house, run_count
        else:
            run_count = one(house, deck, run_count)

# Main
def bj(player, house, deck):
    pnl = 0

    rounds = 0
    x_rounds = []
    y_pnl = []
    x_rounds.append(0)
    y_pnl.append(pnl)
    capital = 1000
    run_count = 0
    true_count = 0

    for i in range(3000):

        # Variables that need reset every round
        stand = False
        double = False
        house_blackjack = False
        player = [[],
                  [],
                  [],
                  []]
        insurance = False
        house = []
        splitace = False
        hands = 1
        wager = []
        finpoint = []

        # Reload the deck
        if len(deck) <= 36:
            base = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # 0 is A and the 3 10s stand for JQK
            deck = base * 4 * 6
            run_count = 0
        
        # Stop if broke
        if capital <= 10:
            pnl = capital - 1000
            x_rounds.append(rounds)
            y_pnl.append(pnl)
            break

        #================================================================#
        #======================DEALING AND SPLITTING=====================#
        #================================================================#

        # Normal deal
        for c in range(2):
            p = random.choice(deck)
            deck.remove(p)
            player[0].append(p)
            h = random.choice(deck)
            deck.remove(h)
            house.append(h)
            rounds += 1

        if player[0][0] == player[0][1]:

            # A and 8
            if player[0][0] in (0,8):
                if player[0][0] == 0:
                    splitace = True
                hands, player = split(player, deck, hands)
            
            # 9
            if player[0][0] == 9 and house[0] in range(2,10):
                hands, player = split(player, deck, hands)

            # 2, 3 and 7
            if player[0][0] in (2,3,7) and house[0] in range(2,8):
                hands, player = split(player, deck, hands)

            # 6
            if player[0][0] == 6 and house[0] in range(2,7):
                hands, player = split(player, deck, hands)

            # 4
            if player[0][0] == 4 and house[0] in (5,6):
                hands, player = split(player, deck, hands)

        #================================================================#
        #======================DEALING AND SPLITTING=====================#
        #================================================================#


        # Adjusting the risk (suggested by Gemini)
        risk = 0.01
        if true_count < 0:
            risk = 0.005
        elif true_count >= 2 and true_count < 3:
            risk = risk * 2
        elif true_count >= 3 and true_count < 4:
            risk = risk * 4
        elif true_count >= 4 and true_count < 5:
            risk = risk * 8
        elif true_count >= 5:
            risk = risk * 12

        # Calculate the size 
        bet = capital * risk

        # Place the wager(s)
        for w in range(0, hands):
            wager.append(bet)

        # Loop through the hands
        for o in range(0, hands):

            # Counting player's cards
            for k in range(0, len(player[o])):
                if player[o][k] in range(2,7):
                    run_count += 1
                elif player[o][k] in (0,10):
                    run_count -= 1

        # Counting dealer's cards
        if house[0] in range (2,7):
            run_count += 1
        elif house[0] in (0,10):
            run_count -= 1

        # Calculate true count for insurance
        remain_deck = len(deck) / 52
        true_count = run_count / remain_deck
        
        # Insurance (first case in illustrious 18)
        if house[0] == 0 and true_count >= 3:
            insurance = True



        # Black Jack cases

        if sum(house) == 10 and 10 in house:
            house_blackjack = True

            # Count the second card in dealer's hand
            

        for b in range(0, hands):
            player_blackjack = False

            # Check if hand bj or not
            if sum(player[b]) == 10 and 10 in player[b]:
                player_blackjack = True

            # Insurance cases
            if insurance == True:
                if house_blackjack == True:
                    capital += bet
                else:
                    capital -= bet * 0.5
            
            # Player got bj
            if player_blackjack == True and house_blackjack == False:
                capital += 1.5
                player.pop(b)
                player.append([])
                hands -= 1

            

            
            
            













        # ======================================================================== #
        # =====================SPECIAL CASE FOR SPLIT ACES======================== #
        # ======================================================================== #
        if len(splita) > 0:
            # Calculate player point and store
            suml, _, _ = handval(player)
            finpoint.append(suml)
            continue

        else:
            if splitace == True:

                # House turn
                house, run_count = hoturn(house, deck, run_count)
                # Calculate dealer's hand
                suml, _, _ = handval(house)
                sumh = suml

                # Check all the hands 
                while len(finpoint) > 0:
                    capital, finpoint, wager = wl(finpoint, sumh, capital, wager)    
                    continue
        # ======================================================================== #
        # =====================SPECIAL CASE FOR SPLIT ACES======================== #
        # ======================================================================== #




    
        # Check if any split case if left
        if any(split_queues):
            splih = True




        # Check illustrious (2 cards and no A)
        if 0 not in player and len(player) == 2:# ----> If there are 2 cards hard hands can't have an A

            double, stand, run_count = specstrat(player, house, deck, double, stand, run_count, remain_deck)

            # Deciding win or lose (if double or stand or busted)
            
            if double == True or stand == True:
                if double == True:
                    bet = bet * 2
                    wager[-1] = bet

                # Calculate player point and store
                suml, _, _ = handval(player)
                finpoint.append(suml)

                # If all split hands are done, dealer's turn 
                if splih == False:
                    house, run_count = hoturn(house, deck, run_count)
    
                    # Calculate dealer's hand
                    suml, _, _ = handval(house)
                    sumh = suml
                
                    while len(finpoint) > 0:
                        capital, finpoint, wager = wl(finpoint, sumh, capital, wager)
                
            # Check basic strat
            else:
                busted, double, stand, run_count = basicstrat(player, deck, house, run_count, stand, double, remain_deck)

                # Deciding win or lose (if double or stand or busted)

                if busted == True:
                    capital -= wager[-1]
                    wager.pop(-1)

                if double == True or stand == True:
                    if double == True:
                        bet = bet * 2
                        wager[-1] = bet

                    # Calculate player point and store
                    suml, _, _ = handval(player)
                    finpoint.append(suml)

                    # If all split hands are done, dealer's turn 
                    if splih == False:
                        house, run_count = hoturn(house, deck, run_count)

                        # Calculate dealer's hand
                        suml, _, _ = handval(house)
                        sumh = suml

                        while len(finpoint) > 0:
                            capital, finpoint, wager = wl(finpoint, sumh, capital, wager)
        
        # Check basic strat (2 cards and soft hand)
        else:
            busted, double, stand, run_count = basicstrat(player, deck, house, run_count, stand, double, remain_deck)

            # Deciding win or lose (if double or stand or busted)
            if busted == True:
                capital -= wager[-1]
                wager.pop(-1)

        
            if double == True or stand == True:
                if double == True:
                    bet = bet * 2
                    wager[-1] = bet

                # Calculate player point and store
                suml, _, _ = handval(player)
                finpoint.append(suml)

                # If all split hands are done, dealer's turn
                if splih == False:
                    house, run_count = hoturn(house, deck, run_count)

                    # Calculate dealer's hand
                    suml, _, _ = handval(house)
                    sumh = suml
                
                    while len(finpoint) > 0:
                        capital, finpoint, wager = wl(finpoint, sumh, capital, wager)
        
        # Calculate pnl
        if rounds % 5 == 0:
            pnl = capital - 1000
            x_rounds.append(rounds)
            y_pnl.append(pnl)

    max_round = x_rounds[-1]
    pnl = y_pnl[-1]

    #=================# 
    #====THE GRAPH====#
    #=================#
    plt.figure(figsize=(10,5))
    plt.plot(x_rounds, y_pnl, color="black", linewidth=1)

    plt.fill_between(x_rounds, y_pnl, 0, where=[v >= 0 for v in y_pnl], color="green", alpha=0.3, interpolate=True)
    plt.fill_between(x_rounds, y_pnl, 0, where=[v <= 0 for v in y_pnl], color="red", alpha=0.3, interpolate=True)

    plt.axhline(y = 0, color = "gray")
    plt.text(x = max_round * 0.97, y = pnl - 40, s = f"{pnl:.2f}", color = "dimgray", fontsize = 9)
    plt.plot(max_round, pnl, marker = "o", markersize = 2, color ="red")

    plt.title("PnL Tracking")
    plt.xlabel("Rounds")
    plt.ylabel("PnL")

    plt.legend()
    plt.show()
            
bj(player, house, deck)