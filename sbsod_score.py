import pandas as pd
import re

df = pd.read_csv("data/VR_Locomotion_Pre_During_Post-experiment Survey_April 30, 2025_20.26.csv", skiprows=2)

sbsod_mapping = {
    1: '{"ImportId":"QID1718035752_1"}',
    2: '{"ImportId":"QID1718035752_2"}',
    3: '{"ImportId":"QID1718035752_3"}',
    4: '{"ImportId":"QID1718035752_4"}',
    5: '{"ImportId":"QID1718035752_5"}',
    6: '{"ImportId":"QID1718035752_6"}',
    7: '{"ImportId":"QID1718035752_7"}',
    8: '{"ImportId":"QID1718035753_1"}',
    9: '{"ImportId":"QID1718035753_2"}',
    10: '{"ImportId":"QID1718035753_3"}',
    11: '{"ImportId":"QID1718035753_4"}',
    12: '{"ImportId":"QID1718035753_5"}',
    13: '{"ImportId":"QID1718035753_6"}',
    14: '{"ImportId":"QID1718035753_7"}',
    15: '{"ImportId":"QID1718035753_8"}'
}

reverse_scored = {1, 3, 4, 5, 7, 9, 14}

def extract_score(val):
    if pd.isnull(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    match = re.match(r"^\s*(\d+)", str(val))
    if match:
        return float(match.group(1))
    return None

def compute_sbsod(row):
    total = 0
    for i in range(1, 15):
        col = sbsod_mapping[i]
        val = row.get(col, None)
        val_num = extract_score(val)
        if val_num is None:
            return None
        score = 8 - val_num if i in reverse_scored else val_num
        total += score
    return total / 15

df["SBSOD_Score"] = df.apply(compute_sbsod, axis=1)

id_column = '{"ImportId":"QID1718035737_TEXT"}'

for idx, row in df.iterrows():
    participant_id = row.get(id_column, f"Row_{idx}")
    score = row["SBSOD_Score"]
    if pd.notnull(score):
        print(f"Participant {participant_id}: SBSOD Score = {score:.2f}")
    else:
        print(f"Participant {participant_id}: SBSOD Score = N/A (incomplete data)")

df.to_csv("SBSOD_scored.csv", index=False)
print("SBSOD scores saved to SBSOD_scored.csv.")