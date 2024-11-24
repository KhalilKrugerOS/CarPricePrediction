import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest


base_url = "https://www.automobile.tn/fr/neuf/"
# fetch url using requests
def getPageContent(url):
    res = requests.get(url)
    return res.content


constructors = [] 
models = []
features = []
links = []
technicalFileLinks = []
valuesfeatures = []

# create a soup : from html to python dict
src = getPageContent("https://www.automobile.tn/fr/neuf")
soup = BeautifulSoup(src, 'lxml')
constructors_list = soup.select("div.container a")

for i in range(len(constructors_list)):
    constructors.append(constructors_list[i]['href'])
    #adding the names that exist in href
# /fr/neuf/constructor ==> constructor

print(constructors[0].split('/')[3])
constructors = [ cons.split('/')[3] for cons in constructors  ]
links = [ base_url + constructor for constructor in constructors ]  # extracting links
links = links[0:10]
#print(links)
for link in links:
    page2 = getPageContent(link)
    soup2 = BeautifulSoup(page2, "lxml")
    print("the link is " + link)
    articles_list = soup2.select("div.articles div.versions-item a")
    for i in range(len(articles_list)):
        technicalFileLinks.append(articles_list[i]['href'])
   
    technicalFileLinks = [ base_url + '/'.join(technicalfilelink.split('/')[3:]) for technicalfilelink in technicalFileLinks ]
    for technicalfilelink in technicalFileLinks:
        soup = BeautifulSoup(getPageContent(technicalfilelink), "lxml")
        if  soup.select("div#specs.technical-details") == []:
            print("the technical file of the car" + technicalfilelink + " is on another page")
            technicalFileLinks.remove(base_url + '/'.join(technicalfilelink.split('/')[5:]))
            versions = soup.select("td.specs a")
            versions = [ version["href"] for version in versions ]
            for i in range(len(versions)):
                versions[i] = '/'.join(versions[i].split('/')[3:])
                technicalFileLinks.append(base_url + versions[i])
    print("finished processing")
            
            

models = []
series = []
prix = []
garanties = []
performances = []
vitesseMax = []
consommationUrbaine = []
consommationExtraUrbaine = []
volumeDeCoffre = []
nombredeCylindres = []
puissanceFiscale = []


techfile = technicalFileLinks[0]
page = getPageContent(techfile)
soup = BeautifulSoup(page, "lxml")
    
caracteristiques = soup.find_all("td")
price = soup.select("div.buttons div span")
#print("the price is ")
#print(price)
models.append(caracteristiques[1])
series.append(caracteristiques[3])
prix.append(price[0].text)
garanties.append(caracteristiques[7])
performances.append(caracteristiques[9])
vitesseMax.append(caracteristiques[21])
consommationUrbaine.append(caracteristiques[23])
consommationExtraUrbaine.append(caracteristiques[24])
volumeDeCoffre.append(caracteristiques[26])
nombredeCylindres.append(caracteristiques[29])
puissanceFiscale.append(caracteristiques[9])
print('the model is ' + models[0].text)
print('the series is ' + series[0].text)
print('the price is ' + prix[0].text)    
print('the garantie is ' + garanties[0].text)
print('the performance is ' + performances[0].text)
print('the vitesse max is ' + vitesseMax[0].text)
print('the consommation urbaine is ' + consommationUrbaine[0].text)
print('the consommation extra urbaine is ' + consommationExtraUrbaine[0].text)
print('the volume de coffre is ' + volumeDeCoffre[0].text)
print('the nombre de cylindres is ' + nombredeCylindres[0].text)
#print(puissanceFiscale)



