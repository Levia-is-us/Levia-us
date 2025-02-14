

<code_breakdown>
Identified function:
- save_markdown_to_gitbook (method of SaveMarkdownToGitbook class decorated via @run_tool)

Function signature:
def save_markdown_to_gitbook(content, gitbook_api_key, azure_file_server_key, user_website_url)

Parameters:
1. content (no type hint) - required - markdown/text content to process
2. gitbook_api_key (no type hint) - required - API key for GitBook access
3. azure_file_server_key (no type hint) - required - Credentials for Azure file storage
4. user_website_url (no type hint) - required - Base URL for constructed result

Return value:
- String containing final URL or error message (type: str)

Purpose:
Uploads markdown content to GitBook through a multi-step process involving Azure file storage upload, GitBook API interactions for content import, and change request management.

Notable aspects:
1. Uses global singleton instances for GitBookAPI and file_manage
2. Implicit requirement for .env file configuration
3. Relies on first organization/space from GitBook API responses
4. Automatic cleanup of uploaded files on errors
5. No explicit type validation for input parameters

Edge cases/issues:
- Fails if user has no organizations/spaces in GitBook
- Potential race conditions with global _gitbook/_file_manage
- Assumes first item in organizations/spaces lists is correct
- No retry mechanism for API calls
- Return type inconsistency (URL string vs error message string)
</code_breakdown>

```json
{
  "functions": [
    {
      "method": "save_markdown_to_gitbook",
      "short_description": "Save markdown content to GitBook via API integration",
      "detailed_description": "Processes markdown content by uploading to Azure storage, importing to GitBook through API calls, managing change requests, and returning the final URL. Handles error cleanup and API interactions with GitBook's organization/space structure.",
      "inputs": [
        {
          "name": "content",
          "type": "str",
          "required": true,
          "description": "Markdown/text content to be saved, required for article creation"
        },
        {
          "name": "gitbook_api_key",
          "type": "str",
          "required": true,
          "description": "API key for GitBook authentication, obtained from environment configuration"
        },
        {
          "name": "azure_file_server_key",
          "type": "str",
          "required": true,
          "description": "Credentials for Azure file storage service, used for temporary content hosting"
        },
        {
          "name": "user_website_url",
          "type": "str",
          "required": true,
          "description": "Base URL prefix for the final published content location"
        }
      ],
      "output": {
        "description": "Final published URL string on success, error message string on failure",
        "type": "str"
      }
    }
  ]
}
```