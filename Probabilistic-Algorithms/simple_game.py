import random

def throw_dice():
    return random.randint(1,6), random.randint(1,6)

n = 100
winnings=0

results={'w':0, 'l':0}
for i in range(n):
    g, r = throw_dice()
    if g<r: 
        results['w']+=1
        winnings+=2
    else:
        results['l']+=1
        winnings-=1

print("Wins: {w}\tLosses:{l}".format(w=results['w'],l=results['l']))
print("Money used: {n}".format(n=n))
print("Winnings: {w}".format(w=winnings))
print("Total: {t}".format(t=winnings-n))
    

