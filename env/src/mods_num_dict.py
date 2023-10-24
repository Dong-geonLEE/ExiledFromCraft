import json

with open('../../RePoE/RePoE/data/mods.json') as f:
    test = json.load(f)

mods_num_dict = {}
mods_num = 0

for j in test:
    if test[j]['domain'] == 'item' or test[j]['domain'] == 'crafted':
        if test[j]['generation_type'] == 'prefix' or test[j]['generation_type'] == 'suffix':
            mods_num_dict[j] = mods_num
            mods_num += 1

n_file_path = 'json/mods_num.json'
with open(n_file_path, 'w', encoding='utf-8') as ffff:
    json.dump(mods_num_dict, ffff, indent='\t')