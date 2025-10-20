# CRUD 기본 틀

FastAPI + MongoDB(Be0anie) 백엔드와 Vite(바닐라 JS, Tailwind) 프론트엔드로 구성된 간단 CRUD 스켈레톤입니다. Post 엔티티 기준으로 생성/조회/수정/삭제가 동작합니다.

## 요구 사항

- Python 3.11+
- Node.js 18+
- 로컬 MongoDB 6+ (또는 Docker)

## 백엔드 실행 (FastAPI)

PowerShell 기준 명령어입니다.

```
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

기본 DB 접속: `mongodb://localhost:27017/crud` (`backend/app/core/config.py`)

헬스체크: http://localhost:8000/health

## MongoDB (선택: Docker)

로컬에 MongoDB가 없다면 Docker로 띄울 수 있습니다.

```
docker run -d --name jungle-crud-mongo -p 27017:27017 mongo:6
```

## 프론트엔드 실행 (Vite)

개발 서버는 `/api` 경로를 `http://localhost:8000`으로 프록시합니다.

```
cd frontend
npm ci
npm run dev
```

접속: http://localhost:5173/home.html

## 주요 엔드포인트

- POST `/api/v1/posts/` 글 생성
- GET `/api/v1/posts/` 전체 목록
- GET `/api/v1/posts/{id}` 단건 조회
- PATCH `/api/v1/posts/{id}` 부분 수정
- DELETE `/api/v1/posts/{id}` 삭제

요청/응답 스키마는 `backend/app/models/post.py` 참고

## 폴더 구조 개요

- `backend/app/main.py` FastAPI 앱 초기화, Beanie/Mongo 연결, 라우터 등록
- `backend/app/models/post.py` Post 도큐먼트 및 DTO
- `backend/app/routers/posts.py` Post CRUD API 라우터
- `frontend/vite.config.js` 개발 프록시 설정(`/api` -> `localhost:8000`)
- `frontend/home.html`, `frontend/src/home.js` 간단 CRUD UI

## 참고

- CORS: `http://localhost:5173` 허용되어 있습니다.
- 위치값(GeoJSON Point) 저장을 위한 `location` 필드가 포함되어 있으며 2dsphere 인덱스를 초기화 시 생성합니다. 사용하지 않아도 무방합니다.
