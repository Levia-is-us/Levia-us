import requests


class GitBookAPI:
    def __init__(self, gitbook_api_token):
        self.api_token = gitbook_api_token
        self.base_url = "https://api.gitbook.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_organizations(self):
        response = requests.get(f"{self.base_url}/orgs", headers=self.headers)
        return response.json()

    def get_spaces(self, organization_id):
        response = requests.get(
            f"{self.base_url}/orgs/{organization_id}/spaces", headers=self.headers
        )
        return response.json()

    def get_pages(self, space_id):
        response = requests.get(
            f"{self.base_url}/spaces/{space_id}/content", headers=self.headers
        )
        return response.json()

    def import_content(self, space_id, content):
        response = requests.post(
            f"{self.base_url}/spaces/{space_id}/content/import",
            headers=self.headers,
            json=content,
        )
        return response.json()

    def import_content_by_page_id(self, space_id, page_id, content):
        response = requests.post(
            f"{self.base_url}/spaces/{space_id}/content/page/{page_id}/import",
            headers=self.headers,
            json=content,
        )
        return response.json()

    def create_change_request(self, space_id, title):
        # """create change request"""
        url = f"{self.base_url}/spaces/{space_id}/change-requests"
        data = {
            "subject": title,
        }

        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def merge_change_request(self, space_id, change_request_id):
        url = f"{self.base_url}/spaces/{space_id}/change-requests/{change_request_id}/merge"
        response = requests.post(url, headers=self.headers)
        return response.json()
