from time import sleep
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

# Función para convertir los precios a números
def get_numero(precio):
    return int(precio.replace('$', '').replace(',', ''))


#url_pag = 'https://www.espaciourbano.com/resumen_barrio_arriendos.asp?pCiudad=10000&pTipoInmueble=1&nCiudad=Medellin%20Zona%201%20-%20Centro&nBarrio=Manrique'
#url_pag = 'https://www.espaciourbano.com/resumen_barrio_arriendos.asp?pCiudad=10000&pTipoInmueble=1&nCiudad=Medellin%20Zona%201%20-%20Centro&nBarrio=Villa%20Hermosa'
#url_pag = 'https://www.espaciourbano.com/resumen_barrio_arriendos.asp?pCiudad=10000&pTipoInmueble=1&nCiudad=Medellin%20Zona%201%20-%20Centro&nBarrio=Campo%20Valdes'
s = Service('D:/My/Work/WebScrap/chromedriver.exe')
driver = webdriver.Chrome(service=s)

def searchItems(url_pag,casas):
    
    try:
        driver.get(url_pag)

        anuncios = driver.find_elements(By.CLASS_NAME,'row')    

        for anuncio in anuncios:
            precio_element = anuncio.find_elements(By.XPATH,'.//h3[contains(text(), "Precio")]')
            if len(precio_element) > 0:
                precio = precio_element[0].text.replace('Precio ', '')
                link_element = anuncio.find_elements(By.XPATH,'.//a[@class="btn btn-primary"]')
                if len(link_element) > 0:
                    link = link_element[0].get_attribute('href')
                    casas.append({'precio':precio,'link':link})

        pagination = driver.find_element(By.CLASS_NAME,'pagination')

        # Buscar los enlaces dentro del elemento de paginación
        enlaces = pagination.find_elements(By.TAG_NAME,'a')

        #extraer el texto y la URL
        
        texto = enlaces[1].text
        url = enlaces[2].get_attribute('href')        

        num = re.findall('\d+', texto)
        n1 = int(num[0])
        n2 = int(num[1])        

        if n1 != n2:                     
            searchItems(str(url),casas)      
                    
    except Exception as e:
       print('finalizó', e)



casas = []

searchItems(url_pag,casas)

casas_ordenadas = sorted(casas, key=lambda x: get_numero(x['precio']))

casas_baratas = []

for casa in casas_ordenadas:
    print(casa)

print('Inmuebles vistos: ',len(casas_ordenadas))

for casa in casas_ordenadas[:5]:
    casas_baratas.append(casa)

for casa in casas_baratas:
    print(casa)

driver.quit()