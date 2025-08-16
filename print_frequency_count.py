from collections import Counter
import csv

def print_frequency_count(data):

    sorted_items = data.most_common()

    # Write to CSV file
    with open("frequency_count.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Item", "Count"])  # Header row
        for item, count in sorted_items:
            writer.writerow([item, count])

    return