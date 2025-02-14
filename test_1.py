from engine.utils.tokenizer import is_message_too_long

text = """
    <code_breakdown>
    **List of Functions Identified:**
    - `save_markdown_to_gitbook`

    **Function: `save_markdown_to_gitbook`**

    i. **Function Signature:**
    ```python
    """
    
print(is_message_too_long(text, 10, 1))
