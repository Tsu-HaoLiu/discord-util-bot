import re
import os

def remove_special_characters(text: str) -> str:
    pattern = r'[^a-zA-Z0-9\s]'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def delete_file(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)
