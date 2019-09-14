import json
from ast import literal_eval

with open('pw_dicke_15q.json', 'r') as JSON:
       temp = json.load(JSON)
       
pairwise_entanglement_dicke15q = {literal_eval(key): value for key, value in temp.items()}       
