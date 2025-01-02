import pandas as pd

def save_to_excel(df, filename):
    df["ProductID"] = df["ProductID"].astype(str)
    
    df = df.sort_values(by="Purchase Date", ascending=False)
    df = df.groupby("Purchase Date", group_keys=False).apply(
        lambda x: x.sample(frac=1)
    ).reset_index(drop=True)
    df = df.sort_values(by="Purchase Date", ascending=False).reset_index(drop=True)
    df.to_excel(filename, index=False)
    print(f"Excel file '{filename}' has been created.")