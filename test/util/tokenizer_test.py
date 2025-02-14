import os
import sys
import dotenv
import websockets

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
env_path = os.path.join(project_root, ".env")
dotenv.load_dotenv(env_path)

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from engine.utils.tokenizer import num_tokens_from_string, num_tokens_from_messages

# Example 1: Calculate tokens for single strings
test_strings = ["Hello World!", "Hello, World!", "Hello Hello World World!"]

models = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]

print("=== String Token Calculation ===")
for string in test_strings:
    print(f"\nText: {string}")
    for model in models:
        tokens = num_tokens_from_string(string, model)
        print(f"{model}: {tokens} tokens")

# Example 2: Calculate tokens for conversation messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hello! Happy to help you."},
    {"role": "user", "content": "What is 1+1?"},
    {"role": "assistant", "content": "1+1=2"},
]

print("\n=== Conversation Message Token Calculation ===")
for model in ["gpt-3.5-turbo", "gpt-4"]:
    tokens = num_tokens_from_messages(messages, model)
    print(f"{model}: {tokens} tokens")
    
    
doc = """
<code_breakdown>
**List of Functions Identified:**
- `save_markdown_to_gitbook`

**Function: `save_markdown_to_gitbook`**

i. **Function Signature:**
```python
def save_markdown_to_gitbook(content, article_title, gitbook_api_key):
```

ii. **Parameters:**
- `content`
  - **Type:** Inferred as `str` (string containing markdown or other textual content)
  - **Required:** Yes
  - **Description:** The markdown or string content to be saved to GitBook.
  
- `article_title`
  - **Type:** Inferred as `str` (string representing the title of the article)
  - **Required:** Yes
  - **Description:** The title of the article to be created in GitBook.
  
- `gitbook_api_key`
  - **Type:** Inferred as `str` (string representing the GitBook API key)
  - **Required:** Yes
  - **Description:** The API key used to authenticate with the GitBook API.

iii. **Return Value:**
- **Description:** Returns a URL string pointing to the saved GitBook article upon successful execution. Returns error message strings if input validation fails or if certain operations fail.
- **Type:** `str`

iv. **Purpose:**
The `save_markdown_to_gitbook` function uploads markdown content as an article to GitBook. It handles the conversion of markdown to HTML, uploads the content, interacts with the GitBook API to create and merge change requests, and ultimately returns the URL of the newly created GitBook article.

v. **Notable Aspects of the Implementation:**
- Utilizes a global instance of `GitBookAPI` to manage interactions with the GitBook service.
- Performs input validation to ensure `content` and `article_title` are provided.
- Converts markdown content to HTML using the `markdown` library before uploading.
- Manages file operations such as uploading and deleting temporary files based on the operation's success.
- Handles API interactions to retrieve organizations and spaces, import content, and manage change requests.
- Implements exception handling for network-related errors and JSON decoding issues, ensuring that temporary files are cleaned up in case of failures.

vi. **Edge Cases or Potential Issues:**
- **Organization and Space Retrieval:** Assumes that at least one organization and one space exist. If `get_organizations` or `get_spaces` returns an empty list, the function will fail.
- **Global Variable Usage:** Uses a global `_gitbook` instance, which may lead to issues in concurrent environments or if multiple instances are needed.
- **Error Handling:** Returns error messages as strings, which might not be the best practice for error handling. Raising exceptions could provide more flexibility.
- **Lack of Type Hints:** Parameters and return types are not explicitly typed, which can lead to ambiguities and make the code harder to maintain.
- **File Management:** Relies on external functions `upload_file` and `delete_file` without checking for their success beyond the context provided.
</code_breakdown>

```json
{
  "functions": [
    {
      "method": "save_markdown_to_gitbook",
      "short_description": "Save markdown content to GitBook",
      "detailed_description": "Uploads markdown or string content as an article to GitBook. It converts markdown to HTML, uploads the content, interacts with the GitBook API to create and merge change requests, and returns the URL of the newly created GitBook article. Handles input validation and manages temporary file operations to ensure consistency.",
      "inputs": [
        {
          "name": "content",
          "type": "str",
          "required": true,
          "description": "The markdown or string content to be saved to GitBook."
        },
        {
          "name": "article_title",
          "type": "str",
          "required": true,
          "description": "The title of the article to be created in GitBook."
        },
        {
          "name": "gitbook_api_key",
          "type": "str",
          "required": true,
          "description": "The API key used to authenticate with the GitBook API."
        }
      ],
      "output": {
        "description": "Returns the URL of the saved GitBook article upon success or an error message string if the operation fails.",
        "type": "str"
      }
    }
  ]
}
```
"""

print("\n=== Document Token Calculation ===")
doc_tokens = num_tokens_from_string(doc, "gpt-3.5-turbo")
print(f"gpt-3.5-turbo: {doc_tokens} tokens")
