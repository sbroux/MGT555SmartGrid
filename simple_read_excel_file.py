import os # For file path operations
import pandas as pd   # For reading Excel file

excel_path = os.path.join(os.path.dirname(__file__), 'databases', 'database_test_PV_Power.csv')

def main():
    # Load solar power data from Excel file using Pandas
    df_PV = pd.read_csv(excel_path, on_bad_lines='skip')

    print(df_PV)

if __name__ == "__main__":
    main()