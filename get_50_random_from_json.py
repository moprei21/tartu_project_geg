import json
import random

def get_50_random_from_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Randomly select 50 entries
    selected_data = random.sample(data, 50)

    # Write the selected entries to a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(selected_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_file = "data/ger/corrected_sents_train.json"  # Replace with your input JSON file
    output_file = "data/ger/degec.wo.singleedit.50.json"  # Replace with your desired output JSON file
    get_50_random_from_json(input_file, output_file)

    input_file = "data/est/estgec.wo.singleedit.json"  # Replace with your input JSON file
    output_file = "data/est/estgec.wo.singleedit.50.json"  # Replace with your desired output JSON file
    get_50_random_from_json(input_file, output_file)