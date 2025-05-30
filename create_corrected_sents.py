import sys

sys.stdout.reconfigure(encoding="utf-8")

with open("data/est/estgec.test.wo.singleedit.txt", "r", encoding="utf-8") as f:
    data = f.read()
    data = data.split("\n\n")
    tuple_data = []
    for d in data:
        d = d.split("\n")
        tuple_data.append(d)

cleaned_tuple_data = []

for t in tuple_data:
    annotations = t[1].split("|||")
    _, index_start, index_end = annotations[0].split(" ")
    gold_standard_words = annotations[2]
    cleaned_tuple_data.append((t[0], (index_start, index_end, gold_standard_words)))

corr_sents = []

for t in cleaned_tuple_data:
    sent = t[0].split(" ")[1:]
    index_start, index_end, gold_standard_words = t[1]
    corrected_sent = "C " + " ".join(
        sent[: int(index_start)] + [gold_standard_words] + sent[int(index_end) :]
    )
    corr_sents.append(corrected_sent)


final_data = []
for i in range(len(tuple_data)):
    new_tuple = []
    new_tuple.append(tuple_data[i][0])  # Original sentence
    new_tuple.append(tuple_data[i][1])  # Annotations
    new_tuple.append(corr_sents[i])  # Corrected sentence

    final_data.append(new_tuple)

# write to json
import json

with open(f"data/est/estgec.wo.singleedit.json", "w", encoding="utf-8") as f:
    json.dump(
        final_data, f, ensure_ascii=False, indent=4
    )  # Use ensure_ascii=False for UTF-8 characters
