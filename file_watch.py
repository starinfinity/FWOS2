import paramiko
import json
import re


def get_server_credentials(server_key):
    with open('server_creds.json', 'r') as file:
        server_creds = json.load(file)

    if server_key in server_creds:
        return server_creds[server_key]
    else:
        raise ValueError(f"Server key '{server_key}' not found in server_creds.json")


def check_file(task):
    try:
        # Get the server credentials
        creds = get_server_credentials(task['server_key'])

        hostname = creds['hostname']
        username = creds['username']
        password = creds['password']

        # Connect to the server using SFTP
        transport = paramiko.Transport((hostname, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in the directory
        files = sftp.listdir(task['filepath'])

        # Check if any filename matches the pattern (regex)
        pattern = re.compile(task['filename'])
        for file in files:
            if pattern.match(file):
                print(f"File {file} found in {task['filepath']}")
                sftp.close()
                transport.close()
                return True

        print(f"File matching {task['filename']} not found in {task['filepath']}")
        sftp.close()
        transport.close()
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
