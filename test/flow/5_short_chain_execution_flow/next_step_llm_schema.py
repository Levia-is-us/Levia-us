next_step_proceed_schema = {
    "type": "object",
    "required": ["step", "can_proceed", "extracted_arguments"],
    "properties": {
        "step": {
            "type": "string",
            "description": "The current step number being executed"
        },
        "can_proceed": {
            "type": "boolean",
            "enum": [True],
            "description": "Indicates whether the current step can proceed"
        },
        "extracted_arguments": {
            "type": "object",
            "required": ["required_arguments"],
            "properties": {
                "required_arguments": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "required": ["source", "method", "value"],
                        "properties": {
                            "source": {
                                "type": "string",
                                "description": "Source of the argument value ('context' or step number)"
                            },
                            "method": {
                                "type": "string",
                                "enum": ["LLM", "direct", "code"],
                                "description": "Method used to get the argument value"
                            },
                            "value": {
                                "description": "The actual value of the argument"
                            }
                        },
                        "additionalProperties": False
                    },
                    "description": "Map of required arguments with their source, method and value"
                }
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}

cannot_proceed_schema = {
    "type": "object",
    "required": ["step", "can_proceed", "missing_required_arguments"],
    "properties": {
        "step": {
            "type": "string",
            "description": "The current step number being executed"
        },
        "can_proceed": {
            "type": "boolean",
            "enum": [False],  # Only allows false, as this is the "cannot proceed" schema
            "description": "Indicates that the current step cannot proceed"
        },
        "missing_required_arguments": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of required arguments that are missing"
        },
        "needed_optional_arguments": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of optional arguments that are needed for this step"
        },
        "remarks": {
            "type": "string",
            "description": "Natural language explanation of why the step cannot proceed"
        }
    },
    "additionalProperties": False
}