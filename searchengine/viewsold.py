from django.shortcuts import render

# Create your views here.

from bs4 import BeautifulSoup
from bs4.element import AttributeValueWithCharsetSubstitution
import requests
import lxml


class website():
    def __init__(self, name, searchLink, link, tag, chosenClass, scrapingType):
        self.name = name
        self.searchLink = searchLink
        self.link = link
        self.tag = tag
        self.chosenClass = chosenClass
        self.scrapingStyle = scrapingType
    
    def checkIfHasLink(self, argument):
        if ( (argument.startswith("http:/") == True) or (argument.startswith("https:/") == True) ):
            return(argument)
        else: 
            return(self.link + argument)

    def scraping(self, argument):
        # "~°Ñ°~" is placed where the search term should be, so we can replace it with the argument here
        self.searchLink = self.searchLink.replace("~°Ñ°~", argument)

        r = requests.get(self.searchLink)
        soup = BeautifulSoup(r.content, "lxml")

        #These are the 2 lists we are returning
        content = []
        
        if (self.scrapingStyle == "basic") :
            #Getting the headlines and links, the most compatible way I found, since it can find the link in an element's children
            #Why so? because using the iteration 2 times, once for heads and once for links was slower and more network intensive
            #Also, neither the .get("href") and ["href"] methods were working, just kinda made my own
            allHtml = soup.find_all(f"{self.tag}", class_= f"{self.chosenClass}")

            for x in allHtml:
                head = (x.get_text()).strip()
                x = (str(x)).split('"')

                #This is surely not the best way to do it, but ERIC just kept refusing to index href so I had to substract 1, rather than add 1 like the rest
                if self.name != "ERIC":
                    index = x.index(" href=") + 1
                else:
                    for element in x:
                        if element.find(" href="): index = x.index(element) - 1

                link = (self.checkIfHasLink(x[index]))

                content.append([head, link])

                            
        #Another way to get everything, more efficient but its not always supported
        elif (self.scrapingStyle == "select"):
            for x in range(15):
                cssSelector = (self.tag).replace("~°Ñ°~", f"{x}") #Setting up the selector 
                selectedHtml = soup.select(cssSelector) 
                if type(cssSelector) == str:
                    for x in selectedHtml:
                        content.append( [(x.get_text()).strip(), (self.checkIfHasLink(x.get("href")))] ) 

        return(content)

scholar = website( "Scholar", "https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q=~°Ñ°~&btnG=", "",
"h3", "gs_rt", "basic")

researchgate = website("ResearchGate","https://www.researchgate.net/search/publication?q=~°Ñ°~", "https://www.researchgate.net/", "div",
"nova-legacy-e-text nova-legacy-e-text--size-l nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-v-publication-item__title",
"basic")

basesearch = website("Bielefeld Academic Search Engine", "https://www.base-search.net/Search/Results?lookfor=~°Ñ°~&name=&oaboost=1&newsearch=1&refid=dcbasen",
"https://www.base-search.net/" ,"a" ,"bold", "basic")

eric = website("ERIC", "https://eric.ed.gov/?q=~°Ñ°~", "https://eric.ed.gov/?q=investigator!&id=", "div", "r_t", "basic")
    
pubmed = website("Pubmed", "https://pubmed.ncbi.nlm.nih.gov/?term=~°Ñ°~", "https://pubmed.ncbi.nlm.nih.gov/",
"article.full-docsum:nth-child(~°Ñ°~) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)", "", "select")

elsevier = website("Elsevier", "https://www.elsevier.com/search-results?query=~°Ñ°~", "https://www.elsevier.com/", 
"article.search-result:nth-child(~°Ñ°~) > header:nth-child(1) > h2:nth-child(1) > a", "", "select")

libgen = website("Libgen", "https://libgen.is/scimag/?q=~°Ñ°~",
"https://libgen.is", ".catalog > tbody:nth-child(2) > tr:nth-child(~°Ñ°~) > td:nth-child(2) > p:nth-child(1) > a:nth-child(1)", "", "select")

listOfPages = [eric, scholar]
fullListOfPages = [pubmed, scholar, eric, libgen, basesearch, researchgate, elsevier]

def homepage(request):
    content = []
    placeholder = []
    for y in range(0, 9): 
        placeholder.append(["Placeholder text", "Placeholder link"])

    x = 0
    for webpage in fullListOfPages:
        content.append( {"name" : webpage.name, "combination" : placeholder} )
        x += 1

    print(len(placeholder) , len(content) )


    return render(request, "meetups/index.html", {"content": content})


def searchResults(request, cue_slug):
    searchTerm = "australia"
    content = []
    slugga = [{"slug": f"{searchTerm}"}]

    for webpage in listOfPages:

        returns = webpage.scraping(searchTerm)
        thisWebpage = {"name" : webpage.name, "combination" : returns}
        content.append( thisWebpage )


    return render(request, "meetups/index.html", {"content": content, "slugga" : slugga})