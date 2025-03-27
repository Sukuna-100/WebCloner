import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import messagebox

class WebsiteCloner:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Cloner")
        
        self.label = tk.Label(root, text="Enter URL to clone:")
        self.label.pack(pady=10)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=10)

        self.clone_button = tk.Button(root, text="Clone Website", command=self.clone_website)
        self.clone_button.pack(pady=20)

    def clone_website(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        
        try:
            self.download_website(url)
            messagebox.showinfo("Success", "Website cloned successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_website(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Create a directory for the cloned website
        domain = url.split("//")[-1].split("/")[0]
        os.makedirs(domain, exist_ok=True)

        # Save the main HTML file
        html_file_path = os.path.join(domain, "index.html")
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        # Parse HTML and download assets
        soup = BeautifulSoup(response.text, 'html.parser')
        self.download_assets(soup, url, domain)

    def download_assets(self, soup, base_url, domain):
        # Download images
        for img in soup.find_all('img'):
            img_url = urljoin(base_url, img['src'])
            self.download_file(img_url, domain)

        # Download CSS
        for link in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(base_url, link['href'])
            self.download_file(css_url, domain)

        # Download JavaScript
        for script in soup.find_all('script'):
            if 'src' in script.attrs:
                js_url = urljoin(base_url, script['src'])
                self.download_file(js_url, domain)

    def download_file(self, url, domain):
        try:
            response = requests.get(url)
            response.raise_for_status()
            file_name = os.path.join(domain, os.path.basename(url))
            with open(file_name, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteCloner(root)
    root.mainloop()