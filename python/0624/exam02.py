import urllib.request as req
import urllib.parse

url = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp"
values ={
    'stnId' : '184'
}
params = urllib.parse.urlencode(values)
url = url +"?"+params
res = req.urlopen(url)
get_data = res.read().decode("utf-8")

print(get_data)