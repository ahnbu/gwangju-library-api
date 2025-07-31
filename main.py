# main.py (Final Version with Base Call Number)

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

# --- 핵심 로직 함수 ---
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
            return None

        first_book = book_list[0]
        title = first_book.select_one('dt.tit > a').get_text(strip=True).split('. ', 1)[1]

        results = []
        for book in book_list:
            library = book.select_one('dd.site > span:nth-of-type(1)').get_text(strip=True).replace('도서관:', '').strip()

            call_no_full = "정보 없음"
            call_no_element = book.select_one('dd.data > span:nth-of-type(2)')
            if call_no_element:
                call_no_text = call_no_element.contents[0].strip()
                try:
                    call_no_full = call_no_text.split(':')[1].strip()
                except IndexError:
                    call_no_full = call_no_text
            
            # --- [추가] 기본 청구기호 필드 생성 ---
            base_call_no = call_no_full.split('=')[0]

            status = "알 수 없음"
            due_date = "-"
            status_text_element = book.select_one('div.bookStateBar p.txt')
            if status_text_element:
                status_text = status_text_element.get_text(strip=True)
                if '대출가능' in status_text:
                    status = '대출가능'
                elif '대출불가' in status_text:
                    status = '대출불가'
                    if '(반납예정일:' in status_text:
                        try:
                            due_date = status_text.split('(반납예정일:')[1].split(')')[0].strip()
                        except IndexError:
                            due_date = "확인필요"

            results.append({
                '소장도서관': library,
                '청구기호': call_no_full,      # 전체 청구기호 (복본기호 포함)
                '기본청구기호': base_call_no, # 기본 청구기호 (복본기호 제외)
                '대출상태': status,
                '반납예정일': due_date
            })

        return {"book_title": title, "availability": results}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request Timeout: 도서관 서버가 응답하지 않습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# FastAPI 앱 생성
app = FastAPI()

@app.get("/search-book/{isbn}")
async def search_by_isbn_endpoint(isbn: str):
    result = search_book_logic(isbn)
    if result is None:
        raise HTTPException(status_code=404, detail="해당 ISBN의 도서를 찾을 수 없습니다.")
    return JSONResponse(content=result)
