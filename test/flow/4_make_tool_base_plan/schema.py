failed_output_schema = {
    "type": "object",
    "required": ["status", "reason"],
    "properties": {
        "status": {
            "type": "string",
            "enum": ["failed"],
            "description": "Indicates that the plan execution failed"
        },
        "reason": {
            "type": "string",
            "description": "Detailed explanation of why the plan failed and what tools would be needed"
        }
    },
    "additionalProperties": False
}

success_output_schema = {
    "type": "object",
    "required": ["status", "plan"],
    "properties": {
        "status": {
            "type": "string",
            "enum": ["success"],
            "description": "Indicates that the plan can be executed successfully"
        },
        "plan": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["step", "tool", "data", "step purpose", "description"],
                "properties": {
                    "step": {
                        "type": "string",
                        "pattern": "^step [0-9]+$",
                        "description": "A numbered step indicator (e.g., 'step 1', 'step 2')"
                    },
                    "tool": {
                        "type": "string",
                        "description": "The specific external tool required for this step"
                    },
                    "data": {
                        "type": "string",
                        "description": "Specific data of the tool from the tool_list"
                    },
                    "step purpose": {
                        "type": "string",
                        "description": "The purpose of this step in the plan"
                    },
                    "description": {
                        "type": "string",
                        "description": "A general overview of the objective to be achieved by this tool"
                    }
                },
                "additionalProperties": False
            },
            "minItems": 1
        }
    },
    "additionalProperties": False
}