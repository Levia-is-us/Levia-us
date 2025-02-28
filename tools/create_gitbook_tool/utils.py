
def get_markdown_title(text):
    text = text.replace('```', '').replace('#', '').replace(':', '')
    words = [word for word in text.split() if word.strip()] 
    result = []
    
    has_title = any('title' in word.lower() for word in words)
    has_markdown = any('markdown' in word.lower() for word in words)
    
    if has_title:
        for i in range(len(words)):
            if 'title' in words[i].lower():
                for j in range(1, 4):
                    if i + j < len(words):
                        result.append(words[i + j])
                break
    elif has_markdown:
        for i in range(len(words)):
            if 'markdown' in words[i].lower():
                for j in range(1, 4):
                    if i + j < len(words):
                        result.append(words[i + j])
                break
    else:
        result = words[:3]
    
    return '_'.join(result)
