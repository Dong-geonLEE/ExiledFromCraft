# ExiledFromCrafted 환경에서 아이템을 제작하는 방법을 널리 알려진 방법을 통해 설명하고자 함.
# 이 항목에서 reward는 함수의 형태를 보여주기 위해서만 사용되었고, 실제 값으로는 사용되지 않음.
# Crafting steps of (early, end) sceptre for RF(Righteous Fire).

# cc. Pohx's RF Wiki
# https://www.youtube.com/watch?v=jv0koq8MPXs
# https://www.pohx.net/Crafts

from pprint import pprint
from time import time
import numpy as np

from env.item.make_item import make_item_info
from env.action.orbs import *
from env.action.essence import Essences
from env.action.bench_crafting import Bench_Crafting

"""
Early Sceptre

• [2] You're going to start by purchasing or finding a Fractured Sceptre. You want to make sure the Implicit has anywhere from 26-40% Elemental Damage. If it's lower it's okay

• [1] Note: The item level isn't too important here since we're just trying to get an entry level weapon. If I had to pick I'd go for something Ilvl 82+ I lvl 82 = T1 Damage over time Multiplier +(24–26)% to Damage over Time Multiplier

• Next up we're going to be bulk purchasing Minion Damage Essences. I'd recommend around 10-20 Screaming Essence of Fear (can use higher tier if you would like) Note: If playing SSF you can make this work with just a couple of essences.

• [3] Use a Regal Orb so your sceptre turns rare.

• [4] Use your Essence of Fear on your sceptre to start rolling it. If you hit an open suffix then you're good to go. Simply craft Fire Damage over time Multipler (Note: This requies a betrayl unveil to unlock the craft. You can also ask for assistance in Global 911)

• [5] If you're looking for an above average weapon keep spamming until you either get +1 Fire Gems, All +1 Spell skills or High sources of %Fire Damage over time Multi/Damage Over Time Multi

• [6] Bench Craft Fire Multi (almost always) or Damage Over Time (only if you rolled fire multi on essence or fracture)


Preferred Outcomes:
- #% Elemental(Fire) Damage (26%+) [FireDamagePercentage6+, FireDamagePrefixOnWeapon2+]
- #% Burning Damage (20%+) [BurnDamage1_+]
- #% Damage over time Multiplier (18%+) [GlobalDamageOverTimeMultiplier1h3+]
"""

def Make_Early_Sceptre(step_checking=-1, verbose=False):
    # [1] select base item
    early_sceptre = make_item_info(itembase='sceptre', item_level=82)

    if step_checking == 0 or step_checking == 1:
        print('step [1]: select base item')
        pprint(early_sceptre)

    # [2] 저자는 Elemental Damage #%가 달린 셉터를 '구하는(구입하거나, 자연적으로 드랍)'것을 의미하였지만, 여기서는 fracturing orb를 통해 생성하였다.
    # (자연으로 획득하는 것은 crafting의 의도와는 거리가 멀고, 구입하게되는 셉터는 자연적으로 드랍되거나, 비슷한 방식을 통해 제작되었기 때문에)
    # '분열' 옵션은 변경이 불가능하기 때문에, 조건이 맞지 않는 경우 [1]을 반복하는 과정이 포함됨.

    num_orbs_to_frac = 0
    ww = False

    early_sceptre, reward = Orb_of_Alchemy(early_sceptre)
    early_sceptre, reward = Fracturing_Orb(early_sceptre)
    num_orbs_to_frac += 2

    while ww is False:
        if ('FireDamagePercentage' in early_sceptre['status']['fractured']) or ('FireDamagePrefixOnWeapon' in early_sceptre['status']['fractured']):
            ww = True
            break

        early_sceptre = make_item_info(itembase='sceptre', item_level=82)
        early_sceptre, reward = Orb_of_Alchemy(early_sceptre)
        early_sceptre, reward = Fracturing_Orb(early_sceptre)
        num_orbs_to_frac += 2

        if verbose is True and num_orbs_to_frac % 100 == 0:
            print(num_orbs_to_frac, "th trying fracturing the option")

    if verbose:
        print('fracturing ended at', num_orbs_to_frac, 'th try')

    if step_checking == 0 or step_checking == 2:
        print('step [2]: takes fracturing option')
        pprint(early_sceptre)

    # [3] Regal Orb

    early_sceptre, reward = Regal_Orb(early_sceptre)

    if step_checking == 0 or step_checking == 3:
        print('step [3]: regal orb')
        pprint(early_sceptre)

    # [4] Essence of Fear [Screaming Essence of Fear : {... "Sceptre": "MinionDamageOnWeaponEssence5", ... }]

    early_sceptre, reward = Essences(early_sceptre, "Screaming Essence of Fear")

    if step_checking == 0 or step_checking == 4:
        print('step [4]: essence (Screaming Essence of Fear')
        pprint(early_sceptre)

    # [5] Spamming Essences until get +1 Fire Gems, All +1 Spell skills or High sources
    # weights : (300 / 218,662)
    # [2] 과정과 마찬가지로, 원하는 결과가 나올때 까지 [4]를 반복하는 과정이 포함되어있음.

    check = False
    es_num = 0

    while check is False:
        early_sceptre, reward = Essences(early_sceptre, "Screaming Essence of Fear")

        mod_list = list(early_sceptre['explicit']['prefix'].values()) + list(early_sceptre['explicit']['suffix'].values())

        if 'GlobalSpellGemsLevel1' in mod_list or 'GlobalFireSpellGemsLevel1_' in mod_list:
            if None in mod_list or 'FireDamageOverTimeMultiplier' in mod_list:
                check = True

        es_num += 1

        if verbose is True and es_num % 100 == 0:
            print(es_num, 'th trying essence spamming')

    if verbose:
        print('essences spamming ended at', es_num, 'th try')

    if step_checking == 0 or step_checking == 5:
        print('step [5]: essence spamming')
        pprint(early_sceptre)

    # [6] crafting

    if None in list(early_sceptre['explicit']['suffix'].values()) and \
            'DamageOverTimeMultiplier' not in list(early_sceptre['tag']['mod_groups'].values()):
        crafting_mod = 'JunMaster2FireDamageOverTimeMultiplier3_'

    elif None in list(early_sceptre['explicit']['prefix'].values()) and \
            'DegenerationDamage' not in list(early_sceptre['tag']['mod_groups'].values()):
        crafting_mod = 'EinharMasterDegenerationDamage2'

    else:
        crafting_mod = None

    early_sceptre, reward = Bench_Crafting(early_sceptre, crafting_mod=crafting_mod)

    if step_checking == 0 or step_checking == 6:
        print('step [6]: crafting')
        pprint(early_sceptre)

    print('total actions =', num_orbs_to_frac + es_num + 2)
    # pprint(early_sceptre)
    print('==================================================================================')

    return early_sceptre, num_orbs_to_frac, es_num

frac = []
ess = []
total_num = []
total_time = []

for i in range(10):
    start_time = time()
    early_sceptre, num_orbs_to_frac, es_num = Make_Early_Sceptre(step_checking=-1, verbose=False)

    frac.append(num_orbs_to_frac)
    ess.append(es_num)
    total_num.append(num_orbs_to_frac + es_num + 2)
    total_time.append(time() - start_time)

print('average total number of action:', np.mean(total_num))
print('average total time to complete:', np.mean(total_time))


"""
ExiledFromCrafting 에서 이 Early Sceptre 에 대한 원하는 input, output은 다음과 같다.

input:
goal = {'FireDamagePercentage', 'FireSpellGemsLevel', 'DamageOverMultiplier', 'MinionDamage'}

output:
seq = [{'select_base': (sceptre, 82),
        'fracturing': 'FireDamagePercentage',
        'Regal_orb': 'fixing rarity',
        'Essence': 'Screaming Essence of Fear',
        'Crafting': 'DamageOverTimeMultiplier'}]

"""