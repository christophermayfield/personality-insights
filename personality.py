import sys
import requests
import json
import operator
import twitter
import script as pi
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights



def analyze(handle):

	#The Twitter API credentials
	twitter_consumer_key = 'IneKk1d3i6O0lo5ZZbM4EEfK7'
	twitter_consumer_secret = 'gffvWRNmNF9ZwHm0XPNZ9SFb6JsA0d7jR64BxQSiz49ro3VtVh'
	twitter_access_token = '15281154-OuJBpU0ns2yhwhbOlMutCFLBBNDwP9d05PzUfzotO'
	twitter_access_secret = 'muYF4xiuTZJHb7b2SyPLFfrsfbymFa04j985ofWhBiBmx'

	#Invoking the Twitter API
	twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)

	#Retrieving the last 200 tweets from a user
	statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

	#Putting all 200 tweets into one large string called "text"
	text = ""
	for s in statuses:
	    if (s.lang =='en'):
    			text += s.text.encode('utf-8')

	#Analyzing the 200 tweets with the Watson PI API
	pi_result = PersonalityInsights(username=pi.u, password=pi.p).profile(text)

	#Returning the Watson PI API results
	return pi_result

#flattens the results and stores them in a dictionary.

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data

  #compare function compares two dictionaries(the user's and the celebrity's)
  def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data

  user_handle = "@imchrismayfield"
  celebrity_handle="@IBM"

  user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)


  #First, flatten the results from the Watson PI API
user = flatten(user_result)
celebrity = flatten(celebrity_result)

compared_results = compare(user, celebrity)


sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    print keys,
    print(user[keys]),
    print ('->'),
    print (celebrity[keys]),
    print ('->'),
    print (compared_results[keys])
