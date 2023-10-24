import json
import random

from env.action.utils import add_mod, remove_mod

def _moding_Essesnce(iteminfo, mods):
    mod_file_path = 'RePoE/RePoE/data/mods.json'
    global_mod_file_path = 'env/src/json/global_mods.json'
    essence_mod_file_path = 'env/src/json/essences_mods.json'

    with open(mod_file_path) as f:
        global_mods = json.load(f)

    with open(essence_mod_file_path) as ff:
        es_mods = json.load(ff)

    essence_mod = es_mods.get(mods, {})

    if essence_mod == {}:
        essence_mod = global_mods[mods]

    if essence_mod['generation_type'] == 'prefix':
        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] is None:
                iteminfo['explicit']['prefix'][p] = mods
                iteminfo['tag']['mod_groups'][mods] = essence_mod['groups'][0]
                iteminfo['tag']['implicits_tag'][mods] = essence_mod['implicit_tags']
                iteminfo['num_prefix'] += 1
                break

        if iteminfo['status']['fractured']:
            rd = random.choices(range(2, 5), weights=(8/12, 3/12, 1/12))[0]

        else:
            rd = random.choices(range(3, 6), weights=(8/12, 3/12, 1/12))[0]

        for r in range(rd):
            iteminfo = add_mod(iteminfo, global_mod_file_path)

    elif essence_mod['generation_type'] == 'suffix':
        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] is None:
                iteminfo['explicit']['suffix'][s] = mods
                iteminfo['tag']['mod_groups'][mods] = essence_mod['groups'][0]
                iteminfo['tag']['implicits_tag'][mods] = essence_mod['implicit_tags']
                iteminfo['num_suffix'] += 1
                break

        if iteminfo['status']['fractured']:
            rd = random.choices(range(2, 5), weights=(8 / 12, 3 / 12, 1 / 12))[0]

        else:
            rd = random.choices(range(3, 6), weights=(8 / 12, 3 / 12, 1 / 12))[0]

        for r in range(rd):
            iteminfo = add_mod(iteminfo, global_mod_file_path)

    return iteminfo

def Essences_name():
    with open('RePoE/RePoE/data/essences.json') as f:
        es = json.load(f)

    es_list = list(es.keys())
    es_list.remove('Metadata/Items/Currency/CurrencyCorruptMonolith')
    e = random.choice(es_list)

    return es[e]['name']


def Essences(iteminfo, essence_name):
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] == 'magic':
        reward = -10
        return iteminfo, reward

    with open('RePoE/RePoE/data/essences.json') as f:
        es = json.load(f)

    itemclass = iteminfo['base'].capitalize()

    if '(' in itemclass:
        ic = itemclass.split('(')
        itemclass = ic[0]

        if itemclass == 'Body_armour':
            itemclass = 'Body Armour'

    elif itemclass in ['Axe', 'Mace', 'Sword']:
        itemclass = 'One Hand ' + itemclass

    elif itemclass == 'Rapier':
        itemclass = 'Thrusting One Hand Sword'

    elif itemclass == 'Attack_dagger':
        itemclass = 'One Hand Sword'

    elif itemclass == 'Attack_staff':
        itemclass = 'Staff'

    elif itemclass == 'Two_hand_axe':
        itemclass = 'Two Hand Axe'

    elif itemclass == 'Two_hand_mace':
        itemclass = 'Two Hand Mace'

    elif itemclass == 'Two_hand_sword':
        itemclass = 'Two Hand Sword'

    elif itemclass in ['Unset_ring', 'Bone_ring']:
        itemclass = 'Ring'

    elif itemclass == 'Convoking_wand':
        itemclass = 'Wand'

    elif itemclass == 'Bone_spirit_shield':
        itemclass = 'Shield'

    for e in es:
        if es[e]['name'] == essence_name:
            # 타락의 유물
            if e != 'Metadata/Items/Currency/CurrencyCorruptMonolith':
                mods = es[e]['mods'][itemclass]

            else:
                reward = -10
                return iteminfo, reward

    if (es[e]['level'] < 5) and (iteminfo['rarity'] != 'normal'):
        reward = -10
        return iteminfo, reward

    iteminfo = remove_mod(iteminfo, 0, 0)
    iteminfo = _moding_Essesnce(iteminfo, mods)

    iteminfo['rarity'] = 'rare'
    return iteminfo, reward