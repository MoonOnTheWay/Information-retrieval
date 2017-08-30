# -*- coding: utf-8 -*-
import csv
import random
import numpy as np
import cPickle as Pickle 
import kmeans

# Read Query Model
corpus = "TDT2"
model_path = "../Corpus/model/"+corpus+"/UM/"
query_model = Pickle.load(model_path + "query_model.pkl")
# Preprocess(fit data structure in kmeans.py)
for idx, vec in enumerate(query_model):
	data = kmeans.dataInfo(idx, vec)
	data_list.append(data)
	
# Calculate
for num_of_cluster in [2, 4, 8]:			
	# kmeans
	# return clusters and centeroids
	[clusters, centroids] = kmeans.kmeans(data_list, num_of_cluster)	

	with open("clusters/"+corpus+"/kmeans_" + str(num_of_cluster) + '.txt', 'w') as output:
		# Compute SSE
		sse = 0
		for cur_cluster in xrange(0, len(clusters)):
			# Cluster 
			cluster_name = str(cur_cluster) + "," + centroids[cur_cluster]
			output.write(cluster_name)
			# Item
			data_str = ""
			for data in clusters[cur_cluster]:
				data_str += "," + data.getID()
			output.write(data_str)
			output.write("\n")