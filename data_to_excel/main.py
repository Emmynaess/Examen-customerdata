from data_generator import generate_and_corrupt_data
from file_saver import save_to_excel

def main():
    customer_data = generate_and_corrupt_data(10)
    save_to_excel(customer_data, "customer_data.xlsx")

if __name__ == "__main__":
    main()