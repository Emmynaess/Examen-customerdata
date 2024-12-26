import os
import pandas as pd
import re

def format_phone_number(phone) -> str:
    if pd.isna(phone):
        return ""
    if not isinstance(phone, str):
        phone = str(phone)
    phone = re.sub(r"[^\d+]", "", phone)
    return phone

def is_valid_phone_number(phone) -> bool:
    return phone.startswith("+46") and len(phone) == 12

def main():
    df = pd.read_excel("customer_data.xlsx")

    df["Phone"] = df["Phone"].apply(format_phone_number)

    invalid_conditions = (
        df["First Name"].str.contains(r'\d', na=False) | 
        ~df["Email"].str.contains("@", na=False) |
        ~df["Phone"].apply(is_valid_phone_number) |
        df["Streetname"].isin(["No Street", "Fallback Street"]) |
        df["Postcode"].isin(["No Postcode", "Fallback Postcode"]) |
        df["City"].isin(["No City", "Fallback City"]) |
        df["Municipality"].isin(["No Municipality", "Fallback Municipality"]) |
        df["Purchase Date"].str.contains(r'[^\d-]', na=False) | 
        ~df["Purchase Date"].str.match(r'^\d{4}-\d{2}-\d{2}$', na=False) 
    )

    df_invalid = df[invalid_conditions].copy()
    df_valid = df[~invalid_conditions].copy()

    unique_key = ["First Name", "Last Name", "Email", "Phone", "Purchase Date", "ProductID"]
    missing_columns = [col for col in unique_key if col not in df_valid.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in df_valid: {missing_columns}")

    duplicates_mask = df_valid.duplicated(subset=unique_key, keep="first")
    df_duplicates = df_valid[duplicates_mask].copy()

    df_valid.drop_duplicates(subset=unique_key, keep="first", inplace=True)

    df_invalid = pd.concat([df_invalid, df_duplicates], ignore_index=True)

    print(f"Total rows in the original data: {len(df)}")
    print(f"Invalid rows (including duplicates): {len(df_invalid)}")
    print(f"Rows in valid data (after removing duplicates): {len(df_valid)}")
    print(f"Number of duplicate rows moved to invalid: {len(df_duplicates)}")

    os.makedirs("customer_data_valid", exist_ok=True)
    os.makedirs("customer_data_invalid", exist_ok=True)

    df_valid["ProductID"] = df_valid["ProductID"].astype(str).str.replace(",", "")
    df_invalid["ProductID"] = df_invalid["ProductID"].astype(str).str.replace(",", "")

    with pd.ExcelWriter("customer_data_valid/customer_data_valid.xlsx", engine="openpyxl") as writer:
        df_valid.to_excel(writer, index=False)

    with pd.ExcelWriter("customer_data_invalid/customer_data_invalid.xlsx", engine="openpyxl") as writer:
        df_invalid.to_excel(writer, index=False)

    print("The following files were created:")
    print("  - customer_data_valid/customer_data_valid.xlsx (validated + deduplicated)")
    print("  - customer_data_invalid/customer_data_invalid.xlsx (invalid + duplicates)")

if __name__ == "__main__":
    main()