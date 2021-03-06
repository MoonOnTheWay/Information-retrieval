import sys
sys.path.append("../Tools")

import numpy as np
import ProcDoc

class InputDataProcess(object):
	def __init__(self, num_of_homo_feats = 10, max_qry_length = 1794, max_doc_length = 2907, query_path = None, document_path = None, corpus = "TDT2"):
		res_pos = True
		str2int = True
		self.num_vocab = 51253
		self.max_qry_length = max_qry_length
		self.max_doc_length = max_doc_length
		self.num_of_homo_feats = num_of_homo_feats
		if query_path == None: 
			query_path = "../Corpus/" + corpus + "/Train/XinTrainQryTDT2/QUERY_WDID_NEW"
		if document_path == None:
			document_path = "../Corpus/" + corpus + "/SPLIT_DOC_WDID_NEW"
		# read document, reserve position
		doc = ProcDoc.read_file(document_path)
		self.doc = ProcDoc.doc_preprocess(doc, res_pos, str2int)
			
		# read query, reserve position
		qry = ProcDoc.read_file(query_path)
		self.qry = ProcDoc.query_preprocess(qry, res_pos, str2int)	
		
		# HMMTrainingSet
		self.hmm_training_set = ProcDoc.read_relevance_dict()
		self.homo_feats = self.__genFeature(num_of_homo_feats)
		
	def genPassageAndLabels(self, list_IDs, labels, batch_size):
		qry = self.qry
		doc = self.doc
		max_qry_length = self.max_qry_length
		max_doc_length = self.max_doc_length
		homo_feats = self.homo_feats
		num_of_homo_feats = self.num_of_homo_feats
		psg_mat_batch = np.zeros((batch_size, max_qry_length, max_doc_length, 1))
		homo_feats_batch = np.zeros((batch_size, num_of_homo_feats))
		rel_batch = np.zeros((batch_size))
		# generate passage
		for idx, data_ID in enumerate(list_IDs):
			[q_id, d_id] = data_ID.split("_")
			q_terms = qry[q_id]
			d_terms = np.asarray(doc[d_id])
			psg_mat = np.asarray([[(q_t == d_terms)] for q_t in q_terms]).reshape(len(q_terms), len(d_terms), 1)
			psg_mat = self.__mergeMat(np.zeros((max_qry_length, max_doc_length, 1)), psg_mat)
			psg_mat_batch[idx] = np.copy(psg_mat)
			homo_feats_batch[idx] = homo_feats[q_id]
			rel_batch[idx] = labels[data_ID]
		return [psg_mat_batch, homo_feats_batch, rel_batch]
	
	def genTrainValidSet(self):
		print "generate training set and validation set"
		qry = self.qry
		doc = self.doc
		total_qry = len(qry.keys())
		total_doc = len(doc.keys())
		hmm_training_set = self.hmm_training_set
		labels = {}
		total = total_qry * total_doc
		num_of_train = total * 8 / 10 
		num_of_valid = total - num_of_train
		partition = {'train': [], 'validation': []}
		# relevance between queries and documents
		for q_id in qry:
			for d_id in doc:
				if d_id in hmm_training_set[q_id]:
					labels[q_id + "_" + d_id] = 1
				else:
					labels[q_id + "_" + d_id] = -1
		# partition
		ID_list = labels.keys()
		# shuffle
		np.random.shuffle(ID_list)
		partition['train'] = [id for id in ID_list[:num_of_train]]
		partition['validation'] = [id for id in ID_list[num_of_train:]]
		return [partition, labels]
	
	def __genFeature(self, num_of_homo_feats):
		###################### TODO ######################
		print "generate h features"
		qry = self.qry
		doc = self.doc
		homo_feats = {}
		df = ProcDoc.docFreq(doc)
		
		for q_id, q_terms in qry.items():
			npscq = np.asarray([self.scq(df, q_term) for q_term in q_terms])
			homo_feats[q_id] = np.asarray([np.sum(npscq), np.amax(npscq), np.amin(npscq), np.mean(npscq)])
		
		# np.sum(a)
		# np.amax(a)
		# np.amin(a)
		# np.mean(a)
		# a.prod()**(1.0/len(a))
		# len(a) / np.sum(1.0/a)
		# var = variation(a, axis=0) idmax = np.argmax(var)
		
		return homo_feats
	def scq(self, df, term):
		eps = np.finfo(float).eps
		# print df[term, 1],1 + self.num_vocab/(eps + df[term, 0])
		return (1 + np.log(eps + df[term, 1])) * np.log(1 + self.num_vocab/(eps + df[term, 0]))
		
	def __mergeMat(self, b1, b2, pos = [0, 0]):
		[pos_v, pos_h] = pos
		v_range1 = slice(max(0, pos_v), max(min(pos_v + b2.shape[0], b1.shape[0]), 0))
		h_range1 = slice(max(0, pos_h), max(min(pos_h + b2.shape[1], b1.shape[1]), 0))
		v_range2 = slice(max(0, -pos_v), min(-pos_v + b1.shape[0], b2.shape[0]))
		h_range2 = slice(max(0, -pos_h), min(-pos_h + b1.shape[1], b2.shape[1]))
		b1[v_range1, h_range1] += b2[v_range2, h_range2]
		return b1
if __name__ == "__main__":
	a = InputDataProcess()
	
	


