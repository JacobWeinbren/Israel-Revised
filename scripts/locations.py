import csv
import os
import googlemaps
from dotenv import dotenv_values
from tqdm import tqdm

config = dotenv_values(".env")

# Initialise Google Maps client with API key
gmaps = googlemaps.Client(key=config["GOOGLE_MAPS_API_KEY"])


def read_tsv_files(directory):
    """Reads TSV files from a given directory and extracts unique addresses."""
    addresses = set()
    for filename in os.listdir(directory):
        if filename.endswith(".tsv"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter="\t")
                next(reader)  # Skip header row
                for row in reader:
                    address = f"{row[0]}, {row[1]}"
                    addresses.add(address)
    return addresses


def load_processed_addresses(output_file):
    """Loads addresses that have already been geocoded from the output file."""
    processed = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="\t")
            for row in reader:
                processed.add(row[0])
    return processed


def geocode_addresses(addresses, output_file):
    """
    Geocodes a set of addresses using Google Maps API and writes the results to a file.
    Skips addresses already present in the output file.
    """
    processed_addresses = load_processed_addresses(output_file)

    with open(output_file, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        # Wrap addresses with tqdm for a progress bar
        for address in tqdm(addresses, desc="Geocoding Addresses"):
            if address not in processed_addresses:
                result = gmaps.geocode(address, region="il")
                if result:
                    lat = result[0]["geometry"]["location"]["lat"]
                    lng = result[0]["geometry"]["location"]["lng"]
                    writer.writerow([address, lat, lng])


# Main script execution
if __name__ == "__main__":
    directory = "output/stations"
    output_file = "output/locations.tsv"
    addresses = read_tsv_files(directory)
    geocode_addresses(addresses, output_file)
