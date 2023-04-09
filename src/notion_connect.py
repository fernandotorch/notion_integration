import os
import requests
import json
import yaml


class NotionConnectionManager:
    def __init__(self):
        self.setup()
        self.create_empty_subpage(title_text="Created from Python!")

    def setup(self):
        with open("../.config/config.yaml", "r") as config_params:
            try:
                self.params = yaml.safe_load(config_params)
                self.NOTION_KEY = self.params["NOTION_KEY"]
            except yaml.YAMLError as exc:
                print(exc)

        self.headers = {'Authorization': f"Bearer {self.NOTION_KEY}", 
           'Content-Type': 'application/json', 
           'Notion-Version': '2022-06-28'}

    def get_registered_integrations(self):
        search_params = {"filter": {"value": "page", "property": "object"}}
        search_response = requests.post(
            f'https://api.notion.com/v1/search', 
            json=search_params, headers=self.headers)

        return search_response.json()["results"]

    def create_empty_subpage(self, title_text):
        """ Notion API doesn't allow creating children of workspace, but only subpages """
        search_results = self.get_registered_integrations()
        page_id = search_results[0]["id"]

        create_page_body = {
            "parent": { "page_id": page_id },
            "properties": {
                "title": {
                    "type": "title",
                    "title": [
                        { 
                        "type": "text", 
                        "text": { "content": title_text}
                        }]
                }
            },
            "children": [
            {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{ 
                    "type": "text", 
                    "text": { 
                        "content": "This page was made using an Api call!" 
                    } 
                }]
            }
            }
        ]
        }

        create_response = requests.post(
            "https://api.notion.com/v1/pages", 
            json=create_page_body, headers=self.headers)
        print(create_response.json())
        # print(create_page_body)

if __name__ == "__main__":
    notion_connection = NotionConnectionManager()
