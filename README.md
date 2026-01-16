# graph DB(neo4j) 활용 영화 추천
## graph RAG 소개
- Graph 데이터베이스를 기반으로 한 질의 응답 시스템(GraphRAG)은 전통적인 벡터 기반 RAG 시스템보다 더 정확하고 연관성 있는 답변을 제공함. 
- 자연어 질문을 Neo4j Cypher 쿼리로 변환하여 지식 그래프를 효과적으로 탐색함.

### 특장점:
- 정확한 관계 검색: 그래프 데이터베이스의 관계 중심 구조를 활용해 복잡한 연결 패턴을 찾을 수 있음.
- 컨텍스트 유지: 엔티티 간의 관계를 유지하여 더 풍부한 컨텍스트를 제공함.
구조화된 정보 검색: 단순 텍스트 검색이 아닌 구조화된 방식으로 정보를 검색함.


# 설치 라이브러리
```
pip install langchain, langchain-neo4j, langchain-openai
pip install pandas
```
# 실습 설명
## 실습1
- 파일 : 1.neo4j_movie_graphdb구축_csv.ipynb
### 내용
- 

## 실습2
- 파일 : 2.neo4j_movie_basic_search.ipynb
### 내용
- 

## 실습3
- 파일 : 3.neo4j_movie_full-text_search.ipynb
### 내용
- 

## 실습4
- 파일 : 4.neo4j_movie_vector_search.ipynb
### 내용


## 실습5
- 파일 : 5.neo4j_movie_text2cypher.ipynb

### 내용


## 실습6
- 파일 : 6.neo4j_movie_graphVector_RAG.ipynb

### 내용

## 실습7
- 파일 : 7.neo4j_movie_graphRAG_hybrid.ipynb

### Neo4j 기반 하이브리드 RAG
- Vector RAG + Graph RAG를 활용한 서비스 구현하기


