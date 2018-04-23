import urllib2
from bs4 import BeautifulSoup

CSV_DELIMITER = ";"
symbol_changes = []
keep_scraping = True
outfile = 'SymbolChanges.csv'

webpage = "https://www.nasdaq.com/markets/stocks/symbol-change-history.aspx"
page_query = "?page="
current_page = 1

while keep_scraping:

    query = webpage + page_query + str(current_page)
    symbol_page = urllib2.urlopen(query)
    soup = BeautifulSoup(symbol_page, "html.parser")

    table = soup.find('table', attrs={'class':'SymbolChangeList'})
    rows = table.find_all('tr')
    if "No records" in rows[1].get_text():
        keep_scraping = False
        continue

    for row in rows:
        elements = row.find_all('td')
        if elements == []:
            continue
        elements_unpacked = CSV_DELIMITER.join(map(lambda x: x.get_text().strip(), elements))
        symbol_changes.append(elements_unpacked)
        print(elements_unpacked)

    current_page += 1

with open(outfile, 'w+') as file:
    file.write("old"+CSV_DELIMITER+"new"+CSV_DELIMITER+"date\n")
    for line in symbol_changes:
        file.write(line)
        file.write("\n")