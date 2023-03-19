import requests;
from unidecode import unidecode
from bs4 import BeautifulSoup
import re
import pandas as pd;

def scrape_table_element(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select_one(selector)
    return element.text if element else None

def format_header(string):
    raw_string = unidecode(string)
    pattern = '[A-Z][a-z]+'
    result = re.findall(pattern, raw_string)
    return result

def format_body(string):
    pattern = r"(\d+)º(\d{4})(\d+)([A-Za-z]+)"
    occurrences = re.findall(pattern, string)

    # percorrer as ocorrências e extrair o número, valor e animal em cada uma
    result = []
    for occurrence in occurrences:
        numero = int(occurrence[0])
        value = occurrence[1]
        group = occurrence[2]
        animal = occurrence[3]
        result.append((numero, value, group, animal))
    return result


url = 'https://www.resultadofacil.com.br/resultado-do-jogo-do-bicho/PB'
# pega a primeira tabela da página, que é o ultimo lancamento
selector = 'table'
element = scrape_table_element(url, selector)

tableHeader = element.strip().split(' ')[0]
tableBody = element.strip().split(' ')[1]

formatedHeader = format_header(tableHeader)
formatedBody = format_body(tableBody)

df = pd.DataFrame(formatedBody, columns=formatedHeader)
print(df)