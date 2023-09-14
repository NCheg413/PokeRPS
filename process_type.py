import requests
import json
import time

url = ""
data = None
data_pokemon = None
pokemon = {"result": []}
type_set = set()


with open("type_pokemon.json", "r") as f:
    data = json.load(f)

for key in data["result"]:
    if key != 'shadow' and key != 'unknown':
        type_set.add(key)


def compare_types(a, b, data):
    type_name_a = a["type"]["name"]
    type_name_b = b["type"]["name"]
    type_info_a = data[type_name_a]
    type_info_b = data[type_name_b]
    effective_a = set(type_info_a["effective"])
    neutral_a = set(type_info_a["neutral"])
    effective_b = set(type_info_b["effective"])
    neutral_b = set(type_info_b["neutral"])
    neutral_total = neutral_a | neutral_b
    effective_a = effective_a - neutral_total
    effective_b = effective_b - neutral_total
    tot_effective = effective_a | effective_b
    set_neutral = type_set - tot_effective
    list_effective = list(tot_effective)
    list_neutral = list(set_neutral)
    return {"effective": list_effective, "neutral": list_neutral}


for i in range(1, 899):
    if i > 1010:
        url = "https://pokeapi.co/api/v2/pokemon/" + \
            str(10000 + i - 1010) + "/"
    else:
        url = "https://pokeapi.co/api/v2/pokemon/" + str(i) + "/"
    response = requests.get(url)
    if response.status_code == 200:
        data_pokemon = response.json()
        name = data_pokemon["name"]
        type_s = data_pokemon["types"]
        if len(type_s) > 1:
            info = compare_types(type_s[0], type_s[1], data["result"])
            pokemon["result"].append(
                {"name": name, "type": [type_s[0]["type"]["name"], type_s[1]["type"]["name"]], "stat": info, "imgurl": data_pokemon["sprites"]["front_default"]})
        else:
            info = compare_types(type_s[0], type_s[0], data["result"])
            pokemon["result"].append(
                {"name": name, "type": [type_s[0]["type"]["name"]], "stat": info, "imgurl": data_pokemon["sprites"]["front_default"]})
        print(str(i) + "\n")

        with open("poke_data.json", "w") as f:
            json.dump(pokemon, f, indent=4)
