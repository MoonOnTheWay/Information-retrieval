'''
	parameter				type	
	query_docs_ranking 		dict		{q_key:[d_key...], ...}
	query_list  			list		[q_key, ....]
	query_model 			numpy		[[query_unigram], ....]
	doc_list				list		[d_key, .....]
	doc_model				numpy		[[doc_unigram]]
	
'''

import cPickle as pickle
import numpy as np
import ProcDoc
from math import exp

topM = 9
vocabulary_size = 51253
smoothing = 0.1

''' load data'''
with open("query_list.pkl", "rb") as file:
	query_list = pickle.load(file)
with open("query_model.pkl", "rb") as file:	
	query_model = pickle.load(file)
with open("doc_list.pkl", "rb") as file:
	doc_list = pickle.load(file)
with open("doc_model.pkl", "rb") as file:	
	doc_model = pickle.load(file)
with open("query_ranking_result.pkl", "rb") as file:
	query_docs_ranking = pickle.load(file)

background_model =  ProcDoc.read_background_dict()	

''' smoothing '''
for d_idx, doc_vec in enumerate(doc_model):
	doc_model[d_idx] = (1 - smoothing) * doc_vec + smoothing * background_model

''' relevace model '''
for q_idx, q_key in enumerate(query_list):
	q_vec = query_model[q_idx]
	# relevance top M document
	q_t_d = np.zeros(len(query_docs_ranking[q_key][:topM]))
	w_d = np.zeros(vocabulary_size)
	for rank_idx, doc_key in enumerate(query_docs_ranking[q_key][:topM]):
		doc_idx = doc_list.index(doc_key)
		doc_vec = doc_model[doc_idx]
		# probability of query term in document
		q_non_zero, = np.where(q_vec != 0)
		# product
		# q_t_d[rank_idx] = (np.prod(doc_vec[q_non_zero]) + 0.1)
		# logadd
		for q_t in np.log(doc_vec[q_non_zero]):
			q_t_d[rank_idx] += q_t
		#print exp(q_t_d[rank_idx])
		
		w_d += doc_vec * q_t_d[rank_idx]
	# relevance model
	w_d /= q_t_d.sum(axis = 0)
	query_model[q_idx] = w_d
	
with open("relevance_model_RM.pkl", "wb") as file:	
	pickle.dump(query_model, file, True)
