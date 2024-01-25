# Israeli Elections - Updated

## Data Source

The Election Committee has removed the files from their website, but they can still be accessed unmodified [in my original project](https://github.com/JacobWeinbren/Israel-Data). They are also partially available in the historical section of the [Knesset Election Site](https://www.gov.il/he/Departments/Guides/election-committee-history?chapterIndex=6).

## Process

1. The 1992 election records were corrected using the 926 PDF.
2. For the 19th Knesset, the data was converted from PDF to DOCX and processed using `fix_19.py`.
3. `xlrd` version 1.2.0 is required to execute `process_stations.py`, as it has both xls and xlsx files.
4. `locations.py` requires a Google API Key
