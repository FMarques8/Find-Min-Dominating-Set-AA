import random

def throw_dice():

    return random.randint(1,6)

def throw_n_times(n):

    results ={i+1:0 for i in range(6)}

    for i in range(n+1):
        result = throw_dice()
        results[result] +=1

    return results

#throws = [10,100,1000]

""""
for t in throws:
    results = throw_n_times(t)
    print("Dice thrown {t} times".format(t=t))
    for side in range(1,7):
        print("Face {side}: {prob}%".format(side=side, prob = round(results[side]/t*100, 2)))
        """
