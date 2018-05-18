def get_diphones(mlf):
	'''
	Open MLF for utts and return a dictionary with utts as keys and a
	list of diphones (tuples) as values.
	'''
	utts_list = []
	with open(mlf, 'r') as f:
		for line in f:
			utts_list.append(line.strip())

	utts_str = "|".join(utts_list)
	utts_list = utts_str.split("#!MLF!#")
	utts_list2 = []
	for u in utts_list:
		u2 = u.split("|")
		if len(u2) > 1:
			utts_list2.append(u2[1:-1])

	diphones = {}
	for utt in utts_list2:
		for i, phone in enumerate(utt):
			if i == 0:
				continue
			elif i < len(utt)-1:
				try:
					diphones[utt[0]].append(((utt[i], utt[i+1])))
				except:
					diphones[utt[0]] = [(utt[i], utt[i+1])]

	return diphones


def initialize_wishlist(utts_dict):
	'''
	Given a dictionary of utts and their diphone sequences, make a 
	wishlist of all diphones present in the utts dictionary.
	'''
	wishlist = []
	for utt, seq in utts_dict.items():
		for diphone in seq:
			wishlist.append(diphone)

	return set(wishlist)


def rank_utts(diphones, wishlist):
	'''
	Given a dictionary of utts and their diphone sequences and a 
	wishlist of diphones, return a list of utts and scores ranked 
	by diphone coverage, from greatest to least.
	'''
	utt_scores = {}
	for utt, seq in diphones.items():
		score = 0
		for diph in set(seq):
			if diph in wishlist:
				score += 1
		utt_scores[utt] = score 

	scored_utts = list(utt_scores.items())
	ranked_utts = sorted(scored_utts, key=lambda x: x[1], reverse=True)
	return ranked_utts


def select_utts(wishlist, utts_dict, len_limit):
	'''
	Given a dictionary of utts and their diphone sequences, a wishlist
	of diphones, and a length limit for the number of selected utts, 
	create a list of the best ranked utts, updating the wishlist and 
	rescoring after each new utt is added.
	'''
	init_wishlist = set([x for x in wishlist])
	selected_utts = []
	while len(selected_utts) < len_limit:
		if len(wishlist) == 0:
			wishlist = set([x for x in init_wishlist])
		# rank utts
		ranked_utts = rank_utts(utts_dict, wishlist)

		# pick best utt and add to list
		best = ranked_utts[0][0]
		selected_utts.append(best)	

		# update wishlist
		for diph in utts_dict[best]:
			try:
				wishlist.remove(diph)
			except:
				pass

		# pop selected utt from utts dict
		del utts_dict[best]

	return selected_utts


def main(outfile="selected_utts2.txt", utts_source="shannon_utts.txt", 
		 mlf='shannon_utts.mlf', write=True):
	utts_dict = get_diphones(mlf)
	wishlist = initialize_wishlist(utts_dict)
	selected_utts = select_utts(wishlist, utts_dict, 1500)

	# get indices for selected utts
	utt_indices = []
	for utt in selected_utts:
		utt_indices.append(int(utt[11:15]))

	# write selected utts to file
	if write:
		with open(outfile, 'a', encoding='utf8') as f:
			with open(utts_source, 'r', encoding='utf8') as g:
				lines = g.readlines()
				for i in utt_indices:
					f.write(lines[i])



if __name__ == '__main__':
	main()