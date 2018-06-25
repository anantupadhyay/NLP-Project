import pandas as pd
import threading
import datetime
import random
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
import nltk

def get_non_watched_video(wlist, vdo_dict2, hotelid):
	li = wlist['video_details_id_id'][(wlist['is_watched']==0) & (wlist['hotel_id_id']==hotelid)].values
	li = random.sample(li, min(5, len(li)))
	for x in li:
		vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def get_least_recently_watched(watchlist, vdo_dict2, hotelid):
	wlist = watchlist[['updated_at', 'video_details_id_id']].loc[watchlist['hotel_id_id']==hotelid].dropna()
	li = wlist.sort_values('updated_at').video_details_id_id.unique()
	li = random.sample(li[:min(len(li), 10)], min(5, len(li)))
	for x in li:
		vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def get_recent_video(watchlist, vdo_dict2):
	no_of_days = 45
	dt = (datetime.date.today() - datetime.timedelta(no_of_days)).isoformat()
	li = watchlist['video_details_id_id'][(watchlist['created_at']>=dt)].values
	li = random.sample(li, min(5, len(li)))
	for x in li:
		vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def get_most_complaint_domain(watchlist, vdo_dict2, hotelid):
	from collections import Counter
	# Getting the date of one mnth back
	dt = (datetime.date.today() - datetime.timedelta(1*365/12)).isoformat()
	match = pd.read_csv('dataset/match.csv')
	tags = pd.read_csv('dataset/tags.csv')

	match = match[['tag_id_id', 'hotel_id_id']][(match['is_done']==1) & (match['created_at']>=dt)]
	tag = match[['tag_id_id']][match['hotel_id_id']==hotelid].values
	cnt = Counter(tag.ravel())
	li = []
	for k,f in cnt.most_common(4):
		li.append(k)
	tags.id = tags.id.astype('int')
	tags = tags[tags['id'].isin(li)]
	res = vdo_df['id'][(vdo_df['domain'].isin(tags['domain']))].values
	for x in res:
		if ((x==watchlist['video_details_id_id']) & (hotelid==watchlist['hotel_id_id'])).any():
			vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def recommend_video_without_review(watchlist, vdo_dict2):
	hotelid = 1
	get_non_watched_video(watchlist, vdo_dict2, 1)
	get_least_recently_watched(watchlist, vdo_dict2, 2)
	get_recent_video(watchlist, vdo_dict2)
	get_most_complaint_domain(watchlist, vdo_dict2, hotelid)

def recommend_video_from_review(subject, attribute, domain, department, sent, vdo_dict, watchlist, hotelid):
	# vdo_dict[sent] = "Not Found"
	tmp = vdo_df[vdo_df.subject.isin(subject) & vdo_df.attribute.isin(attribute) & vdo_df.domain.isin(domain) & vdo_df.department.isin(department)]
	if tmp.empty:
		tmp = vdo_df[vdo_df.domain.isin(domain) & vdo_df.department.isin(department) & vdo_df.subject.isin(subject)]
	if not tmp.empty:
		for x in tmp['id'].values:
			if ((x==watchlist['id'].values)&(hotelid==watchlist['hotel_id_id'])).any():
				vdo_dict[x] = tmp[['id','video_name','video_url']][tmp['id']==x].values

def get_video_from_similarity(df, vectorizer, sent, vdo_dict, watchlist, porter):
	vec2 = vectorizer.transform([sent])
	cosim, euclid, i1, i2 = 0.0, float('inf'), -1, -1
	s1, s2 = "", ""
	for x in range(0, len(df['video_name'])):
		token = word_tokenize(df['video_name'][x])
		words = [w.lower() for w in token]
		stem_token = [porter.stem(t) for t in words]
		vec = vectorizer.transform([' '.join(stem_token)])
		tmp = cosine_similarity(vec, vec2)
		if tmp > cosim:
			cosim = tmp
			s1 = df['video_name'][x]
			i1 = x
		tmp2 = euclidean_distances(vec, vec2)
		if tmp2 < euclid:
			euclid = tmp2
			s2 = df['video_name'][x]
			i2 = x

	vdo_dict[i1] = [sent, s1, df['video_url'][df['id']==i1].values]
	vdo_dict[i2] = [sent, s2, df['video_url'][df['id']==i2].values]

def train_tfidf_vectorizer(porter, df):
	doc = []
	for x in df['video_name']:
		tokens = word_tokenize(x)
		words = [w.lower() for w in tokens]
		stem_token = [porter.stem(t) for t in words]
		doc.append(' '.join(stem_token))
	vectorizer = TfidfVectorizer()
	vectorizer.fit(doc)
	return vectorizer

if __name__=="__main__" :
	vdo_df = pd.read_csv('dataset/video.csv')
	watchlist = pd.read_csv('dataset/watchlist.csv')

	video_watch_limit = 45
	till_date = (datetime.date.today() - datetime.timedelta(video_watch_limit)).isoformat()
	watchlist = watchlist[((watchlist['is_watched']==1) & (watchlist['updated_at']<=till_date) | (watchlist['is_watched']==0))]
	# print watchlist.tail()
	df = pd.read_csv('dataset/video_details.csv')
	df = df[df['id'].isin(watchlist['video_details_id_id'].values)]
	df.reset_index(drop=True, inplace=True)
	porter = nltk.PorterStemmer()
	vectorizer = train_tfidf_vectorizer(porter, df)

	vdo_dict = {}
	sentiment = -0.2
		
	review = pd.read_csv('dataset/review.csv')
	procs=[]
	for x in range(0, 7):
		# hotelid = 1
		# sub = review['subject'][x]
		# attrb = review['attribute'][x]
		# domain = review['domain'][x]
		# dept = review['department'][x]
		# recommend_video_from_review([sub], [attrb], [domain], [dept], review['review'][x], vdo_dict, watchlist, hotelid)
		if sentiment <= 0:
			get_video_from_similarity(df, vectorizer, review['review'][x], vdo_dict, watchlist, porter)
		# proc=threading.Thread(target=recommend_video_from_review, args=([sub], [attrb], [domain], [dept], review['review'][x], vdo_dict, watchlist, hotelid))
	# 	procs.append(proc)
	# 	proc.start()

	# for proc in procs:
	# 	proc.join()

	print "Length of 1st one is -> ", len(vdo_dict), '\n'
	for k,v in vdo_dict.items():
		print k, " -> ", v, '\n'

	# vdo_dict2 ={}
	# recommend_video_without_review(watchlist, vdo_dict2)

	# print "Length of 2nd one is -> ", len(vdo_dict2), '\n\n'
	# for k,v in vdo_dict2.items():
	# 	print k, " -> ", v, '\n'

	# # Randomly selecting videos from available list of 1st dictionary
	# for x in range(10):
	# 	k = random.choice(vdo_dict.keys())
	# 	print k, "->", vdo_dict[k]

	# # Randomly picking videos from 2nd dictionary
	# for x in range(5):
	# 	k = random.choice(vdo_dict2.keys())
	# 	print k, "->", vdo_dict2[k]
