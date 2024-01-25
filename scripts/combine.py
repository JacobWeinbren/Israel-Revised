import pandas as pd
import numpy as np


def create_full_address(row):
    return f"{row['Address Name']}, {row['Locality Name']}"


locations = pd.read_csv(
    "output/locations.tsv",
    sep="\t",
    names=["Address", "Latitude", "Longitude"],
    skiprows=1,
)

knesset_to_file = {
    13: "14",
    14: "14",
    15: "17",
    16: "17",
    17: "17",
    18: "19",
    19: "19",
    20: "20",
    21: "21",
    22: "22",
    23: "23",
    24: "24",
    25: "25",
}

for knesset, file_suffix in knesset_to_file.items():
    stations = pd.read_csv(
        f"output/stations/{file_suffix}.tsv",
        sep="\t",
        skiprows=1,
        names=["Locality Number", "Station Number", "Locality Name", "Address Name"],
    )
    stations["Locality Number"] = stations["Locality Number"]
    stations["Station Number"] = stations["Station Number"]

    elections = pd.read_csv(
        f"output/elections/{knesset}.tsv",
        sep="\t",
        skiprows=1,
        names=["Bloc", "Knesset", "Locality", "Station", "Votes"],
    )
    elections["Locality"] = elections["Locality"]
    elections["Station"] = elections["Station"]

    stations["Full Address"] = stations.apply(create_full_address, axis=1)

    merged_data = (
        pd.merge(
            elections,
            stations[["Locality Number", "Station Number", "Full Address"]],
            left_on=["Locality", "Station"],
            right_on=["Locality Number", "Station Number"],
            how="left",
        )
        .merge(locations, left_on="Full Address", right_on="Address", how="left")
        .dropna(subset=["Latitude", "Longitude"])
    )

    merged_data[["Bloc", "Knesset", "Votes", "Latitude", "Longitude"]].to_csv(
        f"output/combined/{knesset}.tsv", sep="\t", index=False
    )
