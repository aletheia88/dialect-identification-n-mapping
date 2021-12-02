import json
import csv

""" Appropriate converting for small dataset"""

'''
Info to extract from the original json

"business_id": "tnhfDv5Il8EaGSXZGiuQGg"
"city": "San Francisco"
"state": "CA"
'''

def convert_to_csv(json_file_name, csv_file_name, column_names):
    
    with open(csv_file_name, 'w') as csv_file:
        csv_file = csv.writer(csv_file)
        csv_file.writerow(column_names)

        with open(json_file_name) as json_file:
            for line in json_file:
                line_contents = json.loads(line)
                business_info = [line_contents[column_name] 
                        for column_name in column_names]
                csv_file.writerow(business_info)

if __name__ == "__main__":
    
    columns_names = ['business_id', 'city', 'state']
    json_file_name = "yelp_academic_dataset_business.json"
    csv_file_name = "yelp_academic_dataset_business.csv"

    convert_to_csv(json_file_name, csv_file_name, columns_names)
