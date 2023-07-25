import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import datetime


def validate_date(date_text):
    try:
        res = datetime.date.fromisoformat(date_text).strftime('%d/%m/%Y')
        if res is None:
            print("Incorrect data format, should be YYYY-MM-DD")
            exit(1)
        return res
    except ValueError:
        print("Incorrect data")
        exit(1)


def validate_charcode(charcode_text):
    codes = ['AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR', 'KZT', 'CAD',
             'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 'UAH', 'CZK', 'SEK',
             'CHF', 'ZAR', 'KRW', 'JPY']
    if charcode_text not in codes:
        print("Wrong ISO code")
        exit(1)


def parse_args():
    request_date = ""
    request_code = ""
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--date':
            if i < len(sys.argv) - 1:
                request_date = validate_date(sys.argv[i + 1])
            else:
                print("date is undefined")
                exit(1)
        if sys.argv[i] == '--code':
            if i < len(sys.argv) - 1:
                validate_charcode(sys.argv[i + 1])
                request_code = sys.argv[i + 1]
            else:
                print("ISO code is undefined")
                exit(1)
    if request_code == "" or request_date == "":
        print(f"Usage: {sys.argv[0]} (--date YYYY-MM-DD --code ISO 4217)")
        exit(1)
    return request_date, request_code


def main(date, code):
    url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date
    document = urlopen(url)
    tree = ET.parse(document)
    root = tree.getroot()
    for child in root.findall('Valute'):
        charcode = child.find("CharCode").text
        value = child.find("Value").text
        name = child.find("Name").text
        if code == charcode:
            print(f"{charcode} ({name}): {value}")
            break


if __name__ == '__main__':
    date, code = parse_args()
    main(date, code)
