
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
python crawler.py https://www.google.ca
```

Depending on your use case, you can choose to add stuff like don't retrieve #comment pages or image links.

I found this script useful for mass archiving links in the Internet Archive.