import json

# Open and read the JSON file
with open("data/raw/traj_data_v2_all89tasks.json", "r") as file:
    data = json.load(file)

fail_ = {}
pass_ = {}


for d in data:
    if d.get("t_commit") is None:
        pass_[d["case_id"]] = d
    else:
        fail_[d["case_id"]] = d

with open("fail_record.json", "w") as file:
    json.dump(fail_, file, indent=4)

with open("pass_record.json", "w") as file:
    json.dump(pass_, file, indent=4)

