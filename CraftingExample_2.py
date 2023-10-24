# ExiledFromCrafted 환경에서 아이템을 제작하는 방법을 널리 알려진 방법을 통해 설명하고자 함.
# 이 항목에서 reward는 함수의 형태를 보여주기 위해서만 사용되었고, 실제 값으로는 사용되지 않음.
# Crafting steps of sceptre at early stage (starter) for RF(Righteous Fire).

# cc. Pohx's RF Wiki
# https://www.youtube.com/watch?v=jv0koq8MPXs
# https://www.pohx.net/Crafts

from pprint import pprint
from time import time
import numpy as np

from env.item.make_item import make_item_info
from env.action.orbs import *
from env.action.essence import Essences, Essences_name
from env.action.bench_crafting import Bench_Crafting

# crafting_seq_ex 에서 보였던 early sceptre 를 제작 방식을 모른채로, 확률적으로 획득하는 여러 과정을 보이고자 함.

goal = {'BurnDamage', 'GlobalFireSpellGemsLevel', 'GlobalDamageOverTimeMultiplier', 'FireDamageOverTimeMultiplier'}
aug_alt_goal = {'BurnDamage', 'GlobalFireSpellGemsLevel', 'FireDamage', 'FireDamagePercentage'
                'GlobalDamageOverTimeMultiplier', 'FireDamageOverTimeMultiplier'}

# [1] chaos spamming until current_state is same as goal state
# approximately, weight is (3750 / 218662) * (250 / 218662) * (1500 / 218662) * (1530 / 218662)
# 'minion damage' in ex1 is essence only option. so it was substituted to 'FireDamageOverTimeMultiplier'
# in this step, tier of each mod is not considered

def Chaos_spamming():
    iteminfo = make_item_info(itembase='sceptre', item_level=82)

    # to make rarity 'rare'
    iteminfo, reward = Orb_of_Alchemy(iteminfo)

    num_orbs = 1
    goal_checking = False

    while goal_checking is False:
        # func _get_observation from ExiledFromCrafted at valuebasedenv.py
        obs = set(iteminfo['tag']['implicits_tag'].keys())

        ch = 0

        for g in goal:
            for o in obs:
                if g in o:
                    ch += 1
                    break

        if ch > 0:
            goal_checking = True
            break

        iteminfo, reward = Chaos_Orb(iteminfo)
        num_orbs += 1

        if num_orbs % 100 == 0:
            print(num_orbs, 'th trying chaos spamming')

        if num_orbs > 10000:
            print("Truncated")
            break

    return iteminfo, num_orbs

# [2] crafting method which used commonly in PoE.
# https://www.craftofexile.com/basics. [Craft of Exile/Basic - Common crafting methods - Alt-aug-regaling]
def Alt_aug_regaling():
    iteminfo = make_item_info(itembase='sceptre', item_level=82)

    done = False
    complete = False

    num_orbs = 0
    num_trying = 0

    while not complete:
        while not done:
            iteminfo, _ = Orb_of_Scouring(iteminfo)
            iteminfo, _ = Orb_of_Transmutation(iteminfo)

            num_orbs += 1
            num_trying += 1
            print(num_trying, 'th tyring with total', num_orbs, 'th action')

            aug = False
            while not aug:
                alt = False
                while not alt:
                    num_orbs += 1
                    iteminfo, _ = Orb_of_Alteration(iteminfo)
                    mods = list(iteminfo['tag']['mod_groups'].values())

                    for m in mods:
                        if m in aug_alt_goal:
                            alt = True

                    if num_orbs % 50 == 0:
                        print(num_orbs, 'in alteration')

                    if num_orbs > 5000:
                        print("시도 횟수가 초과되어 종료합니다.")
                        done = True
                        complete = True
                        break

                if iteminfo['num_prefix'] + iteminfo['num_suffix'] < 2:
                    num_orbs += 1
                    iteminfo, _ = Orb_of_Agumentation(iteminfo)

                mods = list(iteminfo['tag']['mod_groups'].values())

                aug = True
                for m in mods:
                    if m not in aug_alt_goal:
                        aug = False
                        break

            if aug is True:
                print('aug', mods)
                iteminfo, _ = Regal_Orb(iteminfo)
                num_orbs += 1

                mods = list(iteminfo['tag']['mod_groups'].values())

                reg = True
                for m in mods:
                    if m not in aug_alt_goal:
                        reg = False
                        break

                if reg is True:
                    print('reg', mods)
                    iteminfo, _ = Exalted_Orb(iteminfo)
                    num_orbs += 1

                    mods = list(iteminfo['tag']['mod_groups'].values())

                    exal = True
                    for m in mods:
                        if m not in aug_alt_goal:
                            exal = False
                            break

                    if exal is True:
                        done = True

        if done is True:
            complete = True

    return iteminfo, num_orbs


iteminfo, num_orbs = Chaos_Orb()

print(num_orbs)
pprint(iteminfo)

iteminfo, num_orbs = Alt_aug_regaling()

print(num_orbs)
pprint(iteminfo)