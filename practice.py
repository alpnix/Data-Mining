import re
import pprint
from bs4 import BeautifulSoup
import requests


domain = "https://www.imdb.com"
top250 = "/chart/top/?ref_=nv_mv_250"
url = domain + top250

page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")


# beautiful soup testing

def has30classes(classes):
    return classes != None and len(classes) == 30

for elem in soup.find_all(class_=has30classes):
    print(elem.get_text)

# an element that's id only contains letters between a to r
print(soup.find(id=re.compile("^[a-r]*$")))

# () and find_all methods
print(soup("a") == soup.find_all("a"))
print(soup.title(string=True))

# find parent, find sibling
print(soup.find_parent("div"))
print(soup.title.find_next_sibling("link"))
print(soup.a.find_parent("div"))

# previous sibling, next sibling
print(soup.title.find_previous_sibling())
print(soup.title.find_next_sibling())

# find next, find previous
print()
print(soup.title.find_previous())
print(soup.title.find_next())

# soup select methods
print(soup.select("body a"))
print(soup.select("table > thead"))
print(soup.select("a[title]"))

# modifying the dom
soup.a.name = "b"
tag = soup.a
tag.string = "Alp's Calendar"
tag.append(", Hello World")
print(tag)
print(tag.contents)
print(tag.get_text())

new_b = soup.new_tag("b")
new_b.string = "This is a new tag "
tag.insert(0,new_b)
tag.smooth()
print(tag.encode())
print(tag.decode())
"""
printer = pprint.PrettyPrinter()
printer.pprint(soup.head)
"""
# formatter
from bs4.formatter import HTMLFormatter
def uppercase(str):
    return str.upper()
formatter = HTMLFormatter(uppercase)
print(tag.prettify(formatter=formatter))
# comments
from bs4.element import Comment
my_comment = Comment("This is a comment")
tag.insert(2,my_comment)
print(tag.prettify(formatter=formatter))
print(tag.get_text())

print(soup("a") == soup.find_all("a"))


