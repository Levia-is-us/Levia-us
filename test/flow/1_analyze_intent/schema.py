direct_answer_schema = {
    "type": "object",
    "required": ["type", "intent", "response"],
    "properties": {
        "type": {
            "type": "string",
            "enum": ["direct_answer"]
        },
        "intent": {
            "type": "string",
            "description": "Summarized intent explaining why a direct answer was chosen"
        },
        "response": {
            "type": "string",
            "description": "The actual answer content provided to the user"
        }
    },
    "additionalProperties": False
}

call_tools_schema = {
    "type": "object",
    "required": ["type", "short-intent", "intent", "response"],
    "properties": {
        "type": {
            "type": "string",
            "enum": ["call_tools"]
        },
        "short-intent": {
            "type": "string",
            "description": "Summarized normalized intent for calling tools, with specific entities removed"
        },
        "intent": {
            "type": "string",
            "description": "Detailed intent explaining what tools need to be called and why"
        },
        "response": {
            "type": "string",
            "description": "A goal statement for the tool call operation"
        }
    },
    "additionalProperties": False
}