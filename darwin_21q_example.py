import json
from ast import literal_eval

with open('pw_darwin_21q.json', 'r') as JSON:
       temp = json.load(JSON)
       
pairwise_entanglement_darwin21q = {literal_eval(key): value for key, value in temp.items()}       
