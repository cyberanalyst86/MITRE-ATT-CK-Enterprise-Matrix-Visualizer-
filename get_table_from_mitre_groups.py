import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_table_from_url():

    table_index = 0

    url = 'https://attack.mitre.org/groups/'
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables in the page
    tables = soup.find_all('table')
    if not tables:
        raise ValueError("No tables found on the webpage.")

    # Select the desired table by index
    table = tables[table_index]

    # Extract headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.get_text(strip=True))

    # Extract rows
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['td'])
        if cells:
            row = [cell.get_text(strip=True) for cell in cells]
            rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers if headers else None)

    return df



