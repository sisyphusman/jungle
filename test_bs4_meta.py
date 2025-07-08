import re
import random
import requests

from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

tData = requests.get('https://coder-narak.tistory.com/50', headers=headers)
vData = requests.get('https://velog.io/@ubin_ing/use-claude-code-with-figma-mcp', headers=headers)

 # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
tSoup = BeautifulSoup(tData.text, 'html.parser')
vSoup = BeautifulSoup(vData.text, 'html.parser')

tThumbnail_tag = tSoup.find("meta", property="og:image")
tThumbnail_url = tThumbnail_tag['content'] if tThumbnail_tag else None

vThumbnail_tag = vSoup.find("meta", property="og:image")
vTumbnail_url = vThumbnail_tag['content'] if vThumbnail_tag else None

print("Tistory 썸네일 URL:", tThumbnail_url, end="\n")
print("Velog 썸네일 URL:", vTumbnail_url, end="\n")