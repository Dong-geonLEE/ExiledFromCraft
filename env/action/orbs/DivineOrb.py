def Divine_Orb(iteminfo):
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] == 'normal':
        reward = -10
        return iteminfo, reward

    iteminfo = iteminfo

    return iteminfo, reward