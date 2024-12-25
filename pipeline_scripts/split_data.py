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
        df["Municipality"].isin(["No Municipality", "Fallback Municipality"])
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

    print(f"Totalt antal rader i ursprungsdata: {len(df)}")
    print(f"Antal felaktiga (inkl. dubbletter) rader: {len(df_invalid)}")
    print(f"Antal rader i valid (efter borttagna dubbletter): {len(df_valid)}")
    print(f"Antal dubblettrader som flyttades till invalid: {len(df_duplicates)}")

    os.makedirs("customer_data_valid", exist_ok=True)
    os.makedirs("customer_data_invalid", exist_ok=True)

    df_valid.to_excel("customer_data_valid/customer_data_valid.xlsx", index=False)
    df_invalid.to_excel("customer_data_invalid/customer_data_invalid.xlsx", index=False)

    print("Följande filer skapades:")
    print("  - customer_data_valid/customer_data_valid.xlsx (validerad + deduplicerad)")
    print("  - customer_data_invalid/customer_data_invalid.xlsx (felaktig + dubbletter)")

if __name__ == "__main__":
    main()





#-------------------------------

"""import os
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
        df["Municipality"].isin(["No Municipality", "Fallback Municipality"])  
    )


    df_invalid = df[invalid_conditions]
    df_valid = df[~invalid_conditions]

    os.makedirs("customer_data_valid", exist_ok=True)
    os.makedirs("customer_data_invalid", exist_ok=True)

    df_valid.to_excel("customer_data_valid/customer_data_valid.xlsx", index=False)
    df_invalid.to_excel("customer_data_invalid/customer_data_invalid.xlsx", index=False)

    print(f"Totalt antal rader: {len(df)}")
    print(f"Valid: {len(df_valid)} | Invalid: {len(df_invalid)}")
    print("Följande filer skapades:")
    print("  - customer_data_valid/customer_data_valid.xlsx")
    print("  - customer_data_invalid/customer_data_invalid.xlsx")

if __name__ == "__main__":
    main()"""