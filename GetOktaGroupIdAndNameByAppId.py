import csv
import requests

# Define your Okta domain and API token
your_okta_domain = "<<okta_domain>>" #okta domain
api_token = "<<api_token>>" #api token

# Define the headers for the API request
headers = {"Authorization": f"SSWS {api_token}"}

# Function to get group IDs by app ID
def get_group_ids(app_id):
    url = f"https://{your_okta_domain}/api/v1/apps/{app_id}/groups"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching groups for app ID {app_id}: {response.status_code}")
        return []
    groups = response.json()
    group_ids = [group['id'] for group in groups]
    return group_ids

# Function to get group name by group ID
def get_group_name(group_id):
    url = f"https://{your_okta_domain}/api/v1/groups/{group_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching group details for group ID {group_id}: {response.status_code}")
        return "Not Found"
    group = response.json()
    return group.get('profile', {}).get('name', 'Not Found')

# Read app IDs from CSV file and get group IDs and names
def read_csv_and_get_group_info(csv_file_path):
    app_group_info = {}
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            app_id = row[0]
            group_ids = get_group_ids(app_id)
            group_info = [{"id": group_id, "name": get_group_name(group_id)} for group_id in group_ids]
            app_group_info[app_id] = group_info if group_info else [{"id": "Not Found", "name": "Not Found"}]
    return app_group_info

# Example usage
csv_file_path = 'app_ids.csv'
app_group_info = read_csv_and_get_group_info(csv_file_path)
for app_id, groups in app_group_info.items():
    #print(f"App ID: {app_id}")
    for group in groups:
        print(f"App ID: {app_id}, Group ID: {group['id']}, Group Name: {group['name']}")
