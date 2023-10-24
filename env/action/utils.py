import random
import json

def _checking_mod_group(iteminfo_tag_groups, group):
    current_groups = iteminfo_tag_groups.values()

    for g in current_groups:
        if g == group:
            return False

    # False: 중복, True: 괜찮음
    return True

def item_to_observation(iteminfo):
    """
    :param
        iteminfo: item's information in environment as dictionary form
    :return:
        observation: item's current status as set form
        (class, level, rarity, status, mod1, mod2, mod3, mod4, mod5, mod6, head_implicits)
    """

    observation = []

    item_types = {'sceptre': 0, 'claw': 1, 'mace': 2, 'axe': 3, 'wand': 4, 'rapier': 5, 'sword': 6, 'dagger': 7,
                  'attack_dagger': 8, 'two_hand_sword': 9, 'two_hand_axe': 10, 'two_hand_mace': 11, 'bow': 12,
                  'staff': 13, 'attack_staff': 14, 'amulet': 15, 'ring': 16, 'belt': 17, 'gloves(str_armour)': 18,
                  'gloves(dex_armour)': 19, 'gloves(int_armour)': 20, 'gloves(str_dex_armour)': 21,
                  'gloves(str_int_armour)': 22, 'gloves(dex_int_armour)': 23, 'boots(str_armour)': 24,
                  'boots(dex_armour)': 25, 'boots(int_armour)': 26, 'boots(str_dex_armour)': 27,
                  'boots(str_int_armour)': 28, 'boots(dex_int_armour)': 29, 'helmet(str_armour)': 30,
                  'helmet(dex_armour)': 31, 'helmet(int_armour)': 32, 'helmet(str_dex_armour)': 33,
                  'helmet(str_int_armour)': 34, 'helmet(dex_int_armour)': 35, 'body_armour(str_armour)': 36,
                  'body_armour(dex_armour)': 37, 'body_armour(int_armour)': 38, 'body_armour(str_dex_armour)': 39,
                  'body_armour(str_int_armour)': 40, 'body_armour(dex_int_armour)': 41,
                  'body_armour(str_dex_int_armour)': 42, 'quiver': 43, 'shield(str_shield)': 44,
                  'shield(dex_shield)': 45, 'shield(int_shield)': 46, 'shield(str_dex_shield)': 47,
                  'shield(str_int_shield)': 48, 'shield(dex_int_shield)': 49, 'unset_ring': 50,
                  'bone_ring': 51, 'convoking_wand': 52, 'bone_spirit_shield': 53}

    item_class = item_types[iteminfo['base']]
    observation.append(item_class)
    observation.append(iteminfo['item_level'])

    rarity = -1
    if iteminfo['rarity'] == 'normal':
        rarity = 0

    elif iteminfo['rarity'] == 'magic':
        rarity = 1

    elif iteminfo['rarity'] == 'rare':
        rarity = 2

    observation.append(rarity)

    status = 0
    mods = []

    # "status": {'influence': None, 'corrupted': False, 'fractured': None, 'crafted': None}

    if iteminfo['status']['influence']:
        status += 8

    if iteminfo['status']['corrupted']:
        status += 4

    if iteminfo['status']['fractured']:
        status += 2
        mods.append(iteminfo['status']['fractured'])

    if iteminfo['status']['crafted']:
        status += 1

    observation.append(status)

    # from mod1 ~ mod6

    for p in iteminfo['explicit']['prefix']:
        mods.append(iteminfo['explicit']['prefix'][p])

    for s in iteminfo['explicit']['suffix']:
        mods.append(iteminfo['explicit']['suffix'][s])

    with open('env/src/json/mods_num.json') as f:
        mods_num_dict = json.load(f)

    for m in mods:
        if m is None:
            observation.append(-1)

        elif m == 'veiled':
            observation.append(-2)

        else:
            num = mods_num_dict[m]
            observation.append(num)

    if iteminfo['head_implicit']:
        head = iteminfo['head_implicit'].values()
        for h in head:
            num = mods_num_dict[h]
            observation.append(num)
            break

    else:
        observation.append(-1)

    return observation

def add_mod(iteminfo, file_path, prefix=0, suffix=0):
    with open(file_path) as ff:
        mod_dict = json.load(ff)

    if iteminfo['num_prefix'] + iteminfo['num_suffix'] >= 6:
        reward = -10
        return iteminfo

    # add a mod w/o consideration about prefix or suffix
    if prefix == 0 and suffix == 0:
        valid_position = False
        while valid_position is False:
            mod = random.choices(population=list(mod_dict[iteminfo['base']].keys()),
                                 weights=mod_dict[iteminfo['base']]['mod_weight'])

            if mod_dict[iteminfo['base']][mod[0]]['required_level'] > iteminfo['item_level']:
                continue

            position = mod_dict[iteminfo['base']][mod[0]]['generation_type']

            if (position == 'prefix' and iteminfo['num_prefix'] >= 3) or (
                    position == 'suffix' and iteminfo['num_suffix'] >= 3):
                continue

            tag_group = mod_dict[iteminfo['base']][mod[0]]['groups'][0]

            # 접두어 변경불가, 접미어 변경불가

            if _checking_mod_group(iteminfo['tag']['mod_groups'], tag_group):
                valid_position = True

        explicits = iteminfo['explicit'][position]

        for (k, v) in explicits.items():
            if v is None:
                explicits[k] = mod[0]
                break

        iteminfo['explicit'][position] = explicits
        iteminfo['tag']['mod_groups'][mod[0]] = tag_group
        iteminfo['tag']['implicits_tag'][mod[0]] = mod_dict[iteminfo['base']][mod[0]]['implicit_tags']

        if position == 'prefix':
            iteminfo['num_prefix'] += 1
        elif position == 'suffix':
            iteminfo['num_suffix'] += 1

    else:
        while prefix > 0:
            if iteminfo['num_prefix'] >= 3:
                reward = -10
                return iteminfo

            valid_position = False
            while valid_position is False:
                mod = random.choices(population=list(mod_dict[iteminfo['base']].keys()),
                                     weights=mod_dict[iteminfo['base']]['mod_weight'])

                if mod_dict[iteminfo['base']][mod[0]]['required_level'] > iteminfo['item_level']:
                    continue

                position = mod_dict[iteminfo['base']][mod[0]]['generation_type']

                if position == 'suffix':
                    continue

                tag_group = mod_dict[iteminfo['base']][mod[0]]['groups'][0]

                if _checking_mod_group(iteminfo['tag']['mod_groups'], tag_group):
                    valid_position = True

            explicits = iteminfo['explicit']['prefix']

            for (k, v) in explicits.items():
                if v is None:
                    explicits[k] = mod[0]
                    break

            iteminfo['explicit']['prefix'] = explicits
            iteminfo['tag']['mod_groups'][mod[0]] = tag_group
            iteminfo['tag']['implicits_tag'][mod[0]] = mod_dict[iteminfo['base']][mod[0]]['implicit_tags']
            iteminfo['num_prefix'] += 1
            prefix -= 1

        while suffix > 0:
            if iteminfo['num_suffix'] >= 3:
                reward = -10
                return iteminfo

            valid_position = False
            while valid_position is False:
                mod = random.choices(population=list(mod_dict[iteminfo['base']].keys()),
                                     weights=mod_dict[iteminfo['base']]['mod_weight'])

                if mod_dict[iteminfo['base']][mod[0]]['required_level'] > iteminfo['item_level']:
                    continue

                position = mod_dict[iteminfo['base']][mod[0]]['generation_type']

                if position == 'prefix':
                    continue

                tag_group = mod_dict[iteminfo['base']][mod[0]]['groups'][0]

                if _checking_mod_group(iteminfo['tag']['mod_groups'], tag_group):
                    valid_position = True

            explicits = iteminfo['explicit']['suffix']

            for (k, v) in explicits.items():
                if v is None:
                    explicits[k] = mod[0]
                    break

            iteminfo['explicit']['suffix'] = explicits
            iteminfo['tag']['mod_groups'][mod[0]] = tag_group
            iteminfo['tag']['implicits_tag'][mod[0]] = mod_dict[iteminfo['base']][mod[0]]['implicit_tags']
            iteminfo['num_suffix'] += 1
            suffix -= 1

    return iteminfo

def remove_mod(iteminfo, num_pre_to_remove=0, num_suf_to_remove=0):
    if num_pre_to_remove > iteminfo['num_prefix'] or num_suf_to_remove > iteminfo['num_suffix']:
        raise Exception("Number of mod you request to remove is over item's mod number")

    if num_pre_to_remove == 0 and num_suf_to_remove == 0:
        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] != None:
                pp = iteminfo['explicit']['prefix'][p]

                iteminfo['tag']['mod_groups'].pop(pp, None)
                iteminfo['tag']['implicits_tag'].pop(pp, None)

                iteminfo['explicit']['prefix'][p] = None
                iteminfo['num_prefix'] -= 1

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] != None:
                ss = iteminfo['explicit']['suffix'][s]

                iteminfo['tag']['mod_groups'].pop(ss, None)
                iteminfo['tag']['implicits_tag'].pop(ss, None)

                iteminfo['explicit']['suffix'][s] = None
                iteminfo['num_suffix'] -= 1

        iteminfo['status']['crafted'] = None

    else:

        prefix = []
        suffix = []

        for mod in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][mod] != None:
                prefix.append(mod)

        for mod in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][mod] != None:
                suffix.append(mod)

        num = random.sample(prefix, k=num_pre_to_remove)

        for i in num:
            iteminfo['tag']['mod_groups'].pop(iteminfo['explicit']['prefix'][i], None)
            iteminfo['tag']['implicits_tag'].pop(iteminfo['explicit']['prefix'][i], None)
            iteminfo['explicit']['prefix'][i] = None
            iteminfo['num_prefix'] -= 1

            if iteminfo['status']['crafted'] == iteminfo['explicit']['prefix'][i]:
                iteminfo['status']['crafted'] = None

        num = random.sample(suffix, k=num_suf_to_remove)

        for i in num:
            iteminfo['tag']['mod_groups'].pop(iteminfo['explicit']['suffix'][i], None)
            iteminfo['tag']['implicits_tag'].pop(iteminfo['explicit']['prefix'][i], None)
            iteminfo['explicit']['suffix'][i] = None
            iteminfo['num_suffix'] -= 1

            if iteminfo['status']['crafted'] == iteminfo['explicit']['suffix'][i]:
                iteminfo['status']['crafted'] = None

    return iteminfo

def reroll_mod(iteminfo, file_path):
    with open(file_path) as ff:
        mod_dict = json.load(ff)

    base_mod_pool = mod_dict[iteminfo['base']]

    keys = list(iteminfo['tag']['mod_groups'].keys())
    groups = list(iteminfo['tag']['mod_groups'].values())

    new_keys = [0 for i in range(len(keys))]

    for i in range(len(groups)):
        in_tag_groups = []
        for mod in base_mod_pool:
            if mod != 'mod_weight':
                if (base_mod_pool[mod]['groups'][0] == groups[i]) and (
                        iteminfo['item_level'] > base_mod_pool[mod]['required_level']
                ):
                    in_tag_groups.append(mod)

        rd = random.choice(in_tag_groups)
        new_keys[i] = rd

    for i in range(len(new_keys)):
        num = [1, 2, 3]

        for j in num:
            if iteminfo['explicit']['prefix'][j] == keys[i]:
                iteminfo['explicit']['prefix'][j] = new_keys[i]

            elif iteminfo['explicit']['suffix'][j] == keys[i]:
                iteminfo['explicit']['suffix'][j] = new_keys[i]

    mod_groups = {}
    for i in range(len(new_keys)):
        mod_groups[new_keys[i]] = groups[i]

    implicit = {}
    implicits_tag = list(iteminfo['tag']['implicits_tag'].values())
    for i in range(len(new_keys)):
        implicit[new_keys[i]] = implicits_tag[i]

    iteminfo['tag']['mod_groups'] = mod_groups
    iteminfo['tag']['implicits_tag'] = implicit

    return iteminfo

def convert_action_int_to_type(action_pool, action_int):
    if action_pool == 1:
        if action_int < 11:
            action_type = 'orb'

        elif action_int < 15:
            action_type = 'craft'

    else:
        if action_int < 11:
            action_type = 'orb'

        elif action_int < 116:
            action_type = 'essence'

        elif action_int < 119:
            action_type = 'craft'

        elif action_int < 2059:
            action_type = 'fossil'

    return action_type


def add_inf(iteminfo, influence=None):
    reward = 0
    influence_list = ['shaper', 'elder', 'eyrie', 'basilisk', 'adjudicator', 'crusader', 'exarch', 'eater']

    if influence not in influence_list:
        reward = -10
        return iteminfo, reward

    if iteminfo['status']['fractured']:
        reward = -10
        return iteminfo, reward

    if iteminfo['item_level'] < 68:
        reward = -10
        return iteminfo, reward

    iteminfo['status']['influence'] = influence

    return iteminfo, reward

# inf mod for 'shaper', 'elder', 'eyrie', 'basilisk', 'adjudicator', 'crusader'
def add_inf_mod(iteminfo):
    with open('env/src/json/influence_mods.json') as ff:
        inf_mod_dict = json.load(ff)

    with open('env/src/json/global_mods.json') as f:
        global_mod_dict = json.load(f)

    itemclass = iteminfo['base']
    item_inf = iteminfo['status']['influence']

    base = itemclass

    if '(' in itemclass:
        ic = itemclass.split('(')
        base = ic[0]

    elif 'two_hand' in itemclass:
        ic = itemclass.split('_')
        base = '2h_' + ic[-1]

    elif 'attack_staff' in itemclass:
        base = 'warstaff'

    spawn_tag = base + '_' + item_inf

    mod = []
    mod_weights = []
    for j in inf_mod_dict[itemclass][item_inf]:
        for t in inf_mod_dict[itemclass][item_inf][j]['spawn_weights']:
            if t['tag'] == spawn_tag:
                mod_weights.append(t['weight'])
                mod.append(j)

    global_mod = list(global_mod_dict[itemclass].keys())
    global_mod_weight = global_mod_dict[itemclass]['mod_weight']

    mod = mod + global_mod
    mod_weights = mod_weights + global_mod_weight

    check = False
    where = 'global'

    while check is False:
        rd = random.choices(population=mod, weights=mod_weights)[0]

        if rd in global_mod:
            generation_type = global_mod_dict[itemclass][rd]['generation_type']
            where = 'global'

        else:
            generation_type = inf_mod_dict[itemclass][item_inf][rd]['generation_type']
            where = 'inf'

        if generation_type == 'prefix' and iteminfo['num_prefix'] < 3:
            check = True

        elif generation_type == 'suffix' and iteminfo['num_suffix'] < 3:
            check = True

    if where == 'global':
        implicit = global_mod_dict[itemclass][rd]['implicit_tags']
        group = global_mod_dict[itemclass][rd]['groups']

    elif where == 'inf':
        implicit = inf_mod_dict[itemclass][item_inf][rd]['implicit_tags']
        group = inf_mod_dict[itemclass][item_inf][rd]['groups']

    if generation_type == 'prefix':
        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] is None:
                iteminfo['explicit']['prefix'][p] = rd
                iteminfo['tag']['implicits_tag'] = implicit
                iteminfo['tag']['mod_groups'] = group
                iteminfo['num_prefix'] += 1
                break

    elif generation_type == 'suffix':
        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] is None:
                iteminfo['explicit']['suffix'][s] = rd
                iteminfo['tag']['implicits_tag'] = implicit
                iteminfo['tag']['mod_groups'] = group
                iteminfo['num_suffix'] += 1
                break

    return iteminfo