import ProcDoc

def Probability_LSA(bg_word, doc_wc_dict, doc_topic_prob_dict, topic_word_prob_dict, doc_word_topic_prob_dict):
	topic_word_prob_dict = {}
	doc_topic_prob_dict = {}
	doc_word_topic_prob_dict = {}
	doc_wc_dict = {}
	bg_word = {}
	interative = 0
	while has_converged(interative):
		Evaluate(bg_word, doc_wc_dict, doc_topic_prob_dict, topic_word_prob_dict, doc_word_topic_prob_dict)
		Maximum(doc_wc_dict, doc_topic_prob_dict, topic_word_prob_dict, doc_word_topic_prob_dict)
		interative += 1
	return [topic_word_prob_dict, doc_topic_prob_dict, doc_wc_dict]	
	
def Evaluate(bg_word, doc_wc_dict, doc_topic_prob_dict, topic_word_prob_dict, doc_word_topic_prob_dict):
	# P(T| D, w)
	for word, freq in bg_word.items():
		for doc_name, doc_wc_list in doc_wc_dict.items():
			denominator = 0.0
			for topic, prob in doc_topic_prob_dictp[doc_name].items():
				w_t = topic_word_prob_dict[topic][word]
				t_d = doc_topic_prob_dict[doc_name][topic]
				denominator += w_t * td
			for topic, prob in doc_topic_prob_dictp[doc_name].items():
				w_t = topic_word_prob_dict[topic][word]
				t_d = doc_topic_prob_dict[doc_name][topic]
				doc_word_topic_prob_dict[doc_name][word][topic] = w_t * t_d / denominator
		

def Maximum(doc_wc_dict, doc_topic_prob_dict, topic_word_prob_dict, doc_word_topic_prob_dict):
	# P(w | T)
	for tp, w_prob_list in topic_word_prob_dict.items():	
		for word, word_prob in w_prob_list.items():
			denominator = 0.0
			for w, w_p in w_prob_list.items():
				for doc_name, doc_wc_list in doc_wc_dict.items():
					d_w_c = doc_wc_list[w]
					d_w_t_p = doc_word_topic_prob_dict[doc_name][w][tp]
					denominator += d_w_c * d_w_t_p
			molecellur = 0.0		
			for doc_name, doc_wc_list in doc_wc_dict.items():
				d_w_c = doc_wc_list[word]
				d_w_t_p = doc_word_topic_prob_dict[doc_name][word][tp]
				molecellur += d_w_c * d_w_t_p
				
			topic_word_prob_dict[tp][word] = molecellur / denominator
		
	# P(T| D)
	for doc_name, topic_list in doc_topic_prob_dict.items():
		for tp, tp_prob in topic_list.items():
			denominator = ProcDoc.word_sum(doc_wc_dict[doc_name]) * 1.0
			molecellur = 0.0
			for d_w, doc_wc in doc_wc_dict[doc_name].items():
				d_w_c = doc_wc
				d_w_t_p = doc_word_topic_prob_dict[doc_name][d_w][tp]
				molecellur += d_w_c * d_w_t_p / denominator
			doc_topic_prob_dict[doc_name][tp] = molecellur
			
	
def has_converged(interative):
	return interative < 100