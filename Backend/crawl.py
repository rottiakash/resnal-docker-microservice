from resanal.models import Fetch,Result
import xlrd
import requests
from lxml import html
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

post_payload = {'Token': '55af47bae3a4104902c28cea54dcce98ae34318b', 'captchacode': 'iV4DKr'}
post_headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
  'Accept': '*/*',
  'Cache-Control': 'no-cache',
  'Postman-Token': '864cb406-0cf9-4518-93aa-66023eef8e00',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://results.vtu.ac.in/_CBCS/resultpage.php?lns=1BI17CS010&captchacode=uFPXjv&Token=9da2da7349afd3ed906f17e8fbf3d284a55b29ba',
  'Connection': 'keep-alive'
}

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import numpy as np
import cv2

def getNewSession():
    url = "https://results.vtu.ac.in/_CBCS/index.php"

    headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
  'Accept': '*/*',
  'Cache-Control': 'no-cache',
  'Postman-Token': 'b222b1f1-1fed-4490-965a-805f53a28e97',
  'Host': 'results.vtu.ac.in',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}
    response = requests.request("GET", url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_url = "https://results.vtu.ac.in"+(soup.find_all('img')[1])['src']
    token = soup.find_all('input',attrs={'name':"Token"})
    post_payload['Token'] = token[0]['value']
    img_headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
  'Accept': '*/*',
  'Cache-Control': 'no-cache',
  'Postman-Token': '063fdb07-fe60-466a-be5e-fe08dec56a21',
  'Host': 'results.vtu.ac.in',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}
    img_headers['Cookie'] = str(response.headers['Set-Cookie']).rstrip("; path=/'")
    post_headers['Cookie'] = img_headers['Cookie']
    response = requests.request("GET", img_url, headers=img_headers,verify=False)
    with open("cap.png", 'wb') as file:
        file.write(response.content)
    image = cv2.imread("cap.png")
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([-10,-10,62])
    upper = np.array([10,10,142])
    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(result, result, mask=mask)
    cv2.imwrite('mask.png', mask)
    cv2.imwrite('out.png', image)
    cv2.imwrite('result.png', result)
    cv2.waitKey()
    post_payload['captchacode'] = pytesseract.image_to_string(Image.open("mask.png"))

def getResult(USN):
    post_payload['lns'] = USN
    url = "https://results.vtu.ac.in/_CBCS/resultpage.php"
    res = requests.request("POST", url, headers=post_headers, data = post_payload, verify=False)
    if 'Invalid captcha code !!!' in res.text:
        print("Invalid Captcha, getting new session")
        getNewSession()
        return(getResult(USN))
    elif "Redirecting to VTU Results Site" in res.text:
        getNewSession()
        return(getResult(USN))
    elif "University Seat Number is not available or Invalid..!" in res.text:
        return 404
    elif "Please check website after 4 hour --- !!!" in res.text:
        print("IP BLOCKED...CHECK PROXY...PRESS ANY KEY TO CONTINUE")
        input()
        getResult(USN)
    elif "Semester : 5" in res.text:
        soup = BeautifulSoup(res.content, 'html.parser')
        result = [soup.find_all('td')[3].text.lstrip(' : ')]
        table = soup.find_all('div',attrs={'class':'divTable'})[0]
        rows = table.find_all('div',attrs={'class':'divTableRow'})[1:]
        for row in rows:
            sub = {}
            cells = row.find_all('div',attrs={'class':'divTableCell'})
            sub['subcode'] = cells[0].text
            sub['subname'] = cells[1].text
            sub['ia'] = cells[2].text
            sub['ea'] = cells[3].text
            sub['total'] = cells[4].text
            sub['result'] = cells[5].text
            result.append(sub)
        return result
    elif "Semester" in res.text:
        return 404
    else:
        getNewSession()
        return(getResult(USN))

# Django Part
book = xlrd.open_workbook('1BI17CS.xlsx')
first_sheet = book.sheet_by_index(0)
i = 1
while True:
    if first_sheet.cell_value(i,0) == "end":
        break
    USN = first_sheet.cell_value(i,0)
    print("USN:-"+first_sheet.cell_value(i,0))
    res = getResult(USN)
    if(res==404):
        print("USN Invalid")
        i += 1
    else:
        result = Result()
        result.name = res[0]
        print(result.name)
        res = res[1:]
        result.usn = USN
        result.sem = 5
        result.section = first_sheet.cell_value(i,1)
        result.batch = 2017
        result.save()
        for r in res:
            fetch = Fetch()
            fetch.usn = result
            fetch.subcode = r['subcode']
            fetch.subname = r['subname']
            fetch.intmarks = r['ia']
            fetch.extmarks = r['ea']
            fetch.totalmarks = r['total']
            fetch.save()
        i += 1
print("Done")