import random

def player(prev_play, opponent_history=[], player_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    counter = {"R": "P", "P": "S", "S": "R"}
    moves = ["R", "P", "S"]
    n = 3 

    # Opening strat
    if len(opponent_history) < n:
        move = moves[len(opponent_history) % 3]
        player_history.append(move)
        return move

    # ABBEY
    if len(opponent_history) >= 3 and all(x == opponent_history[-1] for x in opponent_history[-3:]):
        move = counter[opponent_history[-1]]
        player_history.append(move)
        return move

    # KRIS
    seq = tuple(opponent_history[-n:])
    markov = {}
    for i in range(len(opponent_history) - n):
        key = tuple(opponent_history[i:i+n])
        next_move = opponent_history[i+n]
        markov[key] = markov.get(key, {})
        markov[key][next_move] = markov[key].get(next_move, 0) + 1

    if seq in markov:
        predicted = max(markov[seq], key=markov[seq].get)
        move = counter[predicted]
    else:
        recent = opponent_history[-9:]
        predicted = max(set(recent), key=recent.count)
        move = counter[predicted]

    player_history.append(move)
    return move
