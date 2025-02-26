from engine.flow.executor.transformation_code_llm import transformation_code_llm

def transform_code(next_step_reply, user_id, ch_id):
    input = next_step_reply["extracted_arguments"]["required_arguments"]
    output = next_step_reply["output"]

    return transformation_code_llm(input, output)

