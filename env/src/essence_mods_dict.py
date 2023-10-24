import json

with open('../../RePoE/RePoE/data/mods.json') as f:
    test = json.load(f)

es_dict = {}

for j in test:
    if test[j]['is_essence_only'] is True:
        es_dict[j] = test[j]

# save dictionaries to json file

file_path = 'json/essences_mods.json'

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(es_dict, file, indent='\t')