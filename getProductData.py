import requests, bs4, csv, re
from tkinter import *
from tkinter.ttk import *


def getProductsLinkAsList():
    productLinksList = []
    file = open('productsLink.txt', 'r', encoding='utf-8')
    productLinks = file.read()
    file.close()
    productLinksList = productLinks.split('\n')
    return productLinksList

def getDigikalaTitle(soup):
    digikalaTitle = ''
    try:
        digikalaTitleTag = soup.find('section', {'class': 'c-product__info'}).find('h1', {'class': 'c-product__title'})
    except:
        return digikalaTitle

    try:
        digikalaTitle = digikalaTitleTag.text.strip()
    except:
        digikalaTitle = ''
    return digikalaTitle

def setType(digikalaTitle):
    type = ''
    typeRegex = re.compile(r'(^.*)مردانه|(^.*)زنانه')
    typeList = typeRegex.findall(digikalaTitle)
    for elem in typeList:
        type = ''.join(elem)
    return type

def setBrand(digikalaTitle):
    brand = ''
    brandRegex = re.compile(r'مردانه(.*)مدل|زنانه(.*)مدل')
    brandList = brandRegex.findall(digikalaTitle)
    for elem in brandList:
        brand = ''.join(elem)
    
    if brand == '':
        brandRegex = re.compile(r'عطر جیبی زنانه(.*)مدل|عطر جیبی مردانه(.*)مدل')
        brandList = brandRegex.findall(digikalaTitle)
        for elem in brandList:
            brand = ''.join(elem)

    if brand == '': 
        brandRegex = re.compile(r'(\S+\s\S+\s)مدل')
        brandList = brandRegex.findall(digikalaTitle)
        try:
            brandList.remove('زنانه')
            brandList.remove('مردانه')
            brandList.remove('پرفیوم')
        except:
            pass
        for elem in brandList:
            brand = ''.join(elem)

    if brand == '':
        brandRegex = re.compile(r'زنانه(.*)حجم|مردانه(.*)حجم')
        brandList = brandRegex.findall(digikalaTitle)
        for elem in brandList:
            brand = ''.join(elem)
    return brand

def setModel(digikalaTitle):
    model = ''
    modelRegex = re.compile(r'مدل(.*)حجم')
    modelList = modelRegex.findall(digikalaTitle)
    for elem in modelList:
        model = ''.join(elem)
    
    if model == '':
        modelRegex = re.compile(r'زنانه(.*)حجم|مردانه(.*)حجم')
        modelList = modelRegex.findall(digikalaTitle)
        for elem in modelList:
            model = ''.join(elem)
    return model

def setPrice(soup):
    pricePureTag = soup.find('div', {'class': 'c-product__seller-price-pure js-price-value'})
    pricePreviousTag = soup.find('div', {'class': 'c-product__seller-price-prev js-rrp-price'})
    if pricePureTag == None:
        price = ''
        discountPrice = ''
    elif pricePreviousTag != None:
        price = pricePreviousTag.text.strip()
        discountPrice = pricePureTag.text.strip()
    elif pricePureTag != None and pricePreviousTag == None:
        price = pricePureTag.text.strip()
        discountPrice = ''
    return price, discountPrice

def search(soup, columnTitle):
    resultParamValue = ''
    try:
        liparams = soup.find('div', {'id': 'params'}).find_all('li')
    except:
        return resultParamValue
    for li in liparams:
        try:
            paramKey = li.find('div', {'class': 'c-params__list-key'}).find('span').text
        except:
            paramKey = ''

        try:
            paramValue = li.find('div', {'class': 'c-params__list-value'}).find('span')
        except:
            paramValue = ''

        if re.search(columnTitle, paramKey):
            paramValueList = re.split(',| و |،', paramValue.text.strip())
            resultParamValue = '، '.join([str(elem).strip() for elem in paramValueList])

    return resultParamValue    
    

def storeResultAsTXT(paramsList):
    file = open('productDatasa.txt', 'a', encoding='utf8')
    for param in paramsList:
        file.write(str(param).strip() + ';')
    file.write('\n')
    file.close()

def storeResultAsCSV(paramsList):
    csvFile = open('productsData.csv', 'a', encoding='utf8')
    csvWriter = csv.writer(csvFile, delimiter=';')
    csvWriter.writerow(paramsList)
    csvFile.close()

# paramsTitle = ['برند', 'مدل', 'عنوان سایت دیجی کالا', 'جنسیت', 'حجم', 'نت آغازین', 'نت میانی', 'نت پایانی', 'سال معرفی', 'نوع رایحه', 'ساختار رایحه', 'غلظت', 'ماندگاری', 'کشور سازنده', 'قمیت', 'قیمت با تخفیف']

productLinksList = getProductsLinkAsList()

def main():
    # settings for progressbar
    productlink = 9971
    download = 0
    # end settings
    
    while download < productlink:
        model = ''
        brand = ''
        type = ''
        sex, volume, firstnote, middlenote, lastnote, introYear, fragranceType, fragranceStruct, density, durability, country = '', '', '', '', '', '', '', '', '', '', ''

        response = requests.get(productLinksList[download])
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        
        digikalaTitle = getDigikalaTitle(soup)

        brand = setBrand(digikalaTitle)
        type = setType(digikalaTitle)
        model = setModel(digikalaTitle)

        # set "price" and "discountPrice" variables
        price, discountPrice = setPrice(soup)
        
        # set variables (ul->li)
        sex = search(soup, 'مناسب برای')
        volume = search(soup, 'حجم')
        firstnote = search(soup, 'نت آغازی')
        middlenote = search(soup, 'نت میانی')
        lastnote = search(soup, 'نت پایانی')
        introYear = search(soup, 'سال معرفی')
        fragranceType = search(soup, 'نوع رایحه')
        fragranceStruct = search(soup, 'ساختار رایحه')
        density = search(soup, 'غلظت')
        durability = search(soup, 'ماندگاری')
        country = search(soup, 'کشور مبدا برند')

        # set all variable in a List
        paramsList = [brand, model, type, digikalaTitle, sex, volume, firstnote, middlenote, lastnote, introYear, fragranceType, fragranceStruct, density, durability, country, price, discountPrice]

        # store data in file
        if brand.strip() != '' or model.strip() != '':
            storeResultAsTXT(paramsList)
            # storeResultAsCSV(paramsList)

        # settings for progressbar
        bar['value']+=(1/productlink)*100
        percent.set(str(int(((download+1)/productlink)*100))+"%")
        text.set(str(download+1)+"/"+str(productlink)+" product downloaded")
        download+=1
        window.update()


# settings for progressbar
window = Tk()
percent = StringVar()
text = StringVar()
bar = Progressbar(window,orient=HORIZONTAL,length=600)
bar.pack(pady=10)
percentLabel = Label(window,textvariable=percent).pack()
taskLabel = Label(window,textvariable=text).pack()
button = Button(window,text="download",command=main).pack()
window.mainloop()