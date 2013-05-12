import urllib
from bs4 import BeautifulSoup

def parse_query(url, limit):
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
		topResults.append((words, page_link, img_link))
		if i == limit:
			break
	return topResults
	
def parse_page(url):
	soup = _getSoup(url)
	movie_dict = {}
	try:
		movie_dict['title'] = soup.find('span', itemprop="name").string
		movie_dict['year'] = int(movie_dict['title'].find_next('span').find('a').string)
		movie_dict['genres'] = [genre.string.strip() for genre in soup.find('div', itemprop="genre").find_all('a')]
		movie_dict['rating'] = float(soup.find('span', itemprop="ratingValue").string)
		movie_dict['actors'] = _getActors(soup)
		movie_dict['directors'] = _getDirectors(soup)
		return movie_dict
	except AttributeError:
		return None
	
	
def _getDirectors(soup):
	directors = soup.find('div', class_='txt-block', itemprop="director")
	director_list = []
	if directors:
		director_list = [a.string for a in directors.find_all('a', text=True)]
	return director_list


def _getActors(soup):
	cast_table = soup.find('table', class_="cast_list")
	actors = []
	if cast_table:
		actors = cast_table.find_all('span', class_="itemprop", itemprop="name", text=True)
		actors = [a.string for a in actors]
	return actors
	
	
def GetRating(url):
	soup = _getSoup(url)
	return soup.find('span', itemprop="ratingValue").string

def _getSoup(url):
	f = urllib.urlopen(url)
	html = f.read()
	with open('cast_html.html', 'w') as cast_file:
		cast_file.write(html)
	return BeautifulSoup(html)