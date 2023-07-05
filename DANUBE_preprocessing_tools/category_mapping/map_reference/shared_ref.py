from pathlib import Path

PATH_REF_FOLDER = Path(__file__).parent
print(PATH_REF_FOLDER)

def dataframe_to_dictionary(df, col_key_name, col_val_name):
    keys = df[col_key_name].tolist()
    values = df[col_val_name].tolist()

    dictionary = dict(zip(keys, values))

    return dictionary