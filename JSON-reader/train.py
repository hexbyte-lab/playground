import requests

# Step 1: Set URL
url = "https://jsonplaceholder.typicode.com/users"

# Step 2: Make request
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    for user in data:
        print(user["name"])
else:
    print(f"Error: {response.status_code}")

# # Step 3: Parse JSON
# data = response.json()  # Python list of dicts

# # Step 4: Access and print data
# for user in data:
#     print(f"Name: {user['name']}, Email: {user['email']}")
