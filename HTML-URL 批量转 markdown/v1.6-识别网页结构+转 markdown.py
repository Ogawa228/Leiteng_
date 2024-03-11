import requests
from bs4 import BeautifulSoup
from chardet import detect

def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.content
        # Use the chardet library to detect encoding
        charset_detected = detect(html_content)
        encoding = charset_detected['encoding']
        # If encoding is detected, try to decode content with it
        if encoding is not None:
            html_content = html_content.decode(encoding)
        # If no encoding detected, use the response's apparent_encoding
        else:
            html_content = html_content.decode(response.apparent_encoding)
        return html_content, None
    except requests.HTTPError as http_err:
        return None, f"HTTP error occurred: {http_err}"
    except Exception as err:
        return None, f"An error occurred: {err}"

def extract_links_and_structure(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        text = a.get_text().strip()
        href = a['href']

        # Determine the nesting level
        parents = a.find_parents()
        level = len(set([p.name for p in parents if p.name in ['ul', 'ol']])) - 1
        indentation = '  ' * level

        # Consider Markdown link format
        markdown_link = f"{indentation}- [{text}]({href})"
        links.append(markdown_link)

    return '\n'.join(links)

# Prompt the user to input the URL
user_input_url = input("Please enter the URL of the website you want to extract: ")

content, error = fetch_website_content(user_input_url)

if content:
    links_markdown = extract_links_and_structure(content)
    # Save the extracted links to a file
    links_filename = 'website_links.md'
    with open(links_filename, 'w', encoding='utf-8') as md_file:
        md_file.write(links_markdown)
    print(f"The extracted links have been saved to {links_filename}")
else:
    print(error)