from table2csv import *

url = "http://lawandorder.wikia.com/wiki/Law_%26_Order_episodes"

soup = SurLaTableSoup(url, css={"class": "wikitable"})
print soup.describe()

table = soup.extract_biggest_table()
records = table.astype('dict',columns=[1,2,3,4], link_columns=[2])
