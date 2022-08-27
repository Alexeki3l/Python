"""
Obtiene datos de AliExpress y Amazon.
Nombre,precio,url,calificaiones y cantidad de valoraciones
"""


from bs4 import BeautifulSoup
import requests
import time
from requests_html import AsyncHTMLSession
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_items_by_name(name):

    """
    Obtiene los nombres, las clasificaciones, los precios, las imagenes y las url de los productos
    encontrados segun el criterio de busqueda. Este criterio sera el string que se pase por
    parametro 
    """

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language":"en",
    }
    tiempo_init = time.time()
    product_names   =[]
    ratings         =[]
    ratings_count   =[]
    prices          =[]
    product_urls    =[]
    images          =[]

    search_query = name.replace(" ","+")
    url_amazon = "https://www.amazon.com/s?k={0}".format(search_query)

    url_aliexpress = "https://es.aliexpress.com/wholesale?&SearchText={0}".format(search_query)

    # SCRAPER AMAZON
    """for i in range(1,20):
            
        print('Procesando {0}...'.format(url_amazon + '&page={0}'.format(i)))
        try:
            response = requests.get(url_amazon + '&page={0}'.format(i), headers=headers)
        except:
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
                
        resultados = soup.find_all('div', {'class':'s-result-item', 'data-component-type':'s-search-result'})
        cont = 1    
            # ITERAR EN CADA ARTICULO DE CADA PAGINA
        for result in resultados:
                    # product_name = result.h2.text
                    product_name = result.find('span', {'class':'a-text-normal'}).text 
                    product_url = result.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get('href')
                    product_url = "https://www.amazon.com" + product_url
                    try:
                        rating = result.find('i', {'class':'a-icon'}).text
                        rating_count = str(result.find_all('span', {'aria-label':True})[1].text)
                        
                        rating_count = rating_count.split(",")
                        
                        if len(rating_count)==2:
                            rating_count = int(rating_count[0] + rating_count[1])
                            
                        else:
                            rating_count = rating_count[0]
                            
                            if not len(rating_count.split(" "))>1:
                                rating_count = int(rating_count[0])
                                
                    except:            
                        rating = None
                        rating_count = None
                        
                    try:
                        price = (result.find('span',{'class':'a-offscreen'}).text)[1:]
                        image = result.find('img',{'class':'s-image'}).get('src')
                    except:   
                        continue

                    image = get_image(name,image, headers)

                    images.append(image)

                    product_url = 'https://www.amazon.com' + result.h2.a['href']
                    product_names.append(product_name)
                    ratings.append(rating)
                    ratings_count.append(rating_count)
                    prices.append(price)
                    product_urls.append(product_url) 
                     
                    print(cont,"---",product_name, price, rating, rating_count, product_url)
                    cont = cont + 1 
                    
             """         
    
    # SCRAPER ALIEXPRESS
    for i in range(1,3):
            
        print('Procesando {0}...'.format(url_aliexpress + '&page={0}'.format(i)))
        url = url_aliexpress + '&page={0}'.format(i)

        option = Options()
        option.headless = True

        #Craendo un driver para Firefox 
        driver = webdriver.Firefox(options=option)
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)

        #Haciendo scroll hasta el final de la pagina
        iter=1
        while True:
                scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
                Height=250*iter
                driver.execute_script("window.scrollTo(0, " + str(Height) + ");")
                if Height > scrollHeight:
                    print('Fin de pagina')
                    break
                time.sleep(1)
                iter+=1

        #Obtener el cuerpo de la pagina       
        body = driver.execute_script("return document.body")
        source = body.get_attribute('innerHTML') 

        #we iterate through the different albums with beautifulsoup and load the data into the flat file
        soup = BeautifulSoup(source, "html.parser")
        resultados = soup.find_all('a', {'class':'_3t7zg _2f4Ho'})

        contador = 1
        for resultado in resultados:
            try:
                product_name = resultado.find('h1', {'class':'_18_85'}).text
            except:
                print("Error al obtener el nombre")  

            try:  
                product_url = "https:" + resultado.get('href')
            except:
                print("Error al obtener la URL")  
                
            try:
                price = resultado.find('div',{'class':'mGXnE _37W_B'}).text
                price = float(price.replace('US $',' '))
            except:
                print("Error al obtener el precio") 

            try:
                rating = resultado.find('span',{'class':'eXPaM'}).text
                rating = float(rating)
                
            except:
                print("No tiene clasificacion")  
                rating = 0

            try:
                navegador = webdriver.Firefox(options=option)
                navegador.get(product_url)
                body_page = navegador.execute_script("return document.body")
                source = body_page.get_attribute('innerHTML') 

                sopa = BeautifulSoup(source, "html.parser")
                # ----------------------------------------------------------
                rating_count = sopa.find('span',{'class':'product-reviewer-reviews black-link'}).text
                rating_count = rating_count.split(" ")    
                rating_count = rating_count[0]
            except:
                print("Nadie a dado su criterio sobre este producto")
                rating_count = 0

            try:
                imagen = "http:" + resultado.find('img',{'class':'_1RtJV product-img'}).get('src')
            except:
                print("Error. No se obtuvo la imagen del producto")

            image = get_image(name,imagen, headers)

            images.append(image)
            product_names.append(product_name)
            ratings.append(rating)
            ratings_count.append(rating_count)
            prices.append(price)
            product_urls.append(product_url) 
            
            print(contador,"---",product_name,"--",product_url,"--",price,"--",rating,"--",rating_count)
            
            navegador.close()
            if contador == 3:
                print("Salir")
                break

            contador +=1
        #finally we close the file and the driver
        # file1.close()

        driver.close()

    print("Busqueda Terminada...")     
    return product_names, ratings, ratings_count, prices, product_urls, images

# ----Los sgtes metodos son para el proyecto de Django en el que se estaba trabajando

# Se encarga de obtener la URL de cada nombre que se le pase
def get_link(name):
    search_query = name.replace(" ","+")
    url = "https://www.amazon.com/s?k={0}".format(search_query)
    return url


# Se encarga de descargar las imagenes y guardarlas en la carpeta 'media'
def get_image(name, url_image, headers):
    
    index = name.replace(' ','_')

    # Obtengo la imagen de dicha url_image  
    imagen = requests.get(url_image, headers).content
    # Obtengo el mismo nombre de la imagen de la URL para descargarla con el mismo nombre
    name = url_image.split('/')
    name = name[-1]
    name = name[:-4]
    # Obtengo la ruta del projecto para guardar las imagenes
    ruta = os.path.dirname(__file__)
    ruta = ruta.split("\scraper_app")
    ruta = ruta[0]
    ruta = os.path.join(ruta, 'media')
    ruta = ruta + "/" + index
    print(ruta)
    # Creo una carpeta en caso de no existir en dicha ruta para guardar las imagenes.
    if not os.path.exists(ruta):
        os.mkdir(ruta)
        fullname = ruta + "/" + name
        open(fullname +'.jpg', 'wb').write(imagen)
        print('descargando:{}.jpg'.format(name))
    else:
        list_archivos = os.listdir(ruta)
        if name in list_archivos:
            print("Ya existe este archivo")
        else:
            fullname = ruta + "/" + name
    
            open(fullname +'.jpg', 'wb').write(imagen)
            print('descargando:{}.jpg'.format(name))

    # Retorno la ruta de la imagen apartir de la carpeta creada con nombre del Item para DJANGO la encuentre
    return index + "/" + "{}.jpg".format(name)


get_items_by_name("core i9")