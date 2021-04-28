from scipy.io import loadmat
import json
from measurements import users, john_doe

anthro = loadmat("../../CIPIC_hrtf_database/anthropometry/anthro.mat")


def comparison(key, pinna, body, angles):
    if "pinna" in key:
        return sum(map(lambda x: x * x, pinna))
    elif "body" in key:
        return sum(map(lambda x: x * x, body))
    return sum(map(lambda x: x * x, angles))


def dot_product(key, other_list, pinna, body, angles):
    if "pinna" in key:
        return sum(map(lambda x, y: x * y, pinna, other_list))
    elif "body" in key:
        return sum(map(lambda x, y: x * y, body, other_list))
    return sum(map(lambda x, y: x * y, angles, other_list))


def apply_weight(key, val):
    if "pinna" in key:
        return 2 * val
    elif "angle" in key:
        return 3 * val
    return val


def calc_single_measurement_difference(measurement_type, measurement_arr):
    diffs = []
    john_doe_arr = john_doe[measurement_type]
    for i, value in enumerate(measurement_arr, start=0):
        diff = abs(value - john_doe_arr[i])
        diffs.append(diff)
    return diffs


def calc_avg_difference(user):
    differences = {"pinna": [], "body": [], "angles": []}
    differences["pinna"] = calc_single_measurement_difference("pinna", user["pinna"])
    differences["body"] = calc_single_measurement_difference("body", user["body"])
    differences["angles"] = calc_single_measurement_difference("angles", user["angles"])
    f = open("differences.txt", "a")
    f.write(
        f"{user['name']} differences: \n\npinna: {differences['pinna']} \n\nbody: {differences['body']} \n\nangles: {differences['angles']}\n\n\n\n"
    )
    f.close()


# pinna, body, and angles
other_values = [anthro["D"].tolist(), anthro["X"].tolist(), anthro["theta"].tolist()]


for user in users:
    calc_avg_difference(user)

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
            val = abs(
                dot_product(key, arr, user["pinna"], user["body"], user["angles"])
                - comparison(key, user["pinna"], user["body"], user["angles"])
            )
            val = apply_weight(key, val)
            person = results[person_index]
            person["values"][key] = val

    avg = lambda list: sum(list) / len(list)

    best_fit = None

    for result in results:
        curr = avg(result["values"].values())
        if best_fit == None or curr < avg(best_fit["values"].values()):
            best_fit = result
        # print(f"Results for {result['index']}: {avg(result['values'].values())}")

    print(f"\033[94m{user['name']}'s best fit: {str(best_fit)}\n\033[0m")
    f = open("data.txt", "a")
    f.write(f"{user['name']}'s best fit: {str(best_fit)}\n\n")
    f.close()
