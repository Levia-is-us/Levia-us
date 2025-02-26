import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from engine.flow.executor.transformation_code_llm import transformation_code_llm

if __name__ == "__main__":
    input_structure = """[{'url': 'https://www.apple.com/iphone/', 'summary': "Apple's official page listing iPhone 16 Pro, iPhone 16 Pro Max, iPhone 16, iPhone 16 Plus, and iPhone 16e as current models. The iPhone 16 series was released in September 2024, while the iPhone 16e is a newer addition designed for Apple Intelligence."}, {'url': 'https://en.wikipedia.org/wiki/List_of_iPhone_models', 'summary': "Wikipedia's comprehensive list of iPhone models, confirming the iPhone 16, 16 Plus, 16 Pro, and 16 Pro Max as the most recent flagship models released in September 2024. The iPhone 16e is also noted as part of the 2025 lineup."}, {'url': 'https://www.macworld.com/article/228816/best-iphone-pro-mini-max.html', 'summary': "Macworld's updated comparison chart identifying the iPhone 16 series (Pro, Pro Max, 16, 16 Plus) and iPhone 16e as Apple's current models, with the 16e being the latest release in February 2025."}]
    """
    output_structure = """['https://www.apple.com/iphone/', 'https://en.wikipedia.org/wiki/List_of_iPhone_models', 'https://www.macworld.com/article/228816/best-iphone-pro-mini-max.html']
    """
    code_str = transformation_code_llm(input_structure, output_structure)
    print("code_str: ", code_str)

    exec(code_str)
    result = eval("extract_urls(" + input_structure + ")")
    print("result: ", result)