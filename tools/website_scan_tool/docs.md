

<code_breakdown>
The analysis focuses on identifying functions decorated with @simple_tool, but the provided code uses @run_tool instead. After careful examination:

1. **Identified Functions**:
   - Only the `website_scan` method in the `WebsiteScanTool` class serves as the primary function for website scanning. While the class is decorated with `@run_tool`, the method itself lacks explicit decorators. However, it is the operational entry point for the tool.

2. **Function Signature**:
   - `def website_scan(self, url_list: list, intent: str):`

3. **Parameters**:
   - `url_list: list` (required): List of URLs with summaries to scan.
   - `intent: str` (required): Guides content extraction during scanning.

4. **Return Value**:
   - Returns extracted information (type varies). The normal return value depends on `get_summary_links` (undefined in the code), while errors return a string (e.g., "website connection timeout").

5. **Function Purpose**:
   - Scans websites by collecting links, removing duplicates, extracting content, and summarizing based on intent.

6. **Notable Aspects**:
   - Handles specific timeout errors explicitly.
   - Relies on helper functions (`get_all_links`, `get_summary_links`, etc.) with undefined implementations.

7. **Edge Cases**:
   - Timeout errors return a string instead of structured data.
   - Unhandled exceptions propagate upward.
   - Empty `url_list` may result in incomplete processing.
</code_breakdown>

```json
{
  "functions": [
    {
      "method": "website_scan",
      "short_description": "Scan websites and extract relevant information based on intent",
      "detailed_description": "Scans provided URLs by first extracting all links, removing duplicates, fetching content, and generating a summary filtered by the specified intent. Handles website connection timeouts explicitly.",
      "inputs": [
        {
          "name": "url_list",
          "type": "list",
          "required": true,
          "description": "List of URLs (with summaries) to scan for content"
        },
        {
          "name": "intent",
          "type": "str",
          "required": true,
          "description": "Guiding intent to filter relevant content during scanning"
        }
      ],
      "output": {
        "description": "Extracted information based on intent or error message for timeouts",
        "type": "varies (str/dict/list)"
      }
    }
  ]
}
```