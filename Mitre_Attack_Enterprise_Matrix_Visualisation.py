import pandas as pd
from Format_MIITRE_ATTACK_Enterprise_Matrix import *
from Highlight_Techniques_Multiple_Threat_Actor import *
from get_table_from_mitre_groups import *
from get_mitre_groups_techniques import *
from get_threat_actor_group_from_file import *

if __name__ == "__main__":

    #format mitre attack enterprise matrix excel
    format_mitre_attack_enterprise_matrix()

    #get threat actor groups table from "https://attack.mitre.org/groups/"
    df = get_table_from_url()

    #get threat actor group from file
    threat_actor_group_list = get_threat_actor_group_from_file("threat_actor_group.txt")

    # Convert both column and filter values to lowercase for comparison

    filtered_df = df[df['Name'].str.lower().isin([val.lower() for val in threat_actor_group_list])]

    #convert threat actor group id to list
    group_id_list = filtered_df["ID"].values.tolist()

    df_list = []

    #get threat actor group techniques for each threat actor group in the threat_actor_group_list
    for group_id in group_id_list:

        print(group_id)

        df = get_mitre_groups_techniques(group_id)

        df_list.append(df)

    df_concat = pd.concat(df_list)

    #format threat actor group technique ids

    technique_id_list = []

    for index, row in df_concat.iterrows():

        if row["ID"] == row["ID.1"]:

            technique_id_list.append(row["ID"])

        else:

            technique_id = str(row["ID"]) + str(row["ID.1"].replace(".", "/"))

            technique_id_list.append(technique_id)

    data = {

        "mitre" : technique_id_list

    }

    df_technique_id = pd.DataFrame(data)

    Highlight_Techniques_Multiple_Threat_Actor(df_technique_id)


