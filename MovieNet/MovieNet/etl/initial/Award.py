import json
import pprint
import AwardHtmlParser
from bs4 import BeautifulSoup
from movieapp.models import Movie
from movieapp.models import Actor
from movieapp.models import Director
from datetime import datetime

def _getId(name, awardType, year=None):

	if awardType == "movie":
		# If it is a movie, then check if the movie is a substring of some query. Then find the shortest result of all matches
		matches = Movie.objects.filter(title__istartswith=name, year__exact=year)
		if not matches:
			match = None
		else:
			bestLength = float("Inf")
			for result in matches:
				result_length = len(result.title)
				if result_length < bestLength:
					match_id = result.id
					match = result.title
					bestLength = result_length
	else:
		if awardType == "actor":
			match = Actor.objects.filter(name__iexact=name)
		else:
			match = Director.objects.filter(name__iexact=name)
		if match:
			match_id = match[0].id
	
	if not match:
		return None
	else:
		return match_id

if __name__ == '__main__':
	start = datetime.now()
	ILLEGAL_AWARDS = ["SPECIAL AWARD", "SPECIAL ACHIEVEMENT AWARD"]
	actorHeaders = ["ACTOR -- LEADING ROLE", "ACTRESS -- LEADING ROLE", \
					"ACTOR -- SUPPORTING ROLE", "ACTRESS -- SUPPORTING ROLE"]
	directorHeaders = ["DIRECTING", "ASSISTANT DIRECTOR"]
	
	with open("sources/awards.txt") as award_file:
		soup = BeautifulSoup(award_file.read())
	awards = AwardHtmlParser.parseAwards(soup)
	with open("awardStruct.txt", 'w') as awardStructFile:
		pprint.pprint(awards, awardStructFile, indent=4)
	
	AWARD_INDEX = 0
	MOVIE_INDEX = 1
	ACTOR_INDEX = 2
	DIR_INDEX = 3
	
	json_dict = [[], [], [], []]
	count = [1, 1, 1, 1]
	for awardHeader, awardNameDict in awards.items():
		for awardName, yearDict in awardNameDict.items():
			if awardName in ILLEGAL_AWARDS:
				continue
			for year, nominationDict in yearDict.items():
				if '/' in year:
					year = str(int(year[:year.index('/')]) + 1)
				json_dict[AWARD_INDEX].append({'model':'movieapp.award', 'pk':count[AWARD_INDEX], 'fields':{
							'name':awardName, 'year':int(year)}})
				count[AWARD_INDEX] += 1
				nominationsSeen = []
				for nomination, won in nominationDict.items():
					names = nomination[0]
					movieId = _getId(nomination[1], "movie", int(year))
					if not movieId:
						continue
					if ((not names or (awardHeader not in actorHeaders and awardHeader not in directorHeaders)) 
							and movieId not in nominationsSeen):
						json_dict[MOVIE_INDEX].append({'model':'movieapp.movienomination', 'pk':count[MOVIE_INDEX], 
									'fields':{'movie':movieId, 'award':count[AWARD_INDEX]-1, 'won':won}})
						count[MOVIE_INDEX] += 1
					else:
						for name in names:
							if awardHeader in actorHeaders:
								actorId = _getId(name, "actor")
								if actorId:
									json_dict[ACTOR_INDEX].append({'model':'movieapp.actornomination', 
											'pk':count[ACTOR_INDEX], 'fields':{'movie':movieId, 'actor':actorId, 
											'award':count[AWARD_INDEX]-1, 'won':won}})
									count[ACTOR_INDEX] += 1
							elif awardHeader in directorHeaders:
								directorId = _getId(name, "director")
								if directorId:
									json_dict[DIR_INDEX].append({'model':'movieapp.directornomination', 
											'pk':count[DIR_INDEX], 'fields':{'movie':movieId, 'director':directorId, 
											'award':count[AWARD_INDEX]-1, 'won':won}})
									count[DIR_INDEX] += 1
					nominationsSeen.append(movieId)
	
	with open("../../../movieapp/fixtures/award.json", 'w') as json_file:
		json.dump(json_dict[AWARD_INDEX], json_file, indent=4)
	with open("../../../movieapp/fixtures/movieAward.json", 'w') as json_file:
		json.dump(json_dict[MOVIE_INDEX], json_file, indent=4)
	with open("../../../movieapp/fixtures/actorAward.json", 'w') as json_file:
		json.dump(json_dict[ACTOR_INDEX], json_file, indent=4)
	with open("../../../movieapp/fixtures/directorAward.json", 'w') as json_file:
		json.dump(json_dict[DIR_INDEX], json_file, indent=4)
	
	end = datetime.now()
	print end-start
					