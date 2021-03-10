def soup_tohtml():
  body = (await page.content()).encode("utf8")
  soup = BeautifulSoup(body, "lxml")
  with open("output1.html", "w", encoding='utf-8') as file:
    file.write(str(soup))

def html_tojson():
  