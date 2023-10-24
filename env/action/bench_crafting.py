import json
import random

def Bench_Crafting(iteminfo, crafting_mod=None):
    crafting_file_path = 'env/src/json/crafting_bench_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] is True:
        reward = -10
        return iteminfo, reward

    with open(crafting_file_path) as ff:
        craft_dict = json.load(ff)

    base = iteminfo['base']

    if base in ['bone_ring', 'convoking_wand', 'bone_spirit_shield']:
        if base == 'bone_ring':
            base = 'ring'
        elif base == 'convoking_wand':
            base = 'wand'
        elif base == 'bone_spirit_shield':
            base = 'shield(int_shield)'

    if crafting_mod is None:
        bench_class = craft_dict[iteminfo['base']]['default']
        bench_keys = list(bench_class.keys())

        crafting_mod = random.choices(population=bench_keys)[0]

    if 'Einhar' in crafting_mod or 'CannotChange' in crafting_mod:
        bench_class = craft_dict[base]['default']

    elif 'Jun' in crafting_mod:
        bench_class = craft_dict[base]['veil']

    if bench_class[crafting_mod]['generation_type'] == 'prefix':
        if iteminfo['num_prefix'] >= 3:
            reward = -10
            return iteminfo, reward

        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] is None:
                iteminfo['explicit']['prefix'][p] = crafting_mod

                if iteminfo['status']['crafted'] == 'StrIntMasterItemGenerationCanHaveMultipleCraftedMods':
                    v = 0

                else:
                    iteminfo['tag']['mod_groups'][crafting_mod] = bench_class[crafting_mod]['groups'][0]
                    iteminfo['tag']['implicits_tag'][crafting_mod] = bench_class[crafting_mod]['implicit_tags']
                    iteminfo['num_prefix'] += 1

                break

    elif bench_class[crafting_mod]['generation_type'] == 'suffix':
        if iteminfo['num_suffix'] >= 3:
            reward = -10
            return iteminfo, reward

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] == None:
                iteminfo['explicit']['suffix'][s] = crafting_mod
                iteminfo['tag']['mod_groups'][crafting_mod] = bench_class[crafting_mod]['groups'][0]
                iteminfo['tag']['implicits_tag'][crafting_mod] = bench_class[crafting_mod]['implicit_tags']
                iteminfo['num_suffix'] += 1
                break

    iteminfo['status']['crafted'] = crafting_mod

    if 1 <= iteminfo['num_prefix'] + iteminfo['num_suffix'] <= 2:
        iteminfo['rarity'] = 'magic'

    elif iteminfo['num_prefix'] + iteminfo['num_suffix'] >= 3:
        iteminfo['rarity'] = 'rare'

    return iteminfo, reward


def Aisling_Veil_Crafting(iteminfo):
    reward = 0

    if iteminfo['status']['corrupted'] is True:
        reward = -10
        return iteminfo, reward

    if iteminfo['status']['crafted'] == 'veiled':
        reward = - 10
        return iteminfo, reward

    if iteminfo['num_prefix'] + iteminfo['num_suffix'] == 0:
        rd = random.choice(['p', 's'])

        if rd == 'p':
            iteminfo['explicit']['prefix'][rd] = 'veiled'
            iteminfo['num_prefix'] += 1

        elif rd == 's':
            iteminfo['explicit']['suffix'][rd] = 'veiled'
            iteminfo['num_suffix'] += 1

    elif iteminfo['num_prefix'] + iteminfo['num_suffix'] < 6:
        empty_pos = []

        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] is None:
                empty_pos.append(p)

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] is None:
                empty_pos.append(s + 3)

        rd = int(random.choices(population=empty_pos)[0])

        if rd <= 3:
            iteminfo['explicit']['prefix'][rd] = 'veiled'
            iteminfo['num_prefix'] += 1

        elif rd > 3:
            rd -= 3
            iteminfo['explicit']['suffix'][rd] = 'veiled'
            iteminfo['num_suffix'] += 1

    elif iteminfo['num_prefix'] + iteminfo['num_suffix'] >= 6:

        current_num = []

        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] != None:
                current_num.append(p)

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] != None:
                current_num.append(s + 3)

        rd = random.choices(population=current_num)[0]

        if rd <= 3:
            rm_mod = iteminfo['explicit']['prefix'][rd]
            iteminfo['tag']['mod_groups'].pop(rm_mod)
            iteminfo['tag']['implicits_tag'].pop(rm_mod)
            iteminfo['explicit']['prefix'] = 'veiled'

        if rd > 3:
            rd -= 3
            rm_mod = iteminfo['explicit']['suffix'][rd]
            iteminfo['tag']['mod_groups'].pop(rm_mod)
            iteminfo['tag']['implicits_tag'].pop(rm_mod)
            iteminfo['explicit']['suffix'] = 'veiled'

    iteminfo['status']['crafted'] = 'veiled'
    iteminfo['tag']['mod_groups']['veiled'] = 'veiled'
    iteminfo['tag']['implicits_tag']['veiled'] = 'veiled'

    return iteminfo, reward