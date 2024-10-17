# from urllib.request import urlopen
import urllib.request as request

url = "http://uta.pw/shodou/img/28/214.png"
savename = 'testimg01.png'
imsi_img = request.urlopen(url).read()
with open(savename, "wb") as fs:
    fs.write(imsi_img)

