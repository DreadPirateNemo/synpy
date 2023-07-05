import html
import requests
import re
from bs4 import BeautifulSoup
from typing import AnyStr
from urllib.parse import urljoin


url = input("Enter a URL: ")
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails = []

for string in soup.stripped_strings:
    match = re.search(email_pattern, string)
    if match:
        emails.append(match.group())

with open('emails.txt', 'w') as f:
    for email in emails:
        f.write(email + '\n')

def urljoin(
    base: AnyStr,
    url: AnyStr | None,
    allow_fragments: bool = True
) -> AnyStr | None:
    if url is None:
        return None
    return base + url
