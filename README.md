네, 아주 좋은 생각입니다. API를 안정적으로 운영하기 위한 Uptime Robot 설정은 프로젝트의 완성도를 높이는 중요한 부분이므로, `README.md`에 포함하는 것이 매우 바람직합니다.

프로젝트 배포 후 유지보수 단계까지 친절하게 안내하는 최종 `README.md` 파일을 작성해 드리겠습니다.

---

### 최종 `README.md` (Uptime Robot 가이드 포함)

```markdown
# 경기도 광주시 시립도서관 도서 검색 API (Gyeonggi-do Gwangju City Library API)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 프로젝트 소개 (Overview)

본 프로젝트는 **경기도 광주시 시립도서관**의 도서 소장 정보를 **ISBN**을 기반으로 조회할 수 있는 비공식 API 서버입니다.

경기도 광주시 시립도서관 웹사이트는 상세 검색 페이지에서 POST 요청을 통해서만 ISBN 검색을 지원합니다. 이 API는 해당 과정을 자동화하여, 간단한 GET 요청만으로 특정 도서의 소장 여부와 상세 정보를 JSON 형태로 쉽게 확인할 수 있도록 개발되었습니다.

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

5.  **API 테스트**
    -   웹 브라우저에서 `http://127.0.0.1:8000/search-book/9791130629353` 로 접속합니다.
    -   자동 생성된 API 문서는 `http://127.0.0.1:8000/docs` 에서 확인할 수 있습니다.

## ☁️ 배포하기 (Deployment)

이 프로젝트는 Python 백엔드를 상시 실행하는 **Render.com**에 배포하는 것을 추천합니다. (Vercel, Netlify는 서버리스 함수의 실행 시간제한으로 인해 크롤링 작업에 부적합합니다.)

1.  **GitHub에 프로젝트 Push:** `main.py`와 `requirements.txt`가 포함된 프로젝트를 GitHub 저장소에 Push합니다.

2.  **Render.com 설정:**
    -   [Render](https://render.com/)에 GitHub 계정으로 가입합니다.
    -   **[New +]** > **[Web Service]**를 선택하여 GitHub 저장소를 연결합니다.
    -   아래와 같이 배포 설정을 입력합니다.
        -   **Name**: `gyeonggi-gwangju-library-api` (자유롭게 지정)
        -   **Region**: Singapore (또는 가까운 지역)
        -   **Build Command**: `pip install -r requirements.txt`
        -   **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`
        -   **Instance Type**: `Free` 선택

3.  **배포 완료:** **[Create Web Service]**를 클릭하면 배포가 자동으로 시작됩니다. 몇 분 후 `https://your-service-name.onrender.com` 형태의 공개 URL이 생성됩니다.

## 💡 서버 유지보수: Spin Down 방지하기 (Uptime Robot 설정)

Render의 무료 요금제는 15분간 요청이 없으면 서버를 **슬립 모드(Spin Down)**로 전환합니다. 이 상태에서 다시 요청이 오면 서버가 깨어나는 데 30초 이상 소요될 수 있습니다. 이를 방지하고 API가 항상 즉시 응답하도록 설정합니다.

### 1단계: 헬스 체크 엔드포인트 확인

`main.py`에는 서버의 상태를 확인하는 가벼운 엔드포인트(`/`)가 이미 포함되어 있습니다. 이 주소로 주기적인 요청을 보내 서버를 깨워둘 것입니다.

### 2단계: Uptime Robot 설정

**Uptime Robot**은 지정된 URL을 주기적으로 호출해주는 무료 모니터링 서비스입니다.

1.  [Uptime Robot 웹사이트](https://uptimerobot.com/)로 이동하여 무료 계정을 생성합니다.
2.  로그인 후, 대시보드에서 **[+ Add New Monitor]** 버튼을 클릭합니다.
3.  아래와 같이 모니터 설정을 입력합니다.
    -   **Monitor Type**: `HTTP(S)`
    -   **Friendly Name**: `My Gwangju Library API` (식별하기 쉬운 이름)
    -   **URL or IP**: **Render에서 생성된 내 서비스의 기본 URL** (예: `https://gyeonggi-gwangju-library-api.onrender.com/`)
    -   **Monitoring Interval**: `10 minutes` (15분보다 짧아야 합니다)
4.  **[Create Monitor]** 버튼을 클릭하여 설정을 완료합니다.

이제 Uptime Robot이 10분마다 API 서버를 호출하여, 서버가 잠들지 않고 항상 즉시 응답할 수 있도록 유지해줍니다.

## 📁 파일 구조 (File Structure)

```
.
├── main.py           # FastAPI 애플리케이션 로직
├── requirements.txt  # 프로젝트 의존성 라이브러리 목록
└── README.md         # 프로젝트 설명 파일
```

## 📄 라이선스 (License)

이 프로젝트는 [MIT License](LICENSE)에 따라 배포됩니다.
```
