# scraper-google-scholar

A web scraper that extracts article titles, PDF files, and abstracts from Google Scholar based on a user-specified search query. The scraper also stores this information in a MongoDB database, which is generated during the execution of the scraper.

## Technologies

This project is built with the following technologies:

- ![Python](https://img.shields.io/badge/-Python-yellow?style=flat&logo=python)
- ![Selenium](https://img.shields.io/badge/-Selenium-brightgreen?style=flat&logo=selenium)
- ![MongoDB](https://img.shields.io/badge/-MongoDB-blue?style=flat&logo=mongodb)
- ![PdfMiner](https://img.shields.io/badge/-PdfMiner-orange?style=flat&logo=pdfminer)

## Getting Started

Follow these steps to set up and run the scraper:

1. Create a virtual environment with `python -m venv venv` 
2. Install the dependencies using `pip install -r requirements.txt`
3. Install and set up MongoDB. Follow the instructions in following link: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
4. Verify that your MongoDB connection string is `mongodb://localhost:27017`. You can check this by going into MongoDBCompass.
5. Things you can change in project: 
    1. Query for GOOGLE Scholar at `line 58`
    2. MongoDB database name to create by code at `line 69`
    3. MongoDB collection names to be generated at `line 70`

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
