###############################################
######       FINAL PROJECT              #######
######       Elisa Warner               #######
######          SI 506                  #######
###############################################

(1) General Description of what the project does:
	The project takes in a query term, then searches for articles on it in both twitter and the NYT article search. The program then makes an instance of each of the results. It will also sort articles by the number of words in the article and the tweets by the number of times retweeted.

	There are two classes: Tweet, for the twitter object, and Article, for the NYT article object. Under them are two methods:

	Tweet Class:
	(a) a string method that returns the tweet, when it was posted, and how many times it was retweeted.
	(b) a countletters method that returns a dictionary of each letter and how many times it appeared in the tweet.

	Article Class:
	(a) a string method that returns when the article was printed and on what page it was printed.
	(b) a translate method that returns the article title changed by a Caesar Ciper (where a=b)

(2) What you should expect to happen when you run the project
	You should first see a reference to the cache. Next, you will see the top NYT articles sorted by word count and the top Tweets sorted by number of time retweeted. Then, you will see an invocation of the translate() method for 10 NYT Articles and the Top 5 most common letters for 15 Tweets, using the countletters() method. Lastly you will see an invocation of 10 test methods.


(3) Modules imported:
    (a) requests
    (b) json
    (c) tweepy
    (d) twitter_info
    (e) unittest
    (f) string

(4) Additional modules you need to install with pip to run the project
    (a) You must pipinstall requests
    (b) You must pipinstall json
    (c) You must pipinstall tweepy
    (d) You must have the twitter_info file in the same folder as this program (included in attachments)
    (e) unittest should be default included, but if not you may have to pipinstall unittest
    (f) string should be default included, but if not you may have to pipinstall string

(5) All filenames included in submission, and what each one represents:
	(a) Cool_data.csv - comma-separate value output from the program. Gives you top 5 most comon words for a search term in the NYT and Twitter, respectively
	(b) elisawa_final.py - code file to execute in terminal
	(c) final_cache.json - cache file to hold internet data
	(d) README.txt - how to run files
	(e) READMEq9.PNG - a visual of the output you should get
	(f) READMEq9_2.PNG - a continued visual of the output you should get
	(g) twitter_info.py - a python file containing private twitter key data

(5) Exactly how to run the project
	Go to the command prompt/terminal window and type in: python elisawa_final.py
	Make sure to run it on python 2.7

	If you want to change a query search, go to line 159 and change the query_word to a different string based on your query interests.

	You can hide the sorted articles/tweets text by putting '#' at the beginning of each line between lines 183-192

	You can hide the additional method output by putting '#' at the beginning of each line between lines 201-209

(6) How to access cached data
	Data is cached under a file called final_cache.json. You can open the cache file with notepad or other text editor software.

(7) How to get live data: e.g.
	The only query term in the cache is "Trump". Try other famous people such as "Obama", "Biden", or "Bush" as a test to access articles and tweets that are not in the cache yet.

(8) Approximate lines of code on which each of the project requirements is achieved:

PROJECT REQUIREMENTS:
    (a) Getting data from 2 different sources (data access functions)
		NYT Data: 127-139
		Twitter Data: 142-153
    (b) caching your data in a file: 
		save to cache: 119-124
		open cache: 99-108
		caching pattern: 111-117
    (c) At least one non-trivial sorting operation:177, 184, 208, 243, 252, 112
    (d) 2 class definitons:
		Tweet: 36-44
		Article: 61-67
    (e) 3 instance variables per definition:
		Tweet: 38-44
		Article: 63-67
    (f) 2 methods per class: 
		Tweet: 46-47, 49-56
		Article: 69-71, 73-79
    (g) Invocation of at least 1 instance:
	Create the instance: 173-174
	Invoke the instsance: 183-185,190-192, 201-203, 206-209
    (h) Data processing/computation: 215-222, 225-232
    (i) Human-readable output: see file "Cool_data.csv", included
	215-257
    (j) 8 test methods: 276-320
	Methods invoked at 320

(9) Image: see file READMEq9.PNG
	Output: see Cool_data.csv

(10) Why I chose this project:
	I chose this project because I wanted to learn how to pull Twitter data, and this option included Twitter.

(11) Citation of any code that is not mine in the project files:
	def params_unique_combination : 111-117
	citation: Jaclyn Cohen, Lecture 14

	translate method: 76-78
	citation:https://www.tutorialspoint.com/python/string_translate.htm

(12) Anything else I want you guys to know:
	Thanks for the great semester! Sorry if I was ever too active/annoying :D

	Oh, and also, I sorted the NYT articles by word count instead of relevance/number of hits and I sorted Tweets by number of times retweeted instead of number of times favorited. 