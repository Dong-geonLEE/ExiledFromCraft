import random as rd

def Orb_of_Annulment(iteminfo):
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['num_prefix'] + iteminfo['num_suffix'] == 0:
        reward = -10
        return iteminfo, reward

    exp_num = []

    for i in iteminfo['explicit']['prefix']:
        if iteminfo['explicit']['prefix'][i] != None:
            exp_num.append(i)

    for i in iteminfo['explicit']['suffix']:
        if iteminfo['explicit']['suffix'][i] != None:
            exp_num.append(i + 3)

    r = rd.choice(exp_num)

    if r <= 3:
        r_mod = iteminfo['explicit']['prefix'][r]

        iteminfo['tag']['implicits_tag'].pop(r_mod)
        iteminfo['tag']['mod_groups'].pop(r_mod)

        iteminfo['explicit']['prefix'][r] = None
        iteminfo['num_prefix'] -= 1

    elif r > 3:
        r = r - 3
        r_mod = iteminfo['explicit']['suffix'][r]

        iteminfo['tag']['implicits_tag'].pop(r_mod)
        iteminfo['tag']['mod_groups'].pop(r_mod)

        iteminfo['explicit']['suffix'][r] = None
        iteminfo['num_suffix'] -= 1

    return iteminfo, reward