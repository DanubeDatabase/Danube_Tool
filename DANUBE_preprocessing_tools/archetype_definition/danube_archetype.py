from config_show import print_log


def associate_4_danube_vars_archetype(df):

    print_log('TODO - ASSOCIATE ARCHS ENTRIES in DF')
    print("For now - df_archs = df -> need to add algo")

    df_archs = df # to add operations !!!

    return df_archs



def join_df_build_lay(df, DANUBE_LAYERS):
    print("TODO - ADD ALGO TO JOIN OUTPUT WITH DANUBE_LAYERS['DANUBE_BUILD_PREPROCESS']['layer'] BY ID_BUILD")
    print("For now - layer_joined_df = None -> need to add algo")

    layer_joined_df = None
    print(type(layer_joined_df))

    return layer_joined_df


def main_arch(df, DANUBE_LAYERS):
    print_log("+" * 100)
    print_log("Run archetype_definition : Archetype definition")
    print_log("+" * 100)

    df_archs = associate_4_danube_vars_archetype(df)

    layer_joined_df = join_df_build_lay(df_archs, DANUBE_LAYERS)

    return layer_joined_df