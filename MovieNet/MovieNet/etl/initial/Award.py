from bs4 import BeautifulSoup
import json
import AwardHtmlParser
from movieapp.models import Movie
from movieapp.models import Actor
from movieapp.models import Director

def _getId(name, awardType, idHash, year=None):
	if name in idHash:
		return (idHash[name], idHash)
	
	if awardType != "movie" and ' ' in name:
		index = name.index(' ')
		name = name[(index + 1):] + ', ' + name[:index]
	if awardType == "movie":
		# If it is a movie, then check if the movie is a substring of some query. Then find the shortest result of all matches
		matches = Movie.objects.filter(title__istartswith=name, year__exact=year)
		if not matches:
			match = None
		else:
			bestLength = float("Inf")
			for result in matches:
				result_length = len(result.name)
				if result_length < bestLength:
					movieId = result.id
					match = result.name
					bestLength = result_length
	else:
		if awardType == 'actor':
			match = Actor.objects.filter(name__iexact=name)
		else:
			match = Director.objects.filter(name__iexact=name)
		if match:
			movieId = match.id
	
	if not match:
		idHash[name] = None
		return (None, idHash)
	else:
		return (movieId, idHash)


actorHeaders = ["ACTOR -- LEADING ROLE", "ACTRESS -- LEADING ROLE", \
				"ACTOR -- SUPPORTING ROLE", "ACTRESS -- SUPPORTING ROLE"]
directorHeaders = ["DIRECTING", "ASSISTANT DIRECTOR"]

soup = BeautifulSoup(open("awards.txt").read())
awards = AwardHtmlParser.parseAwards(soup)

award_json = open("../../movieapp/fixtures/award.json", 'w')
movie_award_json = open("../../movieapp/fixtures/movieAward.json", 'w')
actor_award_json = open("../../movieapp/fixtures/actorAward.json", 'w')
director_award_json = open("../../movieapp/fixtures/directorAward.json", 'w')

awardStruct = []
movieStruct = []
actorStruct = []
directorStruct = []

awardCount = 0
movieCount = 0
actorCount = 0
directorCount = 0

idHash = {}
for awardHeader, awardNameDict in awards.items():
	for awardName, yearDict in awardNameDict.items():
		years = sorted(list(yearDict.keys()))
		for year in years:
			nominationDict = yearDict[year]
			if '/' in year:
				year = str(int(year[:year.index('/')]) + 1)
			awardStruct.append({'model':'myapp.award', 'pk':awardCount, 'fields':{
						'name':awardName, 'year':year}})
			awardCount += 1
			for nomination, won in nominationDict.items():
				names = nomination[0]
				movieId, idHash = _getId(nomination[1], "movie", idHash, year)
				if not movieId:
					continue
				if not names or (awardHeader not in actorHeaders and awardHeader not in directorHeaders):
					movieStruct.append({'model':'myapp.movienomination', 'pk':movieCount, 'fields':{
								'mid':movieId, 'name':awardName, 'year':year, 'won':won}})
					movieCount += 1
				else:
					for name in names:
						if awardHeader in actorHeaders:
							actorId, idHash = _getId(name, "actor", idHash)
							if actorId:
								actorStruct.append({'model':'myapp.actornomination', 'pk':actorCount, 'fields':{
											'mid':movieId, 'aid':actorId, 'name':awardName, 'year':year, 'won':won}})
								actorCount += 1
						elif awardHeader in directorHeaders:
							directorId, idHash = _getId(name, "director", idHash)
							if directorId:
								directorStruct.append({'model':'myapp.directornomination', 'pk':actorCount, 'fields':{
											'mid':movieId, 'aid':directorId, 'name':awardName, 'year':year, 'won':won}})
								directorCount += 1

award_json.write(json.dumps(awardStruct, indent=4))
movie_award_json.write(json.dumps(movieStruct, indent=4))
actor_award_json.write(json.dumps(actorStruct, indent=4))
director_award_json.write(json.dumps(directorStruct, indent=4))

award_json.close()
movie_award_json.close()
actor_award_json.close()
director_award_json.close()
					