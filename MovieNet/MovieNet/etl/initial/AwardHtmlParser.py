#Assumes the html has awards listed alphabetically
def parseAwards(soup):
	years_and_headers = soup.find_all('dt')
	headers = getHeaders(soup)
	awardDict = {}
	i = -1
	for elem in headers:
		awardDict[elem] = {}
	for elem in years_and_headers:
		if elem.find('b') and elem.find('b').string in headers:
			i += 1
		else:
			year = _strip_year(elem.find('a').string)
			rows = elem.find_next('table').find_all('tr')
			awardNames = [row.find('a').string for row in rows if 'valign' not in row.attrs]
			for award in awardNames:
				if award not in awardDict[headers[i]]:
					awardDict[headers[i]][award] = {}
				awardDict[headers[i]][award][year] = {}
			for row in rows:
				#current tag is the header for an award within a year
				if row.find('a') and row.find('a').string in awardNames:
					awardName = row.find('a').string
					continue
				#it is a special award (not including these)
				elif 'special' in awardName.lower() and 'award' in awardName.lower():
					continue
				#have an actual nomination
				else:
					won = False
					if row.find('td').string == '*':
						won = True
					first_a = row.find('a')
					if first_a.parent.name != 'i' and first_a.string:
						name = tuple(first_a.string.split(','))
					elif first_a.find_next('a', text=True):
						name = tuple(first_a.find_next('a').string.split(','))
					else:
						name = None
					#if this award does not contain a movie of any kind then skip it
					if not row.find('i') or (not row.find('i').find('a') and not row.find('i').string):
						continue;
					elif row.find('i').string:
						movie = row.find('i').string
					else:
						movie = row.find('i').find('a').string
					if awardName not in awardDict[headers[i]]:
						awardDict[headers[i]][awardName] = {}
						awardDict[headers[i]][awardName][year] = {}
					awardDict[headers[i]][awardName][year][(name, movie)] = won
					won = False
	return awardDict
			
def getHeaders(soup):
	a = soup.find_all('dt')
	return [header.find('b').string for header in a if header.find('b') != None]		
		
def _strip_year(year_string):
	if year_string and ' ' in year_string:
		year = year_string[:year_string.index(' ')]
		return year.strip()
	else:
		return year_string.strip()