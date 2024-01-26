import pyexcel, math


def load_bloc_data(file_name, knesset_numbers):
    """Load bloc data for specified Knesset numbers."""
    bloc_data = {k: [] for k in knesset_numbers}
    for record in pyexcel.get_records(file_name=file_name):
        knesset = int(record["Knesset #"])
        if knesset in knesset_numbers:
            bloc_data[knesset].append(
                (record["Bloc"], record["Excel Name"], int(record["Party ID"]))
            )
    return bloc_data


def process_and_save_knesset_data(knesset, config, bloc_data):
    """Process and save voting data for a specific Knesset year."""
    vote_data = pyexcel.get_records(
        file_name=config["book"],
        sheet_name=config["sheet"],
        start_row=config["header_row"],
    )[config["skip_rows"] :]

    aggregated_results = {}
    for row in vote_data:
        locality, station = extract_codes(row, config, knesset)
        if locality is None:
            continue

        for bloc, excel_column, party_id in bloc_data.get(knesset, []):
            if excel_column in row:
                vote_count = int(row[excel_column])
                key = (knesset, locality, station, bloc, party_id)
                aggregated_results.setdefault(
                    key,
                    {
                        "Knesset": knesset,
                        "Locality": locality,
                        "Station": station,
                        "Bloc": bloc,
                        "Votes": 0,
                        "Party": party_id,
                    },
                )["Votes"] += vote_count

    file_name = f"output/elections/{knesset}.tsv"
    pyexcel.save_as(
        records=aggregated_results.values(), dest_file_name=file_name, delimiter=","
    )


def extract_codes(row, config, knesset):
    """Extract locality and station codes, handling different formats based on provided columns."""
    try:
        locality = float(row[config["locality_col"]])
        station = float(row[config["station_col"]])
        if locality == config["military_booth"]:
            return None, None

        if knesset in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]:
            locality *= 10
        if knesset in [14, 15, 18, 19, 20, 21, 22, 23, 24, 25]:
            station *= 10

        return int(locality), int(station)
    except ValueError:
        return None, None


def main():
    """Main function to process and save voting data for multiple Knesset years."""

    knesset_data = {
        13: {
            "book": "data/13/1992 Elections Corrected.xlsx",
            "sheet": "Corrected",
            "header_row": 2,
            "skip_rows": 1,
            "locality_col": "Locality code",
            "station_col": "Polling station code",
            "military_booth": None,
        },
        14: {
            "book": "data/14/results_14.xls",
            "sheet": "הבחירות לכנסת 1996 לפי קלפי",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "סמל קלפי",
            "military_booth": None,
        },
        15: {
            "book": "data/15/results_15.xls",
            "sheet": "Knesset",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "קלפי",
            "military_booth": 0,
        },
        16: {
            "book": "data/16/results_16.xls",
            "sheet": "TOZAOT",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "סמל קלפי",
            "military_booth": 0,
        },
        17: {
            "book": "data/17/results_17.xls",
            "sheet": "kalfiyot",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "מספר קלפי",
            "military_booth": 0,
        },
        18: {
            "book": "data/18/results_18.xls",
            "sheet": "kalpiot",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "סמל קלפי",
            "military_booth": 0,
        },
        19: {
            "book": "data/19/results_19.xls",
            "sheet": "קובץ תוצאות כנסת 19 לפי ישובים ",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "מספר קלפי",
            "military_booth": 875,
        },
        20: {
            "book": "data/20/results_20.xls",
            "sheet": "expb (1)",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "מספר קלפי",
            "military_booth": 875,
        },
        21: {
            "book": "data/21/21.xlsx",
            "sheet": "expb",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "מספר קלפי",
            "military_booth": 99999,
        },
        22: {
            "book": "data/22/תוצאות הבחירות 22 לפי קלפיות בישובים.xlsx",
            "sheet": "תוצאות הבחירות 22 לפי קלפיות בי",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "קלפי",
            "military_booth": 9999,
        },
        23: {
            "book": "data/23/results_23_by_kalpi.xlsx",
            "sheet": "expb",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "קלפי",
            "military_booth": 9999,
        },
        24: {
            "book": "data/24/24.xlsx",
            "sheet": "expb",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "קלפי",
            "military_booth": 9999,
        },
        25: {
            "book": "data/25/25.xlsx",
            "sheet": "expb",
            "header_row": 0,
            "skip_rows": 0,
            "locality_col": "סמל ישוב",
            "station_col": "קלפי",
            "military_booth": 9999,
        },
    }

    knesset_numbers = knesset_data.keys()
    bloc_data = load_bloc_data("data/Blocs.tsv", knesset_numbers)

    for knesset, config in knesset_data.items():
        print(f"Processing Knesset: {knesset}")
        process_and_save_knesset_data(knesset, config, bloc_data)


if __name__ == "__main__":
    main()
