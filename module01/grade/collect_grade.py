#!/usr/bin/env python3

import requests
import json
import sys
import base64
import hmac
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_random_number(seed: str) -> str:
    secret_key = "INSERT_KEY_HERE"
    # Convert the seed and key to bytes
    seed_bytes = seed.encode('utf-8')
    key_bytes = secret_key.encode('utf-8')
    # Create the HMAC-SHA-256 hash
    hmac_digest = hmac.new(key_bytes, seed_bytes, hashlib.sha256).digest()
    # Convert the entire HMAC digest to an integer
    large_int = int.from_bytes(hmac_digest, byteorder='big')
    # Convert the integer to a string and take the first 8 digits
    pseudonym = str(large_int)[:8]
    return pseudonym


def sign(data):
    # Load the private key
    with open("rsa_private_key.pem", "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None,
        )

    # Sign the data
    signature = private_key.sign(
        data=data.encode(), padding=padding.PKCS1v15(), algorithm=hashes.SHA256()
    )
    cleanedSignature = base64.b64encode(signature).decode("utf-8")
    return cleanedSignature

if __name__ == "__main__":

    # Switch when developing
    filename = "lti.json"
    # filename = "dev-lti.json"

    with open(filename, "r") as f:
        student_data = json.load(f)
    student_id = generate_random_number(student_data["user_id"])
    exercise_id = "exercise01"

    url = "https://external-service.fly.dev/result"
    headers = {"Content-Type": "application/json"}
    payload = {
        "exerciseId": exercise_id,
        "studentId": student_id,
    }

    payload_to_be_signed = json.dumps(payload, separators=(",", ":"))
    signature = sign(payload_to_be_signed)
    data = {"payload": payload, "signature": signature}
    data_to_send = json.dumps(data, separators=(",", ":"))
    response = requests.post(url, headers=headers, data=data_to_send)
    if response.status_code != 200:
        error_message = response.json().get("error")
        print(f"ERROR: Error sending request to Vikaa")
        print(error_message)
        sys.exit(f"Sending request failed, status code not 200: {error_message}")

    grade = response.json()["grade"]
    feedback = response.json()["feedback"]

    print(
        f"""
        <h3>Result Retrieval Success</h3>
        <p>You achieved {grade} out of 100 points.</p></br>
        <b>Feedback:</b></br>
        <p>{feedback}</p>
    """
    )
    print("TotalPoints: {}\nMaxPoints: {}".format(grade, 100))