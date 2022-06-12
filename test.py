from urllib.request import urlopen
from urllib.parse import quote_plus as qp # 아스키코드로 변환
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from flask import Flask, render_template
from flask import request, redirect
 
app = Flask(__name__)


@app.route('/crawling/')
def crawling():
    tag = request.args.get('tag')
    baseUrl = 'https://www.instagram.com/explore/tags/'
    plusUrl = tag
    url = baseUrl + qp(plusUrl)

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html)

    insta = soup.select('.v1Nh3.kIKUG._bz0w') # 이미지 클래스명

    # 이미지 수집, 저장하기
    # 참고로, 이미지추가하는 스크롤 기능 미사용
    n = 1 # 이미지 순번

    for i in insta :
        print('https://www.instagram.com'+i.a['href']) # a태그의 속성 href만 가져오기
        imgUrl = i.select_one('.KL4Bh').img['src'] # 이미지가 속한 태그 > src태그만 가져오기
        
        # 이미지 저장하기
        with urlopen(imgUrl) as f : 
            # 저장위치 : img폴더
            # 파일명 : 검색어 + 순서, 확장자 : jpg, 이미지파일쓰기 : wb
            with open('./static/img/' + plusUrl + str(n) + '.jpg', 'wb') as h :
                img = f.read()
                h.write(img)
            n += 1
    
    driver.quit() # 작업완료후 웹드라이버 종료

    resultUrl = '/result/'+str(tag)+'/'

    return redirect(resultUrl)


@app.route('/')
def index():
    return f'''
        <!doctype html>
            <html>
                <body>
                    <h1>태그 입력</h1>
                    <form action=/crawling/ method="GET">
                        <input type="text" name="tag" placeholder="태그입력">
                        <input type="submit" value="크롤링">
                    </form>
                </body>
            </html>
    '''

@app.route('/result/<tag>/')
def result(tag):
    TAG = str(tag)
    return render_template('result.html', tag = TAG)

app.run(debug=True)
