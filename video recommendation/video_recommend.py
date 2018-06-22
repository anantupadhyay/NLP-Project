import pandas as pd 
import threading
import datetime

def recommend_video_from_review(subject, attribute, domain, department, sent, vdo_dict):
	vdo_dict[sent] = "Not Found"
	tmp = vdo_df[vdo_df.subject.isin(subject) & vdo_df.attribute.isin(attribute) & vdo_df.domain.isin(domain) & vdo_df.department.isin(department)]
	if tmp.empty:
		tmp = vdo_df[vdo_df.domain.isin(domain) & vdo_df.department.isin(department) & vdo_df.subject.isin(subject)]
	if not tmp.empty:
		vdo_dict[sent] = tmp[['id','video_name','video_url']].values

def get_recent_video(vdo_dict2):
	dt = (datetime.date.today() - datetime.timedelta(3*365/12)).isoformat()
	li = vdo_df['id'][vdo_df['created_at']>=dt].sample(3).values
	for x in li:
		vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def get_non_watched_video(df, vdo_dict2):
	li = df['video_details_id_id'][(df['is_watched']==0) & (df['hotel_id_id']==1)].sample(3).values
	for x in li:
		vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def get_least_recently_watched(df, vdo_dict2):
	

def get_most_complaint_domain(vdo_dict2):
	tags = pd.read_csv('dataset/tags.csv')
	dt = (datetime.date.today()-datetime.timedelta(2*365/12)).isoformat()
	res = vdo_df['id'][vdo_df['domain']==tags['domain'][tags['created_at']>=dt].mode().values[0]].sample(1).values
	for x in res:
		vdo_dict2[x] = vdo_df[['video_name', 'video_url']][vdo_df['id']==x].values

def recommend_video_without_review(vdo_dict2):
	df = pd.read_csv('dataset/watchlist.csv')
	get_non_watched_video(df, vdo_dict2)
	get_least_recently_watched(df, vdo_dict2)
	get_recent_video(vdo_dict2)
	get_most_complaint_domain(vdo_dict2)

vdo_df = pd.read_csv('dataset/video.csv')
if __name__=="__main__" :
	review = pd.read_csv('dataset/review.csv')
	procs=[]
	vdo_dict = {}
	for x in range(0, 7):
		sub = review['subject'][x]
		attrb = review['attribute'][x]
		domain = review['domain'][x]
		dept = review['department'][x]
		proc=threading.Thread(target=recommend_video_from_review, args=([sub], [attrb], [domain], [dept], review['review'][x], vdo_dict))
		procs.append(proc)
		proc.start()

	for proc in procs:
		proc.join()

	for k,v in vdo_dict.items():
		print k, " -> ", v, '\n'

	vdo_dict2 ={}
	recommend_video_without_review(vdo_dict2)
	# for k,v in vdo_dict2.items():
		# if len(v)==0:
			# del vdo_dict2[k]

	for k,v in vdo_dict2.items():
		print k, " -> ", v, '\n'