#!/usr/bin/python

import time
import datetime
import tweepy
import csv
from pymongo import MongoClient
import pymongo
import sys
import math
import re
import os
from collections import defaultdict
try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit
from bson.binary import Binary
import gzip
try:
    import cPickle as pickle
except ImportError:
    import pickle
import json
import io
import base64
import random

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
import id_list

stop_words = set([u'all', 'gt', 'go', 'follow', 'issues', 'votes', 'tx', 'tweet', 'obamacare', 'young', u'to', 'program', 'voted', u'under', 'women', 'town', u'very', 'every', u'yourselves', u'did', 'ryan', 'race', 'team', 'small', "i'll", 'says', 'leaders', 'ted', 'sign', 'video', 'pass', u'further', 'even', u'what', 'business', 'find', u'above', 'new', 'ever', 'public', 'dem', 'full', 'iran', 'never', u'here', 'let', 'address', u'hers', 'strong', 'change', 'great', 'potus', '30', 'action', "i'm", 'honor', 'via', 'love', 'campaign', 'win', 'county', 'put', '1st', 'use', u'from', 'usa', 'visit', 'bush', 'next', u'few', 'live', 'call', '6', 'black', u'themselves', u'until', 'today', u'more', 'share', 'must', u'me', 'high', 'join', 'mc', 'rights', u'this', 'work', 'mt', u'can', u'of', 'meet', u'my', 'history', 'give', 'tax', 'states', 'want', 'times', 'needs', 'end', 'breaking', '1', u'how', 'economy', 'w', 'may', 'stop', u'after', 'coming', u'such', 'law', 'man', u'a', 'remember', 'st', u'so', 'things', 'talk', 'help', 'office', "don't", u'over', 'years', u'through', 'committee', 'cuts', 'still', u'its', u'before', 'thank', 'la', 'better', 'policy', u'ours', 'bipartisan', 'texas', '2012', u'then', u'them', 'good', 'iowa', 'nation', u'they', u'not', u'now', 'discuss', u'nor', 'always', '--', 'boehner', u'each', 'everyone', u'doing', 'ed', 'energy', 'hard', 'year', u'our', 'event', 'special', u'out', u'rt', 'rep', 'since', 'looking', 're', 'health', '7', 'got', 'gov', 'gop', 'shows', 'working', 'city', 'million', 'free', 'members', 'ask', 'care', 'could', 'days', 'david', 'american', "today's", 'think', 'first', u'yourself', 'another', 'president', 'vote', 'open', 'tomorrow', "doesn't", 'story', 'service', 'top', u'their', '2', u'too', 'passed', 'white', 'john', 'speaking', 'statement', u'that', 'hillary', 'part', 'believe', u'herself', u'than', "here's", 'obama', '11', '10', '12', '15', 'future', u'were', u'and', 'tonight', 'talking', 'say', u'have', 'need', u'any', 'congrats', '-', 'take', u'which', 'sure', u'who', u'most', 'plan', 'america', u'why', u'don', 'proud', 'm', 'voting', 'show', 'bring', 'businesses', 'democrats', 'debate', 'one', 'state', u'should', u'only', 'going', 'candidates', '8', 'local', u'do', u'his', 'get', 'watch', 'dc', 'report', u'during', 'dr', u'him', 'h', 'morning', 'bad', u'she', 'ohio', u'where', 'learn', 'fair', 'national', 'see', 'college', u'are', 'sen', 'paul', 'best', 'said', 'reform', 'federal', 'away', 'please', '3', 'r', u'between', u'we', 'jobs', 'job', 'cut', 'joe', 'news', 'debt', 'come', u'both', 'c', 'last', 'country', 'taking', u'against', u's', 'senator', "can't", 'co', 'community', 'poll', 'speak', 'conference', "it's", 'create', 'political', u'been', 'mark', u'whom', 'much', 'meeting', 'pm', 'wants', 'life', 'families', 'romney', 'republicans', '2015', '2014', u'those', u'myself', 'save', 'look', u'these', 'means', 'bill', 'budget', 'governor', u'will', u'while', 'many', 'va', 'voters', u'is', 'speech', u'it', u'itself', 'dems', u'in', 'ready', u'if', 'pay', 'make', u'same', 'speaker', '9', 'party', 'day', 'week', 'yesterday', '000', "obama's", 'tune', 'keep', u'off', 'center', u'i', 'floor', 'well', u'the', u'yours', 'left', 'icymi', u'just', u'being', 'money', 'thanks', 'questions', 'world', 'yes', 'yet', 'republican', 'family', 'candidate', u'had', 'hall', 'barack', '4', u'has', 'real', 'around', 'government', 'read', 'big', 'game', 'know', 'press', 'amp', 'like', 'd', 'lost', 'continue', u't', 'night', 'security', 'making', u'because', 'deal', 'people', 'senate', 'twitter', u'some', 'back', 'oh', 'economic', 'election', 'home', u'ourselves', u'for', 'fox', u'does', 'cnn', 'leader', u'be', 'power', 'leadership', 'post', u'by', 'hearing', u'on', u'about', 'would', 'getting', u'theirs', 'scott', 'stand', 'act', u'or', u'own', 'clinton', u'into', 'washington', 'two', u'down', 'right', u'your', u'her', 'friends', 'support', u'there', 'long', 'fight', 'start', 'pa', "we're", 'way', 'house', 'forward', u'was', 'war', 'happy', 'media', u'himself', 'hr', u'but', 'hear', u'with', u'he', 'made', 'friday', u'up', 'us', 'tell', 'record', u'below', 'agree', u'am', 'mike', u'an', u'as', u'at', 'et', 'politics', 'check', u'again', u'no', u'when', 'insurance', 'rally', 'ny', u'other', '5', u'you', 'really', "you're", "'s", 'congress', 'students', 'welcome', "let's", 'important', 'chris', 'weekend', 'ago', 'lead', 'calls', 'u', 'time', u'having', u'once'])


class Logger(object):
    outs = [sys.stdout]

    def __init__(self, tag):
        self.tag = tag

    def stamp(self, message):
        return '[{}][{}]--{}\n'.format(self.tag, datetime.datetime.now(), message)

    def d(self, message):
        self.write(message)

    def write(self, message):
        for o in Logger.outs:
            o.write(self.stamp(message))

    def flush(self):
        pass

class Unigram_Classifier_DB:
    def __init__(self, url, db_name, affiliations):
        self.log = Logger("Unigram_Classifier_DB")
        self.tweet_filter_range = 50
        self.client = MongoClient(url)
        self.db = self.client[db_name]
        self.classifier_tweets = self.db['unigram_classifier_tweets']
        self.classifier_meta_event = self.db['unigram_classifier_meta_event']
        self.classifier_meta_term = self.db['unigram_classifier_meta_term']
        self.classifier_scores = self.db['unigram_scores']
        self.classifier_tweets_cache = defaultdict(list)
        self.classifier_meta_event_cache = {}
        self.classifier_meta_term_cache = {}
        self.classifier_meta_event_cache_count = {}
        self.classifier_meta_term_cache_count = {}
        self.affiliations = affiliations
        #tweets_dict = {}
        self.setup_index()

    def setup_index(self):
        classifier_tweets_index = [('tweet.tweet_id', pymongo.ASCENDING), ('event', pymongo.ASCENDING)]
        for affiliation in self.affiliations:
            classifier_tweets_index.append(('scores.'+affiliation, pymongo.ASCENDING))
        self.classifier_tweets.create_index(classifier_tweets_index)
        self.classifier_meta_event.create_index([('event', pymongo.ASCENDING), ('affiliation', pymongo.ASCENDING)])
        self.classifier_meta_term.create_index([('event', pymongo.ASCENDING), ('term', pymongo.ASCENDING), ('affiliation', pymongo.ASCENDING)])
        self.classifier_scores.create_index([('event', pymongo.ASCENDING), ('term', pymongo.ASCENDING), ('affiliation', pymongo.ASCENDING)])

    def clear(self):
        self.classifier_tweets.drop()
        self.classifier_meta_event.drop()
        self.classifier_meta_term.drop()
        #tweets_dict = {}

    def update_event_inc(self, event, user_id, affiliation):
        if event not in self.classifier_meta_event_cache:
            self.get_event_meta(event)
        if user_id not in self.classifier_meta_event_cache[event][affiliation]:
            self.classifier_meta_event_cache[event][affiliation].add(user_id)
            self.classifier_meta_event_cache_count[event][affiliation] += 1

    def update_term_inc(self, event, term, user_id, affiliation):
        if event not in self.classifier_meta_term_cache:
            self.get_term_meta(event, term)
        if (user_id, term) not in self.classifier_meta_term_cache[event][affiliation]:
            self.classifier_meta_term_cache[event][affiliation].add((user_id, term))
            if (event, term) not in self.classifier_meta_term_cache_count:
                self.classifier_meta_term_cache_count[(event, term)] = {affiliation:0 for affiliation in self.affiliations}
            self.classifier_meta_term_cache_count[(event, term)][affiliation] += 1

    def binary_to_obj(self, binary):
        x = io.BytesIO(binary)
        f = gzip.GzipFile(mode='r', fileobj=x)
        obj = pickle.load(f)
        f.close()
        x.close()
        return obj

    def obj_to_binary(self, obj):
        x = io.BytesIO()
        f = gzip.GzipFile(mode='wb', fileobj=x)
        pickle.dump(obj, f)
        f.close()
        binary = Binary(x.getvalue())
        x.close()
        return binary
    
    def get_event_meta(self, event):
        #event_cache {event: {affiliation: [user_ids]} } #event_cache_count {event: {affiliation: int}}
        if event in self.classifier_meta_event_cache:
            return self.classifier_meta_event_cache_count[event]
        data = {c['affiliation']:set(c['user_ids']) for c in self.classifier_meta_event.find({'event': event})}
        for affiliation in self.affiliations:
            if affiliation not in data:
                data[affiliation] = set()
        self.classifier_meta_event_cache[event] = data
        self.classifier_meta_event_cache_count[event] = {affiliation:len(user_ids) for affiliation, user_ids in data.items()}
        return self.get_event_meta(event)

    def get_term_meta(self, event, term):
        #event_cache {event: {affiliation: [user_id_term_pairs]} } #event_cache_count {(event,term): {affiliation: int}}
        if event in self.classifier_meta_term_cache:
            if (event,term) in self.classifier_meta_term_cache_count:
                return self.classifier_meta_term_cache_count[(event,term)]
            else:
                return {affiliation:0 for affiliation in self.affiliations}
        data = {c['affiliation']:self.binary_to_obj(c['user_id_term_pairs']) for c in self.classifier_meta_term.find({'event': event})}
        for affiliation in self.affiliations:
            if affiliation not in data:
                data[affiliation] = set()
        self.classifier_meta_term_cache[event] = data
        #setup classifier_meta_term_cache_count
        for affiliation, user_id_term_pairs in data.items():
            for user_id, term in user_id_term_pairs:
                if (event, term) not in self.classifier_meta_term_cache_count:
                    self.classifier_meta_term_cache_count[(event, term)] = {affiliation:0 for affiliation in self.affiliations}
                self.classifier_meta_term_cache_count[(event, term)][affiliation] += 1
        return self.get_term_meta(event, term)

    def store_tweet(self, tweet, event, scores, score_detail):
        assert len(scores) == len(self.affiliations)
        self.classifier_tweets_cache[event].append({'tweet': tweet, 'event': event, 'scores': scores, 'score_detail': score_detail})

    def flush_tweets(self):
        to_add_all = []
        to_remove_all = set()
        for c in list(self.classifier_tweets.find({'event': {'$in':list(self.classifier_tweets_cache.keys())}}, ['scores', 'event'])):
            self.classifier_tweets_cache[c['event']].append(c)
        self.log.d('flush tweets #events {}'.format(len(self.classifier_tweets_cache)))
        for event, tweets in self.classifier_tweets_cache.items():
            to_remove = set([x['_id'] for x in tweets if '_id' in x])
            to_add = {}
            for affiliation in self.affiliations:
                tweets.sort(key = lambda x: x['scores'][affiliation])
                to_remove.intersection_update([x['_id'] for x in tweets[self.tweet_filter_range:-self.tweet_filter_range] if '_id' in x])
                for x in tweets[0:self.tweet_filter_range] + tweets[-self.tweet_filter_range:]:
                    if '_id' not in x:
                        to_add[(x['event'], x['tweet']['tweet_id'])] = x
            to_add_all += list(to_add.values())
            to_remove_all.update(to_remove)
        if to_remove_all:
            self.log.d('remove tweets {}'.format(len(to_remove_all)))
            self.classifier_tweets.remove({'_id':{'$in':list(to_remove_all)}})
        if to_add_all:
            self.log.d('add tweets {}'.format(len(to_add_all)))
            self.classifier_tweets.insert_many(to_add_all)
        self.classifier_tweets_cache.clear()

    def flush_event_supplementary(self):
        group_stage = { '_id' : '$event', 'avg': { '$avg': "$count" }}
        for affiliation in self.affiliations:
        	group_stage[affiliation] = { '$sum': { '$cond': [ { '$eq': [ "$affiliation", affiliation ] }, "$count", 0 ] } }
            
        project_stage = {'event': '$_id', 'avg': 1}
        for affiliation in self.affiliations:
        	project_stage[affiliation] = 1

        pipline = [{'$match'  : {}},
            	   {'$project': {'event': 1, 'affiliation': 1, 'count': { '$size': '$user_ids' }}},
            	   {'$group' : group_stage},
            	   {'$project': project_stage},
            	   {'$out': 'unigram_classifier_meta_event_popularity' }
        	      ]
        self.classifier_meta_event.aggregate(pipline)
        self.log.d('complete flush_event_supplementary')

    def unigram_score(self, event, affiliation, term):
        event_counts = self.get_event_meta(event)
        term_counts = self.get_term_meta(event, term)
        assert len(term_counts) == 2
        term_count = term_counts[affiliation]
        other_term_count = sum([c for a,c in term_counts.items() if a != affiliation])
        other_event_count = sum([c for a,c in event_counts.items() if a != affiliation])
        other_portion = (float(other_term_count)+1)/(other_event_count+1)
        this_portion = (float(term_count)+1)/(event_counts[affiliation]+1)
        mp_score = this_portion * math.log(this_portion / other_portion)
        return mp_score

    def flush(self, insert=False, use_pickle=False):
        self.flush_tweets()
        if (use_pickle):
            self.log.d('flush using pickle')
            with gzip.GzipFile('classifier_meta_event.pgz', 'w+') as f:
                pickle.dump(self.classifier_meta_event_cache, f)
            with gzip.GzipFile('classifier_meta_term.pgz', 'w+') as f:
                pickle.dump(self.classifier_meta_term_cache, f)
            self.classifier_meta_event_cache.clear()
            self.classifier_meta_term_cache.clear()
            return
        self.log.d('flush event_meta {}'.format(len(self.classifier_meta_event_cache)))
        for event, data in self.classifier_meta_event_cache.items():
            for affiliation, user_ids in data.items():
                if user_ids:
                    if insert:
                        self.classifier_meta_event.insert({'event':event, 'affiliation':affiliation, 'user_ids':list(user_ids), 'count': len(user_ids)})
                    else:
                        self.classifier_meta_event.update_one({'event':event, 'affiliation':affiliation}, {"$set": {'user_ids':  list(user_ids), 'count': len(user_ids) }}, upsert=True)
        self.log.d('flush term_meta {}'.format(len(self.classifier_meta_term_cache)))
        for event, data in self.classifier_meta_term_cache.items():
            for affiliation, user_id_term_pairs in data.items():
                if user_id_term_pairs:
                    if insert:
                        #print("INSERTING")
                        self.classifier_meta_term.insert({'event':event, 'affiliation':affiliation,      'user_id_term_pairs':self.obj_to_binary(user_id_term_pairs)})
                    else:
                        #print("UPDATING")
                        self.classifier_meta_term.update_one({'event':event, 'affiliation':affiliation}, {"$set": {'user_id_term_pairs':  self.obj_to_binary(user_id_term_pairs)}}, upsert=True)

        
        self.log.d('flush unigram scores {}'.format(len(self.classifier_meta_term_cache)))
        already_done = set()
        for event, data in self.classifier_meta_term_cache.items():
            for affiliation, user_id_term_pairs in data.items():
                for user_id, term in user_id_term_pairs:
                    if (event, affiliation, term) not in already_done:
                        already_done.add((event, affiliation, term))
                        count = self.get_term_meta(event, term)[affiliation]
                        score = self.unigram_score(event, affiliation, term)
                        if insert:
                            self.classifier_scores.insert({'count': count, 'score': score, 'event':event, 'affiliation':affiliation, 'term':term})
                        else:    self.classifier_scores.update_one({'event':event,'affiliation':affiliation,'term':term}, {"$set": {'count': count, 'score': score}}, upsert=True)
                    
        self.classifier_meta_event_cache.clear()
        self.classifier_meta_term_cache.clear()
        self.flush_event_supplementary()

    def close(self):
        self.client.close()

class Unigram_Classifier:
    def __init__(self, db):
        self.db = db
        self.tag_re = re.compile(r"( #|^#)(?P<tag>(\w|-)+)")

    def get_tags(self, tweet):
        if 'hashtags' not in tweet or type(tweet['hashtags']) != list:
            matches = self.tag_re.findall(self.clean_text(tweet['text']))
            return [x[1].lower() for x in matches if not x[1].isdigit()]
        else:
            return [tag['text'].lower() for tag in tweet['hashtags']]

    def clean_text(self, text):
        return re.sub(r"http\S+", "", text)

    def get_terms(self, tweet):
        text = self.clean_text(tweet['text'])
        terms = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text)
        terms = [t.lower() for t in terms]
        terms = [t for t in terms if (t not in stop_words) and (not t.isdigit())]
        return set(terms)

    def calculate_score(self, terms, event):
        scores = defaultdict(list)
        event_counts = self.db.get_event_meta(event)
        if any([c < 50 for c in event_counts.values()]):
            return None
        if len(terms) == 0:
            return None
        for t in terms:
            term_counts = self.db.get_term_meta(event, t)
            assert len(term_counts) == 2
            for affiliation, term_count in term_counts.items():
                #other_term_count = sum([c for a,c in term_counts.items() if a != affiliation])
                #other_event_count = sum([c for a,c in event_counts.items() if a != affiliation])
                #other_portion = (float(other_term_count)+1)/(other_event_count+1)
                #this_portion = (float(term_count)+1)/(event_counts[affiliation]+1)
                new_score = self.db.unigram_score(event, affiliation, t)#this_portion * math.log(this_portion / other_portion)
                scores[affiliation].append(new_score)
        return {k:max(v) for k,v in scores.items()}, {k:list(zip(terms, v)) for k,v in scores.items()}

    def learn(self, tweet, affiliation):
        terms = self.get_terms(tweet)
        events = self.get_tags(tweet)
        user_id = tweet['user_id']
        for event in events:
            self.db.update_event_inc(event, user_id, affiliation)
            for term in terms:
                self.db.update_term_inc(event, term, user_id, affiliation)
            scores = self.calculate_score(terms, event)
            if scores is None:
                continue
            scores, score_detail = scores
            self.db.store_tweet(tweet, event, scores, score_detail)

class Scrapper_META_DB:
    def __init__(self, url, db_name):
        self.client = MongoClient(url)
        self.db = self.client[db_name]
        self.scrape_meta_collection = self.db['scraper_meta']
        self.lastest_tweet_id_cache = {}

    def clear(self):
        self.scrape_meta_collection.drop()

    def update_latest_tweet_id_of_user(self, user_id, tweet_id):
        if user_id not in self.lastest_tweet_id_cache:
            get_latest_tweet_id_of_user(user_id)
        if tweet_id > self.lastest_tweet_id_cache[user_id]:
            self.lastest_tweet_id_cache[user_id] = tweet_id

    def get_latest_tweet_id_of_user(self, user_id):
        if user_id in self.lastest_tweet_id_cache:
            if self.lastest_tweet_id_cache[user_id] == -1:
                return None
            else:
                return self.lastest_tweet_id_cache[user_id]
        row = self.scrape_meta_collection.find_one({'user_id':user_id})
        if row is None:
            self.lastest_tweet_id_cache[user_id] = -1
        else:
            tweet_id = row['latest_tweet_id']
            self.lastest_tweet_id_cache[user_id] = int(tweet_id)
        return self.get_latest_tweet_id_of_user(user_id)

    def flush(self):
        for user_id, tweet_id in self.lastest_tweet_id_cache.items():
            if tweet_id == -1:
                continue
            self.scrape_meta_collection.update_one({'user_id':user_id}, {"$set": {'latest_tweet_id': tweet_id}}, upsert=True)

    def close(self):
        self.client.close()

class Scrapper:
    def __init__(self, API_pool, scrapper_meta, callback):
        self.log = Logger("Scrapper")
        self.API_pool = API_pool
        self.scrapper_meta = scrapper_meta
        self.callback = callback

    def scrape(self, target):
        user_id = target['user_id']
        latest_tweet_id = self.scrapper_meta.get_latest_tweet_id_of_user(user_id)
        try:
            tweets = self.API_pool.fetch_tweets(user_id, latest_tweet_id)
        except tweepy.TweepError as e:
            self.log.d('<{}> TweepError: {}'.format(target['user_id'], str(e)))
            return
        except:
            self.log.d('<{}> Unexpected error: {}'.format(target['user_id'], sys.exc_info()[0]))
            raise
        if len(tweets) == 0:
            return
        for tweet in tweets:
            self.callback(tweet, target)
            self.scrapper_meta.update_latest_tweet_id_of_user(user_id, tweet['tweet_id'])

    def run(self, targets):
        total = len(targets)
        for i, target in enumerate(targets):
            user_id = target['user_id']
            self.log.d('scrape {}th user_id: {} {:0.3f}%'.format(i, user_id, float(i)/total*100))
            try:
                self.scrape(target)
            except API_pool.AllBusyError:
                self.log.d('AllBusyError')
                break
        self.log.d('end run')

class API_pool():
    class AllBusyError(Exception):
        pass

    def __init__(self, authentications, wait=False):
        self.wait = True
        self.log = Logger("API_pool");
        self.APIs = [];
        self.status = []; #-1 is idle, time is busy
        if len(authentications) == 0:
            raise Exception('API_pool: no authentications')
        for authutication in authentications:
            consumer_key = authutication["consumer_key"]
            consumer_secret = authutication["consumer_secret"]
            access_key = authutication["access_key"]
            access_secret = authutication["access_secret"]
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)
            self.APIs.append(tweepy.API(auth))
            self.status.append(-1)
        self.log.d('#authentications: {}'.format(len(authentications)))

    def get_idle_api(self):
        now = time.time()
        for i,st in enumerate(self.status):
            if now >= st:
                self.log.d("use authentication {}".format(i))
                self.status[i] = -1
                return self.APIs[i]
        if self.wait:
            self.log.d("waiting 1min")
            time.sleep(60) #don't need to wait 15min because some authentication may recover earlier
            return self.get_idle_api()
        else:
            raise API_pool.AllBusyError()
            return None

    def set_busy(self, api):
        i = self.APIs.index(api)
        self.status[i] = time.time() + 15*60 #15 mins

    def parse_tweet(self, tweet):
        return {'tweet_id': tweet.id, 'created_at': tweet.created_at, 'text': tweet.text, 'hashtags': tweet.entities.get('hashtags')}

    def parse_tweets(self, tweets, user_id):
        #tweets2 = []
        ##for i in tweets:
        #    if (i.text not in tweets_dict):
        #        tweets_dict[i.text] = 1
        #        tweets2.append(i)
        #tweets = tweets2
        tweets = [self.parse_tweet(t) for t in tweets]
        for tweet in tweets:
            tweet['user_id'] = user_id
        return tweets

    def fetch_tweets(self, user_id, latest):
        api = None
        try:
            if latest is None :
                api = self.get_idle_api()
                new_tweets = api.user_timeline(user_id = user_id, count = 200)
            else:
                new_tweets = []
                finished = False
                max_id = None
                while not finished:
                    api = self.get_idle_api()
                    if max_id is not None:
                        page = api.user_timeline(user_id = user_id, count = 200, max_id = max_id)
                    else:
                        page = api.user_timeline(user_id = user_id, count = 200, since_id = latest-1) #return less than or equal to latest
                    page.sort(key = lambda x:x.id, reverse=True) #smaller index has larger id
                    if len(page) == 0:
                        break
                    self.log.d("get {}'s tweets page {} {}-{} latest: {}".format(user_id, len(page), page[0].id if page else None, page[-1].id if page else None, latest))
                    if max_id is not None and page[-1].id >= max_id:
                        self.log.d('fetch tweet error old_max_id={} <= new_max_id={}'.format(max_id, page[-1].id))
                        break
                    max_id = page[-1].id
                    for t in page:
                        if t.id > latest:
                            new_tweets.append(t)
                        else:
                            finished = True
                            break
                    if len(page) < 200:
                        break
            new_tweets = self.parse_tweets(new_tweets, user_id)
            self.log.d("get {}'s tweets {} {}-{} latest: {}".format(user_id, len(new_tweets), new_tweets[0]['tweet_id'] if new_tweets else None, new_tweets[-1]['tweet_id'] if new_tweets else None, latest))
            self.log.d("get {}'s tweets {} {}-{} latest: {}".format(user_id, len(new_tweets), new_tweets[0]['created_at'] if new_tweets else None, new_tweets[-1]['created_at'] if new_tweets else None, latest))
            return new_tweets
        except tweepy.RateLimitError:
            self.log.d('RateLimitError')
            self.set_busy(api)
            return self.fetch_tweets(user_id, latest)

def build_targets(democrats, republicans):
    random.shuffle(democrats) #in case all keys get RateLimitError
    random.shuffle(republicans)
    targets = []
    i = 0
    while True:
        if i >= len(democrats) and i >= len(republicans):
            break
        if i < len(democrats):
            targets.append({'user_id': democrats[i],   'affiliation': 'democrats' })
        if i < len(id_list.republicans):
            targets.append({'user_id': republicans[i], 'affiliation': 'republicans' })
        i += 1
    return targets

def get_section(l, i, j):
    print(i,j)
    assert i >= 0 and j >= 0 and i < j
    part_size = float(len(l))/j
    # TEMP EDIT: USE ENTIRE THING ##############################################################################################################################################
    return l #l[int(part_size*i) : int(part_size*(i+1))]

if __name__ == '__main__':
    log = Logger('main')
    if len(sys.argv) != 3:
        raise Exception('wrong number of arguments')
    democrats_ids = get_section(id_list.democrats, int(sys.argv[1]), int(sys.argv[2]))
    republicans_ids = get_section(id_list.republicans, int(sys.argv[1]), int(sys.argv[2]))
    log.d('democrats_ids {} {}-{}'.format(len(democrats_ids), democrats_ids[0], democrats_ids[-1]))
    log.d('republicans_ids {} {}-{}'.format(len(republicans_ids), republicans_ids[0], republicans_ids[-1]))
    targets = build_targets(democrats_ids, republicans_ids)
    log.d('#targets: {}'.format(len(targets)))
    url = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/cs4300')
    parsed_url = urlsplit(url)
    db_name = parsed_url.path[1:]
   # authentications = json.loads(base64.b64decode(os.getenv('TWEET_AUTHENTICATIONS', 'W10=').encode('ascii')).decode('ascii'))
    #log.d(str(authentications))
    #import base64;base64.b64encode(json.dumps(authutications))
    #export TWEET_AUTHENTICATIONS=ABOVE_RESULT_WITHOUT_QUOT
    authentications = [{"consumer_secret": "BfcpZijhDD8xqvV6FSo6MOtn7rWgahjy25j0pAvSz2nrnaTCpQ", "access_key": "3877172955-okHQebGAFkGQR9Umn0enhzJCetn9Jqf83rtOQcw", "consumer_key": "7MLUo51A96kO1C8d6VYvd2G25", "access_secret": "SaUrB3ETDY0uZcwqEq5yLtwV71Lidno8KkLESnNxi8YuF"}, {"consumer_secret": "FbmY3Hv6VCn83HrFPvPyDYyY6EtubBXff9eCyaT4XTCB1q1zlK", "access_key": "3877172955-86PXAfliiE15siEHswHKU28ZUpfNWTwqe4l1Mni", "consumer_key": "oNPpB2s30cPsL5GsbpCotI8Ld", "access_secret": "Ae3iAbCcaBw4eFequKwwIzPl0rcFzyETMGOslpq8hIsKP"}, {"consumer_secret": "w43cxsth5jsf7SeI4LBG3cqK02vOJZHAfMvLOIv0SS3MNLawaD", "access_key": "3877172955-bjwuASM26nkKUGXS8Sc67Aec7EBZFxWZJ9whPNZ", "consumer_key": "iMo6Xgic4BJDL8QMk4diLnHrJ", "access_secret": "7Xc3nYMBzsJB20KozJtDTNLjc857GkZTiV6nuc5nSWsTb"}, {"consumer_secret": "Nni6aW5JGr1m2uZ10dsizqRZmx7V7gshiMcx2k8iHDYqk75N9b", "access_key": "3877172955-TgoBLcomOfEitZsVTzBILmqpdqxLzhSvz8BaPpe", "consumer_key": "KykSJ2ecnLZ0fhdpNe9UXKiqk", "access_secret": "6JmuZlz91e4IcedXflKL2zGdNwgkYxV0WMIQDIbW7CQaY"}, {"consumer_secret": "5MYfaR7sPsvUpqDqFbwjG1AsXovJhg6F72KcdLSV1ZfLOb1X8d", "access_key": "717524076248477701-wqOvtvOXTsPa93RiyoZtKXv778MkFDS", "consumer_key": "s2HobRFCjSkNvt8VsrPMJfDVH", "access_secret": "EHA0qJQc1dxWPylF5Eq4rIHLZIoYqdqV3ZKK2Rz8P2jvK"}, {"consumer_secret": "2QkVh4TkO4m6bjwXbFpbG0UE8vN3O22eAyDhyydHUSKBxVEiFm", "access_key": "717524076248477701-aJUgF3uOuTD90qX1WmHNWRT2LXMLhUg", "consumer_key": "oDhRm2Q4DuRY9RGx9UtVl0kzo", "access_secret": "TNnt6xsJCGuljpA3IrbCR915HSQatCxGXcYgEaZlsMNdQ"}, {"consumer_secret": "p7Ap6gpQH0CpUnLL3fUF5EzFcRQjpkzAzxlw6704JtQmJ7fiS5", "access_key": "717524076248477701-MTZo9J9h4yZZBgNYv6rpfKu2IUvLAfY", "consumer_key": "t4xzUgIWRz05rJKrKuEIZlbOC", "access_secret": "18KTcI5sUgW6dQya2EQZ00OXI7furHkuMxIbrxrhAjSrh"}, {"consumer_key": "eNfjPJT12a1aiFGaVSNnn6nTg", "consumer_secret": "wJk3RhuhUo5MFNnnLaJQIM2Q93gFeMMfWGUzoYd6z49z8Kis2w", "access_key": "717950588076601344-yDbU6iN96hMagodDyv2iqTxuiNQ7VkS", "access_secret": "OycOAMytzLXlik4qO32iLWxPoPaqNmoXlDrW6QfhhX7Vd"}]
    unigram_classifier_db = Unigram_Classifier_DB(url, db_name, ['democrats', 'republicans'])
    scrapper_meta_db = Scrapper_META_DB(url, db_name)
    classifier = Unigram_Classifier(unigram_classifier_db)
    api_pool = API_pool(authentications)
    scrapper = Scrapper(api_pool, scrapper_meta_db, lambda tweet, target: classifier.learn(tweet, target['affiliation']))
    scrapper.run(targets)
    unigram_classifier_db.flush()
    unigram_classifier_db.close()
    scrapper_meta_db.flush()
    scrapper_meta_db.close()
    log.d('main thread exits.')
