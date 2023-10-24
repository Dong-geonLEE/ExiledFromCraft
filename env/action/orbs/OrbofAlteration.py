import random
from env.action.utils import add_mod, remove_mod

def Orb_of_Alteration(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'magic':
        reward = -10
        return iteminfo, reward

    iteminfo = remove_mod(iteminfo)

    num = random.choices(range(1, 3), weights=[0.5, 0.5])

    if num[0] == 1:
        iteminfo = add_mod(iteminfo, global_mod_file_path)

    elif num[0] == 2:
        iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1)
        iteminfo = add_mod(iteminfo, global_mod_file_path, suffix=1)

    return iteminfo, reward