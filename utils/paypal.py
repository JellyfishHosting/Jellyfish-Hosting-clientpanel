from config import client_id_paypal, client_secret_paypal
import requests
def get_access_token():
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, auth=(client_id_paypal, client_secret_paypal), data=data)
    return response.json()['access_token']