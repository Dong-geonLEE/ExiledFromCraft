import random
from env.action.utils import add_mod, remove_mod

def Chaos_Orb(iteminfo):
    global_mod_file_path = 'env/src/json/global_mods.json'
    reward = 0

    if iteminfo['status']['corrupted'] == True:
        reward = -10
        return iteminfo, reward

    if iteminfo['rarity'] != 'rare':
        reward = -10
        return iteminfo, reward

    iteminfo = remove_mod(iteminfo)

    if iteminfo['status']['fractured'] == None:
        rd = random.choices(range(4, 7), weights=(8 / 12, 3 / 12, 1 / 12))

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

    else:
        rd = random.choices(population=range(3, 6),
                            weights=(8 / 12, 3 / 12, 1 / 12))

        if iteminfo['num_prefix'] > 0:
            if rd[0] == 3:
                fix_type = random.choice(['s', 'p'])

                if fix_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

                elif fix_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

            elif rd[0] == 4:

                fix_type = random.choice(['s', 'o'])

                if fix_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=3)

                elif fix_type == 'o':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

            elif rd[0] == 5:
                iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=3)

        elif iteminfo['num_suffix'] > 0:
            if rd[0] == 3:
                fix_type = random.choice(['s', 'p'])

                if fix_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=1)

                elif fix_type == 's':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=1, suffix=2)

            elif rd[0] == 4:

                fix_type = random.choice(['p', 'o'])

                if fix_type == 'p':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=1)

                elif fix_type == 'o':
                    iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=2, suffix=2)

            elif rd[0] == 5:
                iteminfo = add_mod(iteminfo, global_mod_file_path, prefix=3, suffix=2)

    return iteminfo, reward
