import urllib.request
from bs4 import BeautifulSoup

def ParseQuery(url, limit):
	print(url)
	soup = _getSoup(url)
	relevant_titles = soup.find('a', {'name':"tt"})
	if relevant_titles == None:
		return None
	results = relevant_titles.find_next('table').find_all('tr')
	topResults = []
	i = 0
	for result in results:
		page_link = 'www.imdb.com' + result.find('a')['href']
		img_link = result.find('img')['src']
		words = ''.join([word for word in result.find_all(text=True) if word != ' '])
		topResults.append((word, page_link, img_link))
		if i == limit:
			break
	return topResults
	
def ParsePage(url):
	soup = _getSoup(url)
	name = soup.find('span', itemprop="name").string
	year = name.find_next('span').find('a').string
	genres = [genre.string.strip() for genre in soup.find('div', itemprop="genre").find_all('a')]
	rating = soup.find('span', itemprop="ratingValue").string
	
def GetRating(url):
	soup = _getSoup(url)
	return soup.find('span', itemprop="ratingValue").string

def _getSoup(url):
	f = urllib.request.urlopen(url)
	return BeautifulSoup(f.read())