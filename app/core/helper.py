import re

def format_string_for_slack(text: str) -> str:
    newline = """
    """
    print(f"Original text: {text}")
    formatted_text = text.replace('\n', newline)
    
    if formatted_text.startswith('"'):
        formatted_text = formatted_text[1:]
    
    if formatted_text.endswith('"'):
        formatted_text = formatted_text[:-1]

    print(f"Formatted text: {formatted_text}")
    return formatted_text



