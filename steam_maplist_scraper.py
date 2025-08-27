import os
import sys
import json
import requests
import webbrowser
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageTk  # For window icon

# ------------------------- RESOURCE HANDLER ------------------------- #
def resource_path(relative_path: str) -> str:
    """
    Returns the absolute path to a resource, works for PyInstaller --onefile.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ------------------------- CONFIGURATION ------------------------- #
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "theme": "darkly",      # Default ttkbootstrap theme
    "last_url": "",         # Last entered Steam Workshop URL
    "include_id": False,    # Include map IDs in results
    "auto_copy": False      # Automatically copy map list to clipboard
}

def load_config() -> dict:
    """
    Load configuration from config.json. Fallback to default if file missing or corrupt.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(cfg: dict):
    """
    Save configuration back to config.json.
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
    except Exception:
        messagebox.showerror("Error", "Failed to save configuration.")

config = load_config()

# ------------------------- TKINTER WINDOW ------------------------- #
root = ttk.Window(themename=config["theme"])
style = ttk.Style()
root.title("Steam Workshop Maplist Creator")
root.geometry("520x480")
root.resizable(False, False)

# ------------------------- ICON SETUP ------------------------- #
ICON_PATH = resource_path("icon.ico")
try:
    img = ImageTk.PhotoImage(file=ICON_PATH)
    root.iconphoto(False, img)
    root._icon_image = img  # Keep reference alive to prevent __del__ error
except Exception:
    pass

# ------------------------- THREAD POOL ------------------------- #
executor = ThreadPoolExecutor(max_workers=1)  # Background fetch thread

# ------------------------- STEAM WORKSHOP FUNCTIONS ------------------------- #
def is_valid_steam_url(url: str) -> bool:
    """
    Validate a Steam Workshop collection URL.
    """
    parsed = urlparse(url)
    return parsed.netloc == "steamcommunity.com" and "sharedfiles/filedetails" in parsed.path

def fetch_map_list(url: str, include_id: bool, progress_callback=None):
    """
    Fetch map names (optionally with IDs) from a Steam Workshop collection page.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return None, f"Failed to retrieve page: {e}"

    soup = BeautifulSoup(resp.content, "html.parser")
    map_items = soup.find_all("div", class_="workshopItemTitle")
    if not map_items:
        return None, "No map items found. Please check the URL."

    results = []
    total = len(map_items)
    for idx, item in enumerate(map_items):
        parent_link = item.find_parent("a")
        if parent_link and "id=" in parent_link.get("href", ""):
            map_id = parent_link["href"].split("id=")[-1]
            map_name = item.text.strip()
            results.append(f"{map_name}:{map_id}" if include_id else map_name)
        if progress_callback:
            progress_callback(int((idx + 1) / total * 100))

    return results, None

# ------------------------- FILE & CLIPBOARD FUNCTIONS ------------------------- #
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def save_map_list(map_names):
    """
    Save map list to a user-selected text file.
    """
    if not map_names:
        return False, "No maps to save."
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Map List"
    )
    if not path:
        return False, "Save operation cancelled."
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(map_names))
        return True, f"Map list saved to {path}"
    except Exception as e:
        return False, f"Error saving file: {e}"

def copy_to_clipboard(map_names):
    """
    Copy map list to clipboard using pyperclip if available.
    """
    if not CLIPBOARD_AVAILABLE:
        messagebox.showwarning(
            "Clipboard Not Available",
            "Install 'pyperclip' module to enable clipboard functionality:\n\npip install pyperclip"
        )
        return
    try:
        pyperclip.copy("\n".join(map_names))
        messagebox.showinfo("Success", "Map list copied to clipboard!")
    except Exception:
        messagebox.showerror("Error", "Failed to copy to clipboard.")

# ------------------------- GUI CALLBACKS ------------------------- #
def on_fetch_click():
    """
    Triggered when user clicks 'Fetch Maps'. Validates URL and starts background fetch.
    """
    url = url_entry.get().strip()
    if not url or not is_valid_steam_url(url):
        messagebox.showerror("Error", "Please enter a valid Steam Workshop Collection URL.")
        return

    fetch_button.config(state="disabled")
    progress_var.set(0)
    status_label.config(text="Fetching maps...")

    # Save last options
    config.update({"last_url": url, "include_id": include_id_var.get()})
    save_config(config)

    # Run fetching in background thread
    executor.submit(fetch_and_display_maps, url, include_id_var.get())

def update_progress(value: int):
    """
    Safely update progress bar from background thread.
    """
    progress_var.set(value)
    root.update_idletasks()

def fetch_and_display_maps(url, include_id):
    """
    Background task: fetch map list and update GUI.
    """
    maps, error = fetch_map_list(url, include_id, update_progress)
    root.after(0, lambda: fetch_button.config(state="normal"))

    if error:
        root.after(0, lambda: status_label.config(text=""))
        root.after(0, lambda: messagebox.showerror("Error", error))
        return

    if not maps:
        root.after(0, lambda: status_label.config(text="No maps found"))
        return

    root.after(0, lambda: status_label.config(text=f"Found {len(maps)} maps"))
    root.after(0, lambda: show_map_preview(maps))

def show_map_preview(maps):
    """
    Display map list in a preview window with save/copy options.
    """
    preview = ttk.Toplevel(root)
    preview.title("Map List Preview")
    preview.geometry("480x360")
    preview.resizable(False, False)

    ttk.Label(preview, text="Map List Preview", font=("Helvetica", 14, "bold")).pack(pady=10)

    frame = ttk.Frame(preview)
    frame.pack(fill="both", expand=True, padx=15, pady=10)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10))
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    for m in maps:
        listbox.insert(tk.END, m)

    # Buttons frame
    btn_frame = ttk.Frame(preview)
    btn_frame.pack(fill="x", padx=15, pady=10)

    ttk.Button(btn_frame, text="💾 Save", command=lambda: save_and_show_result(maps)).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="📋 Copy", command=lambda: copy_to_clipboard(maps)).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="❌ Close", command=preview.destroy).pack(side="right", padx=5)

    # Auto-copy if enabled
    if config.get("auto_copy"):
        copy_to_clipboard(maps)

def save_and_show_result(maps):
    """
    Save map list and show confirmation dialog.
    """
    success, msg = save_map_list(maps)
    (messagebox.showinfo if success else messagebox.showerror)("Result", msg)

# ------------------------- ADDITIONAL CALLBACKS ------------------------- #
def open_github():
    """Open GitHub profile in default browser."""
    webbrowser.open("https://github.com/ZoniBoy00")

def toggle_theme():
    """Switch between dark and light ttkbootstrap themes."""
    config["theme"] = "cosmo" if config["theme"] == "darkly" else "darkly"
    style.theme_use(config["theme"])
    save_config(config)

def toggle_auto_copy():
    """Enable or disable automatic clipboard copying."""
    config["auto_copy"] = auto_copy_var.get()
    save_config(config)

# ------------------------- GUI ELEMENTS ------------------------- #
main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=15, pady=15)

ttk.Label(main, text="Steam Workshop Maplist Creator", font=("Helvetica", 14, "bold")).pack(pady=10)
ttk.Label(main, text="Collection URL:").pack(anchor="w", pady=(5,2))
url_entry = ttk.Entry(main, width=60)
url_entry.pack(fill="x")
url_entry.insert(0, config["last_url"])

include_id_var = tk.BooleanVar(value=config.get("include_id", False))
auto_copy_var = tk.BooleanVar(value=config.get("auto_copy", False))

options_frame = ttk.Frame(main)
options_frame.pack(fill="x", pady=8)
ttk.Checkbutton(options_frame, text="Include Map IDs", variable=include_id_var).pack(side="left", padx=5)
ttk.Checkbutton(options_frame, text="Auto-copy to clipboard", variable=auto_copy_var, command=toggle_auto_copy).pack(side="left", padx=5)

fetch_button = ttk.Button(main, text="Fetch Maps", command=on_fetch_click, bootstyle="primary")
fetch_button.pack(pady=10)

progress_var = tk.IntVar()
ttk.Progressbar(main, variable=progress_var, maximum=100).pack(fill="x", pady=5)

status_label = ttk.Label(main, text="", font=("Helvetica", 9))
status_label.pack(pady=5)

footer = ttk.Frame(root)
footer.pack(side="bottom", fill="x", pady=8)

ttk.Button(footer, text="🌐 GitHub", command=open_github).pack(side="left", padx=10)
ttk.Label(footer, text="Developed by ZoniBoy00", font=("Helvetica", 9, "italic")).pack(side="left", expand=True)
ttk.Button(footer, text="🌓 Theme", command=toggle_theme).pack(side="right", padx=10)

# ------------------------- RUN APP ------------------------- #
root.mainloop()
