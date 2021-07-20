import requests, bs4
from tkinter import *
from tkinter.ttk import *

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }

# pass request to the site and return requests object.
def passRequest(address):   
    response = requests.get(address)
    try:
        response.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    return response

# get link tags (html "a" tags)
def getLinkTags(response):
    noStarchSoup = bs4.BeautifulSoup(response.text, features="html.parser") # make a beautifulSoup object to parse html codes.
    ultag = noStarchSoup.find('ul', {'class': 'c-listing__items'})
    divTags = ultag.find_all('div', {'class': 'c-product-box__title'})
    linkTags = []
    for divTag in divTags:
        linkTags.append(divTag.find('a', {'class': 'js-product-url'}))
    return linkTags

# get href attribute of each html "a" tag and store this hrefs in a file.
def storeHrefs(data):
    file = open('productsLink.txt', 'a', encoding='utf-8')
    for d in data:
        file.write('https://www.digikala.com' + d['href'] + '\n')
    file.close()

# main block of codes ----> gets the single page links of each product
# for pagenum in range(1, 278):
#     address = 'https://www.digikala.com/search/category-perfume/?pageno=' + str(pagenum) + '&sortby=4'
#     response = passRequest(address)
#     linkTags = getLinkTags(response)
#     storeHrefs(linkTags)

# for pagenum in range(1, 178):
#     address = 'https://www.digikala.com/search/category-pocket-perfumes/?pageno=' + str(pagenum) + '&sortby=4'
#     response = passRequest(address)
#     linkTags = getLinkTags(response)
#     storeHrefs(linkTags)


def start():
    # pages = 277
    # download = 0
    # while download < pages:
    #     address = 'https://www.digikala.com/search/category-perfume/?pageno=' + str(download+1) + '&sortby=4'
    #     response = passRequest(address)
    #     linkTags = getLinkTags(response)
    #     storeHrefs(linkTags)
        
    #     download+=1
    #     bar['value']+=(1/pages)*100
    #     percent.set(str(int((download/pages)*100))+"%")
    #     text.set(str(download)+"/"+str(pages)+" pack1 links downloaded")
    #     window.update()

    pages = 177
    download = 0
    while download < pages:
        address = 'https://www.digikala.com/search/category-pocket-perfumes/?pageno=' + str(download+1) + '&sortby=4'
        response = passRequest(address)
        linkTags = getLinkTags(response)
        storeHrefs(linkTags)
        
        download+=1
        bar['value']+=(1/pages)*100
        percent.set(str(int((download/pages)*100))+"%")
        text.set(str(download)+"/"+str(pages)+" pack2 links downloaded")
        window.update()


window = Tk()
percent = StringVar()
text = StringVar()
bar = Progressbar(window,orient=HORIZONTAL,length=600)
bar.pack(pady=10)
percentLabel = Label(window,textvariable=percent).pack()
taskLabel = Label(window,textvariable=text).pack()
button = Button(window,text="download",command=start).pack()
window.mainloop()