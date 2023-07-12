import pandas as pd

from config_show import print_log


def generalization_archetype_rules(df_gen):  # Modify
    # define df_gen['arch_dept_id'], df_gen['arch_comm_id'] (all cases in df_gen have null id)
    print("TODO")
    df_gen['arch_dept_id'] = "missing"  # put later the algorithms to give an existing 'arch_dept_id'
    df_gen['arch_comm_id'] = "missing"  # put later the algorithms to give an existing 'arch_comm_id'

    return df_gen


def main_archetype_generalization(df):  # do not modify
    """separate the df into 2 parts, one with arch_id other without it
    apply the generalization rules to the part without arch_id
    provide the final df with all values"""
    print_log("*" * 100)
    print_log("Run step 2 of archetype processing : main_archetype_generalization")
    print_log("*" * 100)

    df_ok = df[df.arch_dept_id.notnull()]
    df_gen = df[df.arch_dept_id.isnull()]

    df_gen = generalization_archetype_rules(df_gen)

    final_df = pd.concat([df_ok, df_gen])
    final_df.sort_values('ID_BUILD', inplace=True)

    return final_df
