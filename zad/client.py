import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method   1111111111111
    payload = {
        "method": "echo",
        "params": ["echome!"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print("data 1: ",response)

    assert response["result"] == "echome!"
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 0

    # Example echo method JSON-RPC 1.0  222222222222
    payload = {
        "method": "echo",
        "params": ["echome!"],
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print("data 2: ",response)

    # Example add method  333333333333333
    payload = {
        "method": "add",
        "params": [1, 2],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print("data 3: ",response)

    assert response["result"] == 3
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1

    # Example foobar method  44444444444444444
    payload = {
        "method": "foobar",
        "params": {"foo": "json", "bar": "-rpc"},
        "jsonrpc": "2.0",
        "id": 3,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print("data 4: ",response)

    assert response["result"] == "json-rpc"
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3

    # Example exception    555555555555555
    payload = {
        "method": "add",
        "params": [0],
        "jsonrpc": "2.0",
        "id": 4,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print("data 5: ",response)
    assert response["error"]["message"] == "Invalid params"
    assert response["error"]["code"] == -32602
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 4

    # Example exception    666666666666666
    payload = {
        "method": "generate",
        "params": [],
        "jsonrpc": "2.0",
        "id": 5,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print("data 6: ",response)


if __name__ == "__main__":
    main()
