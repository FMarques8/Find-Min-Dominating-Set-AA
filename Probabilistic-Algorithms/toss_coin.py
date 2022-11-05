import random 

def toss_coin(tails_prob=0.5):

    if random.random() < tails_prob:
        return 0
    
    return 1

def toss_several(n_of_tosses ,tails_prob=0.5):

    for n in n_of_tosses:
        group_toss=[]

        for i in range(n):
            group_toss.append()

    return group_toss