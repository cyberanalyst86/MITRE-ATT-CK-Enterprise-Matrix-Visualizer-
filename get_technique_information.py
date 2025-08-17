import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

def get_tactic(tactic_links):

    tactic_list = []

    for link in tactic_links:

        pattern = r'TA\d+'
        match_link_text = re.search(pattern, str(link))

        if match_link_text:

            pattern = r'>\s*(.*?)\s*</a>'
            match = re.search(pattern, str(link))

            if match:
                # Group 1 contains the captured text
                tactic = match.group(1).strip()
                tactic_list.append(tactic)
            else:
                tactic = "Error"

        else:
            continue

    return tactic_list

    return

def get_mitigation(mitigation_links):

    #print(f"--- Mitigations Section ---")
    #print(f"Found {len(mitigation_links)} links referencing '/mitigations/M1056'.")
    #print("Associated paragraphs:")
    processed_paragraphs_mitigation = set()  # To avoid printing the same paragraph multiple times


    mitigation_list = []


    for link in mitigation_links:
        # Find the closest parent table row (<tr>) for the link
        # This assumes the mitigation link and its description are in the same row
        table_row = link.find_parent('tr')

        if table_row:
            # Find all paragraph tags within this table row
            paragraphs_in_row = table_row.find_all('p')
            mitigations_in_row = table_row.find_all('a')

            pattern = r'>\s*(.*?)\s*</a>'
            match = re.search(pattern, str(mitigations_in_row[-1]))

            if match:
                # Group 1 contains the captured text
                mitigation =  match.group(1).strip()
            else:
                mitigation = "Error"


            for p_tag in paragraphs_in_row:

                paragraph_text = p_tag.get_text(strip=True)

                # Use the paragraph text as a unique identifier to avoid duplicates
                if paragraph_text not in processed_paragraphs_mitigation:

                    #print("-" * 30)
                    #print(mitigation)
                    #print(f"Link Text: {link.get_text(strip=True)}")
                    #print(f"Link URL: {link['href']}")
                    #print(f"Associated Paragraph: {paragraph_text}")  # Print first 300 chars

                    mitigation_id = link.get_text(strip=True)
                    mitigation_desc = paragraph_text

                    processed_paragraphs_mitigation.add(paragraph_text)

                    mitigation_measure = str(mitigation_id) + "; " + str(mitigation) + "; " + str(mitigation_desc)

                    mitigation_list.append(mitigation_measure)
        else:
            Error = "Error"
            # Fallback if not in a table row, try finding a subsequent paragraph
            # This might be less precise depending on HTML structure
            #next_paragraph = link.find_next('p')
            #if next_paragraph:
            #    paragraph_text = next_paragraph.get_text(strip=True)
            #    if paragraph_text not in processed_paragraphs_mitigation:
            #        print("-" * 30)
            #        print(f"Link Text (Fallback): {link.get_text(strip=True)}")
            #        print(f"Link URL (Fallback): {link['href']}")
            #        print(f"Associated Paragraph (Fallback): {paragraph_text}")
            #        processed_paragraphs_mitigation.add(paragraph_text)

    if not processed_paragraphs_mitigation:
        print("No associated paragraphs found for the specified mitigation links.")

    return mitigation_list

def get_detection(datasource_links):

    #print(f"--- Datasources Section ---")
    #print(f"Found {len(datasource_links)} links referencing '/datasources/'.")
    #print("Associated paragraphs:")
    processed_paragraphs_datasource = set()  # To avoid printing the same paragraph multiple times

    detection_list = []

    for link in datasource_links:
        # Find the closest parent table row (<tr>) for the link
        # This assumes the datasource link and its description are in the same row
        table_row = link.find_parent('tr')

        if table_row:
            # Find all paragraph tags within this table row
            paragraphs_in_row = table_row.find_all('p')
            detections_in_row = table_row.find_all('a')

            pattern = r'>\s*(.*?)\s*</a>'
            match = re.search(pattern, str(detections_in_row[-1]))

            if match:
                # Group 1 contains the captured text
                detection_source = match.group(1).strip()
            else:
                detection_source = "Error"

            for p_tag in paragraphs_in_row:
                paragraph_text = p_tag.get_text(strip=True)
                # Use the paragraph text as a unique identifier to avoid duplicates
                if paragraph_text not in processed_paragraphs_datasource:
                    #print("-" * 30)
                    #print(detection)
                    #print(f"Link Text: {link.get_text(strip=True)}")

                    link_text = link.get_text(strip=True)

                    pattern = r'DS\d+'
                    match_link_text = re.search(pattern, str(link_text))

                    if match_link_text:
                        # Group 1 contains the captured text
                        detection_id = match_link_text.group()
                    else:
                        detection_id = link_text

                    #print(f"Link URL: {link['href']}")
                    #print(f"Associated Paragraph: {paragraph_text}")  # Print first 300 chars

                    detection_desc = paragraph_text

                    detection_measure = str(detection_id) + "; " + str(detection_source) + "; " + str(detection_desc)

                    detection_list.append(detection_measure)

                    processed_paragraphs_datasource.add(paragraph_text)


        else:
            Error = "Error"
            # Fallback if not in a table row, try finding a subsequent paragraph
            # This might be less precise depending on HTML structure
            #next_paragraph = link.find_next('p')
            #if next_paragraph:
            #    paragraph_text = next_paragraph.get_text(strip=True)
            #    if paragraph_text not in processed_paragraphs_datasource:

            #        print("-" * 30)
            #        print(f"Link Text (Fallback): {link.get_text(strip=True)}")
            #        print(f"Link URL (Fallback): {link['href']}")
            #        print(f"Associated Paragraph (Fallback): {paragraph_text}")
            #        processed_paragraphs_datasource.add(paragraph_text)

    if not processed_paragraphs_datasource:
        print("No associated paragraphs found for the specified datasource links.")

    return detection_list

def get_website_content(url):
    """
    Fetches the content of a given URL and parses it with BeautifulSoup.

    Args:
        url (str): The URL of the website to fetch.

    Returns:
        tuple: A tuple containing:
            - BeautifulSoup object: The parsed HTML content if successful.
            - str: An error message if fetching or parsing fails, otherwise None.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup, None
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching content from {url}: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"

def get_technique_information(counter):

    top_n = counter.most_common(5)

    # Extract just the values into a list
    technique_id_list = [item[0] for item in top_n]

    base_url = "https://attack.mitre.org/techniques/"

    df_list = []

    for technique_id in technique_id_list:

        url = str(base_url) + str(technique_id)

        print(url)

        soup_object, error_message = get_website_content(url)

        #print(soup_object)

        if soup_object:
            #print(f"Successfully fetched and parsed: {url}")
            #print(f"Page Title: {soup_object.title.string if soup_object.title else 'No title found'}\n")

            title = soup_object.title.string if soup_object.title else 'No title found'


            tactic_links = soup_object.find_all('a', href=lambda href: href and "/tactics/" in href)

            tactic_list = get_tactic(tactic_links)


            # --- Section for Mitigations ---
            # Find all <a> tags that have an href containing "/mitigations/M1056"
            mitigation_links = soup_object.find_all('a', href=lambda href: href and "/mitigations/" in href)

            if mitigation_links:

                mitigation_list = get_mitigation(mitigation_links)

            else:
                print("No links found with 'href' containing '/mitigations/'.")

            print("\n" + "=" * 50 + "\n")  # Separator for different sections

            # --- Section for Datasources ---
            # Find all <a> tags that have an href containing "/datasources/"
            datasource_links = soup_object.find_all('a', href=lambda href: href and "/datasources/" in href)

            if datasource_links:

                detection_list = get_detection(datasource_links)

            else:
                print("No links found with 'href' containing '/datasources/'.")

        else:
            print(f"Failed to fetch or parse content: {error_message}")


        data = {
            "url" : [url],
            "tactic" : [tactic_list],
            "Technique" : [title.split("-")[0]],
            "mitigation" : ['\n'.join(mitigation_list)],
            "detection" : ['\n'.join(detection_list)]
        }

        df = pd.DataFrame(data)

        df_list.append(df)

    df_concat = pd.concat(df_list)
    df_concat.to_excel("defence_measure.xlsx", index=False)