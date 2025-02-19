import re


text = """ <input_breakdown>- 1. Main Topic or Request: - 

 - User inquires about OpenAI's recent updates or activities. - 

 - Keywords: OpenAI, recent, what they've done.

2. Can it be directly answered?: - 

 - Partially answerable: My knowledge is current up to October 2023, I can list important events until that point (such as GPT-4 release, ChatGPT Enterprise, etc.). - 

 - Cannot fully answer: If user needs information after October 2023 (like 2024 updates), it's beyond my knowledge scope.

3. Key Point Analysis: - 

 - Explicit Statement: User clearly requests to know OpenAI's recent developments. - 

 - Implicit Inference: User may be interested in product updates, research progress, or business partnerships, but hasn't specified which area.

4. Conclusion: - 

 - Provide known information with time limitations, falls under direct answer category. - 

 - If updated information is needed, suggest using external tools, though user hasn't explicitly requested further action.
</input_breakdown>

"""


def extract_stream_analysis(text):
    json_start = text.find("{")
    json_end = text.rfind("}") + 1
    json_text = text[json_start:json_end]
    return json_text

# print(extract_stream_analysis(text))

text = "@@@@AA<hello asd"
result = re.search("<([^>]+)>", text)
if result:  
    print(result.group(1))
else:
    print("not found")
