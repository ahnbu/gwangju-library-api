# 광주 시립도서관 도서 검색 API (Gwangju Library Book Availability API)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 프로젝트 소개 (Overview)

본 프로젝트는 **광주광역시 시립도서관**의 도서 소장 정보를 **ISBN**을 기반으로 조회할 수 있는 비공식 API 서버입니다.

광주 시립도서관 웹사이트는 상세 검색 페이지에서 POST 요청을 통해서만 ISBN 검색을 지원합니다. 이 API는 해당 과정을 자동화하여, 간단한 GET 요청만으로 특정 도서의 소장 여부와 상세 정보를 JSON 형태로 쉽게 확인할 수 있도록 개발되었습니다.

## ✨ 주요 기능 (Features)

-   ISBN을 통한 도서 정보 및 소장 현황 검색
-   도서 제목, 소장 도서관, **전체 청구기호(복본기호 포함)**, **기본 청구기호**, 대출 상태, **반납 예정일** 정보 제공
-   결과를 표준 JSON 형식으로 반환하여 다른 서비스와 쉽게 연동 가능
-   Render.com 등 클라우드 플랫폼에 배포할 수 있도록 구성

## 🛠️ 기술 스택 (Tech Stack)

-   **Backend:** Python
-   **API Framework:** FastAPI
-   **HTTP Requests:** Requests
-   **HTML Parsing:** BeautifulSoup4
-   **ASGI Server:** Uvicorn
-   **WSGI Server (for Deployment):** Gunicorn

## 🚀 API 사용법 (API Endpoints)

### 도서 정보 조회

-   **URL:** `/search-book/{isbn}`
-   **Method:** `GET`
-   **URL Params:**
    -   `isbn`: `string` (Required) - 검색하고자 하는 도서의 13자리 ISBN

---

#### ✅ 성공 응답 (Success Response - 200 OK)

API는 도서의 기본 정보와 함께, 각 소장 도서관별 상세 정보를 리스트 형태로 반환합니다.

```json
{
  "book_title": "절제의 기술 : 유혹의 시대를 이기는 5가지 삶의 원칙",
  "availability": [
    {
      "소장도서관": "초월도서관",
      "청구기호": "199.1-브298절=2",
      "기본청구기호": "199.1-브298절",
      "대출상태": "대출가능",
      "반납예정일": "-"
    },
    {
      "소장도서관": "광남도서관",
      "청구기호": "199.1-브298절",
      "기본청구기호": "199.1-브298절",
      "대출상태": "대출불가",
      "반납예정일": "2025.08.09"
    }
  ]
}
```
**필드 설명:**
- `청구기호`: 도서관에서 책을 식별하는 완전한 고유 기호입니다. 동일한 책이 여러 권일 경우, `=` 뒤에 붙는 **복본기호**가 포함될 수 있습니다.
- `기본청구기호`: 복본기호를 제외한 순수 청구기호입니다.
- `반납예정일`: `대출불가` 상태일 때만 날짜가 표시되며, 그 외에는 `"-"`로 표시됩니다.

#### ❌ 실패 응답 (Error Responses)

-   **도서를 찾지 못한 경우 (404 Not Found)**
    ```json
    {
      "detail": "해당 ISBN의 도서를 찾을 수 없습니다."
    }
    ```
-   **도서관 서버 응답이 없는 경우 (408 Request Timeout)**
    ```json
    {
      "detail": "Request Timeout: 도서관 서버가 응답하지 않습니다."
    }
    ```

## ⚙️ 로컬 환경에서 실행하기 (Local Development Setup)

1.  **Git 저장소 복제 (Clone)**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **가상 환경 생성 및 활성화**
    ```bash
    # 가상 환경 생성
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS / Linux
    source venv/bin/activate
    ```

3.  **필요 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API 서버 실행**
    ```bash
    uvicorn main:app --reload
    ```
    `--reload` 플래그는 코드가 변경될 때마다 서버를 자동으로 재시작해줍니다.

5.  **API 테스트**
    -   웹 브라우저에서 `http://127.0.0.1:8000/search-book/9791130629353` 로 접속하여 결과를 확인합니다.
    -   자동 생성된 API 문서는 `http://127.0.0.1:8000/docs` 에서 확인할 수 있습니다.

## ☁️ 배포하기 (Deployment)

이 프로젝트는 Python 백엔드를 상시 실행하는 **Render.com**에 배포하는 것을 추천합니다. (Vercel, Netlify는 서버리스 함수의 실행 시간제한으로 인해 크롤링 작업에 부적합합니다.)

1.  **GitHub에 프로젝트 Push:** `main.py`와 `requirements.txt`가 포함된 프로젝트를 GitHub 저장소에 Push합니다.

2.  **Render.com 설정:**
    -   [Render](https://render.com/)에 GitHub 계정으로 가입합니다.
    -   **[New +]** > **[Web Service]**를 선택하여 GitHub 저장소를 연결합니다.
    -   아래와 같이 배포 설정을 입력합니다.
        -   **Name**: `gwangju-library-api` (자유롭게 지정)
        -   **Region**: Singapore (또는 가까운 지역)
        -   **Build Command**: `pip install -r requirements.txt`
        -   **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
        -   **Instance Type**: `Free` 선택

3.  **배포 완료:** **[Create Web Service]**를 클릭하면 배포가 자동으로 시작됩니다. 몇 분 후 `https://your-service-name.onrender.com` 형태의 공개 URL이 생성됩니다.

## 📁 파일 구조 (File Structure)

```
.
├── main.py           # FastAPI 애플리케이션 로직
├── requirements.txt  # 프로젝트 의존성 라이브러리 목록
└── README.md         # 프로젝트 설명 파일
```

## 📄 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)에 따라 배포됩니다.
