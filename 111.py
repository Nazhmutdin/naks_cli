import requests
from lxml import html

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://naks.ru',
    'Referer': 'https://naks.ru/assp/reestrperson2/index.php?PAGEN_1=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = 'PAGEN_1=1&arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D=%EA%F3%EC%E0%F0&arrFilter_pf%5Bshifr_ac%5D=&arrFilter_pf%5Buroven_ac%5D=&arrFilter_pf%5Bnum_ac%5D=&arrFilter_ff%5BCODE%5D=&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'

# response = requests.post('https://naks.ru/registry/personal/', data=data, headers=headers)

# tree = html.fromstring(response.text)

aa = "GDKkwme wkednef"

print(aa.split(","))

# print(tree.xpath("//table[@class='tabl']//tr[@bgcolor]"))

# with open("page.html", "w", encoding="windows-1251") as file:
#     file.write(response.text)