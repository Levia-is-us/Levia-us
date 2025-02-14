import os
import sys
import json
import markdown
import requests

from dotenv import load_dotenv


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
sys.path.append(project_root)
load_dotenv(env_path)

from engine.tool_framework import run_tool
from engine.tool_framework import BaseTool
from tools.create_gitbook_tool.gitbookapi import GitBookAPI
from tools.create_gitbook_tool.fileManage import file_manage, get_top_title_with_hash

_gitbook = None
_file_manage = None


@run_tool
class SaveMarkdownToGitbook(BaseTool):
    """Tool for saving markdown content to GitBook"""
    def save_markdown_to_gitbook(content, gitbook_api_key,azure_file_server_key,user_website_url):
        global _gitbook
        global _file_manage

        if _gitbook is None:
            _gitbook = GitBookAPI(gitbook_api_key)

        if _file_manage is None:
            _file_manage = file_manage(azure_file_server_key)

        if not content:
            print("Please input markdown or string content!", file=sys.stderr)
            return "Please input markdown or string content!"

        article_title = get_top_title_with_hash(content)
        markdown_content = markdown.markdown(content)
    
        file_info = _file_manage.upload_file(markdown_content, article_title)

        try:
            organizations = _gitbook.get_organizations()
            organization_id = organizations["items"][0]["id"]

            if not organizations:
                _file_manage.delete_file(file_info["name"])
                return "Get organizations failed! please check your gitbook api key"

            # Gets the default space
            spaces = _gitbook.get_spaces(organization_id)
            space_id = spaces["items"][0]["id"]

            content = {"url": file_info["url"], "source": "markdown"}

            importContent = _gitbook.import_content(space_id, content)

            if not importContent:
                _file_manage.delete_file(file_info["name"])
                return "Import content failed!"

            # 3. create change request
            change_request = _gitbook.create_change_request(
                space_id=space_id,
                title="automerge",
            )

            # 4. merge change request
            merge_result = _gitbook.merge_change_request(space_id, change_request["id"])

            if not merge_result:
                _file_manage.delete_file(file_info["name"])
                return "Merge change request failed!"

            return user_website_url + article_title

        except requests.exceptions.RequestException as e:
            _file_manage.delete_file(file_info["name"])
            print(f"Error occurred: {e},file_info: {file_info}", file=sys.stderr)
        except json.JSONDecodeError as e:
            _file_manage.delete_file(file_info["name"])
            print(f"JSON decode error: {e},file_info: {file_info}", file=sys.stderr)
