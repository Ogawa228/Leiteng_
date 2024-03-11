import requests
from bs4 import BeautifulSoup
import chardet
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page_structure_selenium(url):
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6, a')))

    page_structure = []
    current_hierarchy = []  # Keep track of the current section hierarchy
    
    elements = browser.find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6, a')
    for element in elements:
        tag_name = element.tag_name
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header_level = int(tag_name[1])
            header_text = element.text.strip()
            
            # Trim the hierarchy if we move up levels
            current_hierarchy = current_hierarchy[:header_level-1]
            
            # Add or replace the current level's header
            if len(current_hierarchy) < header_level:
                current_hierarchy.append(header_text)
            else:
                current_hierarchy[header_level-1] = header_text
            
            page_structure.append(("#" * header_level, header_text))
        elif tag_name == 'a':
            href = element.get_attribute('href')
            text = element.text.strip() or "No Text"
            if href:
                # Assume it is a child of the current header level
                indent = " " * (4 * (len(current_hierarchy)))
                markdown_link = f"{indent}- [{text}]({href})"
                page_structure.append(("", markdown_link))
    
    browser.quit()
    return page_structure

def write_page_structure_to_file(page_structure, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for depth, content in page_structure:
            if depth:  # This is a header
                file.write(depth + " " + content + '\n\n')
            else:  # This is a link
                file.write(content + '\n')

# Ask for the URL from user input
url = input("请输入要提取Markdown链接的网页的URL:")
if not url:
    print("未输入URL。程序已退出。")
    exit(1)

# Output file location
output_filename = "markdown_links_with_structure.md"

# Fetch and parse the webpage structure
page_structure = get_page_structure_selenium(url)

# Write to a markdown file
write_page_structure_to_file(page_structure, output_filename)

print(f"Markdown链接和网页结构已经被写入到文件 {output_filename}。")