import requests
import json
import tweepy
import twitter_info
import unittest
from string import maketrans

"""
Class: Tweet
	Instance variables:
		self.retweet: number of times retweeted
		self.text: status message
		self.postday: day of the week posted
		self.postmonth: month posted
		self.postdate: day of the month posted
		self.postyear: year posted
	Methods:
		__str__: returns the status message, when it was posted, and how many times retweeted
		countletters: counts how many letters were in the tweet message

Class: Article
	Instance variables:
		self.word_count: how many words are in the article
		self.title: the main title of the article
		self.snippet: the snippet text from the article
		self.pub_date: the date published
		self.print_page: which page it was printed on in the print version of the NYT
	Methods:
		__str__: tells you the date that the article was printed and what page it was found on the print version
		translate: a fun method that translates the title with a Caesar cipher
"""

#Define a class representing a Tweet
#At least 3 instance variables
#2 methods
class Tweet(object):
	def __init__(self,data_dict):
		self.retweet = data_dict['retweet_count']
		self.text = data_dict['text'].encode('ascii','replace')
		datelist = data_dict['created_at'].split()
		self.postday = datelist[0]
		self.postmonth = datelist[1]
		self.postdate = datelist[2]
		self.postyear = datelist[-1]

	def __str__(self):
		return "The status message was: {} \n It was posted on {}, {} {} {} and was retweeted {} times.".format(self.text, self.postday, self.postmonth, self.postdate, self.postyear, self.retweet)

	def countletters(self):
		letter_dict = {}
		validletters = 'abcdefghijklmnopqrstuvwxyz'

		for letter in self.text:
			if letter.lower() in validletters:
				letter_dict[letter.lower()] = letter_dict.get(letter.lower(), 0) + 1
		return letter_dict

#Define a class representing a New York Times Article
#3 instance variables
#2 methods
class Article(object):
	def __init__(self,data_dict):
		self.word_count = data_dict['word_count']
		self.title = data_dict['headline']['main'].encode('ascii','replace')
		self.snippet = data_dict['snippet'].encode('ascii','replace')
		self.pub_date = data_dict['pub_date']
		self.print_page = data_dict['print_page']

	def __str__(self):
	#returns when the article was printed and on what page
		return "This article was printed on {} on page {} of the New York Times".format(self.pub_date,self.print_page)

	def translate(self):
	#fun method that translates title with Caesar Cipher
		#Translates the Main Title To Code
		beforetab = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		aftertab = 'bcdefghijklmnopqrstuvwxyzaBCDEFGHIJKLMNOPQRSTUVWXYZA'
		translatetab = maketrans(beforetab,aftertab)
		return self.title.translate(translatetab)

####################### CACHE INFO ##################################

#tweepy code for authorization
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

#NYT api key
api_key = 'f52e2c2277504115a2a590669e93c15e'

#open cache
CACHE_FNAME = "final_cache.json"

#open cache
try:
	fhnd = open(CACHE_FNAME,'r')      #opens cache if its there
	cache = fhnd.read()              #reads from cache
	CACHE_DICTION = json.loads(cache) #loads cache into a dictionary
	print "Loading cache data..."             #lets me know it found the cache (troubleshooting)
	fhnd.close()                      #close file
except:
    CACHE_DICTION = {}                #if there is no cache, creates a dictionary anyway
    print "No cache detected"       #troubleshooting (lets me know there is no cache)

#unique params
def params_unique_combination(baseurl, params_d, private_keys=["api-key"]):
    alphabetized_keys = sorted(params_d.keys())    #sorts the parameter keys so the each search for the same topic is identified
    res = []                                       #creates empty list for cache names
    for k in alphabetized_keys:
        if k not in private_keys:                  #if the parameter is not an api key then append it to the list res
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_" + "_".join(res)           #join res and the baseurl as a unique identifier

#save to cache
def write_cache(cache_dict):
    fhnd = open(CACHE_FNAME,'w')        #opens the cache file
    fhnd.write(json.dumps(cache_dict))  #dumps the dictionary into the file
    fhnd.close()                        #close the cache file
    return "Save successful"            #can print this for troubleshooting

#Request data
def requestnytdata(query):
	params_d = {'q':query, 'api-key':api_key}      # this is the dictionary for my query and the api key
	baseurl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'  # the baseurl to call up data
	key = params_unique_combination(baseurl,params_d)  #create a unique identifier

	if key not in CACHE_DICTION:
		try:
			response = requests.get(baseurl, params=params_d)      # request data from NYT api
			CACHE_DICTION[key] = json.loads(response.text)   #add output to the cache
			write_cache(CACHE_DICTION)           #save this to the cache file
		except:
			print "Could not request the data from New York Times. Please try again later."
			quit()


def requesttwitterdata(query):
	params_d = {'search':query}  #This is to tell the function for a unique identifier that I chose the method "user_timeline" with query as my query
	key = params_unique_combination('www.tweepy.org',params_d)  #call the function to create a unique identifier
	if key not in CACHE_DICTION:
		try:
			data = api.search(query)     #request the data
			CACHE_DICTION[key] = data           #add the data to CACHE_DICTION under the unique identifier
			write_cache(CACHE_DICTION)          #call up the function to save the data in the cache
			return "Twitter Data Saved to cache"
		except:
			print "Could not request the data from Twitter. Please try again later."
			quit()


##################### USER INPUT: QUERY TOPIC ###################################

# TYPE HERE TO CHANGE THE QUERY TOPIC
query_word = "Trump"

#################################################################################

# DON'T CHANGE: ACTUALLY CALL UP FUNCTIONS TO REQUEST DATA
requestnytdata(query_word)
requesttwitterdata(query_word)

#create a list of Article instances and a list of tweet instances
NYTparams = {'q':query_word}
Twitterparams = {'search':query_word}
NYTbase = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
Twitterbase = 'www.tweepy.org'

NYTinstance_list = [Article(a) for a in CACHE_DICTION[params_unique_combination(NYTbase,NYTparams)]['response']['docs']]
Twitterinstance_list = [Tweet(b) for b in CACHE_DICTION[params_unique_combination(Twitterbase,Twitterparams)]['statuses']]

#sort instances by number of words
sorted_NYT_instances = sorted(NYTinstance_list, key = lambda x: x.word_count, reverse= True)

################## USER INPUT: SORTED ARTICLES/TWEETS ###########################

#HIDE THE THIS TEXT BY PUTTING '#' BEFORE EACH LINE

print "\nNYT ARTICLES SORTED BY NUMBER OF WORDS:"
for i in range(len(sorted_NYT_instances)):
	print "({}) {} : {}".format(str(i+1),sorted_NYT_instances[i].word_count, sorted_NYT_instances[i].title)

#sort Tweets by favs
sorted_Twitter_instances = sorted(Twitterinstance_list, key = lambda x: x.retweet, reverse = True)

print "\nTWEETS SORTED BY NUMBER OF TIMES RETWEETED:"
for i in range(len(sorted_Twitter_instances)):
	print "({}) {} : {}".format(str(i+1),sorted_Twitter_instances[i].retweet, sorted_Twitter_instances[i].text)

#################################################################################

################### USER INPUT: USE ADDITIONAL METHODS #######################

#HIDE THE METHODS BY PUTTING '#' BEFORE EACH LINE

# TEST THE TRANSLATE METHOD
print "\nTRANSLATE METHOD FOR NYT ARTICLE TITLES:"
for i in range(len(sorted_NYT_instances)):
	print str(i), sorted_NYT_instances[i].translate()

# TEST THE COUNTLETTERS METHOD
print "\nCOUNTLETTERS METHOD: TOP 5 MOST COMMON LETTERS FOR EACH TWEET"
for i in range(len(sorted_Twitter_instances)):
	letter_keys = sorted(sorted_Twitter_instances[i].countletters().keys(), key = lambda x: sorted_Twitter_instances[i].countletters()[x], reverse=True)
	print 'Tweet {}: {}'.format(str(i+1), ','.join(letter_keys[0:5]))

##############################################################################

################# DO SOMETHING COOL ########################
#counts how many words in each tweet instance
def coolTwitterdata(instance_list):
	textdict = {} #dictionary to keep the word counts

	for inst in instance_list:
		for word in inst.text.split():
			cleanword = word.strip('.,?').lower()
			textdict[cleanword] = textdict.get(cleanword,0) + 1 #uses the get method so you can add new entries in or add to the old entries
	return textdict

#counts how many words in each snippet instance
def coolNYTdata(instance_list):
	snippetdict = {} #dictionary to keep the word counts

	for inst in instance_list:
		for word in inst.snippet.split():
			cleanword = word.strip('.,?@').lower()
			snippetdict[cleanword] = snippetdict.get(cleanword,0) + 1 #uses the get method so you can add new entries in or add to the old entries
	return snippetdict

#save the data to a csv file
def savetofile(title1,cool_data_dict1,title2,cool_data_dict2):
	path = "Cool_data.csv"
	file = open(path,'w')
	header_list = ['word','count']

	#NYT DATA
	file.write(title1 + '\n' + ','.join(header_list) + '\n')
	#sorting the keys so that we have a list of the most common words in descending order
	sortedkeys1 = sorted(cool_data_dict1.keys(), key = lambda x: cool_data_dict1[x], reverse=True)

	for key in sortedkeys1[0:5]:
		file.write(key + ',' + str(cool_data_dict1[key]) + '\n')


	#Twitter DATA
	file.write('\n\n' + title2 + '\n' + ','.join(header_list) + '\n')
	#sorting the keys so that we have a list of the most common words in descending order
	sortedkeys2 = sorted(cool_data_dict2.keys(), key = lambda x: cool_data_dict2[x], reverse=True)

	for key in sortedkeys2[0:5]:
		file.write(key + ',' + str(cool_data_dict2[key]) + '\n')

	file.close()

#create headers
NYTtitle = "TOP 5 MOST COMMON WORDS FOR SEARCH TERM %s IN NYT ARTICLE SEARCH" % (query_word)
Twittertitle = "TOP 5 MOST COMMON WORDS FOR SEARCH TERM %s IN TWITTER SEARCH" % (query_word)

#call up the function to make the cool data and save it
savetofile(NYTtitle,coolNYTdata(NYTinstance_list),Twittertitle,coolTwitterdata(Twitterinstance_list))

########################################## TESTS ######################################################
print "\n************************************************************************************************\n"

false = False
true = True
null = None
testdict = {"type_of_material": "News", "blog": [], "news_desk": "National", "lead_paragraph": "Thursday\u2019s courtroom hearing could turn out to be the final one in a yearslong case that garnered outsize national attention during the 2016 presidential campaign.", "headline": {"main": "Judge Signals He Will Approve Trump University Settlement Despite a Challenge", "print_headline": "Judge Signals He\u2019ll Approve Trump University Settlement Despite a Challenge"}, "abstract": null, "print_page": 13, "word_count": 940, "_id": "58dd93d97c459f24986d78bd", "snippet": "Thursday\u2019s courtroom hearing could turn out to be the final one in a yearslong case that garnered outsize national attention during the 2016 presidential campaign....", "source": "The New York Times", "slideshow_credits": null, "web_url": "https://www.nytimes.com/2017/03/30/us/judge-signals-he-will-approve-trump-university-settlement.html", "multimedia": [{"subtype": "thumbnail", "url": "images/2017/03/31/us/31trumpuniversity-sub/31trumpuniversity-sub-thumbStandard.jpg", "rank": 0, "height": 75, "width": 75, "legacy": {"thumbnailheight": 75, "thumbnail": "images/2017/03/31/us/31trumpuniversity-sub/31trumpuniversity-sub-thumbStandard.jpg", "thumbnailwidth": 75}, "type": "image"}, {"subtype": "xlarge", "url": "images/2017/03/31/us/31trumpuniversity-sub/31trumpuniversity-sub-articleLarge.jpg", "rank": 0, "height": 399, "width": 600, "legacy": {"xlargewidth": 600, "xlarge": "images/2017/03/31/us/31trumpuniversity-sub/31trumpuniversity-sub-articleLarge.jpg", "xlargeheight": 399}, "type": "image"}, {"subtype": "wide", "url": "images/2017/03/31/us/31trumpuniversity-sub/31trumpuniversity-sub-thumbWide.jpg", "rank": 0, "height": 126, "width": 190, "legacy": {"wide": "images/2017/03/31/us/31trumpuniversity-sub/31trumpuniversity-sub-thumbWide.jpg", "widewidth": 190, "wideheight": 126}, "type": "image"}], "subsection_name": null, "keywords": [{"isMajor": "N", "value": "United States Politics and Government", "name": "subject", "rank": 1}, {"isMajor": "N", "value": "Suits and Litigation (Civil)", "name": "subject", "rank": 2}, {"isMajor": "N", "value": "Trump University", "name": "organizations", "rank": 3}, {"isMajor": "N", "value": "Curiel, Gonzalo P", "name": "persons", "rank": 4}], "byline": {"person": [{"organization": "", "role": "reported", "firstname": "Jennifer", "rank": 1, "lastname": "MEDINA"}, {"organization": "", "role": "reported", "firstname": "Steve", "rank": 2, "lastname": "EDER"}], "original": "By JENNIFER MEDINA and STEVE EDER"}, "document_type": "article", "pub_date": "2017-03-30T23:25:06+0000", "section_name": "U.S."}
testTweet = {"contributors": null, "truncated": false, "text": "RT @Hope012015: Trump contradicts State Department on Iran deal https://t.co/VAIoA7dvtu via @HuffPostPol", "is_quote_status": false, "in_reply_to_status_id": null, "id": 855178135255515136, "favorite_count": 0, "entities": {"symbols": [], "user_mentions": [{"id": 2988785197, "indices": [3, 14], "id_str": "2988785197", "screen_name": "Hope012015", "name": "Kenny_ex-GOP"}, {"id": 15458694, "indices": [92, 104], "id_str": "15458694", "screen_name": "HuffPostPol", "name": "HuffPost Politics"}], "hashtags": [], "urls": [{"url": "https://t.co/VAIoA7dvtu", "indices": [64, 87], "expanded_url": "http://www.huffingtonpost.com/entry/trump-state-department-iran_us_58f91827e4b00fa7de1295de?ncid=engmodushpmg00000004", "display_url": "huffingtonpost.com/entry/trump-st\u2026"}]}, "retweeted": false, "coordinates": null, "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", "in_reply_to_screen_name": null, "in_reply_to_user_id": null, "retweet_count": 2, "id_str": "855178135255515136", "favorited": false, "retweeted_status": {"contributors": null, "truncated": false, "text": "Trump contradicts State Department on Iran deal https://t.co/VAIoA7dvtu via @HuffPostPol", "is_quote_status": false, "in_reply_to_status_id": null, "id": 855177428414681088, "favorite_count": 5, "entities": {"symbols": [], "user_mentions": [{"id": 15458694, "indices": [76, 88], "id_str": "15458694", "screen_name": "HuffPostPol", "name": "HuffPost Politics"}], "hashtags": [], "urls": [{"url": "https://t.co/VAIoA7dvtu", "indices": [48, 71], "expanded_url": "http://www.huffingtonpost.com/entry/trump-state-department-iran_us_58f91827e4b00fa7de1295de?ncid=engmodushpmg00000004", "display_url": "huffingtonpost.com/entry/trump-st\u2026"}]}, "retweeted": false, "coordinates": null, "source": "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>", "in_reply_to_screen_name": null, "in_reply_to_user_id": null, "retweet_count": 2, "id_str": "855177428414681088", "favorited": false, "user": {"follow_request_sent": false, "has_extended_profile": false, "profile_use_background_image": false, "default_profile_image": false, "id": 2988785197, "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "verified": false, "translator_type": "none", "profile_text_color": "000000", "profile_image_url_https": "https://pbs.twimg.com/profile_images/560442794553008128/uSXjk-m9_normal.jpeg", "profile_sidebar_fill_color": "000000", "entities": {"description": {"urls": []}}, "followers_count": 31661, "profile_sidebar_border_color": "000000", "id_str": "2988785197", "profile_background_color": "000000", "listed_count": 113, "is_translation_enabled": false, "utc_offset": -18000, "statuses_count": 31134, "description": "Attorney at Law, #TheResistance , #NeverTrump U.S. Const'l Advocate, Independent, Former US Dept of Homeland Security, (fmr Agent), Nat'l Security, Humanitarian", "friends_count": 25492, "location": "Texas, USA", "profile_link_color": "DD2E44", "profile_image_url": "http://pbs.twimg.com/profile_images/560442794553008128/uSXjk-m9_normal.jpeg", "following": false, "geo_enabled": false, "profile_banner_url": "https://pbs.twimg.com/profile_banners/2988785197/1439664561", "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "screen_name": "Hope012015", "lang": "en", "profile_background_tile": false, "favourites_count": 43356, "name": "Kenny_ex-GOP", "notifications": false, "url": null, "created_at": "Sun Jan 18 15:50:54 +0000 2015", "contributors_enabled": false, "time_zone": "Central Time (US & Canada)", "protected": false, "default_profile": false, "is_translator": false}, "geo": null, "in_reply_to_user_id_str": null, "possibly_sensitive": false, "lang": "en", "created_at": "Thu Apr 20 21:52:42 +0000 2017", "in_reply_to_status_id_str": null, "place": null, "metadata": {"iso_language_code": "en", "result_type": "recent"}}, "user": {"follow_request_sent": false, "has_extended_profile": false, "profile_use_background_image": true, "default_profile_image": false, "id": 708236539353030656, "profile_background_image_url_https": null, "verified": false, "translator_type": "none", "profile_text_color": "333333", "profile_image_url_https": "https://pbs.twimg.com/profile_images/830386063210377217/IPOTHsnW_normal.jpg", "profile_sidebar_fill_color": "DDEEF6", "entities": {"description": {"urls": []}}, "followers_count": 4353, "profile_sidebar_border_color": "C0DEED", "id_str": "708236539353030656", "profile_background_color": "F5F8FA", "listed_count": 112, "is_translation_enabled": false, "utc_offset": null, "statuses_count": 75783, "description": "Activist/writer dealing in truth not fake Lover of music(esp. blues) voracious reader and my Lhasa Apso. No trolls/no lists #TheResistance #NotMyPresident", "friends_count": 4996, "location": "North Carolina, USA", "profile_link_color": "1DA1F2", "profile_image_url": "http://pbs.twimg.com/profile_images/830386063210377217/IPOTHsnW_normal.jpg", "following": false, "geo_enabled": true, "profile_banner_url": "https://pbs.twimg.com/profile_banners/708236539353030656/1459459206", "profile_background_image_url": null, "screen_name": "solusnan1", "lang": "en", "profile_background_tile": false, "favourites_count": 57068, "name": "Nance", "notifications": false, "url": null, "created_at": "Fri Mar 11 10:22:04 +0000 2016", "contributors_enabled": false, "time_zone": null, "protected": false, "default_profile": true, "is_translator": false}, "geo": null, "in_reply_to_user_id_str": null, "possibly_sensitive": false, "lang": "en", "created_at": "Thu Apr 20 21:55:30 +0000 2017", "in_reply_to_status_id_str": null, "place": null, "metadata": {"iso_language_code": "en", "result_type": "recent"}}


# Write your tests here. (at least 8)
class TestQuestions(unittest.TestCase):
	def test1(self):
		params_d = {'a':'b', 'c':'d'}
		baseurl = 'www.candycanes.com'
		self.assertEqual(params_unique_combination(baseurl,params_d),'www.candycanes.com_a-b_c-d', "testing instance variable self.query")

	def test2(self):
		a = Article(testdict)
		self.assertEqual(a.word_count, 940, "testing that self.result_num = 1 as default")

	def test3(self):
		a = Article(testdict)
		self.assertEqual(a.title, "Judge Signals He Will Approve Trump University Settlement Despite a Challenge", "testing that self.page = 0 when requested results = 10")
	
	def test4(self):
		a = Article(testdict)
		self.assertEqual(a.print_page, 13, "testing that self.page = 2 when requested results = 21") #0-9, 10-19, 20-29 [0,1,2]

	def test5(self):
		b = Tweet(testTweet)
		self.assertEqual(b.postday, 'Thu', "testing that self.page = 0 as default")

	def test6(self):
		b = Tweet(testTweet)
		self.assertEqual(b.postmonth, 'Apr', "testing unique identifier function")

	def test7(self):
		b = Tweet(testTweet)
		self.assertEqual(b.postdate,'20', "testing api_key is not included in unique identifier")

	def test8(self):
		b = Tweet(testTweet)
		self.assertEqual(b.postyear, '2017',"testing successful run of NYTimes API")

	def test9(self):
		a = Article(testdict)
		self.assertEqual(a.__str__(),"This article was printed on 2017-03-30T23:25:06+0000 on page 13 of the New York Times","testing the string method for Article")

	def test10(self):
		b = Tweet(testTweet)
		self.assertEqual(b.__str__(),"The status message was: RT @Hope012015: Trump contradicts State Department on Iran deal https://t.co/VAIoA7dvtu via @HuffPostPol \n It was posted on Thu, Apr 20 2017 and was retweeted 2 times.","testing the string method for Tweet")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
unittest.main(verbosity=2)