import os
import pandas as pd
import sqlalchemy
import openpyxl


def generate_ddl_from_file(dir_path, file_name, db_connection):
    ddl_text = ''
    entity_name = file_name.replace('.csv', '').lower()
    read_df = pd.read_csv(os.path.join(dir_path, file_name))

    # Clean data
    # Drop nan values
    read_df = read_df.dropna(axis=0, how='all')
    read_df = read_df.dropna(axis=1, how='all')
    # Lower case column names
    read_df.columns = [x.lower() for x in read_df.columns]
    # Get last column name
    last_column_name = read_df[read_df.columns[-1]].name

    # Save clean df
    read_df.to_csv(os.path.join(dir_path, file_name), sep=',', index=False, header=True)

    # Write DDL
    # DDL Header
    ddl_text = ddl_text + f"CREATE TABLE public.{entity_name} ( \n"

    # ID
    ddl_text = ddl_text + "\t ID SERIAL PRIMARY KEY, \n"

    for column_name in read_df.columns:
        column_name = column_name.strip()
        if "date" in column_name.lower():  # Is a date column
            ddl_text = ddl_text + f"\t {column_name} timestamp"
        elif "ts" in column_name.lower():  # Is a date column
            ddl_text = ddl_text + f"\t {column_name} timestamp"
        else:
            ddl_text = ddl_text + f"\t {column_name} varchar(200)"

        if column_name == last_column_name:
            ddl_text = ddl_text + " \n"
        else:
            ddl_text = ddl_text + ", \n"

    ddl_text = ddl_text + f"); \n \n"

    # Create Table in Postgres
    connection.execute(sqlalchemy.text(ddl_text))
    connection.commit()

    # Add Data to Table
    read_df.to_sql(name=entity_name, con=connection, schema='public', if_exists='append', index=False)

    return ddl_text


if __name__ == '__main__':
    print("## Start Script ## \n")

    input_dir = os.path.join(".", "input")
    csv_dir = os.path.join(".", "temp-csv-data")
    ddl_dir = os.path.join(".", "ddl")

    for target_dir in [input_dir, csv_dir, ddl_dir]:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

    ddl_name = 'Generated_DDL.sql'
    ddl_full_text = ''
    excel_file_name ='Example_Excel_File.xlsx'

    # Create a connection to existing DB
    username = 'postgres'
    password = 'example'
    hostname = 'localhost'
    port_number = '5432'
    database_name = 'postgres'

    engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@{hostname}:{port_number}/{database_name}", echo=True)
    connection = engine.connect()

    # Delete old Tables
    print("Delete old Tables... \n")
    with open(os.path.join(ddl_dir, 'Drop_All_Tables.sql')) as file:
        query = sqlalchemy.text(file.read())
        connection.execute(query)
        connection.commit()

    # Save Excel to CSV
    print("Save Excel to CSVs... \n")
    excel_file = os.path.join(input_dir, excel_file_name)
    workbook = openpyxl.load_workbook(excel_file)
    for sheet in workbook.worksheets:
        pd.read_excel(excel_file, sheet_name=sheet.title) \
            .to_csv(os.path.join(csv_dir, f"{sheet.title}.csv"), index=False)
        print(f"Sheet: {sheet.title} has been saved as CSV")  # Sheet Name

    # Read CSVs, create tables and load data
    print("Read CSVs, create tables and load data... \n")
    for filename in os.listdir(csv_dir):
        print(f'File name: {filename}')
        if filename.endswith('.csv'):
            entity_ddl = generate_ddl_from_file(dir_path=csv_dir, file_name=filename, db_connection=connection)
            ddl_full_text = ddl_full_text + entity_ddl
            print("DDL Generated!")
        print('\n')

    dll_sql_file_name = os.path.join(ddl_dir, ddl_name)
    with open(dll_sql_file_name, "w") as text_file:
        text_file.write(ddl_full_text)

    connection.close()
