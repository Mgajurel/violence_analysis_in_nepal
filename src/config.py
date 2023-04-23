import re

# ratopati_re = re.compile(r'''''', re.DOTALL | re.MULTILINE)
# Regex for Insec Online
insec_re =  re.compile(r'''id=\"main\".*?<h2>(?P<title>.*?)</h2>.*?<span class=\"datespan\"> <i class=\"fas fa-calendar-alt\"></i>\s+(?P<date>.*?)\s+</span>.*?<div class=\"main-news\">.*?(?P<main_news>.*?)</div>''', re.MULTILINE | re.DOTALL)

online_re = re.compile(r'''class=\"mb-0\">(?P<title>.*?)</h2>.*?post__time.*?<span>(?P<date>.*?)</span>.*?main__read.*?>(?P<main_news>.*)</div>.*?related-posts-wrap''', re.MULTILINE | re.DOTALL)

ratopati_re = re.compile(r'''class=\"heading\">\n(?P<title>.*?)\n</h2>.*?zmdi-time text-black\"></i>\n<span>(?P<date>.*?)</span>.*?the-content.*?>\n(?P<main_news>.*?)\n</div>''', re.DOTALL | re.MULTILINE)