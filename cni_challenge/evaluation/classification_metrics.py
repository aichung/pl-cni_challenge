#!/shared/python3shared/bin/python3
"""
:Summary:
	With the lack of consensus of which metric is most suitable to determine the most appropriate classifier, we use an inclusive approach. 
	This includes multiple measures which are commonly used in classification tasks, such as accuracy and AUC, allowing for a more intuitive 
	interpretation of the results, in addition to measures such as Geometric-mean and optimized precision 
	(cf. M Hossin and MN Sulaiman. A review on evaluation metrics for data classification evaluations. International Journal of Data Mining & Knowledge Management Process, 5(2):1,2015.) .

:Description:
	We utilize accuracy, error rate, sensitivity, specificity, precision, recall, F-Measure, Geometric-mean, 
	AUC, optimized precision 
	(cf. Hossin and Sulaiman. A review on evaluation metrics for data classification evaluations. International Journal of Data Mining & Knowledge Management Process, 5(2):1,2015).

	It compares estimated classification (est) and "ground truth" (gt)

:Requires:

:TODO:

:AUTHOR: MDS
:ORGANIZATION: MGH/HMS
:CONTACT: software@markus-schirmer.com
:SINCE: 2018-11-12
:VERSION: 0.1
"""
#=============================================
# Metadata
#=============================================
__author__ = 'mds'
__contact__ = 'software@markus-schirmer.com'
__copyright__ = ''
__license__ = ''
__date__ = '2019-04'
__version__ = '0.1'

#=============================================
# Import statements
#=============================================
import sys
import os
import numpy as np
import sklearn.metrics as skm
import getopt
import csv

import pdb

#=============================================
# Helper functions
#=============================================

TP = np.inf
FP = np.inf
TN = np.inf
FN = np.inf
num_p = np.inf
num_n = np.inf

def help():
	print("usage: classification_metrics.py -p <prediction_file> -g <groundtruth_file> -o <outputfile>")
	sys.exit()

def get_confusion_matrix(est, gt):
	global TP, FP, TN, FN, num_p, num_n
	TP = np.float(np.sum(np.logical_and((est==1), (gt==1)).astype(int)))
	TN = np.float(np.sum(np.logical_and((est==0), (gt==0)).astype(int)))
	FP = np.float(np.sum(np.logical_and((est==1), (gt==0)).astype(int)))
	FN = np.float(np.sum(np.logical_and((gt==1), (est==0)).astype(int)))

def get_tpr():
	# sensitivity / recall / hit rate/ true positive rate
	if (TP+FN) == 0:
		return np.nan
	return TP/(TP+FN)

def get_tnr():
	# specificity / selectivity / true negative rate
	if (TN+FP) == 0:
		return np.nan
	return TN/(TN+FP)

def get_ppv():
	# precision / positive predictive value
	if (TP+FP) == 0:
		return np.nan
	return TP/(TP+FP)

def get_npv():
	# negative predictive value
	if (TN + FN) == 0:
		return np.nan
	return TN/(TN + FN)

def get_fnr():
	# false negative rate
	if (FN+TP) == 0 :
		return np.nan
	return FN/(FN+TP)

def get_fpr():
	# false positive rate
	if (FP+TN) == 0:
		return np.nan
	return FP/(FP+TN)

def get_fdr():
	if (FP+TP) == 0 :
		return np.nan
	# false discovery rate
	return FP/(FP+TP)

def get_for():
	# false omission rate
	if (FN+TN)==0:
		return np.nan
	return FN/(FN+TN)

def get_accuracy():
	# accuracy
	if (TP+TN+FP+FN) == 0:
		return np.nan
	return (TP+TN)/(TP+TN+FP+FN)

def get_f1_score():
	# harmonic mean of recall and precision
	if (get_tpr() == 0) or (get_ppv() == 0):
		return np.nan
	return 1./((1./get_tpr() + 1./get_ppv())/2.)

def get_geom_mean():
	# geometric mean of recall and precision
	return np.sqrt(get_tpr() * get_ppv())

def get_mcc():
	# matthews correlation coefficient
	if np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)) == 0:
		return np.nan
	return (TP*TN - FP * FN)/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

def get_bm():
	# informedness / bookmaker informedness
	return (get_tpr() + get_tnr() - 1)

def get_markedness():
	return (get_ppv() + get_npv() - 1)

def get_plr():
	# positive likelihood ratio
	if get_fpr()==0:
		return np.nan
	return get_tpr()/get_fpr()

def get_nlr():
	# negative likelihood ratio
	if get_tnr() == 0:
		return np.nan
	return get_fnr()/get_tnr()

def get_dor():
	# diagnostic odds ratio
	if get_nlr()==0:
		return np.nan
	return get_plr()/get_nlr()

def get_AUC(est, gt):
	fpr, tpr, thresholds = skm.roc_curve(gt, est)
	return skm.auc(fpr, tpr)

def get_OP():
	sn = get_tpr()
	sp = get_tnr()
	P =  sn* (TP+FN) + sp * (TN+FP)
	return P - np.abs(sp-sn)/(sp + sn)

def get_metrics(est, gt):
	# set up global variables
	get_confusion_matrix(est, gt)

	# initialize output
	results = []
	names = []

	names.append('Sensitivity')
	results.append(get_tpr())

	names.append('Specificity')
	results.append(get_tnr())

	names.append('Precision')
	results.append(get_ppv())

	names.append('Negative_predictive_value')
	results.append(get_npv())

	names.append('False_negative_rate')
	results.append(get_fnr())

	names.append('False_positive_rate')
	results.append(get_fpr())

	names.append('False_discovery_rate')
	results.append(get_fdr())

	names.append('False_omission_rate')
	results.append(get_for())

	names.append('Accuracy')
	results.append(get_accuracy())

	names.append('F1_score')
	results.append(get_f1_score())

	names.append('Geom_mean')
	results.append(get_geom_mean())

	names.append('Matthews_CC')
	results.append(get_mcc())

	names.append('Informedness')
	results.append(get_bm())

	names.append('Markedness')
	results.append(get_markedness())

	# names.append('Positive_likelihood_ratio')
	# results.append(get_plr())

	# names.append('Negative_likelihood_ratio')
	# results.append(get_nlr())

	# names.append('Diagnostic_odds_ratio')
	# results.append(get_dor())

	names.append('Optimized_precision')
	results.append(get_OP())

	names.append('AUC')
	results.append(get_AUC(est,gt))

	return results, names

def evaluate_prediction(est, gt):

	# calculate metrics
	results, names = get_metrics(est, gt)

	return results, names

def read_file(filename):
	data = []
	with open(filename, 'r') as fid:
		reader = csv.reader(fid)
		for row in reader:
			data.append(np.int(row[0]))
	return np.asarray(data)

#=============================================
# Main method
#=============================================
def main(argv):
	prediction_file = None
	groundtruth_file = None
	output_file = None

	try:
		opts, args = getopt.getopt(argv[1:],"hp:g:o:",["prediction=","groundtruth=","output="])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:
		if opt == '-h':
			help()
		
		elif opt in ("-p", "--prediction"):
			prediction_file = arg
		elif opt in ("-g", "--groundtruth"):
			groundtruth_file = arg
		elif opt in ('-o', '--output'):
			output_file = arg

	if (prediction_file is None) or (groundtruth_file is None) or (output_file is None):
		help()

	# read input
	est = read_file(prediction_file)
	gt = read_file(groundtruth_file)

	# calculate metrics
	results, names = evaluate_prediction(est, gt)

	# save output
	with open(output_file, 'w') as fid:
		writer = csv.writer(fid)
		for ii in range(len(results)):
			writer.writerow([names[ii],results[ii]])

if __name__ == "__main__":
	main(sys.argv)
