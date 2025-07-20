import pandas as pd
import re
import json

# --- 1. Read and Parse the Data ---
with open('retail_data.sql', 'r') as f:
    sql_content = f.read()

columns = ['Store_ID', 'Footfall', 'Promo_Spend', 'Avg_Basket', 'Returns', 'Net_Sales']
pattern = re.compile(r"INSERT INTO retail_data VALUES \('(.*?)', (\d+), (\d+), (\d+), (\d+), (\d+)\);")
matches = pattern.findall(sql_content)
df = pd.DataFrame(matches, columns=columns)

numeric_cols = ['Footfall', 'Promo_Spend', 'Avg_Basket', 'Returns', 'Net_Sales']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col])

# --- 2. Calculate Correlations ---
correlations = {
    "Footfall-Net_Sales": df['Footfall'].corr(df['Net_Sales']),
    "Avg_Basket-Net_Sales": df['Avg_Basket'].corr(df['Net_Sales']),
    "Footfall-Avg_Basket": df['Footfall'].corr(df['Avg_Basket']),
}

# --- 3. Find the Strongest Pair ---
strongest_pair = max(correlations, key=lambda k: abs(correlations[k]))
strongest_correlation_value = correlations[strongest_pair]

# --- 4. Create the JSON file ---
output_json = {
    "pair": strongest_pair,
    "correlation": round(strongest_correlation_value, 2)
}

with open('correlation.json', 'w') as f:
    json.dump(output_json, f, indent=2)

print(f"Successfully created 'correlation.json' with the result!")
print(json.dumps(output_json, indent=2))