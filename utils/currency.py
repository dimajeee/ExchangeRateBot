import requests
import xml.etree.ElementTree as ET

def get_currency_rate():
    """Получение курсов валют с cbr.ru в виде словаря."""
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    rates = {}
    for currency in root.findall('Valute'):
        char_code = currency.find('CharCode').text
        value = float(currency.find('Value').text.replace(',', '.'))
        if char_code in ['USD', 'EUR']:
            rates[char_code] = value

    return rates
