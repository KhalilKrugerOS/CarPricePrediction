

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
content = getPageContent("https://www.automobile.tn/fr/neuf")
soup = BeautifulSoup(content, 'lxml')
constructors_list = soup.select("div.container a")

for i in range(len(constructors_list)):
    constructors.append(constructors_list[i]['href'])
    #adding the names that exist in href
# /fr/neuf/constructor ==> constructor

#print(constructors[0].split('/')[3])
constructors = [ cons.split('/')[3] for cons in constructors  ]
#print(constructors)
links = [ base_url + constructor for constructor in constructors ]  # extracting links
#print(links)
#print(links[1:2])
links2 = links[1:2]
##print(links)
for link in links2:
    page2 = getPageContent(link)
    sleep(1)
    souplink = BeautifulSoup(page2, "lxml")
    print("the link is " + link)
    print(souplink.select("div.articles div.versions-item a"))
    articles_list = souplink.select("div.articles div.versions-item a")
    for i in range(len(articles_list)):
        technicalFileLinks.append(articles_list[i]['href'])
   
    technicalFileLinks = [ base_url + '/'.join(technicalfilelink.split('/')[3:]) for technicalfilelink in technicalFileLinks ]
    print(technicalFileLinks)
    for technicalfilelink in technicalFileLinks:
        soup4 = BeautifulSoup(getPageContent(technicalfilelink), "lxml")
        if  soup4.select("div#specs.technical-details") == []:
            #print("the technical file of the car" + technicalfilelink + " is on another page")
            technicalFileLinks.remove(base_url + '/'.join(technicalfilelink.split('/')[5:]))
            versions = soup4.select("td.specs a")
            versions = [ version["href"] for version in versions ]
            for i in range(len(versions)):
                versions[i] = '/'.join(versions[i].split('/')[3:])
                technicalFileLinks.append(base_url + versions[i])
    #print("finished processing")
            
#print(technicalFileLinks)

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
page3 = getPageContent(techfile)
soup3 = BeautifulSoup(page3, "lxml")

caracteristiques = soup3.select("dev#specs.technical-details td")
model = soup3.select("h3.page-title")
version = soup3.select("h3.page-title span")
price = soup3.select("div.version-details div span")
#print(model)
#print(version)
#print(price)
##print("the price is ")
##print(price)
#print(caracteristiques)
models.append(model[0].text)
series.append(version[0].text)
prix.append(price[0].text)
garanties.append(caracteristiques[7])
performances.append(caracteristiques[9])
vitesseMax.append(caracteristiques[21])
consommationUrbaine.append(caracteristiques[23])
consommationExtraUrbaine.append(caracteristiques[24])
volumeDeCoffre.append(caracteristiques[26])
nombredeCylindres.append(caracteristiques[29])
puissanceFiscale.append(caracteristiques[9])
# #print('the model is ' + model[0].text)
# #print('the series is ' + series[0])
# #print('the price is ' + prix[0])    
# #print('the garantie is ' + garanties[0].text)
# #print('the performance is ' + performances[0].text)
# #print('the vitesse max is ' + vitesseMax[0].text)
# #print('the consommation urbaine is ' + consommationUrbaine[0].text)
# #print('the consommation extra urbaine is ' + consommationExtraUrbaine[0].text)
# #print('the volume de coffre is ' + volumeDeCoffre[0].text)
# #print('the nombre de cylindres is ' + nombredeCylindres[0].text)
# ##print(puissanceFiscale)



