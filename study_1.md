# React + Vite + Tailwind 구축

### 설명

React: UI를 “컴포넌트”로 쪼개서 만드는 프론트엔드 라이브러리

Vite: 개발 중 번개처럼 빠른 핫리로드를 주는 개발 서버 + 빌드 도구(번들러)

Tailwind CSS: CSS를 미리 만들어둔 유틸리티 클래스로 조립하는 스타일 프레임워크

## React + Vite 설치

1. npm create vite@latest
2. Project Name -> vanilla -> js -> no
3. 해당 프로젝트 폴더 이동 후 npm install
4. npm run dev
5. npm i

## Tailwind css 설치

1. npm install tailwindcss @tailwindcss/vite
2. npm install -D postcss autoprefixer
3. vite.config.js 생성 후 아래 내용 복붙

```
// vite.config.js
import { defineConfig } from 'vite';
import tailwind from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwind()],
});
```

# Backend

python3 -m venv .venv
venv\Scripts\Activate

python -m pip install --upgrade pip
python -m pip install fastapi uvicorn[standard] beanie motor pydantic-settings

### 포트 번호

브라우저 → http://localhost:5173 (Vite)
Vite 프록시 → http://localhost:8000 (FastAPI)
FastAPI → mongodb://localhost:27017/crud (MongoDB)
