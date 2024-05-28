#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/users/
    """
    r = requests.post("http://localhost:5050/api/v1/users", data=json.dumps({ 'name': "Obafisayo" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r.text)
    # print(r_j.get('id') is None)
    # print(r_j.get('name') == "NewUser")