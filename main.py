import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import regex as re

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Set the path to the chromedriver executable
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options )
driver.get('https://scholar.google.com/')

# # Enter the search query and submit the form
search_box = driver.find_element('name', 'q')
search_box.send_keys('data')
search_box.submit()

# Wait for the search results to load
driver.implicitly_wait(10)

# Find the search results elements
results = driver.find_elements('css selector', '.gs_scl')

# Iterate through the search results
for result in results[1:]:
    # Find the title element and extract the text
    
    title_element = result.find_element('css selector', '.gs_rt a')
    title = title_element.text
    print('[Title]:', title)

    # Find the PDF download link and extract the href
    try:
        pdf_element = result.find_element('css selector', '.gs_or_ggsm a')
        file_element = result.find_element('css selector', '.gs_ctg2')
        file_extension = file_element.text
        
        if(file_extension[1:-1] == 'PDF'):
            pdf_url = pdf_element.get_attribute('href')
            print('[URL]: ', pdf_url)

            # downloading PDF file
            chunk_size = 2000
            try:
                r = requests.get(pdf_url, stream=True)
                if(r.headers['Content-Type'] == 'application/pdf'):
                    with open(re.sub(r'[^\w\s]' , '-', title) + '.pdf', 'wb') as f:
                        f.write(r.content)
                        print('[Downloaded]')
                else:
                    print("[STATUS]: Couldn't download PDF attachment because the URL is sending content type other than PDF.")
                    
            except:
                print("[STATUS]: Couldn't download PDF attachment.")

        else:
            print('[STATUS]: No PDF attachment for this article')
    except:
        print('[STATUS]: No attachment for this article')
    print()
        
driver.close()
