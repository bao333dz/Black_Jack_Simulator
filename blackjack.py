import random
import matplotlib.pyplot as plt

# Black Jack

base = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # 0 is A and the 3 10s stand for JQK
deck = base * 4 * 6

# Split
def split(player, deck, hands):
    pending = 0

    for i in range(0,4):
        if len(player[i]) == 0 and pending > 0:
            player[i].append(player[i-1][0])
            p = random.choice(deck)
            deck.remove(p)
            player[i].append(p)
            pending -= 1

        if len(player[i]):  
            while player[i][0] == player[i][1] and hands < 4 and pending < 3:
                player[i].pop(1)
                p = random.choice(deck)
                deck.remove(p)
                player[i].append(p)
                hands += 1
                pending += 1

    return hands, player

# Calculate the value of the cards
def handval(m, player, hs, finpoint):
    i = player[m].count(0)

    suml = sum(player[m])
    
    # If no A
    if i == 0:
        finpoint[m] = suml
        hs[m] = "hard"
        return finpoint, hs
    
    # If only 1 A
    elif i == 1:

        # Hard
        if suml + 11 > 21:
            suml += 1
            finpoint[m] = suml
            hs[m] = "hard"
            return finpoint, hs
        
        # Soft
        else:
            suml += 11
            finpoint[m] = suml
            hs[m] = "soft"
            return finpoint, hs
        
    # If more than 1 A
    else:

        # Soft
        if suml + 11 + (i - 1) <= 21:
            suml += 11 + (i - 1)
            finpoint[m] = suml
            hs[m] = "soft"
            return finpoint, hs
        
        # Hard
        else:
            suml += i
            finpoint[m] = suml
            hs[m] = "hard"
            return finpoint, hs
        
# Take one card
def one(player, deck, run_count, t):
    p = random.choice(deck)
    deck.remove(p)
    player[t].append(p)
    if p in range(2,7):
        run_count += 1
    if p in (0,10):
        run_count -= 1
    return player, run_count
 
# Illustrious 18 (excluding the insurance case)
def specstrat(player, house, deck, double, stand, run_count, finpoint, t):
    
    # Calculate true count
    remain_deck = len(deck) / 52
    true_count = run_count / remain_deck

    # Player 10 and House 10 or House A (double)
    if finpoint[t] == 10 and true_count >= 4 and (house[0] in (0,10)) and len(player[t]) == 2:
        player, run_count = one(player, deck, run_count, t)
        double = True
        return double, stand, run_count, player

    # Player 16
    if finpoint[t] == 16:

        # 10 - 6
        if 10 in player[t] and len(player[t]) == 2:

            # House 10 (stand)
            if house[0] == 10 and true_count >= 0:
                stand = True
                return double, stand, run_count, player

        # House 9 (stand)
        if house[0] == 9 and true_count >= 5:
            stand = True
            return double, stand, run_count, player
                
    # Player 15
    if finpoint[t] == 15:

        # House 10 (stand)
        if house[0] == 10 and true_count >= 4:
            stand = True
            return double, stand, run_count, player
            
        # House 9 (stand)
        if house[0] == 9 and true_count >= 2:
            stand = True
            return double, stand, run_count, player
    
    # Player 14 and House 10 (stand)
    if finpoint[t] == 14 and house[0] == 10 and true_count >= 3:
        stand = True
        return double, stand, run_count, player
        
    # Player 13
    if finpoint[t] == 13:

        # House 2 (hit)
        if house[0] == 2 and true_count < -1:
            player, run_count = one(player, deck, run_count, t)
            return double, stand, run_count, player

        # House 3 (hit)
        if house[0] == 3 and true_count < -2:
            player, run_count = one(player, deck, run_count, t)
            return double, stand, run_count, player
    
    # Player 12
    if finpoint[t] == 12:

        # House 3 (stand)
        if house[0] == 3 and true_count >= 2:
            stand = True
            return double, stand, run_count, player
            
        # House 2 (stand)
        if house[0] == 2 and true_count >= 3:
            stand = True
            return double, stand, run_count, player
        
        # House 4 (hit)
        if house[0] == 4 and true_count < 0:
            player, run_count = one(player, deck, run_count, t)
            return double, stand, run_count, player
            
        # House 5 (hit)
        if house[0] == 5 and true_count < -2:
            player, run_count = one(player, deck, run_count, t)
            return double, stand, run_count, player

        # House 6 (hit)
        if house[0] == 6 and true_count < -1:
            player, run_count = one(player, deck, run_count, t)
            return double, stand, run_count, player

    # Player 11 and House A (double)
    if finpoint[t] == 11 and house[0] == 0 and len(player[t]) == 2:
        if true_count >= 1:
            player, run_count = one(player, deck, run_count, t)
            double = True
            return double, stand, run_count, player

    # Player 9
    if finpoint[t] == 9:

        # House 2 (double)
        if house[0] == 2 and true_count >= 1 and len(player[t]) == 2:
            player, run_count = one(player, deck, run_count, t)
            double = True
            return double, stand, run_count, player

        # House 7 (double)
        if house[0] == 7 and true_count >= 3 and len(player[t]) == 2:
            player, run_count = one(player, deck, run_count, t)
            double = True
            return double, stand, run_count, player

    return double, stand, run_count, player

# Basic Strategy 
def basicstrat(player, deck, house, run_count, stand, double, finpoint, hs, t):

    busted = False

    # Player
    while True:
        
        # Calculate the hand and determine if it hard or soft
        finpoint, hs = handval(t, player, hs, finpoint)

        # Cases for hard hands
        if hs[t] == "hard":

            # Player over 22
            if finpoint[t] > 21:
                busted = True
                return busted, double, stand, run_count, player

            # Player 17 - 21 (stand)
            if finpoint[t] in range(17,22):
                stand = True
                return busted, double, stand, run_count, player
            
            # Player 13 - 16
            if finpoint[t] in range(13,17):

                # House 2 - 6
                if house[0] in range(2,7):

                    # Store the len to see if anything happen or not
                    bf = len(player[t])

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Hit
                    if len(player[t]) != bf:
                        continue

                    # Nothing happen case (stand)
                    else:
                        stand = True
                        return busted, double, stand, run_count, player
                
                # House 7 - A
                else:

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Stand
                    if stand == True:
                        return busted, double, stand, run_count, player

                    # Nothing happen case (hit)
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue
                
            # Player 12
            if finpoint[t] == 12:

                # House 4,5,6
                if house[0] in range(4,7):
                    # Store the len 
                    bf = len(player[t])

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Hit
                    if len(player[t]) != bf:
                        continue

                    # Nothing happen case (stand)
                    else:
                        stand = True
                        return busted, double, stand, run_count, player
            
                # House 2 - 3 or 7 - A (hit)
                else:

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Stand
                    if stand == True:
                        return busted, double, stand, run_count, player

                    # Nothing happen case (hit)
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue


            # Player 11
            if finpoint[t] == 11:

                # House 2 - 10
                if house[0] in range(2,11):

                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Hit
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue

                # House A
                else:

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Double
                    if double == True:
                        return busted, double, stand, run_count, player

                    # Nothing happedn (hit)
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue
            
            # Player 10
            if finpoint[t] == 10:
                
                # House 2 - 9 (double)
                if house[0] in range(2,10):
                
                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Hit
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue

                # House 10 or A
                else:

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Double
                    if double == True:
                        return busted, double, stand, run_count, player

                    # Nothing happedn (hit)
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue
            
            # Player 9
            if finpoint[t] == 9:

                # House 3 - 6 (double)
                if house[0] in range(3, 7):
                                
                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Hit
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue
                
                # House 2 or 7 - A
                else:

                    # Checking illustrious
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # Double
                    if double == True:
                        return busted, double, stand, run_count, player

                    # Nothing happen case (hit)
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue
            
            # Player 4 - 8 (hit)
            if finpoint[t] in range(4, 9):
                player, run_count = one(player, deck, run_count, t)
                continue

        # Cases for soft hands     
        if hs[t] == "soft":

            # Player 19 - 21 (stand)
            if finpoint[t] in range(19, 22):
                stand = True
                return busted, double, stand, run_count, player
            
            # Player 18
            if finpoint[t] == 18:

                # House 3 - 6 (double if allowed)
                if house[0] in range(3,7):

                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Stand
                    else:
                        stand = True
                        return busted, double, stand, run_count, player

                # House 2, 7 or 8 (stand)
                elif house[0] == 2 or house[0] in (7,8):
                    stand = True
                    return busted, double, stand, run_count, player
                
                # House 9 to A (hit)
                else:
                    player, run_count = one(player, deck, run_count, t)
                    continue
            
            # Player 17
            if finpoint[t] == 17:

                # House 3 - 6
                if house[0] in range (3,7):

                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Hit
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue

                # House 2 or 7 - A (hit)
                else:
                    player, run_count = one(player, deck, run_count, t)
                    continue

            # Player 15, 16
            if finpoint[t] in (15, 16):

                # House 4 - 6
                if house[0] in range (4,7):

                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Hit
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue

                # House 2, 3 or 7 - A (hit)
                else:
                    player, run_count = one(player, deck, run_count, t)
                    continue
            
            # Player 13 - 14
            if finpoint[t] in (13, 14):

                # House 5, 6
                if house[0] in (5, 6):

                    # Double if allowed
                    if len(player[t]) == 2:
                        player, run_count = one(player, deck, run_count, t)
                        double = True
                        return busted, double, stand, run_count, player

                    # Hit
                    else:
                        player, run_count = one(player, deck, run_count, t)
                        continue

                # House 2 - 4 or 7 - A (hit)
                else:
                    player, run_count = one(player, deck, run_count, t)
                    continue
             
# Deciding win or lose
def wl(finpoint, sumh, capital, wager, t):

    # Tie
    if (finpoint[t] == sumh and finpoint[t] <= 21 and sumh <= 21) or (finpoint[t] > 21 and sumh > 21):
        return capital

    # House win
    elif (sumh <= 21 and finpoint[t] > 21) or (sumh <= 21 and sumh > finpoint[t]):
        capital -= wager[t]
        return capital

    # Player win
    else:
        capital += wager[t]
        return capital

# House turn
def hoturn(house, deck, run_count):

    while True:
        sumh = hocal(house)
        
        # Dealer hit or stand

        # Stand
        if sumh >= 17:
            return house, run_count

        # Hit
        else:
            h = random.choice(deck)
            deck.remove(h)
            house.append(h)
            if h in range(2,7):
                run_count += 1
            if h in (0,10):
                run_count -= 1

# Calculate val of dealer's cards
def hocal(house):
    i = house.count(0)
    
    sumh = sum(house)
    
    # If no A
    if i == 0:
        return sumh
    
    # If only 1 A
    elif i == 1:

        # Hard
        if sumh + 11 > 21:
            sumh += 1
            return sumh
        
        # Soft
        else:
            sumh += 11
            return sumh
        
    # If more than 1 A
    else:

        # Soft
        if sumh + 11 + (i - 1) <= 21:
            sumh += 11 + (i - 1)
            return sumh
        
        # Hard
        else:
            sumh += i
            return sumh

# Main
def bj (deck):
    pnl = 0
    rounds = 0
    x_rounds = []
    y_pnl = []
    x_rounds.append(0)
    y_pnl.append(pnl)
    capital = 1000
    run_count = 0
    true_count = 0

    for i in range(100000):

        # Variables that need reset every round
        busted = False
        house_blackjack = False
        player = [[],
                  [],
                  [],
                  []]
        insurance = False
        house = []
        splitace = False
        hands = 1
        wager = [0,0,0,0]
        finpoint = [0,0,0,0]
        hs = [0,0,0,0]
        insco = 0
        bustcount = 0

        # Reload the deck
        if len(deck) <= 36:
            base = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # 0 is A and the 3 10s stand for JQK
            deck = base * 4 * 6
            run_count = 0
            true_count = 0
        
        # Stop if broke
        if capital <= 10:
            pnl = capital - 1000
            x_rounds.append(rounds)
            y_pnl.append(pnl)
            break




        # FIRST THING HAPPEN: DETERMINE THE BET
        #########################################################

        remain_deck = len(deck) / 52
        true_count = run_count / remain_deck

        # Adjusting the risk (suggested by Claude-chan)
        risk = 0.001
        if true_count >= 2 and true_count < 3:
            risk = risk * 1.9
        elif true_count >= 3 and true_count < 4:
            risk = risk * 3.8
        elif true_count >= 4 and true_count < 5:
            risk = risk * 5.7
        elif true_count >= 5 and true_count < 6:
            risk = risk * 7.6
        elif true_count >= 6:
            risk = risk * 9.5

        # Calculate the size 
        bet = capital * risk
        ##########################################################




        
        # SECOND THING HAPPEN: DEALER DEAL CARDS
        ###########################################################

        # Normal deal
        for c in range(2):
            p = random.choice(deck)
            deck.remove(p)
            player[0].append(p)
            h = random.choice(deck)
            deck.remove(h)
            house.append(h)
        rounds += 1

        # Counting dealer's cards
        if house[0] in range (2,7):
            run_count += 1
        elif house[0] in (0,10):
            run_count -= 1
        ############################################################







        # THIRD THING HAPPEN (PROLLY): DEALER PEEK, IF GOT BLACKJACK, MATCH END
        ########################################################################

        # If first card is A, insurance option
        if house[0] == 0:

            remain_deck = len(deck) / 52
            insco = run_count

            # Insurance count
            for f in range(2):
                if player[0][f] in range (2,7):
                    insco += 1
                elif player[0][f] in (0,10):
                    insco -= 1

            true_count = insco / remain_deck

            if true_count >= 3:
                insurance = True

        # Check for dealer's blackjack
        if sum(house) == 10 and 10 in house:

            # Count the second card in dealer's hand
            run_count -= 1

            # Count player's card
            for f in range(2):
                if player[0][f] in range (2,7):
                    run_count += 1
                elif player[0][f] in (0,10):
                    run_count -= 1

            # Insurance cases
            if insurance == True:
                capital += bet
                    

            # Check if player got a blackjack or not
            if sum(player[0]) == 10 and 10 in player[0]:
                # Calculate pnl
                pnl = capital - 1000
                x_rounds.append(rounds)
                y_pnl.append(pnl)
                continue
            else:
                capital -= bet
                # Calculate pnl
                pnl = capital - 1000
                x_rounds.append(rounds)
                y_pnl.append(pnl)
                continue

        # Player got blackjack dealer don't
        else:
            if insurance == True:
                capital -= bet * 0.5

            if sum(player[0]) == 10 and 10 in player[0]:

                # Count the second card in dealer's hand
                if house[1] in range (2,7):
                    run_count += 1
                elif house[1] in (0,10):
                    run_count -= 1
    
                # Count player's card
                for f in range(2):
                    if player[0][f] in range (2,7):
                        run_count += 1
                    elif player[0][f] in (0,10):
                        run_count -= 1
                capital += bet * 1.5
                # Calculate pnl
                pnl = capital - 1000
                x_rounds.append(rounds)
                y_pnl.append(pnl)
                continue
        ########################################################################



        # FOURTH THING HAPPEN: SPLIT THE CARDS
        ########################################################################
        
        if player[0][0] == player[0][1]:

            # A and 8
            if player[0][0] in (0,8):
                if player[0][0] == 0:
                    splitace = True
                hands, player = split(player, deck, hands)
            
            # 9
            if player[0][0] == 9 and house[0] in range(2,10) and house[0] != 7:
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
        ########################################################################





        # FIFTH THING HAPPEN: SOME STUFF
        #######################################################################

        # Place the wager(s)
        for w in range(0, len(player)):
            if len(player[w]) > 0: 
                wager[w] = bet

        # Loop through the hands for card counting
        for o in range(0, hands):

            # Counting player's cards
            for k in range(0, len(player[o])):
                if player[o][k] in range(2,7):
                    run_count += 1
                elif player[o][k] in (0,10):
                    run_count -= 1

        # Calculate hand
        for m in range(0, len(player)):
            if len(player[m]) > 0:
                finpoint, hs = handval(m, player, hs, finpoint)
        ########################################################################





        # SIXTH THING HAPPEN (PROLLY): SPLIT ACE CASE
        #######################################################################

        # If split aces case
        if splitace == True:
            
            # House turn
            house, run_count = hoturn(house, deck, run_count)
            sumh = hocal(house)
            # Count second card
            if house[1] in range(2, 7):
                run_count += 1
            if house[1] in (0, 10):
                run_count -= 1

            for a in range(0, len(player)):

                if len(player[a]) > 0: 
                    capital = wl(finpoint, sumh, capital, wager, a)

            # Calculate pnl
            pnl = capital - 1000
            x_rounds.append(rounds)
            y_pnl.append(pnl)
            continue
        #######################################################################






        # SEVENTH THING HAPPEN: MAIN ACTION FOR PLAYER
        #######################################################################



        # Loop for the main actions
        for t in range(0, len(player)):

            stand = False
            double = False

            if len(player[t]) > 0:
                # If hard hands, check illustrious 18
                if 0 not in player[t]:
                    double, stand, run_count, player = specstrat(player, house, deck, double, stand, run_count, finpoint, t)

                    # End player's turn
                    if stand == True or double == True:

                        # Double the bet
                        if double == True:
                            wager[t] = bet * 2

                        # Calculate player's hand
                        finpoint, hs = handval(t, player, hs, finpoint)


                    else:

                        # Check basic strat
                        busted, double, stand, run_count, player = basicstrat(player, deck, house, run_count, stand, double, finpoint, hs, t)

                        # End player's turn

                        # Busted
                        if busted == True:
                            capital -= wager[t]
                            player[t] = []
                            bustcount += 1
                            continue

                        # Double or stand
                        if double == True or stand == True:

                            # Double the bet
                            if double == True:
                                wager[t] = bet * 2
                            
                            # Calculate player's hand
                            finpoint, hs = handval(t, player, hs, finpoint)

                else:
                
                    # Check basic strat
                    busted, double, stand, run_count, player = basicstrat(player, deck, house, run_count, stand, double, finpoint, hs, t)

                    # End player's turn

                    # Busted
                    if busted == True:
                        capital -= wager[t]
                        player[t] = []
                        bustcount += 1
                        continue

                    # Double or stand
                    if double == True or stand == True:

                        # Double the bet
                        if double == True:
                            wager[t] = bet * 2
                        
                        # Calculate player's hand
                        finpoint, hs = handval(t, player, hs, finpoint)
        ##################################################################################





        # EIGHTH THING HAPPEN: DEALER'S TURN
        #################################################################################

        # Count second card
        if house[1] in range(2, 7):
            run_count += 1
        if house[1] in (0, 10):
            run_count -= 1

        # Dealer's turn
        if bustcount < hands:
            house, run_count = hoturn(house, deck, run_count)
            sumh = hocal(house)
        ##################################################################################





        # NINTH THING HAPPEN: NOW WE WRAP IT UPPP
        ##################################################################################

        # Loop to check if win or lose
        for l in range(0, len(player)):
            if len(player[l]) > 0:
                capital = wl(finpoint, sumh, capital, wager, l)
        ##################################################################################

        
        # Calculate pnl
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
            
print(bj(deck))