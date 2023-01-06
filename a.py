import requests

url = "https://www.sciencedirect.com/science/article/pii/S1297320304001313"
response = requests.get(url)

with open("document.pdf", "wb") as f:
    f.write(response.content)
    
r = requests.get(pdf_url, stream=True)
try:
    with open(self.pdf, 'wb') as f:
        for chunk in r.iter_content(chunk_size):
            f.write(chunk)
    f.close()
    return True
except:
    return False  