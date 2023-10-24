import random
import json
from env.action.utils import add_mod, remove_mod

def Veiled_Chaos_Orb(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    crafting_mod_file_path = 'env/src/json/crafting_bench_mods.json'
    reward = 0
    veil_type = ''

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'rare':
        reward = -10
        return iteminfo, reward

    if iteminfo['status']['fractured']:
        rd = random.choices(range(3, 6), weights=(8 / 12, 3/ 12, 1/ 12))[0]

        iteminfo = remove_mod(iteminfo)

        if rd == 3:
            fix_type = random.choice(['s', 'p'])

            if fix_type == 'p':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=1)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2)

            elif fix_type == 's':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, suffix=2)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=1)

        elif rd == 4:
            fix_type = random.choice(['s', 'p', 'o'])

            if fix_type == 'p':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

                elif veil_type == 's':
                    if iteminfo['num_prefix'] == 1:
                        iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

                    elif iteminfo['num_suffix'] == 1:
                        iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3)

            elif fix_type == 's':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    if iteminfo['num_prefix'] == 1:
                        iteminfo = add_mod(iteminfo, global_mod_file_path, suffix=3)

                    elif iteminfo['num_suffix'] == 1:
                        iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

            elif fix_type == 'o':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

        elif rd == 5:
            if iteminfo['num_prefix'] == 1:
                veil_type = random.choice(['p', 's'])

                if veil_type == ['p']:
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=3)

                elif veil_type == ['s']:
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

            elif iteminfo['num_suffix'] == 1:
                veil_type = random.choice(['p', 's'])

                if veil_type == ['p']:
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

                elif veil_type == ['s']:
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=1)

    else:
        rd = random.choices(range(4, 7), weights=(8 / 12, 3 / 12, 1 / 12))

        iteminfo = remove_mod(iteminfo)

        if rd[0] == 4:
            fix_type = random.choice(['s', 'p', '0'])

            if fix_type == 'p':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3)

            elif fix_type == 's':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, suffix=3)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

            elif fix_type == '0':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

        elif rd[0] == 5:
            fix_type = random.choice(['s', 'p'])

            if fix_type == 'p':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=1)

            elif fix_type == 's':
                veil_type = random.choice(['p', 's'])

                if veil_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=3)

                elif veil_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

        elif rd[0] == 6:
            veil_type = random.choice(['p', 's'])

            if veil_type == 'p':
                iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=3)

            elif veil_type == 's':
                iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=2)

    with open(crafting_mod_file_path) as fff:
        craft_mod_dict = json.load(fff)

    veil_mod_dict = craft_mod_dict[iteminfo['base']]['veil']

    if veil_type == 'p':
        finding_mod = False

        while finding_mod is False:
            veil_mod = random.choice(list(veil_mod_dict.keys()))
            if veil_mod_dict[veil_mod]['generation_type'] == 'prefix':
                finding_mod = True

        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] is None:
                iteminfo['explicit']['prefix'][p] = veil_mod
                iteminfo['tag']['mod_groups'][veil_mod] = veil_mod_dict[veil_mod]['groups'][0]
                iteminfo['tag']['implicits_tag'][veil_mod] = veil_mod_dict[veil_mod]['implicit_tags']
                iteminfo['num_prefix'] += 1
                break

    elif veil_type == 's':
        finding_mod = False

        while finding_mod is False:
            veil_mod = random.choice(list(veil_mod_dict.keys()))
            if veil_mod_dict[veil_mod]['generation_type'] == 'suffix':
                finding_mod = True

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] is None:
                iteminfo['explicit']['suffix'][s] = veil_mod
                iteminfo['tag']['mod_groups'][veil_mod] = veil_mod_dict[veil_mod]['groups'][0]
                iteminfo['tag']['implicits_tag'][veil_mod] = veil_mod_dict[veil_mod]['implicit_tags']
                iteminfo['num_suffix'] += 1
                break

    return iteminfo, reward