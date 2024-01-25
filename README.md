# Israeli Elections - Updated

## Data Source

The Election Committee has removed the files from their website, but they remain accessible unaltered [in my original project](https://github.com/JacobWeinbren/Israel-Data). Additionally, they are partially available in the historical section of the [Knesset Election Site](https://www.gov.il/he/Departments/Guides/election-committee-history?chapterIndex=6).

## Process

1. Corrections were made to the 1992 election records using the 926 PDF document.
2. The data for the 19th Knesset was transformed from PDF to DOCX format and then processed with `fix_19.py` to normalise text for comparison purposes and to rectify any errors in rows.
3. To execute `process_stations.py`, which processes station data from xls and xlsx files for various elections, cleans up addresses, and standardizes station numbers, `xlrd` version 1.2.0 must be installed.
4. `process_elections.py` is used to process and store voting data across different Knesset elections and compile vote totals by station and bloc.
5. The script `locations.py` requires a Google API Key to perform geocoding of addresses into latitude and longitude coordinates. This script reads TSV files, identifies unique addresses, and employs the Google Maps API for geocoding.
6. The `combine.py` script merges station data with election results and geocoded locations to produce an extensive dataset.

## Requirements

-   Python 3.x
-   Libraries: `xlrd==1.2.0[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)pyexcel[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)pandas[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)numpy[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)python-docx[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)fastnumbers[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)googlemaps[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)python-dotenv[, ](file:///Users/jacobweinbren/Documents/GitHub/Israel-Revised/README.md#5%2C64-5%2C64)tqdm`
-   A Google API Key for `locations.py` to access the Google Maps Geocoding API.

## Output

The scripts generate output files in the `output` directory, structured as follows:

-   `output/stations/`: Contains TSV files with processed station data for each election.
-   `output/elections/`: Contains TSV files with election results.
-   `output/locations.tsv`: Contains geocoded locations with latitude and longitude.
-   `output/combined/`: Contains the final combined CSV files for each Knesset election.
