import requests

class ApiService:
    def post_json(self, url, data, filterType):
        # send filterType as a separate query parameter
        params = {'filterType': filterType}
        response = requests.post(url, json=data, params=params)
        print(f"POST {url} - filterType={filterType} - Status Code: {response.status_code} - Response: {response.text}")
        return response