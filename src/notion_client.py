"""
Dev notes: 
The Notion API does not yet support uploading files to Notion
"""

import os
import requests
import json
import yaml


class NotionClient:
    def __init__(self):
        self.setup()

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
        
        self.get_registered_pages()

    def get_registered_pages(self):
        search_params = {"filter": {"value": "page", "property": "object"}}
        search_response = requests.post(
            f'https://api.notion.com/v1/search', 
            json=search_params, headers=self.headers)

        self.registered_pages = search_response.json()["results"]
        self.first_page_id = self.registered_pages[0]["id"]

    def create_empty_subpage(self, title_text):
        """ Retrieves first result of registered integrations and creates a new subpage """
        page_id = self.first_page_id

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

    def retrieve_page_info(self, page_id):
        blocks_response = requests.get(
            f"https://api.notion.com/v1/blocks/{self.first_page_id}/children", 
            headers=self.headers)
        print(blocks_response.json())


if __name__ == "__main__":
    client = NotionClient()
    # client.create_empty_subpage(title_text="Created from Python!")
    # client.retrieve_page_info(page_id=integration.first_page_id)
