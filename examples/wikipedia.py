from table2csv import *

url = "http://en.wikipedia.org/wiki/List_of_apocalyptic_and_post-apocalyptic_fiction"
soup = SurLaTableSoup(url, css={"class": "wikitable"})
print soup.describe()

table = soup.extract_biggest_table()
records = table.astype('dict', link_columns=[3])
