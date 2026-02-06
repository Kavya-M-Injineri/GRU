import pandas as pd
import os

csv_path = r'c:\Users\student\Downloads\GRU1\archive\Resume\Resume.csv'
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print("Label Distribution:")
    print(df['Category'].value_counts())
    print(f"\nTotal rows: {len(df)}")
else:
    print("Dataset not found.")
