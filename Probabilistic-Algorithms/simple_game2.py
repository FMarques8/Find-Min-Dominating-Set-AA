import random

def throw_dice():
    
    dice1, dice2 = random.randint(1,6), random.randint(1,6)
    total = dice1+dice2

    return total

def game(guess):

    total = throw_dice()

    if guess == total:
        return guess

    else:
        return -1

attempts=1000
guess = [x for x in range(2,13)] # 1 is impossible to roll -> min = 1+1

for g in guess:
    print("Guess: {}".format(g))
    money=100
    for i in range(attempts):
        money += game(g)
    print("Total: {}".format(money))
        

