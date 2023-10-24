from env.action.utils import add_mod

def Regal_Orb(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'magic':
        reward = -10
        return iteminfo, reward

    iteminfo = add_mod(iteminfo, global_mod_file_path)

    iteminfo['rarity'] = 'rare'

    return iteminfo, reward