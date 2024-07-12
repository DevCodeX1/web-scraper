import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import time
from random import randint

def start_scraping():
    search_term = entry.get()
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a search term.")
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Searching for '{search_term}'...\n\n")

    search_term_encoded = search_term.replace(' ', '+')
    url = f"https://www.google.com/s?k={search_term_encoded}"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]

    headers = {
        "User-Agent": user_agents[randint(0, len(user_agents) - 1)]
    }

    success = False
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('span', class_='a-size-medium a-color-base a-text-normal')  # Example: Scraping product titles

            for idx, result in enumerate(results, start=1):
                result_text.insert(tk.END, f"{idx}. {result.text.strip()}\n")

            success = True
            break
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(randint(1, 3))  # Random delay between retries
            else:
                messagebox.showerror("Request Error", str(e))
        except Exception as e:
            messagebox.showerror("Scraping Error", str(e))
            break

    if not success:
        result_text.insert(tk.END, "Failed to retrieve data after multiple attempts.\n")

app = tk.Tk()
app.title("Web Scraping Bot")

frame = tk.Frame(app)
frame.pack(pady=20)

label = tk.Label(frame, text="Enter Search Term:")
label.pack(side=tk.LEFT)

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(frame, text="Start Scraping", command=start_scraping)
start_button.pack(side=tk.LEFT)

result_text = tk.Text(app, wrap=tk.WORD, height=15, width=80)
result_text.pack(pady=20)

app.mainloop()
