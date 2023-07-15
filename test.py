import requests
import json

# Specify the URL of the Flask server
url = "http://localhost:5000/run_simulation"

# Specify the connections for the simulation
step1_data = {
    "Before": 0,
    "After": 1,
    "StepNum": 1
}

# Send a POST request to the server
response = requests.post(url, json=step1_data)
# Print the response from the server
print(response.text)

# Specify the connections for the simulation
step2_data = {
    "Before": 1,
    "After": 2,
    "StepNum": 2
}

# Send a POST request to the server
response = requests.post(url, json=step2_data)
# Print the response from the server
print(response.text)


# Specify the connections for the simulation
step3_data = {
    "Before": 2,
    "After": 4,
    "StepNum": 3
}

# Send a POST request to the server
response = requests.post(url, json=step3_data)
# Print the response from the server
print(response.text)


response = requests.get('http://localhost:5000/get_gif')
if response.status_code == 200:
    with open('agents.gif', 'wb') as f:
        f.write(response.content)
    print("GIF saved successfully.")
else:
    print("Failed to retrieve GIF.")
