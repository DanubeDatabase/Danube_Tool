from pathlib import Path

PATH_REF_FOLDER = Path(__file__).parent
print(PATH_REF_FOLDER)

PATH_DANUBE_TABLES_FOLDER =  Path(__file__).parent.parent.parent.parent / "PyDANUBE" / "DANUBE_database"
print(PATH_DANUBE_TABLES_FOLDER)


def dataframe_to_dictionary(df, col_key_name, col_val_name):
    keys = df[col_key_name].tolist()
    values = df[col_val_name].tolist()

    dictionary = dict(zip(keys, values))

    return dictionary