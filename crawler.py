import urllib3
import bs4
import certifi
from nltk import sent_tokenize, word_tokenize, pos_tag

LING = "https://en.wikipedia.org/wiki/Linguistics"

# def get_random_urls(n):
# 	'''
# 	Generate a list of n random Wikipedia urls.
# 	'''
# 	urls = []
# 	for i in range(n):
# 		urls.append("https://en.wikipedia.org/wiki/Special:Random")
# 	return urls

def extract_sents(url="https://en.wikipedia.org/wiki/Special:Random", 
				  num_sents=100, outfile=None):
	'''
	Crawl specified urls, extract text, and optionally write sentences
	between 5 and 15 words to an output file. Otherwise, return list
	of sentences.
	'''
	pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', 
						     ca_certs=certifi.where())
	keep_sents = []
	while len(keep_sents) < num_sents:
		html = pm.urlopen(url=url, method="GET").data
		soup = bs4.BeautifulSoup(html, "lxml")
		page = soup.find_all('p')

		for par in page:
			sents = sent_tokenize(par.text)
			for s in sents:
				if len(keep_sents) < num_sents:
					if '"' in s:
						continue
					elif "(" in s:
						continue
					elif ")" in s:
						continue
					elif "‘" in s:
						continue
					elif "’" in s:
						continue
					elif "http" in s:
						continue
					elif "Last updated:" in s:
						continue
					elif "display" in s:
						continue
					elif "\n" in s:
						continue
					elif "genus" in s:
						continue
					elif "species" in s:
						continue
					else:
						tokens = word_tokenize(s)
						if len(tokens) > 15:
							continue
						elif len(tokens) < 5:
							continue
						elif "[" in tokens:
							continue
						else:
							print("Appending new sentence")
							keep_sents.append(s)
				else:
					break

	if outfile:
		with open(outfile, 'a') as f:
			counter = 1
			for s in keep_sents:
				try:
					# f.write('( utt_{:04} "{}" )\n'.format(counter, s))
					f.write('{}\n'.format(s))
					counter += 1
				except:
					pass
	else:
		return keep_sents

# def fix_random_sents(infile="random_sents_294.txt", outfile="fixed294.txt"):
# 	with open(infile, 'r') as f:
# 		with open(outfile, 'w') as g:
# 			counter = 1
# 			for l in f:
# 				l = l.strip('\n')
# 				g.write('( shannon_{:04} "{}" )\n'.format(counter, l))
# 				counter += 1


def main():
	extract_sents(num_sents=10000, outfile="utts.txt")

if __name__ == "__main__":
	main()