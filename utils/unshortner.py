import requests


def validate_url(url: str) -> bool:
    return url.startswith(('https', 'http'))

def unshortner(url: str) -> dict:
    if not validate_url(url):
        return {'404': 'not valid url'}

    session = requests.Session()
    response = session.get(url, allow_redirects=True)

    redirect_list = []
    # Print each redirect
    if len(response.history) > 1:
        for x, redirect in enumerate(response.history, 1):
            print(f"Redirected #{x}: {redirect.url}", )
            redirect_list.append(redirect.url)

    # Print the final URL
    print("Final URL:", response.url)

    return {'cleaned': response.url, 'redirect_history': redirect_list}


