import pandas as pd
import numpy as np


def create_full_address(row):
    return f"{row['Address Name']}, {row['Locality Name']}"


def convert_to_int(column):
    def safe_convert(value):
        try:
            clean_value = "".join(filter(str.isdigit, str(value).strip()))
            return int(np.floor(float(clean_value))) if clean_value else None
        except ValueError:
            return None

    return column.apply(safe_convert)


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
        names=["Address Name", "Locality Name", "Locality Number", "Station Number"],
    )
    stations["Locality Number"] = convert_to_int(stations["Locality Number"])
    stations["Station Number"] = convert_to_int(stations["Station Number"])

    elections = pd.read_csv(
        f"output/elections/{knesset}.tsv",
        sep="\t",
        skiprows=1,
        names=["Bloc", "Knesset", "Locality", "Station", "Votes"],
    )
    elections["Locality"] = convert_to_int(elections["Locality"])
    elections["Station"] = convert_to_int(elections["Station"])

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
        f"output/combined/{knesset}.csv", index=False
    )
