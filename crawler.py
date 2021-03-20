import os
import sys
import httplib2
import urllib
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, SoupStrainer
import time

# Problems:
# - redirection links that contain the main url
# - add %20 to links with spaces

# links
# #
# ?
# /relative
# relative
# mailto

# dict to store urls we visited
s = {}

# classify and store urls
main_urls = []
external_links = set()
weird_links = set()

# black-listed words
skip = {"&url=", "#", ".svg", ".jpg", ".jpeg", ".png", ".gif"}

# checks if main url is inside the current url we're looking at
# excluding re-directs and web-archives
def check_url(main_url, current_url):
	res = current_url.split(main_url)
	return res[0] == "" and len(res) == 2

def rec(current_url, url):

	# make HTTP connection
	try:
		http = httplib2.Http()
		status, response = http.request(current_url)
	except:
		print("Couldn't connect...")
		weird_links.add(current_url)
		return

	try:
		# get all links on current page
		for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
			
			skip_flag = False
			if link.has_attr('href'):

				# remove the ending '/' to prevent duplicates
				link['href'] = link['href'].rstrip('/')
				
				# check black-listed words
				for s in skip:
					if s in link['href']:
						skip_flag = True
				
				# if the link is not black-listed
				if (not skip_flag):
				
					# check absolute links
					if link['href'][:4] == 'http':
						if (check_url(url + '/', link['href'])):
							main_urls.append(link['href'].replace(" ", "%20"))
						else:
							external_links.add(link['href'].replace(" ", "%20"))

					# check relative links
					elif (len(link['href']) > 0) and ((link['href'][0] == '/') or (link['href'][0] == '#')):
						# join main url with a relative link
						new_url = urljoin(current_url, link['href'])
						if (check_url(url + '/', new_url)):
							main_urls.append(new_url.replace(" ", "%20"))
						else:
							external_links.add(link['href'].replace(" ", "%20"))

					# weird links - links that don't fit the prior criteria
					else:
						weird_links.add(link['href'])

	except TypeError:
		print("Undefined coding")


if __name__ == "__main__":

	start_time = time.time()
	url = sys.argv[1]

	# first call to original link
	rec(url.rstrip('/'), url.rstrip('/'))
	s[url] = 1

	# loop through growing list of main urls
	i = 0
	while(i < len(main_urls)):

		main_urls[i] = main_urls[i].rstrip('/')
		# check for duplicate links
		if (main_urls[i] not in s.keys()):
			rec(main_urls[i], url.rstrip('/'))

			# set link as checked in dict
			s[main_urls[i]] = 1
			print(main_urls[i])
		i += 1


	# write all links found to a text file
	folder = os.path.dirname(os.path.abspath(__file__))
	file1 = os.path.join(folder, 'main_urls_' + str(urlsplit(url).netloc) + '.txt')
	file2 = os.path.join(folder, 'externals_' + str(urlsplit(url).netloc) + '.txt')
	file3 = os.path.join(folder, 'weird_' + str(urlsplit(url).netloc) + '.txt')

	with open(file1, "w+", encoding='utf-8') as f:
		for x in sorted(s):
			f.write(x + '\n')

		f.close()

	with open(file2, "w+", encoding='utf-8') as f1:
		for y in sorted(external_links):
			f1.write(y + '\n')

		f1.close()

	with open(file3, "w+", encoding='utf-8') as f2:
		for z in sorted(weird_links):
			f2.write(z + '\n')

		f2.close()

	print("--- %s seconds ---" % (time.time() - start_time))
