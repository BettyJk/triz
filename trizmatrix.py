import pandas as pd
import json

# Load the Excel file
file_path = 'triz21.xlsx'  # update if needed
df = pd.read_excel(file_path, sheet_name=0, header=1)  # assuming first sheet, and row 1 is the header

# The first column contains the "worsening" parameters
worsening_params = df.iloc[:, 0]
improving_params = df.columns[1:]

# Prepare the list to collect contradictions
contradictions = []

# Iterate through the matrix
for i, worsening in worsening_params.items():
    for j, improving in enumerate(improving_params):
        cell = df.iloc[i, j + 1]  # +1 because first column is worsening param

        if pd.notna(cell):  # check if there's a recommendation
            # Clean and parse the principles
            principles = [int(p.strip()) for p in str(cell).split(',') if p.strip().isdigit()]
            contradictions.append({
                "improving": improving,
                "worsening": worsening,
                "principles": principles
            })

# Save to JSON file
output_file = 'triz_matrix_output.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(contradictions, f, ensure_ascii=False, indent=2)

print(f"✅ JSON file saved as: {output_file}")
