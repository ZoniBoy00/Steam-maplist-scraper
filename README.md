# Steam Workshop Maplist Creator

A Python tool with a clean graphical user interface (GUI) for scraping map names from a Steam Workshop collection and saving them into a text file.  
This is especially useful for generating maplists for game servers or personal use.

## ✨ Features

- Scrapes map names directly from any Steam Workshop collection
- Optionally includes map IDs
- Saves results into a text file chosen by the user
- Modern Tkinter + ttkbootstrap GUI
- Option to automatically copy results to clipboard (requires `pyperclip`)
- Background fetching with progress bar
- User-friendly error messages

## 🖥️ GUI Preview

- Input field for the Steam Workshop collection URL  
- Checkboxes for:
  - Including map IDs
  - Auto-copying to clipboard
- Fetch button to scrape maps
- Progress bar showing scraping progress
- Map list preview window with Save, Copy, and Close buttons
- Theme toggle (dark/light)

## ⚙️ Requirements

- **Option 1: Run as Python script**
  - Python **3.10+** recommended
  - Required libraries:
    - `requests`
    - `beautifulsoup4`
    - `ttkbootstrap`
    - `pyperclip` (optional, for clipboard support)
    - `Pillow` (for proper icon handling)

- **Option 2: Run as executable (.exe)**
  - No Python installation required  
  - Just download and run the prebuilt `.exe` file

## 📥 Installation

### 🔹 Option 1: Run with Python

1. Clone this repository or download the script:

    ```bash
    git clone https://github.com/ZoniBoy00/Steam-maplist-scraper.git
    cd Steam-maplist-scraper
    ```

2. Install the required Python libraries:

    ```bash
    pip install requests beautifulsoup4 ttkbootstrap pyperclip pillow
    ```

   *(If clipboard support is not needed, you can skip `pyperclip`.)*

3. Run the script:

    ```bash
    python steam_maplist_scraper.py
    ```

---

### 🔹 Option 2: Run the .exe file

1. Download the latest release from the [Releases](https://github.com/ZoniBoy00/Steam-maplist-scraper/releases) page.  
2. Extract the zip (if needed).  
3. Double-click the `.exe` file to launch the application.  
   *(No installation or Python required.)*

---

## ▶️ Usage

1. Enter the Steam Workshop **collection URL** into the input field.  
2. Configure options:
   - **Include Map IDs** (optional)
   - **Auto-copy to clipboard** (optional)
3. Click **"Fetch Maps"**.  
4. The program will:
   - Display the map list in a preview window  
   - Save the results to a user-selected text file  
   - Copy the map list to clipboard if enabled

---

## 🛠️ Troubleshooting

- **`ModuleNotFoundError: No module named 'bs4'`**  
  Install dependencies with:  
  ```bash
  pip install beautifulsoup4
  ```

* **Clipboard not working**
  Make sure `pyperclip` is installed:

  ```bash
  pip install pyperclip
  ```

* **Icon not showing in taskbar**
  Ensure `icon.ico` is in the same folder as the script/exe.

* **No maps found**
  Ensure the Workshop collection is public and contains valid maps.

---

## 🤝 Contributing

Contributions are welcome!
Feel free to submit issues, fork the repository, and open pull requests to improve the tool.

---

## 📜 License

This project is licensed under the MIT License.
See the [LICENSE](https://github.com/ZoniBoy00/Steam-maplist-scraper/blob/main/LICENSE) file for details.
