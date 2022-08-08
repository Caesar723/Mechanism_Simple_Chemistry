from bs4 import BeautifulSoup
import requests

URL_number="https://periodictableguide.com/protons-neutrons-and-electrons-of-elements/"
URL_radius="http://www.crystalmaker.com/support/tutorials/atomic-radii/index.html"

headers = {
 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
}

def getPage(url:str)->BeautifulSoup:
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text,"html.parser")

def atomNumberFilter(page:BeautifulSoup)->dict:#return the element dict
    result={}
    figure=page.find("figure",class_="wp-block-table aligncenter is-style-regular")
    
    tbody=figure.find("tbody")
    getIter=tbody.findAll("tr").__iter__()
    next(getIter)
    for tr in getIter:
        getTopic=tr.findAll("td")[1]
        getStrong=getTopic.findAll("strong")

        atomDict={"Proton":getStrong[1].string,
                "Neutron":getStrong[2].string,
                "Electron":getStrong[3].string}
        result[getStrong[0].string]=atomDict
    return result
        

def atomRadiusFilter(page:BeautifulSoup,dic:dict)->None:
    getTable=page.find("table")
    getItems=getTable.find_all("tr",bgcolor="#FFFFFF")
    lenItem=len(getItems)
    
    for i,ele in enumerate(dic):
        if i<lenItem:
            Content=getItems[i].find_all("td")
            
            dic[ele]["symbol"]=Content[1].string
            if Content[2].string:
                dic[ele]["atomic_radius"]=Content[2].string
            if Content[3].string:
                dic[ele]["ionic_radius"]=Content[3].string

def checkStrOrNum(get:str):
    return get if ord(get[0])<=ord("9") and ord(get[0])>=ord("0") else '"{}"'.format(get)
    
def makePyFile(ele:dict) ->None:# put code into file
    with open("element.py","w") as f:
            for element in ele:
                getVariable="\n\t".join(["{}={}".format(i,checkStrOrNum(ele[element][i])) for i in ele[element]])
                f.write(
                """
class {}(Element):
\t{}
\n
                """.format(element,
                            getVariable
                )
            )

def main():
    number_page=getPage(URL_number)
    getDict=atomNumberFilter(number_page)
    #makePyFile(getDict)
    #print(getDict)
    radius_page=getPage(URL_radius)
    atomRadiusFilter(radius_page,getDict)
    makePyFile(getDict)
    #print(getDict)

   
    
    
    

if __name__=="__main__":
    main()
