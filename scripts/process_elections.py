import pyexcel


def load_bloc_data(file_name):
    """Load and organise bloc data from a file into a dictionary."""
    bloc_data = {}
    for record in pyexcel.get_records(file_name=file_name):
        key = record["Knesset #"]
        if key not in bloc_data:
            bloc_data[key] = []
        bloc_data[key].append((record["Bloc"], record["Excel Name"]))
    return bloc_data


def extract_codes(row, config):
    """Extract locality and station codes, handling different formats based on provided columns."""
    locality = int(row[config["locality_col"]])
    station = int(row[config["station_col"]])

    if locality == config["military_booth"]:
        return None, None

    return locality, station


def aggregate_votes(knesset, vote_data, bloc_data, config):
    """Aggregate vote counts for each station and bloc."""
    results = []
    for row in vote_data:
        locality, station = extract_codes(row, config)
        if locality is not None:
            for bloc, excel_column in bloc_data[knesset]:
                vote_count = int(row[excel_column])
                results.append(
                    {
                        "Knesset": knesset,
                        "Locality": locality,
                        "Station": station,
                        "Bloc": bloc,
                        "Votes": vote_count,
                    }
                )
    return results


def process_and_save_knesset_data(knesset, config, bloc_data):
    """Process and save voting data for a specific Knesset year."""
    vote_data = pyexcel.get_records(
        file_name=config["book"],
        sheet_name=config["sheet"],
        start_row=config["header_row"],
    )
    for _ in range(config["skip_rows"]):
        next(vote_data)

    results = aggregate_votes(knesset, vote_data, bloc_data, config)

    file_name = f"output/elections/{knesset}.tsv"
    pyexcel.save_as(records=results, dest_file_name=file_name)


def main():
    """Main function to process and save voting data for multiple Knesset years."""
    bloc_data = load_bloc_data("data/Blocs.tsv")

    knesset_data = {
        13: {
            "book": "data/13/1992 Elections Corrected.xls",
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

    for knesset, config in knesset_data.items():
        print(f"Processing Knesset: {knesset}")
        process_and_save_knesset_data(knesset, config, bloc_data)


if __name__ == "__main__":
    main()
