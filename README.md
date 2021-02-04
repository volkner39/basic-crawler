
# basic-crawler

## Dependencies:
* Python 3.5+
* pip install sys
* pip install bs4
* pip install time
* pip install httplib2
* pip install urllib

---

## crawler.py

A basic tool that grabs all the 'a' links from a website.

### Usage:

```
python crawler.py https://www.fsf.org
```

Depending on your use case, you can choose to add stuff like don't retrieve #comment pages or image links.

Useful for mass archiving links into the Internet Archive.

Disclaimer:
It is illegal to scrape websites without their permission. You can look at the robots.txt file hosted on the website to ensure if this is the case or not. I do not take any responsibility or hold any liability for your actions.