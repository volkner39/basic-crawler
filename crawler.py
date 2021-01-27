import sys
import httplib2
import urllib
from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import time

s = {}
main_urls = []
external_links = set()
weird_links = set()

# Problems:
# - not recognizing the main site url

def rec(current_url, url):

	# make HTTP connection
	try:
		http = httplib2.Http()
		status, response = http.request(current_url)
	except:
		print("Couldn't connect lol...")
		weird_links.add(current_url)
		return

	try:
		# get all links on current page
		for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
			if link.has_attr('href'):
			
				if ("#comment" not in link['href']) and ("#respond" not in link['href']):
			
					# remove the ending '/' to prevent duplicates
					link['href'] = link['href'].rstrip('/')
			
					# absolute links
					if link['href'][:4] == 'http':
						if (url not in link['href']):
							external_links.add(link['href'])
						else:
							main_urls.append(link['href'])
					
					# relative links
					elif (len(link['href']) > 1) and (link['href'][0] == '/'):
						# join main url with relative link
						new_url = urljoin(current_url, link['href'])
						main_urls.append(new_url)
				
					# weird links
					else:
					
						if "#comment" not in current_url:
							main_urls.append(urljoin(current_url, link['href']))
									
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
	f = open("main_urls" + ' - ' + url + ".txt", "w")
	f1 = open("externals" + ' - ' + url + ".txt", "w")
	f2 = open("weird" + ' - ' + url + ".txt", "w")
	
	for x in sorted(s):
		f.write(x + '\n')
	
	f.close()
	
	for y in sorted(external_links):
		f1.write(y + '\n')
	
	f1.close()
	
	for z in sorted(weird_links):
		f2.write(z + '\n')
		
	f2.close()
	
	print("--- %s seconds ---" % (time.time() - start_time))
