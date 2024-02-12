import requests

def send_get_request(url, params=None, headers=None):
    try:
        # Send GET request
        response = requests.get(url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request was successful!")
            # Return the JSON response
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
url = "https://jsonplaceholder.typicode.com/todos/1"
params = None
headers = {"User-Agent": "MyApp/1.0"}

json_response = send_get_request(url, params=params, headers=headers)

if json_response is not None:
    print("JSON Response:")
    print(json_response)
