import os
import pandas as pd
import pyodbc

def upload_to_azure():
    file_path = "customer_data_valid/customer_data_valid.xlsx" 
    df = pd.read_excel(file_path)

    server = os.environ["AZURE_SQL_SERVER"]
    database = os.environ["AZURE_SQL_DATABASE"]
    user = os.environ["AZURE_SQL_USER"]
    password = os.environ["AZURE_SQL_PASSWORD"]

    connection_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"Uid={user};"
        f"Pwd={password};"
    )

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    for index, row in df.iterrows():
        try:
            
            # Insert into Customer
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM dbo.Customer
                    WHERE FirstName = ? AND LastName = ? AND Birthdate = ?
                )
                BEGIN
                    INSERT INTO dbo.Customer (FirstName, LastName, Birthdate, CustomerCategory)
                    VALUES (?, ?, ?, ?)
                END
            """, 
            row['First Name'], row['Last Name'], row['Birthdate'],  # För SELECT
            row['First Name'], row['Last Name'], row['Birthdate'], row['Customer Category'])  # För INSERT

            # Retrieve CustomerID
            cursor.execute("""
                SELECT CustomerID FROM Customer
                WHERE FirstName = ? AND LastName = ? AND Birthdate = ?
            """, row['First Name'], row['Last Name'], row['Birthdate'])
            customer_id = cursor.fetchone()[0]

            # Insert into CustomerAddress
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM dbo.CustomerAddress
                    WHERE CustomerID = ? AND StreetName = ? AND Postalcode = ? AND City = ? AND Municipality = ?
                )
                BEGIN
                    INSERT INTO dbo.CustomerAddress (CustomerID, StreetName, Postalcode, City, Municipality)
                    VALUES (?, ?, ?, ?, ?)
                END
            """, 
            customer_id, row['Streetname'], row['Postcode'], row['City'], row['Municipality'],  # För SELECT
            customer_id, row['Streetname'], row['Postcode'], row['City'], row['Municipality'])  # För INSERT

            # Insert into CustomerContactInformation
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM dbo.CustomerContactInformation
                    WHERE CustomerID = ? AND Phone = ? AND Email = ?
                )
                BEGIN
                    INSERT INTO dbo.CustomerContactInformation (CustomerID, Phone, Email)
                    VALUES (?, ?, ?)
                END
            """, 
            customer_id, row['Phone'], row['Email'],  # För SELECT
            customer_id, row['Phone'], row['Email'])  # För INSERT

            # Insert into Purchase
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM dbo.Purchase
                    WHERE CustomerID = ? AND ProductID = ? AND PurchaseDate = ?
                )
                BEGIN
                    INSERT INTO dbo.Purchase (CustomerID, ProductID, PurchaseDate, Quantity, TotalAmount)
                    VALUES (?, ?, ?, ?, ?)
                END
            """, 
            customer_id, row['ProductID'], row['Purchase Date'],  # För SELECT
            customer_id, row['ProductID'], row['Purchase Date'], row['Quantity'], row['Total Amount'])  # För INSERT

            print(f"Row {index} processed successfully.")

        except Exception as e:
            print(f"Error on row {index}: {e}, Data: {row.to_dict()}")
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data from {file_path} has been uploaded to the SQL database.")

if __name__ == "__main__":
        upload_to_azure()
