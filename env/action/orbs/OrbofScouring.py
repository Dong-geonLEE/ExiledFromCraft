from env.action.utils import remove_mod

def Orb_of_Scouring(iteminfo):
    reward = 0

    if iteminfo['rarity'] == 'normal':
        reward = -10
        return iteminfo, reward

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if 'StrMasterItemGenerationCannotChangePrefixes' in iteminfo['explicit']['suffix']:
        iteminfo = remove_mod(iteminfo, num_pre_to_remove=0, num_suf_to_remove=iteminfo['num_suffix'])
        if iteminfo['num_prefix'] == 1:
            iteminfo['rarity'] == 'magic'

    elif 'DexMasterItemGenerationCannotChangeSuffixes' in iteminfo['explicit']['prefix']:
        iteminfo = remove_mod(iteminfo, num_pre_to_remove=iteminfo['num_prefix'], num_suf_to_remove=0)
        if iteminfo['num_suffix'] == 1:
            iteminfo['rarity'] == 'magic'

    else:
        iteminfo = remove_mod(iteminfo, num_pre_to_remove=0, num_suf_to_remove=0)
        iteminfo['rarity'] = 'normal'

    return iteminfo, reward