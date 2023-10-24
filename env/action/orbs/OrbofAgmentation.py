from env.action.utils import add_mod

def Orb_of_Agumentation(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'magic':
        reward = -10
        return iteminfo, reward

    if iteminfo['num_prefix'] == 1 and iteminfo['num_suffix'] == 1:
        reward = -10
        return iteminfo, reward

    elif iteminfo['num_prefix'] == 0:
        iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1)

    elif iteminfo['num_suffix'] == 0:
        iteminfo = add_mod(iteminfo, global_mod_file_path, suffix=1)

    return iteminfo, reward