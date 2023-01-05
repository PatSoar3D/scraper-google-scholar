# scraper-google-scholar

A web scraper that extracts article titles, PDF files, and abstracts from Google Scholar based on a user-specified search query. The scraper also stores this information in a MongoDB database, which is generated during the execution of the scraper.

## Database Structure

The scraper stores data in the following collections:

- `articles`: Contains the ID and name of each article
- `results`: Contains the ID of the corresponding article, the name and version of the result, and the abstract of the article

## Future Work

In future updates, we plan to add versioning functionality to the scraper. This will allow us to update the already present entry for a given article instead of creating a new entry every time we scrape the same link.

## Dependencies

The following dependencies are required to run the scraper:

- `requests`: A library for making HTTP requests
- `selenium`: A library for automating web browser tasks
- `webdriver_chrome`: A library for controlling the Chrome web browser
- `regex`: A library for working with regular expressions
- `pdfminer`: A library for extracting data from PDF files
- `pymongo`: A library for working with MongoDB databases

## Installation

To install the dependencies, run the following command:

pip install -r requirements.txt

This will install all the required libraries.
