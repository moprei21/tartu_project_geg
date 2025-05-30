import json
import sys
import pandas as pd
sys.stdout.reconfigure(encoding="utf-8")

lang = "ger"  # Change to "est" for Estonian
folder = f"results/{lang}/"


file = f"{folder}{lang}gec.wo.singleedit.50.response_0.json"
with open(file, "r", encoding="utf-8") as f:
    data_0 = json.load(f)

file = f"{folder}{lang}gec.wo.singleedit.50.response_1.json"
with open(file, "r", encoding="utf-8") as f:
    data_1 = json.load(f)

file = f"{folder}{lang}gec.wo.singleedit.50.response_2.json"
with open(file, "r", encoding="utf-8") as f:
    data_2 = json.load(f)

file = f"{folder}{lang}gec.wo.singleedit.50.response_3.json"
with open(file, "r", encoding="utf-8") as f:
    data_3 = json.load(f)

df = pd.DataFrame(columns=[
    "original_sentence",
    "response_0",
    "usefulness_1_to_5_0",
    "error_identified_binary_0",
    "response_1",
    "usefulness_1_to_5_1",
    "error_identified_binary_1",
    "response_2",
    "usefulness_1_to_5_2",
    "error_identified_binary_2",
    "response_3",
    "usefulness_1_to_5_3",
    "error_identified_binary_3"
])

for i in range(len(data_0)):
    # write to xlsx file as follows:
    # Original sentence, response 0, response 1, response 2, response 3
    # but always leave two columns empty after each response
    # they are called usefulness_1_to_5 and error_identified_binary
    original_sentence = data_0[i]["text_incorrect"]
    response_0 = data_0[i]["response"]
    response_1 = data_1[i]["response"]
    response_2 = data_2[i]["response"]
    response_3 = data_3[i]["response"]
    # Write to pandas df
    df.loc[i] = [
        original_sentence,
        response_0,
        "",  # usefulness_1_to_5_0
        "",  # error_identified_binary_0
        response_1,
        "",  # usefulness_1_to_5_1
        "",  # error_identified_binary_1
        response_2,
        "",  # usefulness_1_to_5_2
        "",  # error_identified_binary_2
        response_3,
        "",  # usefulness_1_to_5_3
        ""   # error_identified_binary_3
    ]


# Write the DataFrame to an Excel file
output_file = f"{folder}{lang}gec.wo.singleedit.50.xlsx"
print(f"Writing to {output_file}")
df.to_excel(output_file, index=False, engine='openpyxl')