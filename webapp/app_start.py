import uvicorn

# cli 실행 : uvicorn main:app [--port=8000] --reload

# python app_start.py
if __name__ == "__main__":
  uvicorn.run('main:app', 
              host='127.0.0.1', port=8000, reload=True)