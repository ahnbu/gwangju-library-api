# 필요한 라이브러리 설치
# 터미널에서: pip install fastapi uvicorn "python-multipart" requests beautifulsoup4 pandas

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Jupyter Notebook에서 작성했던 함수를 여기에 그대로 붙여넣습니다 ---
def search_book_logic(isbn: str):
    url = "https://lib.gjcity.go.kr:8443/kolaseek/plus/search/plusSearchResultList.do"
    payload = {
        'searchType': 'DETAIL', 'searchKey5': 'ISBN', 'searchKeyword5': isbn,
        'searchLibrary': 'ALL', 'searchSort': 'SIMILAR', 'searchRecordCount': '30'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Referer': 'https://lib.gjcity.go.kr:8443/kolaseek/plus/search/plusSearchDetail.do'
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        book_list = soup.select('ul.resultList.imageType > li')
        if not book_list:
            return None # 결과가 없으면 None 반환

        # 도서 기본 정보 추출 (첫 번째 항목 기준)
        first_book = book_list[0]
        title = first_book.select_one('dt.tit > a').get_text(strip=True).split('. ', 1)[1]
        
        # 소장 정보 추출
        results = []
        for book in book_list:
            # (이전 코드와 동일한 정보 추출 로직)
            library = book.select_one('dd.site > span:nth-of-type(1)').get_text(strip=True).replace('도서관:', '').strip()
            status_text = book.select_one('div.bookStateBar p.txt').get_text(strip=True)
            status = '✅ 대출가능' if '대출가능' in status_text else '❌ 대출불가'
            
            results.append({
                '소장도서관': library,
                '대출상태': status,
            })
            
        df = pd.DataFrame(results)
        
        # 기본 정보와 소장 목록을 함께 반환
        return {"book_title": title, "availability": df.to_dict('records')}

    except requests.exceptions.Timeout:
        # 타임아웃 발생 시 특정 에러 코드를 반환하도록 처리
        raise HTTPException(status_code=408, detail="Request Timeout: 도서관 서버가 응답하지 않습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# FastAPI 앱 생성
app = FastAPI()

@app.get("/search/{isbn}")
async def search_by_isbn_endpoint(isbn: str):
    """
    ISBN을 받아 광주 도서관의 도서 정보를 JSON 형태로 반환하는 API 엔드포인트
    """
    result = search_book_logic(isbn)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found for the given ISBN.")
        
    return JSONResponse(content=result)

# 로컬에서 테스트 실행 방법:
# 1. 위 코드를 main.py로 저장
# 2. 터미널에서 uvicorn main:app --reload 실행
# 3. 웹 브라우저에서 http://127.0.0.1:8000/search/9791130629353 로 접속하여 결과 확인
# 4. 자동 생성된 API 문서: http://127.0.0.1:8000/docs