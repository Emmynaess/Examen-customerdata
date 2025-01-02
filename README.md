
# Automated Data Cleaning and SQL Database Integration

This project automates the generation, validation, and upload of customer data to an SQL database using Python, GitHub Actions, and Azure SQL.

---

## **Preparation**

### **1. Install the Project**
1. Create a virtual environment in VS Code:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **2. Configure Azure Maps**
1. Log in to Azure and create an Azure Maps account.
2. Navigate to your Azure Maps key and copy your **Primary Key**.
3. Create a file in the same folder (data_to_excel) as your scripts called `config.py` and fill it with the following code:
   ```python
   AZURE_MAPS_API_KEY = "your_azure_maps_key"
   ```
   Note: This file should never be uploaded to GitHub. Make sure to add it to `.gitignore`.

### **3. Modify Row Count (Optional)**
If you need to change the number of rows generated, modify the following lines in the respective scripts:
1. **`data_generator.py`**:
   ```python
   def generate_data(rows=10, max_retries=10):
   def generate_and_corrupt_data(rows=10):
   ```
2. **`main.py`**:
   ```python
   customer_data = generate_and_corrupt_data(10)
   ```
Replace `10` with the desired number of rows.

### **4. Generate Customer Data**
1. Run the main script:
   ```bash
   python main.py
   ```
   This will create a file named `customer_data.xlsx` containing the generated customer data.

### **5. Create an Azure SQL Database**
1. Log in to Azure and create:
   - An SQL server.
   - An SQL database linked to the server.
2. Take note of:
   - Server name (e.g., `your-server.database.windows.net`)
   - Database name
   - Username
   - Password

### **6. Create Tables and Populate Products**
1. Open SQL Server Management Studio (SSMS).
2. Connect to your Azure SQL database.
3. Run the following SQL script to create tables and populate products:
   ```sql
   -- Example script is available in 'upload_to_sql.sql'
   -- Copy the code from the file and run it here
   ```

### **7. Configure GitHub Secrets**
1. Go to your GitHub repository.
2. Add the following secrets under **Settings -> Secrets and variables -> Actions**:
   - `AZURE_SQL_SERVER`: Your Azure SQL server name.
   - `AZURE_SQL_DATABASE`: Your database name.
   - `AZURE_SQL_USER`: Your database username.
   - `AZURE_SQL_PASSWORD`: Your database password.
   - `AZURE_MAPS_API_KEY`: Your Azure Maps key.

### **8. Run the Pipeline**
#### Manually
1. Go to your GitHub repository.
2. Run the workflow manually by navigating to the **Actions** tab, selecting the workflow, and clicking **Run workflow**.

#### Automatically
1. Modify the workflow configuration in `.github/workflows/main.yml` to automatically trigger on `git push`:
   ```yaml
   on:
     push:
       branches:
         - main
   ```

---

## **Troubleshooting**
1. Check the logs from GitHub Actions if the pipeline fails.
2. Verify that tables and products have been created correctly in the Azure SQL database.
3. Ensure `config.py` contains a valid Azure Maps key.

---

## **Future Development**
This project serves as a foundation for automated data management. Future improvements could include:
- Integration with other Azure services.
- Visualizations via Power BI.
- Data analysis and predictions using machine learning.

Bon appétit! 🚀
