import pyexcel, ujson
from collections import defaultdict


def load_bloc_data(file_name):
    """Load and organise bloc data from a file into a dictionary."""
    bloc_data = defaultdict(list)
    for record in pyexcel.get_records(file_name=file_name):
        bloc_data[record["Knesset #"]].append((record["Bloc"], record["Excel Name"]))
    return bloc_data


def aggregate_votes(knesset, vote_data, bloc_data, military_code):
    """Aggregate vote counts for each station and bloc from the provided data."""
    voting_results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for row in vote_data:
        locality, station = extract_codes(row, knesset, military_code)
        if locality is not None:
            for bloc, excel_column in bloc_data[knesset]:
                vote_count = int(row[excel_column])
                voting_results[locality][station][bloc] += vote_count

    return voting_results


def extract_codes(row, knesset, military_code):
    """
    Extract locality and station codes from a row of data, based on Knesset number.
    Skips military codes.
    """
    locality_col = "Locality code" if knesset < 14 else "סמל ישוב"
    station_col = (
        "Polling station code"
        if knesset < 14
        else "סמל קלפי"
        if knesset < 19
        else "מספר קלפי"
    )

    locality = int(row[locality_col])
    station = (
        int(row[station_col]) // 10
        if knesset in [13, 16, 17]
        else int(row[station_col])
    )

    if locality == military_code:
        return None, None

    return locality, station


def process_knesset_year(knesset, data_config, bloc_data):
    """Process voting data for a specific Knesset year."""
    vote_data = pyexcel.get_records(
        file_name=data_config["book"],
        sheet_name=data_config["sheet"],
        start_row=data_config["header_row"],
    )
    for _ in range(data_config["skip_rows"]):
        next(vote_data)
    return aggregate_votes(
        knesset, vote_data, bloc_data, data_config["military_settlement"]
    )


def main():
    """Main function to process and save voting data for multiple Knesset years."""
    bloc_data = load_bloc_data("blocs.tsv")
    all_voting_results = {}

    knesset_data = {
        13: {
            "book": "../../data/13/13_Corrected.xls",
            "sheet": "1992pol",
            "header_row": 2,
            "skip_rows": 1,
            "settlement_col": "Locality code",
            "booth_col": "Polling station code",
            "military_settlement": None,
        },
        14: {
            "book": "../../data/14/results_14.xls",
            "sheet": "הבחירות לכנסת 1996 לפי קלפי",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "סמל קלפי",
            "military_settlement": None,
        },
        15: {
            "book": "../../data/15/results_15.xls",
            "sheet": "Knesset",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "קלפי",
            "military_settlement": 0,
        },
        16: {
            "book": "../../data/16/results_16.xls",
            "sheet": "TOZAOT",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "סמל קלפי",
            "military_settlement": 0,
        },
        17: {
            "book": "../../data/17/results_17.xls",
            "sheet": "kalfiyot",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "מספר קלפי",
            "military_settlement": 0,
        },
        18: {
            "book": "../../data/18/results_18.xls",
            "sheet": "kalpiot",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "סמל קלפי",
            "military_settlement": 0,
        },
        19: {
            "book": "../../data/19/results_19.xls",
            "sheet": "קובץ תוצאות כנסת 19 לפי ישובים",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "מספר קלפי",
            "military_settlement": 875,
        },
        20: {
            "book": "../../data/20/results_20.xls",
            "sheet": "expb (1)",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "מספר קלפי",
            "military_settlement": 875,
        },
        21: {
            "book": "../../data/21/21.xls",
            "sheet": "Sheet1",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "מספר קלפי",
            "military_settlement": 99999,
        },
        22: {
            "book": "../../data/22/22.xls",
            "sheet": "Sheet1",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "קלפי",
            "military_settlement": 9999,
        },
        23: {
            "book": "../../data/23/23.xls",
            "sheet": "Sheet1",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "קלפי",
            "military_settlement": 9999,
        },
        24: {
            "book": "../../data/24/24.xls",
            "sheet": "Sheet1",
            "header_row": 0,
            "skip_rows": 0,
            "settlement_col": "סמל ישוב",
            "booth_col": "קלפי",
            "military_settlement": 9999,
        },
    }

    for knesset, config in knesset_data.items():
        print("Processing Knesset:", knesset)
        voting_results = process_knesset_year(knesset, config, bloc_data)
        all_voting_results[knesset] = voting_results

    with open("politics.json", "w") as f:
        ujson.dump(all_voting_results, f)


if __name__ == "__main__":
    main()
