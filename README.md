# Steam Workshop Maplist Creator

This Python script scrapes map names from a Steam Workshop collection and saves them into a `maplist.txt` file. The script is useful for automatically generating a list of maps for game servers or other purposes.

## Features

- Scrapes map names from a Steam Workshop collection
- Outputs a list of map names into a `maplist.txt` file
- Simple and easy to use

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone this repository or download the script:
    ```bash
    git clone https://github.com/yourusername/steam-maplist-creator.git
    cd steam-maplist-creator
    ```

2. Install the required Python libraries:
    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

1. Open the script `steam_maplist_scraper.py` and update the URL variable with your desired Steam Workshop collection URL:
    ```python
    url = "https://steamcommunity.com/sharedfiles/filedetails/?id=3316031932"
    ```

2. Run the script:
    ```bash
    python steam_maplist_scraper.py
    ```

3. After running, a file named `maplist.txt` will be generated in the same directory, containing the names of the maps from the collection.

## Troubleshooting

- If you encounter the error `ModuleNotFoundError: No module named 'bs4'`, ensure you have installed the required libraries using:
    ```bash
    pip install beautifulsoup4
    ```
- Make sure the Steam Workshop URL you are using is publicly accessible and correct.

## Contributing

Feel free to submit issues, fork the repository, and make pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ZoniBoy00/Steam-maplist-scraper/blob/main/LICENSE) file for details.
