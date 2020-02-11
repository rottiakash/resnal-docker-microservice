import requests
import bs4
from lxml import html
import pytesseract
from PIL import Image
import re

s = requests.Session()
headers = {'Referer': 'http://results.vtu.ac.in/resultsvitavicbcs_19/index.php',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                'Upgrade-Insecure-Requests': '1',  'Cookie': 'PHPSESSID=p0er4ucik6ieka4f7lh1h2sn47'
        , 'Connection': 'keep-alive'}
image = s.get("http://results.vtu.ac.in/resultsvitavicbcs_19/captcha_new.php", headers=headers)
with open("snap.png", 'wb') as file:
    file.write(image.content)
cap = pytesseract.image_to_string("snap.png")
USN = "1BI15CS177"
url = "http://results.vtu.ac.in/resultsvitavicbcs_19/resultpage.php"

# url = "http://results.vtu.ac.in/resultsvitavicbcs_19/resultpage.php"
result = requests.get(url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='token']/@value")))[0]
payload = {'lns': USN, 'captchacode': str(cap),
                'token': authenticity_token,
                'current_url': 'http://results.vtu.ac.in/resultsvitavicbcs_19/index.php'}
page = requests.post(url, data=payload, headers=headers)
tree = html.fromstring(page.content)
soup = bs4.BeautifulSoup(page.text,"html.parser")
containers = soup.find_all('div', class_ = 'divTableCell')

copymarks = []
marks = []
imarks = []
emarks = []
scode = []
sname = []
index = [10,16,22,28,34,40,46,52]
index1 = [8,14,20,26,32,38,44,50]
index2 = [9,15,21,27,33,39,45,51]
index3 = [6,12,18,24,30,36,42,48]
index4 = [7,13,19,25,31,37,43,49]
low = 0
high = 5
tg = 26.

for ind in index:
    marks.append((containers[ind].text).encode('utf-8'))
    copymarks.append((containers[ind].text).encode('utf-8'))
for ind in index1:
    imarks.append((containers[ind].text).encode('utf-8'))
for ind in index2:
    emarks.append((containers[ind].text).encode('utf-8'))
for ind in index3:
    scode.append((containers[ind].text))
for ind in index4:
    sname.append((containers[ind].text))
# marks.append((containers[16].text).encode('utf-8'))
# marks.append((containers[22].text).encode('utf-8'))
# marks.append((containers[28].text).encode('utf-8'))
# marks.append((containers[34].text).encode('utf-8'))
# marks.append((containers[40].text).encode('utf-8'))
# marks.append((containers[46].text).encode('utf-8'))
# marks.append((containers[52].text).encode('utf-8'))
for i in range(len(marks)):
    marks[i] = float(marks[i])
for i in range(len(imarks)):
    imarks[i] = float(imarks[i])
for i in range(len(emarks)):
    emarks[i] = float(emarks[i])



for i in range(low,high):
    if(marks[i]<40):
        marks[i] = 0
    elif(marks[i]<45):
        marks[i] = 4*4  
    elif(marks[i]<50):
        marks[i] = 5*4
    elif(marks[i]<60):
        marks[i] = 6*4
    elif(marks[i]<70):
        marks[i] = 7*4
    elif(marks[i]<80):
        marks[i] = 8*4
    elif(marks[i]<90):
        marks[i] = 9*4
    else:
        marks[i] = 10*4

for i in range(len(scode)):
    x = re.search(r'[0-9][0-9][0-9]', str(scode[i]))
    if(x is not None):
        marks[i] = int((marks[i]*3)/4)
    
    
for i in range(high,high+3):
    if(marks[i]<40):
        marks[i] = 0
    elif(marks[i]<45):
        marks[i] = 2*4
    elif(marks[i]<50):
        marks[i] = 2*5
    elif(marks[i]<60):
        marks[i] = 2*6
    elif(marks[i]<70):
        marks[i] = 2*7
    elif(marks[i]<80):
        marks[i] = 2*8
    elif(marks[i]<90):
        marks[i] = 2*9
    else:
        marks[i] = 2*10

print(marks)
print(sname)
print(scode)


#The search() function returns a Match object:

