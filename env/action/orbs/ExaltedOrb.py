from env.action.utils import add_mod

def Exalted_Orb(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'rare':
        reward = -10
        return iteminfo, reward

    if iteminfo['num_prefix'] + iteminfo['num_suffix'] == 6:
        reward = -10
        return iteminfo, reward

    if iteminfo['num_prefix'] == 3:
        add_mod(iteminfo, global_mod_file_path, suffix=1)

    elif iteminfo['num_suffix'] == 3:
        add_mod(iteminfo, global_mod_file_path, prefix=1)

    else:
        add_mod(iteminfo, global_mod_file_path)

    return iteminfo, reward