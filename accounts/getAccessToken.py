import json
import subprocess

def getAccessToken(number): 
    jsonData = {
        "username": str(number) + "@",
        "password": str(number) + "@yaantec",
    }

    # Convert the Python dictionary to a JSON-formatted string
    json_data_str = json.dumps(jsonData)

    # Construct the curl command using a list of arguments
    curl_command = ['curl', '-X', 'POST', 'http://127.0.0.1:80/api/api/token/', '-H', 'Content-Type: application/json', '-d', json_data_str]
    
    # Run the curl command using subprocess
    try:
        result = subprocess.run(curl_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Print the output of the command
        print("Output:")
        # print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Print error if the command fails
        print("Error:")
        print(e.stderr)
        return e.stderr

# print (regesterUser(123))
