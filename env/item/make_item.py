import random

#####################################################################################
#                               item base list                                      #
#####################################################################################

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


#####################################################################################
#                                                                                   #
#####################################################################################


def _random_select_itembase(type=None):
    item_types = {'weapons':['sceptre', 'claw', 'mace', 'axe', 'wand', 'rapier', 'sword',
                             'dagger', 'attack_dagger', 'two_hand_sword', 'two_hand_axe',
                             'two_hand_mace', 'bow', 'staff', 'attack_staff'],
                  'jewelry':['amulet', 'ring', 'belt'],
                  'gloves':['gloves(str_armour)', 'gloves(dex_armour)', 'gloves(int_armour)',
                            'gloves(str_dex_armour)', 'gloves(str_int_armour)', 'gloves(dex_int_armour)'],
                  'boots':['boots(str_armour)', 'boots(dex_armour)', 'boots(int_armour)',
                            'boots(str_dex_armour)', 'boots(str_int_armour)', 'boots(dex_int_armour)'],
                  'helmet':['helmet(str_armour)', 'helmet(dex_armour)', 'helmet(int_armour)',
                            'helmet(str_dex_armour)', 'helmet(str_int_armour)', 'helmet(dex_int_armour)'],
                  'body_armour':['body_armour(str_armour)', 'body_armour(dex_armour)', 'body_armour(int_armour)',
                                'body_armour(str_dex_armour)', 'body_armour(str_int_armour)',
                                'body_armour(dex_int_armour)', 'body_armour(str_dex_int_armour)'],
                  'auxiliary':['quiver', 'shield(str_shield)', 'shield(dex_shield)', 'shield(int_shield)',
                               'shield(str_dex_shield)', 'shield(str_int_shield)', 'shield(dex_int_shield)'],
                  'sepcial':['unset_ring', 'bone_ring', 'convoking_wand', 'bone_spirit_shield']
                  }

    if type == None:
        bases = []
        for t in item_types:
            bases += item_types[t]

    else:
        bases = item_types[type]

    base = random.choice(bases)

    return base

def make_item_info(itembase=None, item_level=None, rarity='normal', influence=None):

    if itembase in [None, 'weapons', 'jewelry', 'gloves', 'boots', 'helmet', 'body_armour', 'auxiliary', 'special']:
        itembase = _random_select_itembase(itembase)

    if item_level is None:
        item_level = random.choice(range(1,101))

    return {"base":itembase, "item_level":item_level, "rarity":rarity,
                "head_implicit": {}, "num_prefix":0, "num_suffix":0,
                "explicit":{'prefix':{1:None, 2:None, 3:None}, 'suffix':{1:None, 2:None, 3:None},},
                "status":{'influence':influence, 'corrupted':False, 'fractured':None, 'crafted':None},
                "tag":{'implicits_tag':{}, 'mod_groups':{}},
                }