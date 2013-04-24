import IMDBParser
import csv
import urllib
import re

sql_file = open("IMDBRatingSQL.sql", 'w')
sql_file.write("ALTER TABLE Movie ADD IMDBRating NUMBER(2, 1)")
f = open("dvd_data_csv.txt")
#So that we start at real data, read through first line which contains headers
f.readline()
reader = csv.reader(f)
for line in reader:
	dvd_name = line[0]
	year = None
	match = re.match("(?P<movie>.+)[ ]*\(?P<paren>(.+\))", dvd_name)
	if match:
		dvd_name = match.group('movie')
		paren = match.group('paren')
		if re.match("19[0-9]{2}|20(0[0-9]|1[0-3])", paren):
			year = paren
	url = 'http://www.imdb.com/find?q=' + urllib.parse.quote_plus(dvd_name) + 's=all'
	query = IMDBParser.ParseQuery(url, 1)
	if query_result == None:
		continue
	page_link = query_result[1]
	rating = IMDBParser.GetRating(page_link)
	sql_file.write("UPDATE Movie SET IMDBRating=" + float(rating) + " WHERE Name=" + dvd_name + "\n")

f.close()
sql_file.close()
	

