from bs4 import BeautifulSoup
import requests
SEARCH_ENDPOINT = 'http://wordassociations.net/search?hl=en&w='
def make_request(word):
	# headers needed to simulate browsers. 
	headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 'referer' : 'http://wordassociations.net/search?hl=en&w=' + word}
	return requests.post(SEARCH_ENDPOINT + word, headers=headers).text

def find_associations(word):
	html_str = make_request(word)
	# print(html_str)
	associations = []
	parsed_str = BeautifulSoup(html_str, 'html.parser')
	content_level = parsed_str.body.div.find_all('div')[0]
	for d in content_level.find_all('div'):
		if d['class'][0] == 'n-content':
			all_li_elems = d.find_all('li')
			for item in all_li_elems:
				associations.append(item.string)
	return associations

def print_table(n_cols, l):
	l_bound, r_bound = 0, n_cols
	while l_bound < len(l):
		# splicing is safe with invalid indices, so this resolves all edge cases.
		print(" | ".join(l[l_bound:r_bound]))
		l_bound = r_bound
		r_bound = r_bound + n_cols

def listen():
	while 1:
		print('Enter word to find associations for: ')
		word = str(input()).strip()
		associations = find_associations(word)
		if len(associations) == 0:
			print('No associations were found with this word.')
		else:
			print_table(5, associations)

listen()
