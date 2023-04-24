import re

# ratopati_re = re.compile(r'''''', re.DOTALL | re.MULTILINE)
# Regex for Insec Online
insec_re = re.compile(r'''id=\"main\".*?<h2>(?P<title>.*?)</h2>.*?<span class=\"datespan\"> <i class=\"fas fa-calendar-alt\"></i>\s+(?P<date>.*?)\s+</span>.*?<div class=\"main-news\">.*?(?P<main_news>.*?)</div>''', re.MULTILINE | re.DOTALL)

online_re = re.compile(r'''class=\"mb-0\">(?P<title>.*?)</h2>.*?post__time.*?<span>(?P<date>.*?)</span>.*?main__read.*?>(?P<main_news>.*)</div>.*?related-posts-wrap''', re.MULTILINE | re.DOTALL)

ratopati_re = re.compile(r'''class=\"heading\">\n(?P<title>.*?)\n</h2>.*?zmdi-time text-black\"></i>\n<span>(?P<date>.*?)</span>.*?the-content.*?>\n(?P<main_news>.*?)\n</div>''', re.DOTALL | re.MULTILINE)

dineskhabar_re = re.compile(r'''<h1.*?>\n(?P<title>[\u0900-\u097F\s\S]+)</h1>.*?<span>\n(?P<date>[०१२३४५६७८९]{4}\s[\u0900-\u097F]+\s[०१२३४५६७८९]{1,2},\s[०१२३४५६७८९]{2}:[०१२३४५६७८९]{2})\s*</span>.*?<div class=\"article_body(?P<main_news>.*?)loadDisqus''', re.DOTALL | re.MULTILINE)

nayapatrika_re = ratopati_re = re.compile(r'''<h1>(?P<title>[\u0900-\u097F\s\S]+)</h1>.*?main-dates\">\n\s+<span><i class=\"fa fa-clock\"></i>(?P<date>(?:\")?२०[०१२३४५६७८९]{2}\s+[\u0900-\u097F]+\s+[०१२३४५६७८९]{1,2}\s+[\u0900-\u097F]+\s+[०१२३४५६७८९]{2}\:[०१२३४५६७८९]{2}:[०१२३४५६७८९]{2})(?:\")?</span>(?P<main_news>.*?)main-share''', re.DOTALL | re.MULTILINE)

# setopati_re = re.compile(r'''<h1\sclass=\"news\-big\-title\">(?P<title>[\u0900-\u097F\s\–\-]+)</h1>.*?detail\-box(?P<main_news>.*?).*pub-date\">(?P<date>.*?)</span>''', re.DOTALL | re.MULTILINE)

khabarhub_re = re.compile(r'''<h1\sclass=\"single-title\">(?P<title>[\u0900-\u097F\s\–\-,]+)</h1>.*?<p\s+class=\"single-date\">(?P<date>.*?)(?:\n)?</p>.*?<div class=\"post-entry\">(?P<main_news>.*?)single-date''', re.DOTALL | re.MULTILINE)

