from docx import Document
import pandas as pd
from fastnumbers import fast_real


# Function to normalize text for comparison
def normalize_text(text):
    return "".join(text.split()).replace('"', "").lower()


# Function to check if a row is a header
def is_header(row, headers):
    return all(
        normalize_text(cell.text) == header for cell, header in zip(row.cells, headers)
    )


# Read Document
doc = Document("data/19/AllStations.docx")

# Headers
headers = [
    "צורפ ל-",
    "בוחרי כנסת",
    "נגישה מיוחדת",
    "נגישה",
    "מקום קלפי",
    "כתובת קלפי",
    "סמל קלפי",
    "שם ישוב בחירות",
    "סמל ישוב בחירות",
    "שם ועדה",
    "סמל ועדה",
]
normalized_headers = [normalize_text(h) for h in headers]
data = []

# Process each table
for table in doc.tables:
    for row in table.rows:
        if not is_header(row, normalized_headers):
            # Fix single row error
            row_data = [
                1
                if normalize_text(cell.text) == "1.0ש"
                else fast_real(normalize_text(cell.text), default=cell.text)
                for cell in row.cells
            ]
            data.append(row_data)

# Create DataFrame and write to Excel
df = pd.DataFrame(data, columns=headers)
df.to_excel("data/19/19_stations.xlsx", sheet_name="DataSheet", index=False)
