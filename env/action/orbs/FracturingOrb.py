import random

def Fracturing_Orb(iteminfo):
    reward = 0

    if iteminfo['status']['corrupted'] is True:
        reward = -10
        return iteminfo, reward

    if iteminfo['num_prefix'] + iteminfo['num_suffix'] < 4:
        reward = -10
        return iteminfo, reward

    if iteminfo['status']['fractured']:
        reward = -10
        return iteminfo, reward

    num = []

    for i in iteminfo['explicit']['prefix']:
        if iteminfo['explicit']['prefix'][i] != None:
            num.append(i)

        if iteminfo['explicit']['suffix'][i] != None:
            num.append(i + 3)

    rd = random.choice(num)

    if rd <= 3:
        fractured_mod = iteminfo['explicit']['prefix'].pop(rd)
        iteminfo['status']['fractured'] = fractured_mod


    elif rd > 3:
        rd = rd - 3
        fractured_mod = iteminfo['explicit']['suffix'].pop(rd)
        iteminfo['status']['fractured'] = fractured_mod

    return iteminfo, reward