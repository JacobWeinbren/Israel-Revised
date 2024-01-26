import csv
import json

# Define the path to the TSV file and the output JSON file
tsv_file_path = "data/Blocs.tsv"
json_file_path = "site/src/data/Blocs.json"

# Read the TSV file and convert it to a dictionary with 'Party ID' as keys and 'Party Name' as values
party_data = {}
with open(tsv_file_path, "r", encoding="utf-8") as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter="\t")
    for row in reader:
        party_id = row["Party ID"]
        party_name = row["Party Name"]
        party_data[party_id] = party_name

# Write the dictionary to a JSON file
with open(json_file_path, "w", encoding="utf-8") as jsonfile:
    json.dump(party_data, jsonfile, ensure_ascii=False)
