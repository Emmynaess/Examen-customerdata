import os
import pandas as pd

def format_swedish_phone_number(phone) -> str:
    phone = str(phone)
    if not phone.startswith("+"):
        phone = "+" + phone
    phone = phone.replace(",", "-").replace(" ", "-").strip()
    return phone

def deduplicate_purchases(input_file: str) -> None:
    df = pd.read_excel(input_file)

    print(f"Kolumner i DataFrame: {df.columns.tolist()}")

    unique_key = ["First Name", "Last Name", "Email", "Phone", "Purchase Date", "ProductID"]
    missing_columns = [col for col in unique_key if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in dataframe {missing_columns}")

    before = len(df)
    df = df.drop_duplicates(subset=unique_key, keep="first")
    after = len(df)

    print(f"Antal rader före dubblett-rensning: {before}")
    print(f"Antal rader efter dubblett-rensning: {after}")
    print(f"Antal borttagna dubblettrader: {before - after}")

    df["Phone"] = df["Phone"].astype(str).apply(format_swedish_phone_number)

    # ÖVERSKRIV den befintliga filen
    df.to_excel(input_file, index=False)
    print(f"Deduplicated data saved to: {input_file}")

if __name__ == "__main__":
    deduplicate_purchases("customer_data_valid/customer_data_valid.xlsx")



#----------------------

"""import os
import pandas as pd

def format_swedish_phone_number(phone) -> str:
    phone = str(phone)

    if not phone.startswith("+"):
        phone = "+" + phone

    phone = phone.replace(",", "-").replace(" ", "-").strip()

    return phone

def deduplicate_purchases(input_file: str, output_folder: str) -> None:
    os.makedirs(output_folder, exist_ok=True)
    df = pd.read_excel(input_file)

    print(f"Kolumner i DataFrame: {df.columns.tolist()}")

    unique_key = ["First Name", "Last Name", "Email", "Phone", "Purchase Date", "ProductID"]
    missing_columns = [col for col in unique_key if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in dataframe {missing_columns}")

    before = len(df)
    df = df.drop_duplicates(subset=unique_key, keep="first")
    after = len(df)

    print(f"Antal rader före dubblett-rensning: {before}")
    print(f"Antal rader efter dubblett-rensning: {after}")
    print(f"Antal borttagna dubblettrader: {before - after}")

    df["Phone"] = df["Phone"].astype(str).apply(format_swedish_phone_number)

    output_file = os.path.join(output_folder, "customer_deduplicated_data.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Deduplicated data saved in i: {output_file}")

if __name__ == "__main__":
    deduplicate_purchases(
        input_file="customer_data_valid/customer_data_valid.xlsx",
        output_folder="customer_deduplicated_data"
    )"""



# --------------------

"""import pandas as pd

def deduplicate_purchases(input_file: str, output_file: str) -> None:
    df = pd.read_excel(input_file)

    print(f"Kolumner i DataFrame: {df.columns.tolist()}")

    unique_key = ["First Name", "Last Name", "Email", "Phone", "Purchase Date", "ProductID"]

    missing_columns = [col for col in unique_key if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Följande kolumner saknas i DataFrame: {missing_columns}")

    before = len(df)
    df = df.drop_duplicates(subset=unique_key, keep="first")
    after = len(df)

    print(f"Antal rader före dubblett-rensning: {before}")
    print(f"Antal rader efter dubblett-rensning: {after}")
    print(f"Antal borttagna dubblettrader: {before - after}")

    df.to_excel(output_file, index=False)
    print(f"Deduplicerad data sparad i: {output_file}")

if __name__ == "__main__":
    deduplicate_purchases(
        input_file="customer_data_valid/customer_data_valid.xlsx",  
        output_file="customer_deduplicated_data/customer_data_deduped.xlsx"  
    )"""