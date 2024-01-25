import os
import pandas as pd
import numpy as np


def read_election_data(elections_dir):
    # Read all election data files and return them as a dictionary
    election_data = {}
    for filename in os.listdir(elections_dir):
        if filename.endswith(".tsv"):
            knesset_number = int(filename.split(".")[0])
            df = pd.read_csv(os.path.join(elections_dir, filename), sep="	")
            election_data[knesset_number] = df
    return election_data


def read_station_data(stations_dir):
    # Read all station data files and return them as a dictionary
    station_data = {}
    for filename in os.listdir(stations_dir):
        if filename.endswith(".tsv"):
            knesset_number = int(filename.split(".")[0])
            df = pd.read_csv(os.path.join(stations_dir, filename), sep="	")
            station_data[knesset_number] = df
    return station_data


def read_location_data(locations_file):
    # Read the location data file
    return pd.read_csv(locations_file, sep="	")


def map_knesset_to_stations(knesset_num, station_data):
    # Map the Knesset number to the correct station data
    if knesset_num in station_data:
        return station_data[knesset_num]
    elif knesset_num == 13:
        return station_data[14]
    elif knesset_num in [15, 16]:
        return station_data[17]
    elif knesset_num == 18:
        return station_data[19]
    else:
        raise ValueError("Invalid Knesset number")


def combine_data(election_data, station_data, location_data):
    combined_data = []

    for knesset_num, election_df in election_data.items():
        # Map to the correct station data
        stations_df = map_knesset_to_stations(knesset_num, station_data)

        # Merge election data with station data
        merged_df = pd.merge(
            election_df, stations_df, how="left", on=["Locality", "Station Name"]
        )
        merged_df["Station"] = np.round(merged_df["Station"]).astype(int)

        # Combine address from station data
        merged_df["Address"] = (
            merged_df["Address Name"] + ", " + merged_df["Locality Name"]
        )

        # Merge with location data
        final_df = pd.merge(
            merged_df, location_data, how="left", left_on="Address", right_on="Address"
        )

        # Select and rename columns
        final_df = final_df[
            ["Knesset", "Locality", "Station", "Latitude", "Longitude", "Bloc", "Votes"]
        ]
        final_df.columns = [
            "Knesset",
            "Locality",
            "Station",
            "Lat",
            "Long",
            "Bloc",
            "Vote",
        ]

        combined_data.append(final_df)

    # Concatenate all dataframes
    return pd.concat(combined_data, ignore_index=True)


def main():
    # Paths to directories and files
    elections_dir = "output/elections"
    stations_dir = "output/stations"
    locations_file = "output/locations.tsv"

    # Read data
    election_data = read_election_data(elections_dir)
    station_data = read_station_data(stations_dir)
    location_data = read_location_data(locations_file)

    # Combine data
    combined_data = combine_data(election_data, station_data, location_data)

    # Export the final combined data
    output_file = "output/election_data.tsv"
    combined_data.to_csv(output_file, index=False, sep="\t")


if __name__ == "__main__":
    main()
