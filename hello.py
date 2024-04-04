import requests
import json
from bs4 import BeautifulSoup
import xmltojson


apiUrl = 'https://www.screener.in/'


companySymbol= input("Please enter Company Symbol: ")

print(f'Fetching company details {companySymbol}...')

comUrl = apiUrl + 'company/' + companySymbol + '/consolidated'

resp = requests.get(comUrl)
soup = BeautifulSoup(resp.content, 'html5lib')

formatedData ={}
formatedData['symbol'] = companySymbol
formatedData['companyName'] = soup.find('h1', attrs = {'class':'h2 shrink-text'}).text

rawData = soup.find('div', attrs = {'class':'company-info'})

formatedData['about'] =  rawData.find('div', attrs = {'class':'sub show-more-box about'}).p.text
formatedData['companyLinks'] = {}

links = rawData.find('div', attrs = {'class':'company-links'} )
all_links = links.find_all('a')

formatedData['companyLinks']['website'] = all_links[0].get('href')
formatedData['companyLinks']['bsc'] = all_links[1].get('href')
formatedData['companyLinks']['nse'] = all_links[2].get('href')

topRatios =  rawData.find('ul', attrs = {'id':'top-ratios'})

formatedData['companyLinks']['topRatios'] =[]

for li in topRatios.find_all('li'):
    text = li.find('span', class_='name').text.lstrip().rstrip()
    value =  li.find('span', class_='number').text.lstrip().rstrip()
    temp = { 'name': text , 'value' : value }
    formatedData['companyLinks']['topRatios'].append(temp)


print(formatedData)

saveStat= input("\n\nDo you want to save data as Json (y/n)")

if saveStat == 'y':
    with open(companySymbol+'.json', 'w') as file:
        json.dump(formatedData, file)
    print('\n\nData saved as Json ...')
elif saveStat.lower() == 'n':
    print("Data not saved as JSON.")
