
from time import sleep
from bs4 import BeautifulSoup
from openpyxl.workbook import Workbook
import requests
import pandas as pd
import os

"""URLs validas de prueba"""

# url = 'https://www.amazon.com/SteelSeries-Teclado-mec%C3%A1nico-compacto-juegos/dp/B07TGPN6P2?psc=1&pd_rd_w=0sbx9&content-id=amzn1.sym.c9b3a448-7c3c-4399-ac60-2bdc98844f72&pf_rd_p=c9b3a448-7c3c-4399-ac60-2bdc98844f72&pf_rd_r=179TVCBXXEB4ZVSJAP0S&pd_rd_wg=vnZF6&pd_rd_r=822c40fb-158e-4506-a5b8-d3a26ae9ac07&ref_=sspa_dk_rhf_detail_pt_sub_3&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTVZBMjNHV09ZNTZEJmVuY3J5cHRlZElkPUEwMDA4MzYxMUUzMk1TNTA0NEJaViZlbmNyeXB0ZWRBZElkPUEwMjMzOTY2VUlKNjlRWE9KWTY0JndpZGdldE5hbWU9c3BfcmhmX2RldGFpbCZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

# url = 'https://www.amazon.com/-/es/T-fal-Utensilios-cocina-Titanium-Antiadherente/dp/B00TQJWF1I/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.b97b4e6b-b418-46fa-99e0-99e05eefed1c&crid=N2BWR2PWI4FA&keywords=kitchen+essentials&pd_rd_r=df9d9625-6e5b-47c9-990b-d17b907e23e8&pd_rd_w=JyhgQ&pd_rd_wg=RIrOn&pf_rd_p=b97b4e6b-b418-46fa-99e0-99e05eefed1c&pf_rd_r=9JNRXRK3T3XZ4CMJT5JJ&qid=1658504582&sprefix=kitchen+%2Caps%2C285&sr=8-1'

# url = 'https://www.amazon.com/-/es/Corsair-iCUE-Lighting-Node-PRO/dp/B01MYDTC2C/ref=sr_1_13?keywords=strip+lighting&pd_rd_r=0cec3040-cd35-4c6e-9891-7adf903adb7c&pd_rd_w=YgqrA&pd_rd_wg=9tl6K&pf_rd_p=7738c60e-a1c7-4678-9812-5d82959d511c&pf_rd_r=HF2P3FFFCRHFHNA33XJD&qid=1658852911&sr=8-13'

url = 'https://www.amazon.com/-/es/Phanteks-NEON-Digital-Strip-PH-NELEDKT_M1/dp/B07XLPH8WW/ref=sr_1_26?keywords=strip+lighting&pd_rd_r=0cec3040-cd35-4c6e-9891-7adf903adb7c&pd_rd_w=YgqrA&pd_rd_wg=9tl6K&pf_rd_p=7738c60e-a1c7-4678-9812-5d82959d511c&pf_rd_r=HF2P3FFFCRHFHNA33XJD&qid=1658853051&sr=8-26'

# url = 'https://www.amazon.com/-/es/Delta-Organizador-juguetes-compartimentos-almacenamiento/dp/B074PY2ZGS/ref=sr_1_45?__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=toys&pd_rd_r=fb51e56b-bb34-4ac4-9644-03fde2eb32d9&pd_rd_w=swSI8&pd_rd_wg=fY6to&pf_rd_p=fffb6f02-0490-4c1e-a204-518c7cef06f6&pf_rd_r=4C82VSXCKHETER3WY0CA&qid=1658585554&sr=8-45'


def get_link_data(url):

    """Obtiene el nombre, precio y la imagen de un Articulo en Amazon
        por una URL que se le pase por parametro"""

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language":"en",
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
   
    """Obtener el nombre del Articulo"""
    # Busca el nombre por la etiqueta 'producTitle'
    name = soup.select_one(selector="#productTitle").getText()
    # ELimina los espacios en blanco antes y despues de la cadena contenida en la variable 'name'
    name = name.strip()

    """Obtener el precio del Articulo"""
    # Busca todas las etiquetas 'span' que tenga en este caso una 
    # clase que tenga el nombre 'a-offscreen' y de ellas obtengo la primera
    price = soup.find_all("span", "a-offscreen")[0]
    price = str(price)
    price = price[29:]
    price = float(price[:-7])

    """Obtener la imagen del Articulo"""
    # Busca todas las etiquetas "img" que tenga una clase con ese nombre y 
    # ahi la direccion de la imagen que esta en "src". Esto devuelve la direccion de la imagen
    imagen = soup.find("img", class_="a-dynamic-image").get("src")
    imagen = requests.get(imagen, headers).content

    ruta = os.path.dirname(os.path.abspath(__file__))
    fullname = ruta + "/" + name
   
    open(fullname +'.jpg', 'wb').write(imagen)
    print('descargando:{}.jpg'.format(name))

    return name, price

search = input("¿Que articulos quiere buscar?-->")

def get_items(search):

    """
    Obtiene los nombres, las clasificaciones, los precios y las url de los productos
    encontrados segun el criterio de busqueda. Este criterio sera el string que se pase por
    parametro 
    """

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language":"en",
    }

    search_query = search.replace(" ","+")
    url = "https://www.amazon.com/s?k={0}".format(search_query)

    product_names=[]
    ratings=[]
    ratings_count=[]
    prices=[]
    product_urls=[]

    # BUSCA EN 10 PAGINAS
    for i in range(1,11):
        print('Procesando {0}...'.format(url + '&page={0}'.format(i)))
        response = requests.get(url + '&page={0}'.format(i), headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        resultados = soup.find_all('div', {'class':'s-result-item', 'data-component-type':'s-search-result'})
        
        # ITERAR EN CADA ARTICULO DE CADA PAGINA
        for result in resultados:
            # product_name = result.h2.text
            
            product_name = result.find('span', {'class':'a-text-normal'}).text 
            
            try:
                rating = result.find('i', {'class':'a-icon'}).text
                rating_count = result.find_all('span', {'aria-label':True})[1].text
                
            except AttributeError:
                continue

            try:
                price = (result.find('span',{'class':'a-offscreen'}).text)[1:]
                
                price = float(price)
                
                product_url = 'https://www.amazon.com' + result.h2.a['href']
                product_names.append(product_name)
                ratings.append(rating)
                ratings_count.append(rating_count)
                prices.append(price)
                product_urls.append(product_url) 
                
            except AttributeError:
                continue
        
    sleep(1.5)
    # GUARDAR LOS RESULTADOS EN UNA HOJA EXCEL
    data = {
            'Nombres de Productos':product_names,
            'Ratings':ratings,
            'rating count':ratings_count,
            'Prices':prices,
            'URL Producto':product_urls
            }
    df = pd.DataFrame(data=data)
    df.to_excel('{}.xlsx'.format(search_query), sheet_name='sheet1', index=False)

get_items(search)
    


