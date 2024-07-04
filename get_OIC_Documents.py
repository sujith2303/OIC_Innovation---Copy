import requests
from bs4 import BeautifulSoup

response = requests.get("https://docs.oracle.com/en/cloud/paas/integration-cloud/books.html")
# Check if the request was successful
if response.status_code == 200:
    # Access the content of the response
    html_content = response.text
    print(html_content)
else:
    print("Failed to retrieve data")




soup = BeautifulSoup(html_content, 'html.parser')

book_links = soup.find_all('a', class_=False, parent=soup.find('div', class_="book"))
pdf_links = []
for link in book_links:
  if link.has_attr('href') and link['href'].endswith('.pdf'):
    pdf_links.append(link['href'])

# Print the extracted PDF links
print(pdf_links)

base_url = 'https://docs.oracle.com/en/cloud/paas/integration-cloud/'  # Replace with the actual base URL
for pdf_link in pdf_links:
  full_pdf_url = base_url + pdf_link
  # Download the PDF file
  response = requests.get(full_pdf_url)
  if response.status_code == 200:
      with open('Documentation_OIC/'+pdf_link.split('/')[-1], 'wb') as f:
          f.write(response.content)
      print('PDF downloaded successfully.')
  else:
      print('Failed to download PDF.')
