import random
import pandas as pd
from utils import generate_swedish_phone_number

def introduce_realistic_errors(df, error_probability=0.05):
    for idx in df.index:
        if random.random() < error_probability:
            error_type = random.choice([
                "typo_in_name", "invalid_email", "wrong_phone_format",
                "shifted_date", "missing_value", "duplicate_with_variation"
            ])

            if error_type == "typo_in_name":
                column = random.choice(["First Name", "Last Name"])
                name = df.at[idx, column]
                if len(name) > 3:
                    typo_index = random.randint(0, len(name)-2)
                    typo_name = name[:typo_index] + name[typo_index+1] + name[typo_index] + name[typo_index+2:]
                    df.at[idx, column] = typo_name

            elif error_type == "invalid_email":
                email = df.at[idx, "Email"]
                if "@" in email:
                    df.at[idx, "Email"] = email.replace("@", "")

            elif error_type == "wrong_phone_format":
                phone = df.at[idx, "Phone"]
                df.at[idx, "Phone"] = phone.replace(" ", "").replace("-", "") + random.choice(["", "0", "1"])

            elif error_type == "shifted_date":
                column = random.choice(["Birthdate", "Purchase Date"])
                date_value = df.at[idx, column]
                if date_value and "-" in date_value:
                    parts = date_value.split("-")
                    parts[0] = parts[0] + "2" if parts[0].isdigit() else parts[0]
                    df.at[idx, column] = "-".join(parts)

            elif error_type == "missing_value":
                column = random.choice(["Email", "Phone"])
                df.at[idx, column] = ""

            elif error_type == "duplicate_with_variation":
                duplicate_row = df.loc[idx].copy()
                duplicate_row["Phone"] = generate_swedish_phone_number()
                df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)

    return df