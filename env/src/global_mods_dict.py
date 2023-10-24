import json

# base item list

one_hand_weapon = ['sceptre', 'claw', 'mace', 'axe']
one_hand_ranged = ['wand']
one_hand_sword = ['rapier', 'sword']
one_hand_dagger = ['dagger', 'attack_dagger']

two_hand_weapon = ['sword', 'axe', 'mace']
two_hand_ranged = ['bow']
two_hand_staff = ['staff', 'attack_staff']

jewelry = ['amulet', 'ring', 'belt', 'trinket']

armours = ['gloves', 'boots', 'helmet', 'body_armour']
armours_type = ['str_armour', 'dex_armour', 'int_armour', 'str_dex_armour', 'str_int_armour', 'dex_int_armour']
_armours = ['body_armour']
_armours_type = ['str_dex_int_armour']

quiver = ['quiver']
shield = ['shield']

special_unset = ['unset_ring']
special_minion = ['bone_ring', 'convoking_wand', 'bone_spirit_shield']


with open('../../RePoE/RePoE/data/mods.json') as f:
    test = json.load(f)

with open('../../RePoE/RePoE/data/crafting_bench_options.json') as ff:
    craft = json.load(ff)

itemclasses = one_hand_weapon + one_hand_ranged + one_hand_sword + one_hand_dagger + two_hand_weapon +\
              two_hand_ranged + two_hand_staff + jewelry + armours + quiver + shield

crafting_mod = {}

for ww in itemclasses:
    ccc = []

    if ww == 'rapier':
        wa = "Thrusting One Hand Sword"

    elif ww == 'dagger':
        wa = 'Rune Dagger'

    elif ww == 'attack_dagger':
        wa = 'Dagger'

    elif ww == 'attack_staff':
        wa = 'Warstaff'

    elif ww == 'body_armour':
        wa = 'Body Armour'

    else:
        wa = ww.capitalize()

    for c in craft:
        if wa in c['item_classes']:
            cc = c['actions'].get('add_explicit_mod')
            ccc.append(cc)

    crafting_mod[ww] = ccc

mm = ['One Hand Axe', 'One Hand Mace', 'One Hand Sword',
     'Two Hand Axe', 'Two Hand Mace', 'Two Hand Sword']

for ww in mm:
    ccc = []
    for c in craft:
        if ww in c['item_classes']:
            cc = c['actions'].get('add_explicit_mod')
            ccc.append(cc)

    crafting_mod[ww] = ccc

spawn = []

for j in test:
    if test[j]['domain'] == 'item':
        if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
            spawn.append(test[j]['spawn_weights'])

tags = []
for s in spawn:
    for a in s:
        tags.append(a['tag'])

tags = set(tags)
tags = list(tags)

global_tags = []
influenced_tags = []
influence = ['shaper', 'elder', 'eyrie', 'basilisk', 'adjudicator', 'crusader']


for t in tags:
    n = False
    for i in influence:
        if i in t:
            influenced_tags.append(t)
            n = True

    if n == False:
        global_tags.append(t)

mod_dict = {}
influence_mod_dict = {}
vaal_mod_dict = {}
bench_mod_dict = {}

for ww in one_hand_weapon:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default':{}, 'veil':{}}
    influences = {'shaper':{}, 'elder':{}, 'eyrie':{}, 'basilisk':{},
                  'adjudicator':{}, 'crusader':{}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if s['tag'] == 'weapon' or s['tag'] == 'one_hand_weapon':
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

        if ww == 'axe': ww = 'One Hand Axe'
        elif ww == 'mace': ww = 'One Hand Mace'

        if j in crafting_mod[ww]:
            if 'Jun' in j:
                sub_bench_dict['veil'][j] = test[j]

            else:
                sub_bench_dict['default'][j] = test[j]

        if ww == 'One Hand Axe': ww = 'axe'
        elif ww == 'One Hand Mace': ww = 'mace'

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in one_hand_sword:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if s['tag'] == 'weapon' or s['tag'] == 'sword' or s['tag'] == 'one_hand_weapon':
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if ww == 'sword': ww = 'One Hand Sword'

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

            if ww == 'One Hand Sword': ww = 'sword'

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in one_hand_dagger:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'weapon') or (s['tag'] == 'dagger') or (s['tag'] == 'one_hand_weapon'):
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in one_hand_ranged:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'weapon') or (s['tag'] == 'one_hand_weapon') or (s['tag'] == 'ranged'):
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])
                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in two_hand_weapon:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'weapon') or (s['tag'] == 'two_hand_weapon'):
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])
                            n = True

                    for i in influence:
                        wwi = '2h_' + ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            wa = ww
            ww = 'Two Hand ' + ww.capitalize()

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

            ww = wa

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    wa = 'two_hand_' + ww
    mod_dict[wa] = sub_mods_dict
    influence_mod_dict[wa] = influences
    vaal_mod_dict[wa] = sub_vaal_dict
    bench_mod_dict[wa] = sub_bench_dict

for ww in two_hand_ranged:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'weapon') or (s['tag'] == 'two_hand_weapon') or (s['tag'] == 'ranged'):
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])
                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in two_hand_staff:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'weapon') or (s['tag'] == 'two_hand_weapon') or (s['tag'] == 'staff'):
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])
                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if ww == 'attack_staff':
                            wwi = 'warstaff_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in jewelry:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if (s['tag'] == ww) and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'default') and (s['weight'] != 0):
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])
                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in armours:
    for tt in armours_type:
        sub_mods_dict = {}
        sub_vaal_dict = {}
        sub_bench_dict = {'default': {}, 'veil': {}}
        influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                      'adjudicator': {}, 'crusader': {}}

        weights = []
        vaal_weights = []

        for j in test:
            if 'Royale' not in j:
                if test[j]['domain'] == 'item':
                    n = False
                    for s in test[j]['spawn_weights']:
                        if (s['tag'] == ww) and n is False:
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                        if n is False:
                            if (s['tag'] == 'armour' or s['tag'] == tt) or (s['tag'] == 'default' and s['weight'] != 0):
                                if s['weight'] != 0:
                                    if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                        sub_mods_dict[j] = test[j]
                                        weights.append(s['weight'])

                                    if test[j]['generation_type'] == 'corrupted':
                                        sub_vaal_dict[j] = test[j]
                                        vaal_weights.append(s['weight'])
                                n = True

                        for i in influence:
                            wwi = ww + '_' + i
                            if wwi == s['tag'] and s['weight'] != 0:
                                influences[i][j] = test[j]

                if j in crafting_mod[ww]:
                    if 'Jun' in j:
                        sub_bench_dict['veil'][j] = test[j]

                    else:
                        sub_bench_dict['default'][j] = test[j]

        weights.append(0)
        sub_mods_dict['mod_weight'] = weights

        vaal_weights.append(0)
        sub_vaal_dict['mod_weight'] = vaal_weights

        ta = ww + '(' + tt + ')'
        mod_dict[ta] = sub_mods_dict
        influence_mod_dict[ta] = influences
        vaal_mod_dict[ta] = sub_vaal_dict
        bench_mod_dict[ta] = sub_bench_dict

for ww in _armours:
    for tt in _armours_type:
        sub_mods_dict = {}
        sub_vaal_dict = {}
        sub_bench_dict = {'default': {}, 'veil': {}}
        influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                      'adjudicator': {}, 'crusader': {}}

        weights = []
        vaal_weights = []

        for j in test:
            if 'Royale' not in j:
                if test[j]['domain'] == 'item':
                    n = False
                    for s in test[j]['spawn_weights']:
                        if (s['tag'] == ww) and n is False:
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                        if n is False:
                            if (s['tag'] == 'armour' or s['tag'] == tt) or (s['tag'] == 'default' and s['weight'] != 0):
                                if s['weight'] != 0:
                                    if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                        sub_mods_dict[j] = test[j]
                                        weights.append(s['weight'])

                                    if test[j]['generation_type'] == 'corrupted':
                                        sub_vaal_dict[j] = test[j]
                                        vaal_weights.append(s['weight'])
                                n = True

                        for i in influence:
                            wwi = ww + '_' + i
                            if wwi == s['tag'] and s['weight'] != 0:
                                influences[i][j] = test[j]

                if j in crafting_mod[ww]:
                    if 'Jun' in j:
                        sub_bench_dict['veil'][j] = test[j]

                    else:
                        sub_bench_dict['default'][j] = test[j]

        weights.append(0)
        sub_mods_dict['mod_weight'] = weights

        vaal_weights.append(0)
        sub_vaal_dict['mod_weight'] = vaal_weights

        ta = ww + '(' + tt + ')'
        mod_dict[ta] = sub_mods_dict
        influence_mod_dict[ta] = influences
        vaal_mod_dict[ta] = sub_vaal_dict
        bench_mod_dict[ta] = sub_bench_dict

for ww in quiver:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    sub_bench_dict = {'default': {}, 'veil': {}}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if s['tag'] == ww and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if (s['tag'] == 'default' and s['weight'] != 0) and n is False:
                        if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                            sub_mods_dict[j] = test[j]
                            weights.append(s['weight'])

                        if test[j]['generation_type'] == 'corrupted':
                            sub_vaal_dict[j] = test[j]
                            vaal_weights.append(s['weight'])
                        n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

            if j in crafting_mod[ww]:
                if 'Jun' in j:
                    sub_bench_dict['veil'][j] = test[j]

                else:
                    sub_bench_dict['default'][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict
    bench_mod_dict[ww] = sub_bench_dict

for ww in shield:
    for tt in armours_type:
        sub_mods_dict = {}
        sub_vaal_dict = {}
        sub_bench_dict = {'default': {}, 'veil': {}}
        influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                      'adjudicator': {}, 'crusader': {}}

        weights = []
        vaal_weights = []

        ta = tt.split('_')
        tata = ''
        for a in ta[:-1]:
            tata += a
            tata += '_'
        tata += 'shield'

        for j in test:
            if 'Royale' not in j:
                if test[j]['domain'] == 'item':
                    n = False
                    for s in test[j]['spawn_weights']:
                        if s['tag'] == ww and n is False:
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                        if n is False:
                            if (s['tag'] == tt or s['tag'] == 'armour' or s['tag'] == tata) or \
                                    (s['tag'] == 'default' and s['weight'] != 0):
                                if s['weight'] != 0:
                                    if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                        sub_mods_dict[j] = test[j]
                                        weights.append(s['weight'])

                                    if test[j]['generation_type'] == 'corrupted':
                                        sub_vaal_dict[j] = test[j]
                                        vaal_weights.append(s['weight'])
                                n = True

                        if tt == 'int_armour':
                            if n is False:
                                if s['tag'] == 'focus':
                                    if s['weight'] != 0:
                                        if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                            sub_mods_dict[j] = test[j]
                                            weights.append(s['weight'])

                                        if test[j]['generation_type'] == 'corrupted':
                                            sub_vaal_dict[j] = test[j]
                                            vaal_weights.append(s['weight'])
                                    n = True

                        for i in influence:
                            wwi = ww + '_' + i
                            if wwi == s['tag'] and s['weight'] != 0:
                                influences[i][j] = test[j]

                if j in crafting_mod[ww]:
                    if 'Jun' in j:
                        sub_bench_dict['veil'][j] = test[j]

                    else:
                        sub_bench_dict['default'][j] = test[j]

        weights.append(0)
        sub_mods_dict['mod_weight'] = weights

        vaal_weights.append(0)
        sub_vaal_dict['mod_weight'] = vaal_weights

        ta = ww + '(' + tata + ')'
        mod_dict[ta] = sub_mods_dict
        influence_mod_dict[ta] = influences
        vaal_mod_dict[ta] = sub_vaal_dict
        bench_mod_dict[ta] = sub_bench_dict

for ww in special_unset:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if s['tag'] == 'ring' and n is False:
                        if s['weight'] != 0:
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])

                        n = True

                    if n is False:
                        if (s['tag'] == 'default' and s['weight'] != 0) or (s['tag'] == ww):
                            if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                sub_mods_dict[j] = test[j]
                                weights.append(s['weight'])

                            if test[j]['generation_type'] == 'corrupted':
                                sub_vaal_dict[j] = test[j]
                                vaal_weights.append(s['weight'])
                            n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict

for ww in special_minion:
    sub_mods_dict = {}
    sub_vaal_dict = {}
    influences = {'shaper': {}, 'elder': {}, 'eyrie': {}, 'basilisk': {},
                  'adjudicator': {}, 'crusader': {}}

    weights = []
    vaal_weights = []

    for j in test:
        if 'Royale' not in j:
            if test[j]['domain'] == 'item':
                n = False
                for s in test[j]['spawn_weights']:
                    if ww == 'bone_ring':
                        if s['tag'] == 'ring' and n is False:
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                        if n is False:
                            if (s['tag'] == 'default' and s['weight'] != 0) or (
                                    s['tag'] == 'ring_can_roll_minion_modifiers'):
                                if s['weight'] != 0:
                                    if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                        sub_mods_dict[j] = test[j]
                                        weights.append(s['weight'])

                                    if test[j]['generation_type'] == 'corrupted':
                                        sub_vaal_dict[j] = test[j]
                                        vaal_weights.append(s['weight'])
                                n = True

                    elif ww == 'convoking_wand':
                        if s['tag'] == 'wand' and n is False:
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                        if n is False:
                            if (s['tag'] == 'default' and s['weight'] != 0) or (
                                    s['tag'] == 'weapon_can_roll_minion_modifiers') or (
                                    s['tag'] == 'weapon') or (s['tag'] == 'one_hand_weapon') or (
                                    s['tag'] == 'ranged'
                            ):
                                if s['weight'] != 0:
                                    if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                        sub_mods_dict[j] = test[j]
                                        weights.append(s['weight'])

                                    if test[j]['generation_type'] == 'corrupted':
                                        sub_vaal_dict[j] = test[j]
                                        vaal_weights.append(s['weight'])
                                n = True

                    elif ww == 'bone_spirit_shield':
                        if s['tag'] == 'shield' and n is False:
                            if s['weight'] != 0:
                                if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                    sub_mods_dict[j] = test[j]
                                    weights.append(s['weight'])

                                if test[j]['generation_type'] == 'corrupted':
                                    sub_vaal_dict[j] = test[j]
                                    vaal_weights.append(s['weight'])

                            n = True

                        if n is False:
                            if (s['tag'] == 'default' and s['weight'] != 0) or (
                                    s['tag'] == 'focus_can_roll_minion_modifiers') or (
                                    s['tag'] == 'armour') or (s['tag'] == 'int_armour') or (
                                    s['tag'] == 'focus'
                            ):
                                if s['weight'] != 0:
                                    if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
                                        sub_mods_dict[j] = test[j]
                                        weights.append(s['weight'])

                                    if test[j]['generation_type'] == 'corrupted':
                                        sub_vaal_dict[j] = test[j]
                                        vaal_weights.append(s['weight'])
                                n = True

                    for i in influence:
                        wwi = ww + '_' + i
                        if wwi == s['tag'] and s['weight'] != 0:
                            influences[i][j] = test[j]

    weights.append(0)
    sub_mods_dict['mod_weight'] = weights

    vaal_weights.append(0)
    sub_vaal_dict['mod_weight'] = vaal_weights

    mod_dict[ww] = sub_mods_dict
    influence_mod_dict[ww] = influences
    vaal_mod_dict[ww] = sub_vaal_dict

# weight calculation results from ./calc_weights.py

# global_mods_total_weights = {'sceptre': 218662, 'claw': 151914, 'mace': 113460, 'axe': 140114, 'rapier': 159890, 'sword': 140114, 'dagger': 196324, 'attack_dagger': 160964, 'wand': 199486, 'two_hand_sword': 140114, 'two_hand_axe': 140114, 'two_hand_mace': 113460, 'bow': 133508, 'staff': 219316, 'attack_staff': 175182, 'gloves(str_armour)': 123000, 'gloves(dex_armour)': 114000, 'gloves(int_armour)': 137000, 'gloves(str_dex_armour)': 120000, 'gloves(str_int_armour)': 142000, 'gloves(dex_int_armour)': 133000, 'boots(str_armour)': 95600, 'boots(dex_armour)': 95600, 'boots(int_armour)': 109600, 'boots(str_dex_armour)': 101600, 'boots(str_int_armour)': 114600, 'boots(dex_int_armour)': 114600, 'helmet(str_armour)': 117675, 'helmet(dex_armour)': 117675, 'helmet(int_armour)': 123675, 'helmet(str_dex_armour)': 123675, 'helmet(str_int_armour)': 128175, 'helmet(dex_int_armour)': 128175, 'body_armour(str_armour)': 103700, 'body_armour(dex_armour)': 103700, 'body_armour(int_armour)': 119200, 'body_armour(str_dex_armour)': 109700, 'body_armour(str_int_armour)': 123450, 'body_armour(dex_int_armour)': 123450, 'body_armour(str_dex_int_armour)': 131822, 'amulet': 213850, 'ring': 163850, 'belt': 118550, 'trinket': 19000, 'quiver': 102850, 'shield(str_shield)': 130875, 'shield(dex_shield)': 127475, 'shield(int_shield)': 162356, 'shield(str_dex_shield)': 143475, 'shield(str_int_shield)': 166375, 'shield(dex_int_shield)': 162975, 'unset_ring': 166100, 'bone_ring': 202850, 'convoking_wand': 267726, 'bone_spirit_shield': 211096, 'mod_weight': []}
# influence_mods_total_weights = {'mace_adjudicator': 9350, 'quiver_basilisk': 6000, 'bow_crusader': 8550, 'body_armour_crusader': 5875, 'shield_eyrie': 6750, 'warstaff_basilisk': 8100, 'body_armour_shaper': 10200, 'helmet_elder': 21200, 'amulet_shaper': 24000, 'gloves_basilisk': 8250, 'gloves_shaper': 15400, 'rune_dagger_adjudicator': 14050, '2h_sword_elder': 23700, 'mace_elder': 24100, 'rune_dagger_basilisk': 13700, 'boots_shaper': 7800, 'claw_crusader': 9850, 'claw_eyrie': 10200, 'ring_basilisk': 6850, '2h_mace_crusader': 9650, 'warstaff_eyrie': 7500, 'rune_dagger_elder': 32100, 'mace_shaper': 22400, 'bow_basilisk': 10950, 'bow_eyrie': 9200, 'quiver_eyrie': 6500, 'rune_dagger_shaper': 34700, 'staff_adjudicator': 16950, 'amulet_crusader': 8750, 'belt_elder': 18300, '2h_sword_eyrie': 9700, 'boots_crusader': 6375, 'wand_shaper': 29500, 'shield_shaper': 8800, 'helmet_basilisk': 10250, 'amulet_basilisk': 9500, 'shield_crusader': 5750, 'shield_adjudicator': 6750, 'dagger_crusader': 9850, 'body_armour_basilisk': 4500, 'dagger_basilisk': 9100, 'rune_dagger_eyrie': 18600, 'helmet_crusader': 6625, '2h_mace_eyrie': 7500, 'ring_crusader': 10400, '2h_axe_elder': 23700, 'quiver_elder': 10600, 'mace_eyrie': 8000, 'belt_crusader': 7750, 'body_armour_adjudicator': 6700, 'wand_basilisk': 13850, 'sword_eyrie': 10200, 'belt_adjudicator': 10000, 'body_armour_elder': 7800, 'mace_crusader': 8650, '2h_sword_crusader': 11150, 'helmet_adjudicator': 8375, 'axe_crusader': 9150, '2h_mace_elder': 19800, 'belt_basilisk': 7000, 'helmet_eyrie': 7000, 'claw_adjudicator': 9150, 'ring_shaper': 12850, 'dagger_elder': 23100, 'sword_shaper': 28600, 'sceptre_shaper': 34700, 'rune_dagger_crusader': 17250, '2h_sword_adjudicator': 10550, 'sceptre_eyrie': 14100, 'sceptre_adjudicator': 15250, 'mace_basilisk': 8900, 'boots_adjudicator': 6125, 'axe_shaper': 28600, 'ring_elder': 11200, 'dagger_shaper': 25600, 'warstaff_elder': 24100, 'claw_shaper': 28600, 'warstaff_shaper': 24200, 'body_armour_eyrie': 6000, '2h_mace_adjudicator': 9350, 'wand_eyrie': 14600, 'amulet_eyrie': 11250, '2h_mace_basilisk': 9900, 'dagger_adjudicator': 7650, 'gloves_elder': 19600, 'claw_elder': 30100, 'gloves_eyrie': 8000, 'sword_basilisk': 10100, 'gloves_crusader': 6875, 'warstaff_crusader': 9350, 'staff_eyrie': 14900, 'wand_elder': 26300, '2h_axe_eyrie': 9700, 'sword_adjudicator': 10350, '2h_mace_shaper': 13200, 'axe_elder': 27100, 'boots_basilisk': 7100, 'bow_shaper': 22400, 'quiver_crusader': 7000, 'helmet_shaper': 16700, 'wand_crusader': 14250, 'amulet_elder': 15400, 'belt_eyrie': 7250, 'axe_basilisk': 9100, 'sword_elder': 27100, 'axe_eyrie': 10200, '2h_axe_basilisk': 9100, 'amulet_adjudicator': 8750, 'bow_adjudicator': 7800, 'bow_elder': 18900, 'sword_crusader': 10150, 'staff_elder': 32400, 'boots_eyrie': 5750, 'sceptre_elder': 29800, 'warstaff_adjudicator': 9550, 'belt_shaper': 14300, '2h_sword_basilisk': 11100, 'sceptre_crusader': 15750, '2h_axe_shaper': 18900, 'dagger_eyrie': 10200, 'sceptre_basilisk': 12700, 'ring_adjudicator': 10300, 'wand_adjudicator': 15200, 'quiver_adjudicator': 7000, 'staff_basilisk': 12700, '2h_axe_adjudicator': 10550, '2h_axe_crusader': 10150, 'shield_basilisk': 4250, 'shield_elder': 8200, 'claw_basilisk': 9100, 'staff_shaper': 28600, 'staff_crusader': 16750, 'gloves_adjudicator': 8875, 'quiver_shaper': 11600, 'axe_adjudicator': 10350, '2h_sword_shaper': 24900, 'ring_eyrie': 9400, 'boots_elder': 7700, 'mod_weight': []}

# mod_dict['total_weights'] = global_mods_total_weights
# influence_mod_dict['total_weights'] = influence_mods_total_weights


# save dictionaries to json file

file_path = 'json/global_mods.json'

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(mod_dict, file, indent='\t')

i_file_path = 'json/influence_mods.json'

with open(i_file_path, 'w', encoding='utf-8') as ff:
    json.dump(influence_mod_dict, ff, indent='\t')
#
v_file_path = 'json/vaal_mods.json'

with open(v_file_path, 'w', encoding='utf-8') as fff:
    json.dump(vaal_mod_dict, fff, indent='\t')

b_file_path = 'json/crafting_bench_mods.json'
with open(b_file_path, 'w', encoding='utf-8') as ffff:
    json.dump(bench_mod_dict, ffff, indent='\t')