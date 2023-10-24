import random
from env.action.utils import add_mod

def Orb_of_Alchemy(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'normal':
        reward = -10
        return iteminfo, reward

    rd = random.choices(range(4, 7), weights=(8/12, 3/12, 1/12))

    if rd[0] == 4:
        fix_type = random.choice(['s', 'p', '0'])

        if fix_type == 'p':
            iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=1)

        elif fix_type == 's':
            iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=3)

        elif fix_type == '0':
            iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

    elif rd[0] == 5:

        fix_type = random.choice(['s', 'p'])

        if fix_type == 'p':
            iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=2)

        elif fix_type == 's':
            iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=3)

    elif rd[0] == 6:
        iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=3)

    iteminfo['rarity'] = 'rare'

    return iteminfo, reward