import pandas as pd
import json
import os, glob

# load data from json files to pandas dataframes
def load_data(file):
    data_list = []
    with open(file) as f:
        # since data are not put in list for each entry, we need to loop through each line
        for line in f:
            data = json.loads(line)
            data_list.append(flatten_json(data))
    return pd.DataFrame(data_list)

# flatten nested json, partially referenced from https://www.geeksforgeeks.org/flattening-json-objects-in-python/
def flatten_json(file):
    out = {}
    def flatten(x, name=''):
        # special logic for this dataset
        if type(x) is dict and "$date" in x and len(x) == 1:
            out[name[:-1]] = x['$date']
        elif type(x) is dict and "$oid" in x and len(x) == 1:
            out[name[:-1]] = x['$oid']
        # If the Nested key-value pair is of dict type
        elif type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        # If the Nested key-value pair is of list type
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(file)
    return out

# convert datatime column to datetime
def convert_to_datetime(df, column):
    df[column] = df[column].apply(lambda x: pd.to_datetime(x, unit='ms') if x is not None else x)
    return df

# check duplicate rows
def check_duplicate_row(table_nm, df):
    df_duplicated = df[df.duplicated()]
    if df_duplicated.shape[0] > 0:
        df_duplicated.to_csv(f"../dq_report/duplicate_rows_{table_nm}.csv", index=False) 
    return df.duplicated().sum()

# check column unique
def check_column_unique(df, column):
    return df[column].duplicated().sum()

# check column missing
def check_column_missing(df, column):
    return df[column].isnull().sum()

# check foreign key constraint
def check_foreign_key(df, column, df_ref, column_ref):
    #count
    df_check = df[~df[column].isin(df_ref[column_ref])][column] 
    if df_check.count() > 0:
        df_check.to_csv(f"../dq_report/foreign_key_constraint_{column}.csv", index=False)
    return df[~df[column].isin(df_ref[column_ref])][column].count()

def main():
    os.chdir(os.path.dirname(__file__))
    
    # clean ../dq_report folder
    folder = ['../dq_report']
    for f in folder:
        for f in glob.glob(os.path.join(f, '*')):
            os.remove(f)

    # load data from json files to pandas dataframes
    df_receipts = load_data('../data/receipts.json')
    df_users = load_data('../data/users.json')
    df_brands = load_data('../data/brands.json')

    # preprocessing: transform date (Unix timestamp (ms)) to datetime
    df_receipts = convert_to_datetime(df_receipts, 'createDate')
    df_receipts = convert_to_datetime(df_receipts, 'dateScanned')
    df_receipts = convert_to_datetime(df_receipts, 'purchaseDate')
    df_receipts = convert_to_datetime(df_receipts, 'finishedDate')
    df_receipts = convert_to_datetime(df_receipts, 'pointsAwardedDate')
    df_receipts = convert_to_datetime(df_receipts, 'modifyDate')
    df_users = convert_to_datetime(df_users, 'createdDate')
    df_users = convert_to_datetime(df_users, 'lastLogin')

    # Users table
    print('Users data from users.json')
    print("total rows: ", df_users.shape[0])
    print('dq1: check for duplicate rows')
    print("_id: ", check_duplicate_row("Users", df_users))
    print('dq2: check column unique')
    print("_id: ", check_column_unique(df_users, '_id'))
    print('dq3: check column missing')
    print("_id: ", check_column_missing(df_users, '_id'))

    # Brands table
    print('\nBrands data from brands.json')
    print("total rows: ", df_brands.shape[0])
    print('dq1: check for duplicate rows')
    print("_id: ", check_duplicate_row("Brands", df_brands))
    print('dq2: check column unique')
    print("_id: ", check_column_unique(df_brands, '_id'))
    print('dq3: check column missing')
    print("_id: ", check_column_missing(df_brands, '_id'))

    # Receipts table
    print('\nReceipts data from receipts.json')
    print("total rows: ", df_receipts.shape[0])
    print('dq1: check for duplicate rows')
    print("_id: ", check_duplicate_row("Receipts", df_receipts))
    print('dq2: check column unique')
    print("_id: ", check_column_unique(df_receipts, '_id'))
    print('dq3: check column missing')
    print("_id: ", check_column_missing(df_receipts, '_id'))
    print('dq4: check foreign key constraint')
    print("userId not in Users table: ", check_foreign_key(df_receipts, 'userId', df_users, '_id'))    


if __name__ == '__main__':
    main()