#!/usr/bin/python

# This script takes the output of getDBpediaCandidates.py and computes the recall 
# author: marieke.van.erp@vu.nl
# date: 28 November 2016

import sys

with open('AIDA_dbcandidates_test.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		elements = line.split('\t')
		print(len(elements) - 2 ) 