#!/usr/bin/python

# This script takes the output of getDBpediaCandidates.py and computes the recall 
# author: marieke.van.erp@vu.nl
# date: 28 November 2016

import sys

total_lines = 0
lines_with_match = 0 
lines_without_candidates = 0 
with open('AIDA_dbcandidates_test.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		total_lines = total_lines + 1 
		if "NO DBPEDIA CANDIDATES" in line:
			lines_without_candidates = lines_without_candidates + 1 
			continue 
		elements = line.split("\t")
		# gold standard = elements[1] 
		for candidate in elements[2:]:
			if candidate == elements[1]:
				lines_with_match = lines_with_match + 1 
				continue 
		
lines_without_match = total_lines - lines_without_candidates - lines_with_match 
recall = lines_with_match / total_lines * 100		
print("Total lines: ", total_lines)
print("Lines with match: ", lines_with_match)
print("Lines without match: ", lines_without_match)
print("Recall: ", recall)
print("Lines without candidates: ", lines_without_candidates)


				
			
		
		