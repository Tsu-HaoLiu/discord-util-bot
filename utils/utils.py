import re
import os
import traceback

def remove_special_characters(text: str) -> str:
    pattern = r'[^a-zA-Z0-9\s]'
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text

def delete_file(file_name: str):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
    except Exception as e:
        print(e, traceback.print_exc())

def file_size(filename) -> int:
    return os.stat(filename).st_size

def convert_bytes_to_mb(file_bytes: int) -> float:
    return round(file_bytes / (1024*1024), 2)


def create_formatted_reply(ctx, send_url: str, details: tuple, hide_embed=False) -> str:
    if not details:
        details = ""
    else:
        details = " ".join(details)

    if hide_embed:
        return f"`{ctx.message.content}`\n{details}\n<{send_url}>"

    return f"`{ctx.message.content}`\n{details}\n{send_url}"
