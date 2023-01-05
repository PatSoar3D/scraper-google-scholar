import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import regex as re
from pdfController import pdf_controller
from dbClient import db_client

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Set the path to the chromedriver executable
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options )
driver.get('https://scholar.google.com/')

# creating method to help scrape
def scrape_site(pdf_element):
    try:
        pdf_url = pdf_element.get_attribute('href')
        print('[URL]: ', pdf_url)

        # downloading PDF file
        chunk_size = 2000
        try:
            r = requests.get(pdf_url, stream=True)
            if(r.headers['Content-Type'] == 'application/pdf'):
                pdf_filename = re.sub(r'[^\w\s]' , '-', title) + '.pdf'
                pdf = pdf_controller(pdf_filename)
                if(pdf.save_pdf(pdf_url)):
                    print('[PDF Downloaded]')
                    pdf_abstract = pdf.extract_abstract_from_pdf()
                    print('[Abstract]:', pdf_abstract)
                    
                    # nullify abstract if no abstract is found
                    if(pdf_abstract == None):
                        pdf_abstract = ''
                        
                    # id, pdf_name, article_name, version, abstract
                    resp_id, resp_article_collection, resp_results_collection = dbc.add_data(pdf_filename, title, 1, pdf_abstract)
                    if(resp_id != -1):
                        print('[RECORD SAVED ' + str(resp_id) + ']: ' + str(resp_article_collection) + ':> ' + str(resp_results_collection))
                    else:
                        print("[STATUS]: One of the collections is not created.'")
                else:
                    print("[STATUS]: Couldn't save the PDF attachment to local server")
            else:
                print("[STATUS]: Couldn't download PDF attachment because the URL is sending content type other than PDF.")
        except:
            print("[STATUS]: Couldn't download PDF attachment.")
    except:
        print('[STATUS]: No attachment for this article')
        

# # Enter the search query and submit the form
search_box = driver.find_element('name', 'q')
search_box.send_keys('data')
search_box.submit()

# Wait for the search results to load
driver.implicitly_wait(10)

# Find the search results elements
results = driver.find_elements('css selector', '.gs_scl')

# initialize mongoDB server with already created database
# and then it creates two collections within the database to store articles
dbc = db_client('mongodb://localhost:27017/', 'scraperGoogleScholar')
dbc.create_collections(['articles', 'results'], [{'id': 'int', 'name': 'string'},{'article_id': 'int', 'name': 'string', 'version': 'int', 'abstract': 'string'}])
dbc_record_counter = 0

# Iterate through the search results
for result in results[1:]:
    # Find the title element and extract the text
    title_element = result.find_element('css selector', '.gs_rt a')
    title = title_element.text
    print('[Title]:', title)

    # Find the PDF download link and extract the href
    try:
        file_element = result.find_element('css selector', '.gs_ctg2')
        file_extension = file_element.text
        
        if(file_extension[1:-1] == 'PDF'):
            pdf_element = result.find_element('css selector', '.gs_or_ggsm a')
            scrape_site(pdf_element)
        else:
            print('[STATUS]: Attachment is not of type PDF')
    except:
        try:
            file_element = result.find_element('css selector', '.gs_rt a')
            scrape_site(file_element)
        except:
            print('[STATUS]: Could not find a scrapeable link')
    
    print()
        
driver.close()
