import csv
import json
import glob
import os


def process_tsv_file(file_path):
    location_data = {}
    with open(file_path, newline="", encoding="utf-8") as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in reader:
            pos_key = (float(row["Longitude"]), float(row["Latitude"]))
            bloc = row["Bloc"]
            party = row["Party"]
            votes = int(row["Votes"]) if row["Votes"].isdigit() else 0

            if pos_key not in location_data:
                location_data[pos_key] = {
                    "pos": list(pos_key),
                    "parties": {}
                }

            if bloc not in location_data[pos_key]["parties"]:
                location_data[pos_key]["parties"][bloc] = {}

            if party not in location_data[pos_key]["parties"][bloc]:
                location_data[pos_key]["parties"][bloc][party] = 0

            location_data[pos_key]["parties"][bloc][party] += votes

    return list(location_data.values())


def save_as_json(data, output_directory, file_name):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = os.path.join(output_directory, file_name)
    with open(output_file, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, separators=(",", ":"))


def process_all_election_files(input_directory, output_directory):
    for file_path in glob.glob(os.path.join(input_directory, "*.tsv")):
        file_name = os.path.basename(file_path).replace(".tsv", ".json")
        data = process_tsv_file(file_path)
        save_as_json(data, output_directory, file_name)
        print(f"Processed {file_path} into {output_directory}/{file_name}")


# Usage example
input_directory = "output/combined"
output_directory = "site/src/points"
process_all_election_files(input_directory, output_directory)
