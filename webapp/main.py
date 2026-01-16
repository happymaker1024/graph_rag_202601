from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles


from movie_recommend import main_chain

app = FastAPI(
    title="영화 추천 API",
    description="영화 필모그래피 추천 서비스입니다.",
    version="1.0.0"
)

# 템플릿 & 정적 파일 설정
# templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ✅ 메인 페이지 (프론트엔드)
@app.get("/")
def index(query: str = ""):

    if query:
        answer = main_chain(query)
    else:
        answer = "질문을 입력해주세요."

    return {"answer": answer}



