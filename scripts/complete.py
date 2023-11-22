import json

with open('stella_item_list.tbl.json') as json_file:
    item_stats = json.loads(json_file.read())

with open('item_id.json') as json_file:
    item_id = json.loads(json_file.read())

for dic in item_stats:

    dic['Item name'] = item_id[dic['_item_id']]

with open('stella_item_list_complete.tbl.json', 'w') as json_file:
    json_file.write(json.dumps(item_stats, indent = 2))