import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# suits: 0 > spade, 1 > club, 2 > heart, 3 > diamond
def drawcard(prev_cards):
    chosen = np.array([])
    while (len(chosen) == 0):
        # choose suit
        suit = np.floor(np.random.uniform(0, 4))
        # choose value
        # 1 > Ace, 2 - 9 > 2 - 9, 11 > J, 12 > Q, 13 > K
        value = np.floor(np.random.uniform(1, 14))
        if (not np.any(np.all(prev_cards == np.array([suit, value]), axis=1))):
            chosen = np.array([suit, value])
    return chosen

def card_val(card):
    if (card[1] == 1):
        return -1
    if (card[1] == 13 or card[1] == 12 or card[1] == 11):
        return 10
    else:
        return card[1]

def hand_sum_calc(cards):
    aces = 0
    total = 0
    for card in cards:
        if card_val(card) == -1:
            aces += 1
        else:
            total += card_val(card)
    if aces > 0:
        if ((total + aces - 1 + 11) <= 21):
            total =  total + aces - 1 + 11
        else:
            total = (total + aces)
    if (total == 21 and len(cards == 2)):
        return -1
    return total


def handsum_upcard_game(start_hand, upcard, cutoff):
    shown_cards = np.append(start_hand, upcard, axis=0)
    player_hand = start_hand
    player_hand_sum = hand_sum_calc(start_hand)
    # check for blackjack
    if (not player_hand_sum == -1):
        # player turn
        while (player_hand_sum < cutoff):
            new_card = drawcard(shown_cards)
            player_hand = np.append(player_hand, np.array([new_card]), axis=0)
            player_hand_sum = hand_sum_calc(player_hand)
            shown_cards = np.append(shown_cards, np.array([new_card]), axis=0)
    if (player_hand_sum > 21):
        # print('PH:', player_hand)
        return 0
    else:
        dealer_hand = upcard
        dealer_hand_sum = hand_sum_calc(dealer_hand)
        second_card = 0
        # dealer turn
        while (dealer_hand_sum < 17):
            if (second_card == 0):
                new_card = drawcard(shown_cards)
                dealer_hand = np.append(dealer_hand, np.array([new_card]), axis=0)
                dealer_hand_sum = hand_sum_calc(dealer_hand)
                if (dealer_hand_sum == -1):
                    if (player_hand_sum == -1):
                            # print('PH:', player_hand)
                            # print('DH:', dealer_hand)
                            return 100
                    return 0
                else:
                    if (player_hand_sum == -1):
                        # print('PH:', player_hand)
                        # print('DH:', dealer_hand)
                        return 250
                shown_cards = np.append(shown_cards, np.array([new_card]), axis=0)
                second_card = 1
            else:
                new_card = drawcard(shown_cards)
                dealer_hand = np.append(dealer_hand, np.array([new_card]), axis=0)
                dealer_hand_sum = hand_sum_calc(dealer_hand)
                shown_cards = np.append(shown_cards, np.array([new_card]), axis=0)
        # print('DH:', dealer_hand)
        # print('PH:', player_hand)
        if (dealer_hand_sum > 21):
            return 200
        elif (dealer_hand_sum > player_hand_sum):
            return 0
        elif (dealer_hand_sum < player_hand_sum):
            return 200
        return 100
        
def average_for_upcard_for_cutoff(upcard_val, cutoff):
    # upcard_val = upcard[0][1]
    total_count = 0
    win_total = 0
    # different cards not upcard
    for i in range(1, 14):
        for j in range(1, 14):
            if (i != upcard_val and j != upcard_val and i != j):
                total_count += 16
                for k in range(16):
                    win = handsum_upcard_game(np.array([[0, i], [0, j]]), np.array([[1, upcard_val]]), cutoff)
                    win_total += win
            if (i == upcard_val and j != upcard_val):
                total_count += 12
                for k in range(12):
                    win = handsum_upcard_game(np.array([[0, i], [0, j]]), np.array([[1, upcard_val]]), cutoff)
                    win_total += win
            if (i != upcard_val and j != upcard_val and i == j):
                total_count += 6
                for k in range(6):
                    win = handsum_upcard_game(np.array([[0, i], [0, j]]), np.array([[1, upcard_val]]), cutoff)
                    win_total += win
            if (i == upcard_val and j == upcard_val):
                total_count += 3
                for k in range(3):
                    win = handsum_upcard_game(np.array([[0, i], [0, j]]), np.array([[1, upcard_val]]), cutoff)
                    win_total += win
    return (win_total / total_count)

cutoffs = [i for i in range(11, 21)]
def cutoff_avs_for_upcard(upcard_val):
    cutoff_avs = []
    for cutoff in cutoffs:
        cutoff_tot = 0
        for i in range(1):
            cutoff_tot += average_for_upcard_for_cutoff(upcard_val, cutoff)
        cutoff_avs.append(cutoff_tot / 1)
    print(cutoff_avs)
    return cutoff_avs
cutoff_res = [cutoff_avs_for_upcard(i) for i in range(1, 14)]
colormap = cm.get_cmap('tab20', 13)
colors = [colormap(i) for i in range(13)]
plt.figure(figsize=(15, 15))
for i in range(1, 14):
    plt.plot(cutoffs, np.log(cutoff_res[i-1]), marker='o', linestyle='-', color=colors[i-1], label=f'Dealer Upcard: {i}')
plt.xlabel('Cutoff Point')
plt.ylabel('Log of Average Payout for 100 Bet')
plt.legend(loc='lower left')
plt.savefig("Figure1.png", dpi=300)

