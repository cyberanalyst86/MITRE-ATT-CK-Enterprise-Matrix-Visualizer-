import requests
from bs4 import BeautifulSoup
import pandas as pd

def format_technique_table(df):

    df['ID'].replace('ID', pd.NA, inplace=True)

    # Forward fill
    df['ID'] = df['ID'].fillna(method='ffill')

    return df

def get_mitre_groups_techniques(group_id):

    # Step 1: Fetch the web page
    url = 'https://attack.mitre.org/groups/' + str(group_id)
    response = requests.get(url)
    html_content = response.text

    # Step 2: Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Find the table with specific class
    target_table = soup.find('table', class_='table techniques-used background table-bordered')

    # Step 4: Convert to DataFrame
    if target_table:
        df_list = pd.read_html(str(target_table))
        if df_list:
            df = df_list[0]
            #print("✅ Extracted Table with class='table techniques-used background table-bordered':")
            #print(df.head())  # Display first few rows

            # Optional: Save to CSV

            df_formatted = format_technique_table(df)

            group_id_list = []

            for i in range(len(df_formatted)):

                group_id_list.append(group_id)


            df_formatted["group"] = group_id_list

            return df_formatted

    else:
        print("❌ Table with specified class not found.")
