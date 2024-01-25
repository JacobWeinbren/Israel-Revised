import xlrd
import re
import pyexcel
import math

# Regular expressions for processing strings
number_sub = re.compile(r"(-?[0-9]+\.?[0-9]*)")
space_sub = re.compile(r"\s{2,}")


def process_address(address):
    """Process and clean address strings."""
    address = address.replace(",", " ")
    address = number_sub.sub(" \\1 ", address)
    address = space_sub.sub(" ", address)
    return address.strip()


def process_station_number(election_num, station_number):
    """Process station number based on election number."""
    divisor = 10 if election_num in {13, 16, 17} else 1
    return math.floor(station_number / divisor)


def read_sheet(election_num, config):
    """Read and process data from a worksheet."""
    workbook = xlrd.open_workbook(config["workbook"])
    worksheet = workbook.sheet_by_name(config["worksheet"])
    outname = f"output/stations/{election_num}.tsv"
    rows = worksheet.get_rows()

    data = []

    for _ in range(config["skip_rows"]):
        next(rows)

    for row in rows:
        try:
            locality_number = int(
                math.floor(float(row[config["locality_num_col"]].value))
            )
            station_number = int(
                math.floor(float(row[config["station_num_col"]].value))
            )
        except ValueError:
            return None, None

        if locality_number and station_number:
            station_number = process_station_number(election_num, station_number)
            address_name = process_address(str(row[config["address_name_col"]].value))
            locality_name = process_address(str(row[config["locality_name_col"]].value))

            data.append(
                {
                    "Locality Number": locality_number,
                    "Station Number": station_number,
                    "Locality Name": locality_name,
                    "Address Name": address_name,
                }
            )

    pyexcel.save_as(records=data, dest_file_name=outname, encoding="utf-8")


def process_elections(election_configs):
    """Process elections based on provided configurations."""
    for election_num, config in election_configs.items():
        print(f"Processing Knesset: {election_num}")
        read_sheet(election_num, config)


# Configuration for each election
election_configs = {
    14: {
        "workbook": "data/14/results_14.xls",
        "worksheet": "הבחירות לכנסת 1996 לפי קלפי",
        "skip_rows": 1,
        "locality_num_col": 0,
        "station_num_col": 1,
        "locality_name_col": 3,
        "address_name_col": 4,
    },
    17: {
        "workbook": "data/17/results_17.xls",
        "worksheet": "kalfiyot",
        "skip_rows": 150,
        "locality_num_col": 0,
        "station_num_col": 1,
        "locality_name_col": 2,
        "address_name_col": 3,
    },
    19: {
        "workbook": "data/19/19_stations.xlsx",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 8,
        "station_num_col": 6,
        "locality_name_col": 7,
        "address_name_col": 5,
    },
    20: {
        "workbook": "data/20/TellThePolls.9.3.xls",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 2,
        "station_num_col": 4,
        "locality_name_col": 1,
        "address_name_col": 5,
    },
    21: {
        "workbook": "data/21/kalpies_full_report.xls",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 2,
        "station_num_col": 4,
        "locality_name_col": 1,
        "address_name_col": 6,
    },
    22: {
        "workbook": "data/22/kalpies_report_tofes_b_6th_edition_15_9.xlsx",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 2,
        "station_num_col": 4,
        "locality_name_col": 1,
        "address_name_col": 6,
    },
    23: {
        "workbook": "data/23/kalpies_report_19_1_20_1.xlsx",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 5,
        "station_num_col": 9,
        "locality_name_col": 2,
        "address_name_col": 11,
    },
    24: {
        "workbook": "data/24/kalpies_report_tofes_b_18.3.21.xlsx",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 2,
        "station_num_col": 4,
        "locality_name_col": 1,
        "address_name_col": 6,
    },
    25: {
        "workbook": "data/25/kalpiplaces_kalpieslist_27-10.xlsx",
        "worksheet": "DataSheet",
        "skip_rows": 1,
        "locality_num_col": 2,
        "station_num_col": 4,
        "locality_name_col": 1,
        "address_name_col": 6,
    },
}


process_elections(election_configs)
