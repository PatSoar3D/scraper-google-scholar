import requests
import regex as re

title = 'Are we there yet? Data saturation in qualitative research'
pdf_url = 'https://scholarworks.waldenu.edu/cgi/viewcontent.cgi?article=1466&context=facpubs'
chunk_size = 2000

r = requests.get(pdf_url, stream=True)
with open(re.sub(r'[^\w\s]' , '-', title) + '.pdf', 'wb') as f:
    for chunk in r.iter_content(chunk_size):
        f.write(chunk)