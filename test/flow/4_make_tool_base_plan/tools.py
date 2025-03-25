tools = [{'id': 'smithery_mcp_tool-@wysh3/perplexity-mcp-zerver-find_apis',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@wysh3/perplexity-mcp-zerver"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal request routing", '
                      '"defaultValue": "find_apis"}, {"name": "arguments", '
                      '"type": "object", "required": true, "description": '
                      '"Contains: requirement (string) - Desired '
                      'functionality; context (string) - Project background '
                      'details. Nested parameter requirements unspecified."}], '
                      '"output": {"description": "Results of API evaluation '
                      'process; exact format not specified in documentation", '
                      '"type": "unknown"}}',
              'description': 'This method identifies potential APIs for '
                             'project integration by analyzing functional '
                             'requirements and project context. It utilizes '
                             'internal server configurations and routing '
                             'mechanisms to process API evaluation requests.',
              'details': 'This method identifies potential APIs for project '
                         'integration by analyzing functional requirements and '
                         'project context. It utilizes internal server '
                         'configurations and routing mechanisms to process API '
                         'evaluation requests.',
              'method': 'mcp_call_tool',
              'short_description': 'Find and evaluate APIs for project '
                                   'integration',
              'source': 'smithery',
              'timestamp': 1742378039248.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.332291633,
 'values': []}, {'id': 'smithery_mcp_tool-@wysh3/perplexity-mcp-server-find_apis',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@wysh3/perplexity-mcp-server"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal routing to \'find_apis\' '
                      'tool", "defaultValue": "find_apis"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "JSON object containing: \'requirement\' '
                      "(string) - The functionality to fulfill; 'context' "
                      '(string) - Project-specific context. Necessity of these '
                      'sub-parameters is not explicitly defined."}], "output": '
                      '{"description": "Output details are unspecified in the '
                      'profile (likely returns API evaluation data)", "type": '
                      '"unknown"}}',
              'description': 'Identifies and assesses APIs that could be '
                             'integrated into a project based on specified '
                             'requirements and context.',
              'details': 'Identifies and assesses APIs that could be '
                         'integrated into a project based on specified '
                         'requirements and context.',
              'method': 'mcp_call_tool',
              'short_description': 'Find and evaluate APIs for project '
                                   'integration',
              'source': 'smithery',
              'timestamp': 1742383353101.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.332291633,
 'values': []}, {'id': 'smithery_mcp_tool-@JiantaoFu/appinsightmcp-app-store-search',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@JiantaoFu/appinsightmcp"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'routing", "defaultValue": "app-store-search"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Search parameters: term (string, '
                      "required) - Search term; country (string, default 'us') "
                      '- 2-letter country code; num (number, default 50) - '
                      'Number of results"}], "output": {"description": "Not '
                      'specified in the profile", "type": "Not specified"}}',
              'description': 'Executes an App Store search using MCP '
                             'infrastructure. Requires server configuration '
                             'and tool identifier, accepts search parameters '
                             'through an arguments object.',
              'details': 'Executes an App Store search using MCP '
                         'infrastructure. Requires server configuration and '
                         'tool identifier, accepts search parameters through '
                         'an arguments object.',
              'method': 'mcp_call_tool',
              'short_description': 'Search for apps on the App Store',
              'source': 'smithery',
              'timestamp': 1742379501627.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.262346059,
 'values': []}, {'id': 'smithery_mcp_tool-@bitrefill/bitrefill-mcp-server-search',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@bitrefill/bitrefill-mcp-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal routing", '
                      '"defaultValue": "search"}, {"name": "arguments", '
                      '"type": "object", "required": true, "description": '
                      '"Search criteria container with nested parameters:", '
                      '"nestedParams": [{"name": "query", "type": "string", '
                      '"required": false, "description": "Search term or \'*\' '
                      'for all products"}, {"name": "country", "type": '
                      '"string", "required": false, "description": "ISO '
                      'country code filter (e.g., \'US\', \'IT\')"}, {"name": '
                      '"language", "type": "string", "required": false, '
                      '"description": "Language code for localized results"}, '
                      '{"name": "limit", "type": "number", "required": false, '
                      '"description": "Maximum results per page"}, {"name": '
                      '"skip", "type": "number", "required": false, '
                      '"description": "Pagination offset"}, {"name": '
                      '"category", "type": "string", "required": false, '
                      '"description": "Category filter (e.g., '
                      '\'gaming\')"}]}], "output": {"description": "Search '
                      'results array (exact structure undocumented)", "type": '
                      '"object/array"}}',
              'description': 'Executes product searches including gift cards, '
                             'esims, and mobile topups. Requires prior '
                             'category lookup for optimal results. Accepts '
                             'search terms, country/language filters, and '
                             'pagination parameters.',
              'details': 'Executes product searches including gift cards, '
                         'esims, and mobile topups. Requires prior category '
                         'lookup for optimal results. Accepts search terms, '
                         'country/language filters, and pagination parameters.',
              'method': 'mcp_call_tool',
              'short_description': 'Search for gift cards, esims, mobile '
                                   'topups and related products',
              'source': 'smithery',
              'timestamp': 1742383186816.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.261810601,
 'values': []}, {'id': 'smithery_mcp_tool-@liuyoshio/mcp-compass-recommend-mcp-servers',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@liuyoshio/mcp-compass"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'request routing", "defaultValue": '
                      '"recommend-mcp-servers"}, {"name": "arguments", "type": '
                      '"object", "required": true, "description": "Contains '
                      'query parameters for server discovery. Must include '
                      "'query' string specifying: 1) Target platform/vendor, "
                      '2) Exact operation/service, 3) Technical context."}], '
                      '"output": {"description": "List of matching MCP servers '
                      'with IDs, descriptions, GitHub URLs, and similarity '
                      'scores", "type": "array"}}',
              'description': 'Searches for relevant MCP servers based on '
                             'detailed technical queries. Returns matching '
                             'servers with metadata and similarity scores. '
                             'Requires precise query formatting specifying '
                             'target platform, exact operation, and technical '
                             'context.',
              'details': 'Searches for relevant MCP servers based on detailed '
                         'technical queries. Returns matching servers with '
                         'metadata and similarity scores. Requires precise '
                         'query formatting specifying target platform, exact '
                         'operation, and technical context.',
              'method': 'mcp_call_tool',
              'short_description': 'Discover external MCP servers matching '
                                   'specific operational requirements',
              'source': 'smithery',
              'timestamp': 1742380834317.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.25794667,
 'values': []}, {'id': 'smithery_mcp_tool-@JiantaoFu/appinsightmcp-app-store-reviews',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@JiantaoFu/appinsightmcp"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "app-store-reviews"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Review query parameters '
                      'container", "defaultValue": null}, {"name": '
                      '"arguments.id", "type": "number", "required": true, '
                      '"description": "Numeric App Store application '
                      'identifier", "defaultValue": null}, {"name": '
                      '"arguments.country", "type": "string", "required": '
                      'false, "description": "ISO country code for regional '
                      'reviews", "defaultValue": "us"}, {"name": '
                      '"arguments.page", "type": "number", "required": false, '
                      '"description": "Pagination index for result sets", '
                      '"defaultValue": 1}, {"name": "arguments.sort", "type": '
                      '"string", "required": false, "description": "Review '
                      'sorting method (recent/helpful)", "defaultValue": '
                      'null}], "output": {"description": "Not specified in the '
                      'provided profile documentation", "type": "Unknown"}}',
              'description': 'Retrieves application reviews from the App Store '
                             'using specified parameters including app ID, '
                             'country code, pagination, and sorting '
                             'preferences. Requires server configuration and '
                             'tool routing identifiers.',
              'details': 'Retrieves application reviews from the App Store '
                         'using specified parameters including app ID, country '
                         'code, pagination, and sorting preferences. Requires '
                         'server configuration and tool routing identifiers.',
              'method': 'mcp_call_tool',
              'short_description': 'Get reviews for an App Store app',
              'source': 'smithery',
              'timestamp': 1742379241193.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.238366395,
 'values': []}, {'id': 'smithery_mcp_tool-@bitrefill/bitrefill-mcp-server-detail',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@bitrefill/bitrefill-mcp-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal request '
                      'routing", "defaultValue": "detail"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "JSON object containing product '
                      "parameters. Must include 'id' (string) as Product ID, "
                      'though necessity is implied but not explicitly '
                      'stated."}], "output": {"description": "Detailed product '
                      'information (exact structure not specified in '
                      'profile)", "type": "object (assumed, but not '
                      'documented)"}}',
              'description': 'Fetches comprehensive product details using '
                             'predefined server configurations and product '
                             'identifiers. Requires server ID, tool name for '
                             'routing, and product ID in arguments.',
              'details': 'Fetches comprehensive product details using '
                         'predefined server configurations and product '
                         'identifiers. Requires server ID, tool name for '
                         'routing, and product ID in arguments.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve detailed product information from '
                                   'server',
              'source': 'smithery',
              'timestamp': 1742383277365.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.233111694,
 'values': []}, {'id': 'JobSearchTool-search_jobs',
 'metadata': {'data': '{"method": "search_jobs", "inputs": [{"name": "title", '
                      '"type": "str", "required": true, "description": "Job '
                      "title or keyword to search for (e.g. 'Python "
                      'Developer\', \'Data Scientist\')"}], "output": '
                      '{"description": "A list of matching job postings, where '
                      'each job contains the title and application URL", '
                      '"type": "list"}}',
              'description': "First, I'll identify all the functions within "
                             'the JobSearchTool class which would be executed '
                             'via the run_tool decorator.\n'
                             '\n'
                             'The `@run_tool` decorator is applied to the '
                             'class `JobSearchTool` itself, not to individual '
                             'methods. This means that all the methods within '
                             'this class can potentially be executed as '
                             'tools.\n'
                             '\n'
                             "Let's examine each method:\n"
                             '\n'
                             '1. `search_jobs` function:\n'
                             '   - Signature: `def search_jobs(self, title: '
                             'str):`\n'
                             '   - Parameters: \n'
                             '     - `self`: The instance of the class '
                             '(implicit)\n'
                             '     - `title`: A string representing the job '
                             'title or keyword to search for\n'
                             '   - Return value: A list of job URLs '
                             '(`job_urls` which is defined as `job_list`)\n'
                             '   - Purpose: Searches for jobs based on a title '
                             'or keyword and returns a list of job postings\n'
                             "   - Notable implementation: It doesn't actually "
                             'perform a real search - it just returns a '
                             'pre-defined `job_list`\n'
                             '\n'
                             '2. `job_application` function:\n'
                             '   - Signature: `def job_application(self, '
                             'job_url: list):`\n'
                             '   - Parameters:\n'
                             '     - `self`: The instance of the class '
                             '(implicit)\n'
                             '     - `job_url`: A list of URLs to job '
                             'postings\n'
                             '   - Return value: None explicitly returned '
                             '(returns implicitly `None`)\n'
                             '   - Purpose: Automatically applies to multiple '
                             'jobs using the provided URLs\n'
                             '   - Implementation: Creates a hardcoded list of '
                             'jobs and extracts URLs, then calls an external '
                             '`application` function\n'
                             '\n'
                             'For each method, I need to determine:\n'
                             '- Input parameters with types and whether '
                             "they're required\n"
                             '- Output description and type\n'
                             '- Short and detailed descriptions\n'
                             '\n'
                             'Since both methods are within the class that has '
                             'the `@run_tool` decorator, both would be '
                             'considered as tool functions for our analysis.',
              'details': 'Search jobs across multiple job boards and employer '
                         'websites based on job title or keyword. This '
                         'function aggregates job listings from various '
                         'sources including LinkedIn, Indeed, company career '
                         'pages, and other major job boards.',
              'method': 'search_jobs',
              'short_description': 'Search for jobs across multiple job boards '
                                   'based on job title or keyword',
              'timestamp': 1741853634323.0,
              'tool': 'JobSearchTool',
              'uid': 'levia'},
 'score': 0.230997518,
 'values': []}, {'id': 'smithery_mcp_tool-@wirdes/db-mcp-tool-!tables',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@wirdes/db-mcp-tool"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Internal tool identifier for '
                      'request routing", "defaultValue": "!tables"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Tool-specific parameters object '
                      '(structure undocumented in current profile)"}], '
                      '"output": {"description": "Result from MCP tool '
                      'execution (specific format depends on toolName)", '
                      '"type": "Undocumented - Likely varies by tool"}}',
              'description': 'Invokes an MCP internal tool specified by '
                             'toolName, using a predefined server '
                             'configuration. Required parameters include a '
                             'server reference ID, tool identifier, and '
                             'arguments object. Default values suggest primary '
                             'use for database table operations.',
              'details': 'Invokes an MCP internal tool specified by toolName, '
                         'using a predefined server configuration. Required '
                         'parameters include a server reference ID, tool '
                         'identifier, and arguments object. Default values '
                         'suggest primary use for database table operations.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute MCP package operations using '
                                   'server configuration and tool routing',
              'source': 'smithery',
              'timestamp': 1742376027898.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.225229353,
 'values': []}, {'id': 'smithery_mcp_tool-@ErickWendel/erickwendel-contributions-mcp-check_status',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@ErickWendel/erickwendel-contributions-mcp"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal request '
                      'routing", "defaultValue": "check_status"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Undocumented parameters required for '
                      'API check operation. Structure and requirements not '
                      'specified in available documentation."}], "output": '
                      '{"description": "API health status information '
                      '(specific format not documented)", "type": "Undefined '
                      '(response format not specified in profile)"}}',
              'description': 'Performs a health check on the specified API '
                             'endpoint using predefined server configurations '
                             'and routing identifiers. Validates whether the '
                             'API is operational and responding to requests.',
              'details': 'Performs a health check on the specified API '
                         'endpoint using predefined server configurations and '
                         'routing identifiers. Validates whether the API is '
                         'operational and responding to requests.',
              'method': 'mcp_call_tool',
              'short_description': 'Verify API availability and responsiveness',
              'source': 'smithery',
              'timestamp': 1742378491651.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.219876394,
 'values': []}, {'id': 'smithery_mcp_tool-marginalia-mcp-server-search-marginalia',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "marginalia-mcp-server"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "search-marginalia"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": {"query": {"type": "string", '
                      '"required": true, "description": "Search terms input"}, '
                      '"index": {"type": "number", "required": true, '
                      '"description": "Position in search results (maps to GUI '
                      'dropdown)"}, "count": {"type": "number", "required": '
                      'true, "description": "Maximum number of results to '
                      'return"}}}], "output": {"description": "Search results '
                      'from Marginalia engine (specific schema not defined)", '
                      '"type": "unknown"}}',
              'description': 'Executes web searches through the Marginalia '
                             'Search engine using a predefined server '
                             'configuration. Requires MCP package server '
                             'reference and handles search parameters '
                             'including query, result index position, and '
                             'results count.',
              'details': 'Executes web searches through the Marginalia Search '
                         'engine using a predefined server configuration. '
                         'Requires MCP package server reference and handles '
                         'search parameters including query, result index '
                         'position, and results count.',
              'method': 'mcp_call_tool',
              'short_description': 'Search the web using Marginalia Search',
              'source': 'smithery',
              'timestamp': 1742381585820.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.20740059,
 'values': []}, {'id': 'smithery_mcp_tool-@cdugo/mcp-get-docs-fetch-package-docs',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package ecosystem", "defaultValue": '
                      '"@cdugo/mcp-get-docs"}, {"name": "toolName", "type": '
                      '"string", "required": true, "description": "Fixed '
                      'identifier for internal tool routing within MCP '
                      'infrastructure", "defaultValue": "fetch-package-docs"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Documentation request parameters '
                      'containing: packageName (string) - Name of target '
                      'package, language (string) - Programming '
                      'language/repository type"}], "output": {"description": '
                      '"Undocumented in profile - Likely contains '
                      'documentation content or operation status", "type": '
                      '"Not specified"}}',
              'description': 'Calls a predefined MCP tool to retrieve '
                             'documentation for specific software packages. '
                             'Uses server configuration and internal routing '
                             'identifiers while requiring package name and '
                             'programming language specifications.',
              'details': 'Calls a predefined MCP tool to retrieve '
                         'documentation for specific software packages. Uses '
                         'server configuration and internal routing '
                         'identifiers while requiring package name and '
                         'programming language specifications.',
              'method': 'mcp_call_tool',
              'short_description': 'Fetch package documentation using MCP '
                                   'internal tool',
              'source': 'smithery',
              'timestamp': 1742376300234.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.204672083,
 'values': []}, {'id': 'web_search_tool-web_search',
 'metadata': {'data': '{"method": "web_search", "inputs": [{"name": "intent", '
                      '"type": "str", "required": true, "description": '
                      '"User\'s search purpose or information need that drives '
                      'the web search"}], "output": {"description": "List of '
                      'relevant URLs matching the intent, or error message if '
                      'no results found", "type": "Union[List[str], str]"}}',
              'description': 'The code analysis reveals the following key '
                             'points:\n'
                             '\n'
                             '1. Identified Function:\n'
                             '   - web_search method in WebSearchTool class '
                             '(decorated via @run_tool class decorator)\n'
                             '\n'
                             '2. Function Signature:\n'
                             '   def web_search(self, intent: str)\n'
                             '\n'
                             '3. Parameters:\n'
                             "   - intent: str (required) - User's search "
                             'intent/purpose\n'
                             '\n'
                             '4. Return Value:\n'
                             '   - Union[List[str], str] - Returns either list '
                             'of URLs or error message string\n'
                             '\n'
                             '5. Function Purpose:\n'
                             '   Performs web searches by:\n'
                             '   1. Generating keywords from user intent\n'
                             '   2. Selecting visual/non-visual search based '
                             'on VISUAL environment variable\n'
                             '   3. Extracting relevant URLs from search '
                             'results\n'
                             '   4. Handling empty result scenarios\n'
                             '\n'
                             '6. Notable Aspects:\n'
                             '   - Environment-dependent behavior (VISUAL '
                             'flag)\n'
                             '   - Fallback from visual to non-visual search\n'
                             '   - String return type for error cases '
                             'contradicts docstring claims\n'
                             '   - Relies on undefined utility functions '
                             '(extract_relevance_url, search_visual, etc.)\n'
                             '\n'
                             '7. Edge Cases:\n'
                             '   - Empty content_list from both search '
                             'methods\n'
                             '   - extract_relevance_url returning empty list\n'
                             '   - Missing VISUAL environment variable\n'
                             '   - Potential API failures in undefined helper '
                             'functions\n'
                             '\n'
                             'Ambiguities:\n'
                             '- Actual return type varies between List[str] '
                             'and str despite docstring claims\n'
                             '- Implementation details of '
                             'search_visual/search_non_visual unknown\n'
                             "- extract_relevance_url's exact behavior "
                             'undefined in provided code',
              'details': 'Performs a web search by generating keywords from '
                         "the user's intent, using either visual or non-visual "
                         'search methods. The tool first attempts visual '
                         'search if the VISUAL environment flag is set, '
                         'falling back to non-visual search if needed. '
                         'Extracts relevant URLs from search results and '
                         'returns them. Returns a message string when no '
                         'results are found.',
              'method': 'web_search',
              'short_description': 'Search the web for information based on '
                                   'user intent',
              'timestamp': 1740564330901.0,
              'tool': 'WebSearchTool',
              'uid': 'levia'},
 'score': 0.200584844,
 'values': []}, {'id': 'smithery_mcp_tool-@guilhermelirio/brazilian-cep-mcp-consultar-cep',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference", '
                      '"defaultValue": "@guilhermelirio/brazilian-cep-mcp"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Internal tool routing '
                      'identifier", "defaultValue": "consultar-cep"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains: cep (8-digit numeric string) '
                      '- Brazilian postal code for address lookup"}], '
                      '"output": {"description": "Address details (likely '
                      'contains street, city, state, etc.)", "type": '
                      '"object/undefined"}}',
              'description': 'Interfaces with MCP package to fetch complete '
                             'address information from a Brazilian CEP code. '
                             'Requires valid 8-digit numeric CEP and '
                             'preconfigured server/tool identifiers.',
              'details': 'Interfaces with MCP package to fetch complete '
                         'address information from a Brazilian CEP code. '
                         'Requires valid 8-digit numeric CEP and preconfigured '
                         'server/tool identifiers.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve Brazilian address details by '
                                   'postal code (CEP)',
              'source': 'smithery',
              'timestamp': 1742381509652.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.199372992,
 'values': []}, {'id': 'smithery_mcp_tool-@TheSethRose/fetch-browser-google_search',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@TheSethRose/fetch-browser"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal tool routing", '
                      '"defaultValue": "google_search"}, {"name": "arguments", '
                      '"type": "object", "required": true, "description": '
                      '"Search parameters object containing:", '
                      '"subParameters": [{"name": "query", "type": "string", '
                      '"description": "The search query to execute"}, {"name": '
                      '"responseType", "type": "string", "description": '
                      '"Expected response format (e.g., JSON, HTML)"}, '
                      '{"name": "maxResults", "type": "number", "description": '
                      '"Maximum number of results to return"}, {"name": '
                      '"topic", "type": "string", "description": '
                      '"Category/type of search (e.g., news, images)"}]}], '
                      '"output": {"description": "Google search results in '
                      'format specified by responseType", "type": "Varies '
                      '(undocumented in profile)"}}',
              'description': 'Performs Google searches using specified '
                             'parameters through the MCP infrastructure. '
                             'Requires server/tool configuration references '
                             'and accepts search criteria including query, '
                             'result limits, and response formatting '
                             'instructions. Returns results in formats '
                             'determined by the responseType parameter.',
              'details': 'Performs Google searches using specified parameters '
                         'through the MCP infrastructure. Requires server/tool '
                         'configuration references and accepts search criteria '
                         'including query, result limits, and response '
                         'formatting instructions. Returns results in formats '
                         'determined by the responseType parameter.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute Google searches and return '
                                   'formatted results via MCP',
              'source': 'smithery',
              'timestamp': 1742376610551.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.199080288,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-package-docs-search_package_docs',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "mcp-package-docs"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "search_package_docs"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Search parameters object '
                      'containing: package (string, required) - Target package '
                      'name; query (string, required) - Search terms; language '
                      '(string, required) - Ecosystem/language filter; fuzzy '
                      '(boolean, required) - Fuzzy match toggle; projectPath '
                      '(string, optional) - Local project directory path"}], '
                      '"output": {"description": "Not explicitly specified in '
                      'provided documentation. Likely returns search results '
                      'data structure.", "type": "Unknown"}}',
              'description': 'Executes searches within package documentation '
                             'using specified parameters. Supports fuzzy '
                             'matching and can leverage local project '
                             'configurations. Requires package name, search '
                             'query, and language ecosystem to operate.',
              'details': 'Executes searches within package documentation using '
                         'specified parameters. Supports fuzzy matching and '
                         'can leverage local project configurations. Requires '
                         'package name, search query, and language ecosystem '
                         'to operate.',
              'method': 'mcp_call_tool',
              'short_description': 'Search for symbols or content within '
                                   'package documentation',
              'source': 'smithery',
              'timestamp': 1742376653521.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.197452456,
 'values': []}, {'id': 'smithery_mcp_tool-@tokenizin/mcp-npx-fetch-fetch_json',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from MCP '
                      'package", "defaultValue": "@tokenizin/mcp-npx-fetch"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'service routing", "defaultValue": "fetch_json"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Request parameters object '
                      "containing 'url' (string, required) - target URL and "
                      "'headers' (object, optional) - custom HTTP "
                      'headers"}], "output": {"description": "Undocumented in '
                      'profile - presumed to be fetched JSON content or error '
                      'object", "type": "object/undefined"}}',
              'description': 'Retrieves JSON content from specified URLs using '
                             'a preconfigured MCP server infrastructure. '
                             'Requires infrastructure identifiers and supports '
                             'custom request headers.',
              'details': 'Retrieves JSON content from specified URLs using a '
                         'preconfigured MCP server infrastructure. Requires '
                         'infrastructure identifiers and supports custom '
                         'request headers.',
              'method': 'mcp_call_tool',
              'short_description': 'Fetch JSON data from remote URLs through '
                                   'MCP service',
              'source': 'smithery',
              'timestamp': 1742381483681.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.193095103,
 'values': []}, {'id': 'smithery_mcp_tool-@aindreyway/mcp-codex-keeper-search_documentation',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@aindreyway/mcp-codex-keeper"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal tool routing", '
                      '"defaultValue": "search_documentation"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Search parameters object containing: '
                      'query (string - search terms), category (string - '
                      'category filter), tag (string - tag filter). Necessity '
                      'of individual parameters not specified."}], "output": '
                      '{"description": "Undocumented in profile - likely '
                      'returns documentation search results", "type": '
                      '"Undocumented"}}',
              'description': 'Enables searching through documentation systems '
                             'to retrieve specific information, best '
                             'practices, or procedural guidelines. Essential '
                             'for verifying correct approaches before making '
                             'critical decisions. Requires explicit server '
                             'configuration and tool routing parameters.',
              'details': 'Enables searching through documentation systems to '
                         'retrieve specific information, best practices, or '
                         'procedural guidelines. Essential for verifying '
                         'correct approaches before making critical decisions. '
                         'Requires explicit server configuration and tool '
                         'routing parameters.',
              'method': 'mcp_call_tool',
              'short_description': 'Search through documentation content for '
                                   'technical information and guidelines',
              'source': 'smithery',
              'timestamp': 1742375916866.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.192969456,
 'values': []}, {'id': 'smithery_mcp_tool-@kazuph/mcp-taskmanager-request_planning',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference '
                      'identifier", "defaultValue": '
                      '"@kazuph/mcp-taskmanager"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal routing to request '
                      'planning subsystem", "defaultValue": '
                      '"request_planning"}, {"name": "arguments", "type": '
                      '"object", "required": true, "description": "Contains: '
                      "originalRequest (string) - user's initial request text; "
                      'tasks (array) - list of required action items; '
                      'splitDetails (string, optional) - task division '
                      'rationale"}], "output": {"description": "Initiates '
                      'workflow and returns initial progress status with task '
                      'table", "type": "object"}}',
              'description': 'Registers a new user request and creates an '
                             'associated task workflow. Requires explicit user '
                             'approvals after each task completion and final '
                             'request completion. Manages workflow progression '
                             'through a structured cycle of task execution, '
                             'approval checks, and status updates.',
              'details': 'Registers a new user request and creates an '
                         'associated task workflow. Requires explicit user '
                         'approvals after each task completion and final '
                         'request completion. Manages workflow progression '
                         'through a structured cycle of task execution, '
                         'approval checks, and status updates.',
              'method': 'mcp_call_tool',
              'short_description': 'Initiate user request workflow with task '
                                   'planning and approval system',
              'source': 'smithery',
              'timestamp': 1742374573360.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.191652894,
 'values': []}, {'id': 'smithery_mcp_tool-@wirdes/db-mcp-tool-!export-data',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@wirdes/db-mcp-tool"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed internal routing '
                      'identifier", "defaultValue": "!export-data"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Operation parameters containing table '
                      'identifier", "defaultValue": "N/A (No default in '
                      'original profile)", "subParameters": [{"name": "table", '
                      '"type": "string", "required": true, "description": '
                      '"Target table for operation (specifics '
                      'undocumented)"}]}], "output": {"description": '
                      '"Undocumented in provided profile - likely varies by '
                      'toolName operation", "type": "Undefined"}}',
              'description': 'Invokes a predefined tool in the MCP package '
                             'using server configuration references. Primarily '
                             'designed for data export operations (based on '
                             'default toolName). Requires server ID, tool '
                             'identifier, and operation-specific arguments '
                             'including target table name.',
              'details': 'Invokes a predefined tool in the MCP package using '
                         'server configuration references. Primarily designed '
                         'for data export operations (based on default '
                         'toolName). Requires server ID, tool identifier, and '
                         'operation-specific arguments including target table '
                         'name.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute MCP package tool operations with '
                                   'server configuration',
              'source': 'smithery',
              'timestamp': 1742376464840.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.191499919,
 'values': []}, {'id': 'smithery_mcp_tool-@wysh3/perplexity-mcp-server-get_documentation',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from MCP '
                      'package", "defaultValue": '
                      '"@wysh3/perplexity-mcp-server"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal request routing", '
                      '"defaultValue": "get_documentation"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains \'query\' (string: technology '
                      "to research) and 'context' (string: optional focus "
                      'areas)"}], "output": {"description": "Not specified in '
                      'the profile", "type": "Unknown"}}',
              'description': 'Get comprehensive documentation and practical '
                             'usage examples for specific technologies, '
                             'libraries, or APIs. The function routes requests '
                             'through predefined server configurations and '
                             'requires parameters specifying the target '
                             'technology and optional contextual focus areas.',
              'details': 'Get comprehensive documentation and practical usage '
                         'examples for specific technologies, libraries, or '
                         'APIs. The function routes requests through '
                         'predefined server configurations and requires '
                         'parameters specifying the target technology and '
                         'optional contextual focus areas.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve documentation and usage examples '
                                   'for technologies and APIs',
              'source': 'smithery',
              'timestamp': 1742383239218.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.191035137,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-package-docs-lookup_npm_doc',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference in MCP '
                      'system for docs retrieval", "defaultValue": '
                      '"mcp-package-docs"}, {"name": "toolName", "type": '
                      '"string", "required": true, "description": "Fixed '
                      'identifier for internal service routing", '
                      '"defaultValue": "lookup_npm_doc"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Documentation query parameters '
                      'container", "defaultValue": null}, {"name": '
                      '"arguments.package", "type": "string", "required": '
                      'true, "description": "Target npm package name (e.g., '
                      '\'react\', \'lodash\')"}, {"name": "arguments.version", '
                      '"type": "string", "required": false, "description": '
                      '"Specific package version (semver format)"}, {"name": '
                      '"arguments.projectPath", "type": "string", "required": '
                      'false, "description": "Local directory path for .npmrc '
                      'configuration resolution"}], "output": {"description": '
                      '"NPM package documentation content (exact format '
                      'undefined in profile)", "type": "Undefined (presumably '
                      'string or structured data)"}}',
              'description': 'Interfaces with MCP infrastructure to fetch '
                             'package documentation from npm registry. Handles '
                             'both remote configuration (via serverId) and '
                             'local environment settings (via projectPath). '
                             'Version specification allows for precise '
                             'documentation lookup.',
              'details': 'Interfaces with MCP infrastructure to fetch package '
                         'documentation from npm registry. Handles both remote '
                         'configuration (via serverId) and local environment '
                         'settings (via projectPath). Version specification '
                         'allows for precise documentation lookup.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve NPM package documentation through '
                                   'enterprise toolchain',
              'source': 'smithery',
              'timestamp': 1742376893129.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.19073236,
 'values': []}, {'id': 'smithery_mcp_tool-@Szowesgad/mcp-server-semgrep-compare_results',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@Szowesgad/mcp-server-semgrep"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal routing", '
                      '"defaultValue": "compare_results"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains parameters: old_results '
                      '(string) - Absolute path to older JSON results file; '
                      'new_results (string) - Absolute path to newer JSON '
                      'results file."}], "output": {"description": "Unknown. '
                      'The JSON profile does not specify output details.", '
                      '"type": "unknown"}}',
              'description': 'Compares two scan results by analyzing older and '
                             'newer JSON result files. Requires server '
                             'configuration, tool identifier, and file paths '
                             'for comparison.',
              'details': 'Compares two scan results by analyzing older and '
                         'newer JSON result files. Requires server '
                         'configuration, tool identifier, and file paths for '
                         'comparison.',
              'method': 'mcp_call_tool',
              'short_description': 'Compares two scan results',
              'source': 'smithery',
              'timestamp': 1742381252377.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.190704629,
 'values': []}, {'id': 'smithery_mcp_tool-@openbnb-org/mcp-server-airbnb-airbnb_listing_details',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@openbnb-org/mcp-server-airbnb"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal API routing", '
                      '"defaultValue": "airbnb_listing_details"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Listing query parameters containing: id '
                      '(listing ID), checkin (YYYY-MM-DD), checkout '
                      '(YYYY-MM-DD), adults/children/infants/pets counts, and '
                      'robots.txt bypass flag"}], "output": {"description": '
                      '"Detailed listing information including direct URLs and '
                      'availability data", "type": "object (structure '
                      'undefined in profile)"}}',
              'description': 'Fetches comprehensive information about a '
                             'specific Airbnb listing including availability, '
                             'pricing, and restrictions. Returns direct URLs '
                             'to the listing and handles guest count '
                             'parameters for accurate pricing calculation. '
                             'Requires server configuration reference for '
                             'execution.',
              'details': 'Fetches comprehensive information about a specific '
                         'Airbnb listing including availability, pricing, and '
                         'restrictions. Returns direct URLs to the listing and '
                         'handles guest count parameters for accurate pricing '
                         'calculation. Requires server configuration reference '
                         'for execution.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve Airbnb listing details with '
                                   'direct links',
              'source': 'smithery',
              'timestamp': 1742376985770.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.188129261,
 'values': []}, {'id': 'smithery_mcp_tool-@MeterLong/mcp-doc-search_and_replace',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@MeterLong/mcp-doc"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed internal routing '
                      'identifier", "defaultValue": "search_and_replace"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Search/replace parameters object '
                      'containing: keyword (search target), replace_with '
                      '(replacement text), preview_only (execution control)", '
                      '"defaultValue": {"preview_only": false}}], "output": '
                      '{"description": "Unspecified in documentation - likely '
                      'includes replacement details and execution status", '
                      '"type": "Not documented"}}',
              'description': 'Performs document text replacement operations. '
                             'Supports preview mode to show replacements '
                             'without execution. Requires server configuration '
                             'reference and uses fixed internal routing '
                             'identifier.',
              'details': 'Performs document text replacement operations. '
                         'Supports preview mode to show replacements without '
                         'execution. Requires server configuration reference '
                         'and uses fixed internal routing identifier.',
              'method': 'mcp_call_tool',
              'short_description': 'Search and replace text in documents with '
                                   'preview capabilities',
              'source': 'smithery',
              'timestamp': 1742376778775.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.187739894,
 'values': []}, {'id': 'smithery_mcp_tool-@hbg/mcp-paperswithcode-search_research_areas',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference", '
                      '"defaultValue": "@hbg/mcp-paperswithcode"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Internal routing identifier for search '
                      'API", "defaultValue": "search_research_areas"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Search parameters object '
                      'containing: query (unknown purpose), name (unknown '
                      'purpose), page (pagination index), items_per_page '
                      '(results per request)"}], "output": {"description": '
                      '"List of matching research areas from PapersWithCode", '
                      '"type": "Unknown (presumably JSON array/object)"}}',
              'description': "Executes a search query against PapersWithCode's "
                             'research areas through MCP integration. Requires '
                             'server configuration and supports pagination '
                             'parameters. Used internally for academic '
                             'research taxonomy discovery.',
              'details': "Executes a search query against PapersWithCode's "
                         'research areas through MCP integration. Requires '
                         'server configuration and supports pagination '
                         'parameters. Used internally for academic research '
                         'taxonomy discovery.',
              'method': 'mcp_call_tool',
              'short_description': 'Search research areas in PapersWithCode '
                                   'database',
              'source': 'smithery',
              'timestamp': 1742377735836.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.187668383,
 'values': []}, {'id': 'smithery_mcp_tool-@maximilien/omi-uber-mcp-get_forecast',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@maximilien/omi-uber-mcp"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'routing", "defaultValue": "get_forecast"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains required parameters: latitude '
                      "(number) - Location's latitude, longitude (number) - "
                      'Location\'s longitude"}], "output": {"description": '
                      '"Weather forecast data details not specified in the '
                      'profile", "type": "Unknown"}}',
              'description': 'Get weather forecast for a location using MCP '
                             'package configuration. Requires latitude and '
                             'longitude coordinates in the arguments object. '
                             'Uses internal routing via predefined toolName.',
              'details': 'Get weather forecast for a location using MCP '
                         'package configuration. Requires latitude and '
                         'longitude coordinates in the arguments object. Uses '
                         'internal routing via predefined toolName.',
              'method': 'mcp_call_tool',
              'short_description': 'Get weather forecast for a location',
              'source': 'smithery',
              'timestamp': 1742382696617.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.18748346,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-search-linkup-search-web',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from MCP '
                      'package", "defaultValue": "mcp-search-linkup"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'service routing", "defaultValue": "search-web"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Search parameters container '
                      'object containing:", "parameters": [{"name": "query", '
                      '"type": "string", "required": true, "description": '
                      '"Natural language question format search query"}]}], '
                      '"output": {"description": "Web search results from '
                      'Linkup (specific format not documented)", "type": '
                      '"object"}}',
              'description': 'Executes web searches through the Linkup service '
                             'using predefined MCP configurations. Requires '
                             'server/tool identifiers and a natural language '
                             'query formatted as a question. Designed for '
                             'information retrieval tasks requiring web data.',
              'details': 'Executes web searches through the Linkup service '
                         'using predefined MCP configurations. Requires '
                         'server/tool identifiers and a natural language query '
                         'formatted as a question. Designed for information '
                         'retrieval tasks requiring web data.',
              'method': 'mcp_call_tool',
              'short_description': 'Perform web search queries using Linkup '
                                   'integration',
              'source': 'smithery',
              'timestamp': 1742380898874.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.187155694,
 'values': []}, {'id': 'smithery_mcp_tool-openrpc-mcp-server-rpc_discover',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from MCP '
                      'package", "defaultValue": "openrpc-mcp-server"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'request routing", "defaultValue": "rpc_discover"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Contains server URL parameter: '
                      'server (string, required) - Target server endpoint"}], '
                      '"output": {"description": "OpenRPC discovery document '
                      'detailing available methods, schemas, and server '
                      'capabilities", "type": "object"}}',
              'description': 'Executes JSON-RPC discovery call (rpc.discover) '
                             'to retrieve all available methods from a server '
                             'compliant with OpenRPC Specification. Users can '
                             'query supported methods by providing a server '
                             'URL through the nested arguments parameter.',
              'details': 'Executes JSON-RPC discovery call (rpc.discover) to '
                         'retrieve all available methods from a server '
                         'compliant with OpenRPC Specification. Users can '
                         'query supported methods by providing a server URL '
                         'through the nested arguments parameter.',
              'method': 'mcp_call_tool',
              'short_description': 'Discover available JSON-RPC methods on a '
                                   'server using OpenRPC specification',
              'source': 'smithery',
              'timestamp': 1742380806750.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.186796144,
 'values': []}, {'id': 'smithery_mcp_tool-@himanshusanecha/mcp-osint-server-host_lookup',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@himanshusanecha/mcp-osint-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal tool '
                      'routing", "defaultValue": "host_lookup"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Parameters for target analysis '
                      'containing: [target (string, required) - Undocumented '
                      'analysis target]"}], "output": {"description": '
                      '"Ambiguous - Likely returns host lookup results based '
                      'on target parameter", "type": "Undocumented in '
                      'profile"}}',
              'description': "Calls the 'host_lookup' tool through specified "
                             'MCP server infrastructure to perform target '
                             'analysis. Requires server configuration '
                             'reference, tool identifier, and target parameter '
                             'in arguments object.',
              'details': "Calls the 'host_lookup' tool through specified MCP "
                         'server infrastructure to perform target analysis. '
                         'Requires server configuration reference, tool '
                         'identifier, and target parameter in arguments '
                         'object.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute host lookup operations via MCP '
                                   'server configuration',
              'source': 'smithery',
              'timestamp': 1742380446903.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.186346307,
 'values': []}, {'id': 'smithery_mcp_tool-@openbnb-org/mcp-server-airbnb-airbnb_search',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@openbnb-org/mcp-server-airbnb"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal request routing", '
                      '"defaultValue": "airbnb_search"}, {"name": "arguments", '
                      '"type": "object", "required": true, "description": '
                      '"Search parameters: location (string) - City/state; '
                      'placeId (string) - Google Maps ID; checkin (string) - '
                      'YYYY-MM-DD; checkout (string) - YYYY-MM-DD; adults '
                      '(number); children (number); infants (number); pets '
                      '(number); minPrice (number); maxPrice (number); cursor '
                      '(string) - Pagination token; ignoreRobotsText (boolean) '
                      '- Bypass scraping rules. All parameters optional unless '
                      'otherwise required by Airbnb\'s API."}], "output": '
                      '{"description": "Airbnb listing results with direct '
                      'URLs", "type": "object/array (undocumented)"}}',
              'description': 'Performs Airbnb searches using location, date '
                             'ranges, guest counts, price ranges, and '
                             'pagination. Returns direct listing links. '
                             'Supports Place ID lookups and robots.txt bypass.',
              'details': 'Performs Airbnb searches using location, date '
                         'ranges, guest counts, price ranges, and pagination. '
                         'Returns direct listing links. Supports Place ID '
                         'lookups and robots.txt bypass.',
              'method': 'mcp_call_tool',
              'short_description': 'Search Airbnb listings with filters and '
                                   'pagination',
              'source': 'smithery',
              'timestamp': 1742376929893.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.184390441,
 'values': []}, {'id': 'smithery_mcp_tool-@hbg/mcp-paperswithcode-list_research_area_tasks',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@hbg/mcp-paperswithcode"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "list_research_area_tasks"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Contains: area_id (string, '
                      'required - target research area identifier), page '
                      '(pagination page number), items_per_page (number of '
                      'items per page). Sub-parameter types/requirements '
                      'beyond area_id are unspecified."}], "output": '
                      '{"description": "Unknown - Output format not documented '
                      'in the profile", "type": "Unknown"}}',
              'description': 'Retrieves a list of machine learning tasks '
                             'associated with a specified research area ID '
                             'from PapersWithCode. Uses predefined server '
                             'configurations and internal tool routing '
                             'parameters. Supports pagination via '
                             'page/items_per_page arguments.',
              'details': 'Retrieves a list of machine learning tasks '
                         'associated with a specified research area ID from '
                         'PapersWithCode. Uses predefined server '
                         'configurations and internal tool routing parameters. '
                         'Supports pagination via page/items_per_page '
                         'arguments.',
              'method': 'mcp_call_tool',
              'short_description': 'List research area tasks from '
                                   'PapersWithCode',
              'source': 'smithery',
              'timestamp': 1742377927002.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.183477327,
 'values': []}, {'id': 'smithery_mcp_tool-@chuanmingliu/mcp-webresearch-search_google',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference ID", '
                      '"defaultValue": "@chuanmingliu/mcp-webresearch"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'tool routing", "defaultValue": "search_google"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Search parameters container. '
                      'Contains: query (string, required) - Search terms to '
                      'look up on Google."}], "output": {"description": '
                      '"Search results from Google (exact format not specified '
                      'in profile)", "type": "object"}}',
              'description': "Performs a Google search query using MCP's "
                             'configured web research tools. Requires server '
                             'configuration reference and specific tool '
                             'routing identifier. Accepts search parameters '
                             'through nested arguments object.',
              'details': "Performs a Google search query using MCP's "
                         'configured web research tools. Requires server '
                         'configuration reference and specific tool routing '
                         'identifier. Accepts search parameters through nested '
                         'arguments object.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute Google search via MCP tool system',
              'source': 'smithery',
              'timestamp': 1742374785047.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.182288185,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-hn-search_stories',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'infrastructure", "defaultValue": "mcp-hn"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "search_stories"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Search parameters: query (required '
                      'string) - Search terms; search_by_date (optional '
                      'boolean, default=False) - Date-based search toggle; '
                      'num_results (optional integer, default=10) - Result '
                      'count limit"}], "output": {"description": "Hacker News '
                      'story results matching query parameters. Exact format '
                      'unspecified in documentation.", "type": "array"}}',
              'description': 'Executes search queries against Hacker News '
                             'stories. Optimize queries to 5 words or fewer '
                             'for best results. When search_by_date is False '
                             '(default), results are ranked by relevance, '
                             'points, and comments. Returns 10 results by '
                             'default.',
              'details': 'Executes search queries against Hacker News stories. '
                         'Optimize queries to 5 words or fewer for best '
                         'results. When search_by_date is False (default), '
                         'results are ranked by relevance, points, and '
                         'comments. Returns 10 results by default.',
              'method': 'mcp_call_tool',
              'short_description': 'Search Hacker News stories with '
                                   'configurable parameters',
              'source': 'smithery',
              'timestamp': 1742379618424.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.182180583,
 'values': []}, {'id': 'smithery_mcp_tool-@boorich/mcp-human-loop-evaluate_need_for_human',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@boorich/mcp-human-loop"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'request routing", "defaultValue": '
                      '"evaluate_need_for_human"}, {"name": "arguments", '
                      '"type": "object", "required": true, "description": '
                      '"Contains task details and model capabilities: '
                      "{'taskDescription': 'Description of task being "
                      "evaluated', 'modelCapabilities': 'List of available AI "
                      'capabilities\'}"}], "output": {"description": "Not '
                      'explicitly specified in profile. Likely returns human '
                      'intervention requirement determination", "type": '
                      '"Unknown (Not defined in provided profile)"}}',
              'description': 'Determines whether a given task requires human '
                             'oversight based on task description and AI model '
                             'capabilities. Uses predefined server '
                             'configuration and routing identifiers for MCP '
                             'package integration.',
              'details': 'Determines whether a given task requires human '
                         'oversight based on task description and AI model '
                         'capabilities. Uses predefined server configuration '
                         'and routing identifiers for MCP package integration.',
              'method': 'mcp_call_tool',
              'short_description': 'Evaluate task requirements for human '
                                   'intervention',
              'source': 'smithery',
              'timestamp': 1742381022306.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.182081088,
 'values': []}, {'id': 'smithery_mcp_tool-@himanshusanecha/mcp-osint-server-dig_lookup',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference for '
                      'execution environment", "defaultValue": '
                      '"@himanshusanecha/mcp-osint-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal tool '
                      'routing mechanism", "defaultValue": "dig_lookup"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "DNS lookup parameters containing '
                      'target specification", "nested_params": [{"name": '
                      '"target", "type": "string", "required": true, '
                      '"description": "Domain or IP address to investigate via '
                      'dig tool"}]}], "output": {"description": "Undocumented '
                      'in profile - Likely returns DNS records or dig tool '
                      'output", "type": "Undocumented (Assumed string or '
                      'JSON)"}}',
              'description': 'Routes a dig lookup request to a specified MCP '
                             'server configuration using predefined tool '
                             'identifiers. Requires server reference, tool '
                             'identifier, and target parameters for DNS query '
                             'execution.',
              'details': 'Routes a dig lookup request to a specified MCP '
                         'server configuration using predefined tool '
                         'identifiers. Requires server reference, tool '
                         'identifier, and target parameters for DNS query '
                         'execution.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute DNS lookup tool via MCP '
                                   'infrastructure',
              'source': 'smithery',
              'timestamp': 1742380397013.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180966601,
 'values': []}, {'id': 'smithery_mcp_tool-@wirdes/db-mcp-tool-!pg',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@wirdes/db-mcp-tool"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'tool routing", "defaultValue": "!pg"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "JSON object containing tool parameters '
                      'including connection configuration (exact structure '
                      'undefined)"}], "output": {"description": "Not specified '
                      'in the JSON profile", "type": "unknown"}}',
              'description': 'Routes requests to internal tools using server '
                             'configurations from the MCP package. Requires '
                             'server reference, tool identifier, and '
                             'connection arguments. Default values provided '
                             'for server and tool identifiers.',
              'details': 'Routes requests to internal tools using server '
                         'configurations from the MCP package. Requires server '
                         'reference, tool identifier, and connection '
                         'arguments. Default values provided for server and '
                         'tool identifiers.',
              'method': 'mcp_call_tool',
              'short_description': 'Invoke MCP package tool execution with '
                                   'server configuration',
              'source': 'smithery',
              'timestamp': 1742375814482.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180851623,
 'values': []}, {'id': 'smithery_mcp_tool-@bsmi021/mcp-file-context-server-read_context',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@bsmi021/mcp-file-context-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "read_context"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Configuration object for file '
                      'processing:", "subParameters": [{"name": "path", '
                      '"type": "string", "required": true, "description": '
                      '"File system path to target file/directory"}, {"name": '
                      '"maxSize", "type": "number", "required": false, '
                      '"description": "Maximum file size in bytes before '
                      'chunking (optional)"}, {"name": "encoding", "type": '
                      '"string", "required": false, "description": "Text '
                      'encoding format (e.g., utf8, ascii)"}, {"name": '
                      '"recursive", "type": "boolean", "required": false, '
                      '"description": "Enable directory recursion (default: '
                      'false)"}, {"name": "fileTypes", "type": ["array", '
                      '"string"], "required": false, "description": "Allowed '
                      "file extensions without dots (e.g., ['js', "
                      '\'py\'])"}, {"name": "chunkNumber", "type": "number", '
                      '"required": false, "description": "0-based chunk index '
                      'for large files"}]}], "output": {"description": '
                      '"Processed file contents with metadata, potentially '
                      'chunked", "type": "object/string (undocumented in '
                      'profile)"}}',
              'description': 'Reads and processes code files/directories while '
                             'automatically ignoring common development '
                             'artifacts (.git, node_modules, etc.). Supports '
                             'file type filtering, recursive directory '
                             'scanning, and chunked handling of large files '
                             'through get_chunk_count integration. Optimized '
                             'for code analysis workflows.',
              'details': 'Reads and processes code files/directories while '
                         'automatically ignoring common development artifacts '
                         '(.git, node_modules, etc.). Supports file type '
                         'filtering, recursive directory scanning, and chunked '
                         'handling of large files through get_chunk_count '
                         'integration. Optimized for code analysis workflows.',
              'method': 'mcp_call_tool',
              'short_description': 'Analyze code files with smart filtering '
                                   'and chunked processing',
              'source': 'smithery',
              'timestamp': 1742379376006.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180772647,
 'values': []}, {'id': 'smithery_mcp_tool-@MeterLong/mcp-doc-find_and_replace',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@MeterLong/mcp-doc"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'tool routing", "defaultValue": "find_and_replace"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Payload containing: find_text '
                      '(string, required) - Target search string; replace_text '
                      '(string, required) - Replacement content"}], "output": '
                      '{"description": "Not specified in the profile", "type": '
                      '"Not specified"}}',
              'description': 'Executes a find-and-replace operation using the '
                             "MCP package's document processing tools. "
                             'Requires server configuration reference and '
                             'specific parameter structure in arguments '
                             'payload.',
              'details': 'Executes a find-and-replace operation using the MCP '
                         "package's document processing tools. Requires server "
                         'configuration reference and specific parameter '
                         'structure in arguments payload.',
              'method': 'mcp_call_tool',
              'short_description': 'Find and replace text in documents through '
                                   'MCP integration',
              'source': 'smithery',
              'timestamp': 1742376935850.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180613652,
 'values': []}, {'id': 'smithery_mcp_tool-@oneshot-engineering/mcp-webresearch-search_google',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from MCP '
                      'package", "defaultValue": '
                      '"@oneshot-engineering/mcp-webresearch"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal service '
                      'routing", "defaultValue": "search_google"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Search parameters container: contains '
                      "'query' (string) - Search term(s) to look up. Necessity "
                      'of nested parameters not explicitly defined."}], '
                      '"output": {"description": "Search results data '
                      'structure not specified in profile", "type": "Undefined '
                      '(presumably search results array/object)"}}',
              'description': 'Initiates Google searches using predefined MCP '
                             'server configurations. Requires a search query '
                             'parameter and uses internal routing identifiers '
                             'to connect with the web research subsystem.',
              'details': 'Initiates Google searches using predefined MCP '
                         'server configurations. Requires a search query '
                         'parameter and uses internal routing identifiers to '
                         'connect with the web research subsystem.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute Google search queries through MCP '
                                   'infrastructure',
              'source': 'smithery',
              'timestamp': 1742376170243.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180198282,
 'values': []}, {'id': 'smithery_mcp_tool-@blake365/macrostrat-mcp-find-units',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@blake365/macrostrat-mcp"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'routing to the \'find-units\' tool", "defaultValue": '
                      '"find-units"}, {"name": "arguments", "type": "object", '
                      '"required": true, "description": "JSON object '
                      'containing query parameters: lat (number - valid '
                      'latitude), lng (number - valid longitude), responseType '
                      "(string - 'long' or 'short' for response detail). "
                      'Necessity of lat/lng/responseType parameters is '
                      'unspecified."}], "output": {"description": "Geological '
                      'unit data from Macrostrat based on the provided '
                      'coordinates", "type": "unknown"}}',
              'description': 'This function queries the Macrostrat database '
                             'for geological units using latitude and '
                             'longitude coordinates. It requires server and '
                             'tool configurations, accepts geographic '
                             'coordinates, and allows specifying the response '
                             'detail level (long or short).',
              'details': 'This function queries the Macrostrat database for '
                         'geological units using latitude and longitude '
                         'coordinates. It requires server and tool '
                         'configurations, accepts geographic coordinates, and '
                         'allows specifying the response detail level (long or '
                         'short).',
              'method': 'mcp_call_tool',
              'short_description': 'Query Macrostrat geologic units by '
                                   'location',
              'source': 'smithery',
              'timestamp': 1742381782513.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180192739,
 'values': []}, {'id': 'smithery_mcp_tool-@himanshusanecha/mcp-osint-server-osint_overview',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@himanshusanecha/mcp-osint-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal routing", '
                      '"defaultValue": "osint_overview"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains nested parameters: target '
                      '(string) - No description available. Necessity of '
                      'nested parameters is unspecified."}], "output": '
                      '{"description": "Undocumented in provided profile - '
                      'likely varies by tool implementation", "type": '
                      '"Undefined"}}',
              'description': "Routes requests to the 'osint_overview' tool "
                             'using predefined MCP server configurations. '
                             'Requires a target parameter for OSINT operations '
                             'but provides no documentation about the '
                             "operation's output or target requirements.",
              'details': "Routes requests to the 'osint_overview' tool using "
                         'predefined MCP server configurations. Requires a '
                         'target parameter for OSINT operations but provides '
                         "no documentation about the operation's output or "
                         'target requirements.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute MCP OSINT tool with server '
                                   'configuration',
              'source': 'smithery',
              'timestamp': 1742380557954.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180170611,
 'values': []}, {'id': 'smithery_mcp_tool-openrpc-mcp-server-rpc_call',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from the '
                      'MCP package", "defaultValue": "openrpc-mcp-server"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'request routing", "defaultValue": "rpc_call"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "JSON object containing server URL '
                      '(string), JSON-RPC method name (string), and '
                      'stringified parameters (string). All sub-parameters are '
                      'required."}], "output": {"description": "Result of the '
                      'JSON-RPC method call. Structure depends on the method '
                      'and server response.", "type": "object"}}',
              'description': 'Executes a JSON-RPC method call on a specified '
                             'server URL. Users provide the server URL, method '
                             'name, and parameters as a stringified JSON '
                             'object. The serverId and toolName parameters '
                             'reference internal configurations for routing '
                             'and authentication.',
              'details': 'Executes a JSON-RPC method call on a specified '
                         'server URL. Users provide the server URL, method '
                         'name, and parameters as a stringified JSON object. '
                         'The serverId and toolName parameters reference '
                         'internal configurations for routing and '
                         'authentication.',
              'method': 'mcp_call_tool',
              'short_description': 'Call any JSON-RPC method on a server with '
                                   'parameters',
              'source': 'smithery',
              'timestamp': 1742380700142.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.180119,
 'values': []}, {'id': 'smithery_mcp_tool-@comet-ml/opik-mcp-server-create-project',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@comet-ml/opik-mcp-server"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "create-project"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Project parameters: name (string) - '
                      'Project identifier; description (string) - Project '
                      'details; workspaceName (string, optional) - Custom '
                      'workspace name override"}], "output": {"description": '
                      '"Not specified in provided profile", "type": '
                      '"undefined"}}',
              'description': 'Initializes a new project/workspace using MCP '
                             'infrastructure. Requires server configuration '
                             'reference, tool identifier, and project '
                             'parameters. Uses predefined defaults for server '
                             'connection and tool routing.',
              'details': 'Initializes a new project/workspace using MCP '
                         'infrastructure. Requires server configuration '
                         'reference, tool identifier, and project parameters. '
                         'Uses predefined defaults for server connection and '
                         'tool routing.',
              'method': 'mcp_call_tool',
              'short_description': 'Create new project/workspace via MCP '
                                   'service',
              'source': 'smithery',
              'timestamp': 1742383879000.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.178170383,
 'values': []}, {'id': 'smithery_mcp_tool-@aldrin-labs/solana-docs-mcp-server-search_docs',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@aldrin-labs/solana-docs-mcp-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal request '
                      'routing", "defaultValue": "search_docs"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains search parameters: {\'query\' '
                      '(string, required): Search phrase for documentation '
                      'lookup}"}], "output": {"description": "Not explicitly '
                      'defined in provided profile", "type": "Undocumented"}}',
              'description': 'Executes a documentation search operation using '
                             'MCP infrastructure by routing requests to a '
                             'specified server configuration. Requires a '
                             'search query parameter within the arguments '
                             'object.',
              'details': 'Executes a documentation search operation using MCP '
                         'infrastructure by routing requests to a specified '
                         'server configuration. Requires a search query '
                         'parameter within the arguments object.',
              'method': 'mcp_call_tool',
              'short_description': 'Search through Solana documentation',
              'source': 'smithery',
              'timestamp': 1742380541633.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.175477728,
 'values': []}, {'id': 'smithery_mcp_tool-@DynamicEndpoints/Netlify-MCP-Server-deploy-function',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference", '
                      '"defaultValue": '
                      '"@DynamicEndpoints/Netlify-MCP-Server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed internal routing identifier", '
                      '"defaultValue": "deploy-function"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Function parameters object containing: '
                      'path (string) - Function file location, name (string) - '
                      'Deployment name, runtime (string) - Execution '
                      'environment. Inner parameter requirements '
                      'unspecified."}], "output": {"description": "Output '
                      'details not documented in profile", "type": '
                      '"Unspecified"}}',
              'description': 'Coordinates deployment of serverless functions '
                             'using MCP infrastructure. Requires server '
                             'configuration reference, tool identifier for '
                             'internal routing, and function parameters '
                             'including file path, name, and runtime. Default '
                             'values exist for server/tool references but '
                             'remain required inputs.',
              'details': 'Coordinates deployment of serverless functions using '
                         'MCP infrastructure. Requires server configuration '
                         'reference, tool identifier for internal routing, and '
                         'function parameters including file path, name, and '
                         'runtime. Default values exist for server/tool '
                         'references but remain required inputs.',
              'method': 'mcp_call_tool',
              'short_description': 'Deploy serverless functions via MCP tool '
                                   'routing',
              'source': 'smithery',
              'timestamp': 1742384987809.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.174698,
 'values': []}, {'id': 'website_scan_tool-website_scan',
 'metadata': {'data': '{"method": "website_scan", "inputs": [{"name": '
                      '"url_list", "type": "list", "required": true, '
                      '"description": "List of initial URLs to start website '
                      'scanning from"}, {"name": "intent", "type": "str", '
                      '"required": true, "description": "Guiding purpose for '
                      'content filtering and summarization"}], "output": '
                      '{"description": "Processed website content summary or '
                      'timeout error message", "type": "str"}}',
              'description': 'Identified Function:\n'
                             '1. website_scan (method of WebsiteScanTool '
                             'class)\n'
                             '\n'
                             'Function Signature:\n'
                             'def website_scan(self, url_list: list, intent: '
                             'str)\n'
                             '\n'
                             'Parameters:\n'
                             '- url_list: list (required) - List of URLs to '
                             'scan\n'
                             '- intent: str (required) - The intent to guide '
                             'scanning\n'
                             '\n'
                             'Return Value:\n'
                             '- Returns summary (output from '
                             'get_summary_links) or error message\n'
                             '- Return type appears to be string based on '
                             'error handling, but actual type depends on '
                             'get_summary_links implementation\n'
                             '\n'
                             'Purpose:\n'
                             'Scans websites by extracting links, removing '
                             'duplicates, fetching content, and generating '
                             'intent-based summaries\n'
                             '\n'
                             'Notable Aspects:\n'
                             '1. Relies on multiple helper functions not shown '
                             'in code\n'
                             '2. Specific exception handling for connection '
                             'timeouts\n'
                             '3. Processes links recursively through '
                             'get_all_links\n'
                             '4. Returns raw error message strings in some '
                             'cases\n'
                             '\n'
                             'Potential Issues:\n'
                             '1. Depends on external website accessibility\n'
                             '2. No visible timeout configuration\n'
                             '3. String-based error matching ("website '
                             'connection timeout") is fragile\n'
                             '4. No validation for URL format in url_list\n'
                             '5. Recursive link crawling might cause infinite '
                             'loops with circular references',
              'details': 'Scans provided URLs by recursively extracting all '
                         'links, removing duplicates, fetching content, and '
                         'generating a summary filtered by specified intent. '
                         'Handles website connection timeouts explicitly while '
                         'propagating other errors.',
              'method': 'website_scan',
              'short_description': 'Scan websites and extract intent-based '
                                   'information',
              'timestamp': 1740564260509.0,
              'tool': 'WebsiteScanTool',
              'uid': 'levia'},
 'score': 0.174422309,
 'values': []}, {'id': 'smithery_mcp_tool-zig-mcp-server-get_recommendations',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "zig-mcp-server"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal request '
                      'routing", "defaultValue": "get_recommendations"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Contains: code (string) - Zig '
                      'code to analyze; prompt (string) - Natural language '
                      'query for recommendations. Sub-parameter requirements '
                      'not explicitly specified."}], "output": {"description": '
                      '"Not specified in provided documentation", "type": '
                      '"Undocumented"}}',
              'description': 'Accepts Zig code and a natural language prompt '
                             'to generate code improvement suggestions and '
                             'best practice recommendations. Uses predefined '
                             'server configuration and routing identifiers for '
                             'processing requests.',
              'details': 'Accepts Zig code and a natural language prompt to '
                         'generate code improvement suggestions and best '
                         'practice recommendations. Uses predefined server '
                         'configuration and routing identifiers for processing '
                         'requests.',
              'method': 'mcp_call_tool',
              'short_description': 'Analyze Zig code and provide optimization '
                                   'recommendations',
              'source': 'smithery',
              'timestamp': 1742380249141.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.173747793,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-package-docs-lookup_go_doc',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "mcp-package-docs"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Internal routing identifier for '
                      'documentation service", "defaultValue": '
                      '"lookup_go_doc"}, {"name": "arguments", "type": '
                      '"object", "required": true, "description": '
                      '"Documentation lookup parameters: package (required '
                      'import path), symbol (optional specific identifier), '
                      'projectPath (optional local directory for config '
                      'files)"}], "output": {"description": "Go package '
                      'documentation content (format unspecified)", "type": '
                      '"Not specified in profile"}}',
              'description': 'Looks up documentation for Go packages and '
                             'symbols using MCP infrastructure. Supports both '
                             'standard packages and local projects through '
                             'specified configuration parameters. Requires '
                             'server configuration reference and handles '
                             'internal routing through fixed tool identifier.',
              'details': 'Looks up documentation for Go packages and symbols '
                         'using MCP infrastructure. Supports both standard '
                         'packages and local projects through specified '
                         'configuration parameters. Requires server '
                         'configuration reference and handles internal routing '
                         'through fixed tool identifier.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve Go package documentation through '
                                   'MCP system',
              'source': 'smithery',
              'timestamp': 1742376709487.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.17328386,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-package-docs-lookup_python_doc',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "mcp-package-docs"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Fixed identifier for internal request '
                      'routing", "defaultValue": "lookup_python_doc"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Contains: package (string, '
                      'required) - Package name; symbol (string, optional) - '
                      'Specific symbol documentation; projectPath (string, '
                      'optional) - Local project directory path"}], "output": '
                      '{"description": "Documentation content not described in '
                      'profile", "type": "Undefined in specification"}}',
              'description': 'Look up Python package documentation through MCP '
                             'integration. Supports optional symbol lookup and '
                             'local configuration paths.',
              'details': 'Look up Python package documentation through MCP '
                         'integration. Supports optional symbol lookup and '
                         'local configuration paths.',
              'method': 'mcp_call_tool',
              'short_description': 'Look up Python package documentation',
              'source': 'smithery',
              'timestamp': 1742376826897.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.172924235,
 'values': []}, {'id': 'smithery_mcp_tool-@meowhuman/weather-get_forecast',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@meowhuman/weather"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "get_forecast"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Geographic coordinates: latitude '
                      '(number, required - No description available), '
                      'longitude (number, required - No description '
                      'available)"}], "output": {"description": "Weather '
                      'forecast data (specific format not documented)", '
                      '"type": "Undefined (output schema not specified in '
                      'profile)"}}',
              'description': 'Fetches weather forecast data for a specified '
                             'location using latitude and longitude '
                             'coordinates. Requires preconfigured server '
                             'reference and internal routing identifier.',
              'details': 'Fetches weather forecast data for a specified '
                         'location using latitude and longitude coordinates. '
                         'Requires preconfigured server reference and internal '
                         'routing identifier.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve weather forecast using geographic '
                                   'coordinates',
              'source': 'smithery',
              'timestamp': 1742381422696.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.172579944,
 'values': []}, {'id': 'smithery_mcp_tool-@comet-ml/opik-mcp-server-list-projects',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@comet-ml/opik-mcp-server"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'routing", "defaultValue": "list-projects"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Configuration object for pagination, '
                      'sorting, and workspace filtering. Contains optional '
                      'keys: page (number - page number), size (number - items '
                      'per page), sortBy (string - field to sort by), '
                      "sortOrder (string - 'asc' or 'desc'), workspaceName "
                      '(string - non-default workspace)."}], "output": '
                      '{"description": "List of projects/workspaces (exact '
                      'structure not specified in the profile)", "type": '
                      '"unknown"}}',
              'description': 'Retrieves a paginated and sortable list of '
                             'projects or workspaces from an MCP server. '
                             'Requires server configuration and tool '
                             'identifiers. Supports filtering by workspace and '
                             "pagination controls via the 'arguments' "
                             'parameter.',
              'details': 'Retrieves a paginated and sortable list of projects '
                         'or workspaces from an MCP server. Requires server '
                         'configuration and tool identifiers. Supports '
                         'filtering by workspace and pagination controls via '
                         "the 'arguments' parameter.",
              'method': 'mcp_call_tool',
              'short_description': 'Get a list of projects/workspaces with '
                                   'pagination and sorting',
              'source': 'smithery',
              'timestamp': 1742383623693.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.171626687,
 'values': []}, {'id': 'smithery_mcp_tool-@zick987/mcpxiaohua-get_forecast',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@zick987/mcpxiaohua"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "get_forecast"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Geographic coordinates object '
                      "containing: latitude (number) - Location's latitude, "
                      'longitude (number) - Location\'s longitude"}], '
                      '"output": {"description": "Weather forecast data for '
                      'specified location", "type": "undefined (not specified '
                      'in profile)"}}',
              'description': 'Fetches weather forecast data for a specified '
                             'location through MCP infrastructure. Requires '
                             'server configuration reference and internal tool '
                             'identifier, with geographic coordinates provided '
                             'as nested parameters in the arguments object.',
              'details': 'Fetches weather forecast data for a specified '
                         'location through MCP infrastructure. Requires server '
                         'configuration reference and internal tool '
                         'identifier, with geographic coordinates provided as '
                         'nested parameters in the arguments object.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve weather forecast using geographic '
                                   'coordinates',
              'source': 'smithery',
              'timestamp': 1742381415899.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.171253458,
 'values': []}, {'id': 'smithery_mcp_tool-@wysh3/perplexity-mcp-zerver-search',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Preconfigured server reference from MCP '
                      'package", "defaultValue": '
                      '"@wysh3/perplexity-mcp-zerver"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal API routing", '
                      '"defaultValue": "search"}, {"name": "arguments", '
                      '"type": "object", "required": true, "description": '
                      '"Search parameters container with nested fields:", '
                      '"parameters": [{"name": "query", "type": "string", '
                      '"required": true, "description": "Search terms/phrases '
                      'to query"}, {"name": "detail_level", "type": "string", '
                      '"required": false, "description": "Result verbosity '
                      'level (brief/normal/detailed)"}]}], "output": '
                      '{"description": "Search results from Perplexity.ai", '
                      '"type": "Not specified in profile (likely '
                      'JSON/string)"}}',
              'description': 'Performs search operations on Perplexity.ai '
                             'using predefined server configurations. Allows '
                             'specifying query complexity through '
                             "'detail_level' parameter (brief, normal, "
                             'detailed). Requires API endpoint configuration '
                             'through serverId.',
              'details': 'Performs search operations on Perplexity.ai using '
                         'predefined server configurations. Allows specifying '
                         "query complexity through 'detail_level' parameter "
                         '(brief, normal, detailed). Requires API endpoint '
                         'configuration through serverId.',
              'method': 'mcp_call_tool',
              'short_description': 'Execute Perplexity.ai search queries with '
                                   'configurable detail levels',
              'source': 'smithery',
              'timestamp': 1742377763633.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.170651838,
 'values': []}, {'id': 'smithery_mcp_tool-@HenkDz/postgresql-mcp-server-analyze_database',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@HenkDz/postgresql-mcp-server"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal tool routing", '
                      '"defaultValue": "analyze_database"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Analysis parameters object '
                      'containing:", "subParameters": [{"name": '
                      '"connectionString", "type": "string", "required": true, '
                      '"description": "PostgreSQL connection credentials"}, '
                      '{"name": "analysisType", "type": "string", "required": '
                      'true, "description": "Category of analysis to '
                      'execute"}]}], "output": {"description": "Analysis '
                      'results (format unspecified)", "type": "unknown"}}',
              'description': 'Coordinates analysis of PostgreSQL database '
                             'settings and performance metrics using specified '
                             'connection parameters and analysis type',
              'details': 'Coordinates analysis of PostgreSQL database settings '
                         'and performance metrics using specified connection '
                         'parameters and analysis type',
              'method': 'mcp_call_tool',
              'short_description': 'Analyze PostgreSQL database configuration '
                                   'and performance',
              'source': 'smithery',
              'timestamp': 1742376434217.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.170234889,
 'values': []}, {'id': 'smithery_mcp_tool-mcp-package-version-check_npm_versions',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "mcp-package-version"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal '
                      'routing to the version-checking tool", "defaultValue": '
                      '"check_npm_versions"}, {"name": "arguments", "type": '
                      '"object", "required": true, "description": "JSON object '
                      "containing 'dependencies' (required, from package.json) "
                      "and 'constraints' (optional, version restrictions for "
                      'specific packages)"}], "output": {"description": "Not '
                      'specified in the profile", "type": "unknown"}}',
              'description': 'This function checks the latest stable versions '
                             'of npm packages listed in the dependencies of a '
                             'package.json file. It accepts optional '
                             'constraints to filter specific package versions. '
                             'Requires server configuration and tool '
                             'identifiers for execution.',
              'details': 'This function checks the latest stable versions of '
                         'npm packages listed in the dependencies of a '
                         'package.json file. It accepts optional constraints '
                         'to filter specific package versions. Requires server '
                         'configuration and tool identifiers for execution.',
              'method': 'mcp_call_tool',
              'short_description': 'Check latest stable versions for npm '
                                   'packages',
              'source': 'smithery',
              'timestamp': 1742377619543.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.169742793,
 'values': []}, {'id': 'smithery_mcp_tool-@JiantaoFu/appinsightmcp-app-store-similar',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "MCP server configuration reference", '
                      '"defaultValue": "@JiantaoFu/appinsightmcp"}, {"name": '
                      '"toolName", "type": "string", "required": true, '
                      '"description": "Internal routing identifier for similar '
                      'apps service", "defaultValue": "app-store-similar"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Contains required numeric App ID '
                      'parameter: {\'id\': number} (e.g., 444934666)", '
                      '"defaultValue": null}], "output": {"description": "List '
                      'of similar applications from App Store (exact format '
                      'not specified in profile)", "type": "unknown"}}',
              'description': 'Accesses Apple App Store data through MCP '
                             'infrastructure to find applications similar to '
                             'the specified app ID. Requires server '
                             'configuration reference and uses internal '
                             "routing identifier 'app-store-similar'. "
                             'Mandatory numeric app ID must be provided in '
                             'arguments.',
              'details': 'Accesses Apple App Store data through MCP '
                         'infrastructure to find applications similar to the '
                         'specified app ID. Requires server configuration '
                         'reference and uses internal routing identifier '
                         "'app-store-similar'. Mandatory numeric app ID must "
                         'be provided in arguments.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve similar App Store applications '
                                   'using numeric app ID',
              'source': 'smithery',
              'timestamp': 1742379283061.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.16925849,
 'values': []}, {'id': 'smithery_mcp_tool-@kazuph/mcp-taskmanager-open_task_details',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": "@kazuph/mcp-taskmanager"}, '
                      '{"name": "toolName", "type": "string", "required": '
                      'true, "description": "Fixed identifier for internal API '
                      'routing", "defaultValue": "open_task_details"}, '
                      '{"name": "arguments", "type": "object", "required": '
                      'true, "description": "Contains taskId (string, '
                      'required): Unique identifier for the target task"}], '
                      '"output": {"description": "Undocumented in provided '
                      'profile - likely returns task metadata or status '
                      'details", "type": "Not specified in source data"}}',
              'description': 'Fetches detailed information about a specific '
                             'task using its unique taskId. This method uses '
                             'predefined server configurations and internal '
                             'routing identifiers to access task data at any '
                             'stage of execution.',
              'details': 'Fetches detailed information about a specific task '
                         'using its unique taskId. This method uses predefined '
                         'server configurations and internal routing '
                         'identifiers to access task data at any stage of '
                         'execution.',
              'method': 'mcp_call_tool',
              'short_description': 'Retrieve task details by ID from MCP task '
                                   'manager',
              'source': 'smithery',
              'timestamp': 1742374912350.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.167902425,
 'values': []}, {'id': 'smithery_mcp_tool-@Szowesgad/mcp-server-semgrep-analyze_results',
 'metadata': {'data': '{"method": "mcp_call_tool", "inputs": [{"name": '
                      '"serverId", "type": "string", "required": true, '
                      '"description": "Server configuration reference from MCP '
                      'package", "defaultValue": '
                      '"@Szowesgad/mcp-server-semgrep"}, {"name": "toolName", '
                      '"type": "string", "required": true, "description": '
                      '"Fixed identifier for internal tool routing", '
                      '"defaultValue": "analyze_results"}, {"name": '
                      '"arguments", "type": "object", "required": true, '
                      '"description": "Contains \'results_file\' parameter '
                      '(string, required) specifying absolute path to JSON '
                      'results within MCP directory"}], "output": '
                      '{"description": "Output type not specified in '
                      'documentation", "type": "undefined"}}',
              'description': 'Processes and analyzes code scan results from '
                             'tools like Semgrep using MCP infrastructure. '
                             'Requires a server configuration reference, tool '
                             'identifier, and path to scan results JSON file '
                             'within the MCP directory structure.',
              'details': 'Processes and analyzes code scan results from tools '
                         'like Semgrep using MCP infrastructure. Requires a '
                         'server configuration reference, tool identifier, and '
                         'path to scan results JSON file within the MCP '
                         'directory structure.',
              'method': 'mcp_call_tool',
              'short_description': 'Analyzes security scan results',
              'source': 'smithery',
              'timestamp': 1742380767089.0,
              'tool': 'SmitheryMCPTool',
              'uid': 'levia'},
 'score': 0.167728528,
 'values': []}
 ]