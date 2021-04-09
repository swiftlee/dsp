from scipy.io import loadmat
import json


# anthro = loadmat("./CIPIC_hrtf_database/anthropometry/anthro.mat")
# with open("measurements_pinna.json", "w") as test:
#     json.dump(anthro["D"].tolist(), test)

# with open("measurements_body.json", "w") as test:
#     json.dump(anthro["X"].tolist(), test)

# with open("measurements_angles.json", "w") as test:
#     json.dump(anthro["theta"].tolist(), test)

# Data written to test.json
# with open("test.json") as test:
#     anthro = json.load(test)


# json = json.dumps(anthro["D"].tolist())

anthro = loadmat("./CIPIC_hrtf_database/anthropometry/anthro.mat")

# blake_pinna = [
#     1.7,
#     0.8,
#     1.65,
#     1.4,
#     6.0,
#     3.2,
#     0.45,
#     0.7,
#     1.5,
#     0.9,
#     1.6,
#     1.4,
#     5.8,
#     3.2,
#     0.4,
#     1.2,
# ]
blake_angles = [
    0.461954269868904,
    0.26407549377546696,
    0.3769718724668432,
    0.2946125367651412,
]
blake_pinna = [
    1.618,
    0.776,
    1.423,
    1.665,
    6.484,
    2.858,
    0.343,
    0.985,
    1.432,
    0.639,
    1.413,
    1.274,
    5.848,
    2.683,
    0.288,
    0.915,
]
blake_body = [
    12.880992698596936,
    20.346092519159,
    17.603918390800366,
    2.7579378669648937,
    1.8994567260908997,
    11.026910416223126,
    7.63881707974514,
    10.112343769684019,
    30.05564963005951,
    12.593131968477575,
    26.739370544837563,
    43.814891830833496,
    0.6361594681191154,
    167.64000000000001,
    86.0,
    58.0,
    100.0,
]


def comparison(key):
    if "pinna" in key:
        return sum(map(lambda x: x * x, blake_pinna))
    elif "body" in key:
        return sum(map(lambda x: x * x, blake_body))
    return sum(map(lambda x: x * x, blake_angles))


def dot_product(key, other_list):
    if "pinna" in key:
        return sum(map(lambda x, y: x * y, blake_pinna, other_list))
    elif "body" in key:
        return sum(map(lambda x, y: x * y, blake_body, other_list))
    return sum(map(lambda x, y: x * y, blake_angles, other_list))


# pinna, body, and angles
other_values = [anthro["D"].tolist(), anthro["X"].tolist(), anthro["theta"].tolist()]


person = {
    "index": -1,
    "values": {
        "pinna_value": -1,
        "angle_value": -1,
        "body_value": -1,
    },
}

results = [
    {
        "index": i,
        "values": {
            "pinna_value": -1,
            "angle_value": -1,
            "body_value": -1,
        },
    }
    for i in range(45)
]

for value_index, value in enumerate(other_values, start=0):
    key = (
        "pinna_value"
        if value_index == 0
        else "body_value"
        if value_index == 1
        else "angle_value"
    )
    for person_index, arr in enumerate(value, start=0):
        val = abs(dot_product(key, arr) - comparison(key))
        person = results[person_index]
        person["values"][key] = val

avg = lambda list: sum(list) / len(list)

best_fit = None


for result in results:
    curr = avg(result["values"].values())
    if best_fit == None or curr < avg(best_fit["values"].values()):
        best_fit = result
    print(f"Results for {result['index']}: {avg(result['values'].values())}")


print(f"Best: {str(best_fit)}")


"""
Measurements:
Blake 
D1-D8 [LEFT: 1.7, 0.8, 1.65, 1.4, 6.0, 3.2, 0.45, 0.7, RIGHT: 1.5, 0.9, 1.6, 1.4, 5.8, 3.2, 0.4, 1.2]

Jon 
D1-D8 [LEFT: 1.72, 0.74, 1.53, 1.29, 6.01, 2.73, 0.69, 0.52, RIGHT:1.78, 0.83, 1.57, 1.37, 6.1, 2.65, 0.63, 0.98]

"""
