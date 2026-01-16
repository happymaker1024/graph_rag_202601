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
### 내용 : csv 데이터를 지식 그래프로 만들기
- 지식 그래프를 만들기 위한 node, relation, constraint, index 생성
- 데이터를 지식 그래프 구조로 변환(CSV -> 노드/관계):
    1) Node: 그래프의 노드(정점)를 표현
        - id: 노드의 고유 식별자
        - type: 노드의 유형(예: Movie, Person, Genre)
        - properties: 노드의 속성들(제목, 이름, 평점 등)
    2) Relationship: 두 노드 간의 관계를 표현
        - source: 관계의 시작 노드
        - target: 관계의 목표 노드
        - type: 관계의 유형(예: DIRECTED, ACTED_IN, IN_GENRE)
        - properties: 관계의 속성들
- GraphDB에 저장하기
```
from langchain_neo4j.graphs.graph_document import GraphDocument, Node, Relationship
from langchain_core.documents import Document
```

## 실습2
- 파일 : 2.neo4j_movie_basic_search.ipynb
### 내용 : Cypher 쿼리 기본
- 그래프 패턴 매칭:
    - Cypher의 가장 큰 강점은 노드-관계 패턴을 직관적으로 표현할 수 있음
    - 화살표(->), 관계 타입([:ACTED_IN]) 등을 통해 그래프 구조를 명확히 표현함.
- 데이터 집계 및 변환:
    - count(), collect() 등의 함수를 사용해 결과를 집계하고 변환함.
    - WITH 절을 사용해 중간 결과를 다음 단계로 전달함.
- 가중치 기반 점수 계산:
    - 복합 추천 시스템에서는 다양한 요소(장르, 배우)에 가중치를 부여하여 추천 점수를 계산함.
    - size() 함수로 배열 크기를 계산하고 이를 곱셈 연산에 활용함.
- 매개변수 사용:
    - $actor_name, $movie_title과 같은 매개변수를 사용해 동적 쿼리를 구성함.
    - 이는 SQL의 준비된 문장(Prepared Statement)과 유사한 역할을함.
- OPTIONAL MATCH:
    - SQL의 LEFT JOIN과 유사한 개념으로, 일치하는 패턴이 없어도 결과를 반환함.
    - 복합 추천 시스템에서 장르나 배우가 일치하지 않는 경우에도 계속 처리할 수 있게함.

## 실습3 
- 파일 : 3.neo4j_movie_full-text_search.ipynb
### 내용 : 전문 검색(Full-Text Search)
- 그래프 데이터베이스의 관계 기반 쿼리 기능과 결합되어, 단순한 키워드 검색을 넘어 맥락과 관계를 고려한 지능적인 검색 솔루션을 구현할 수 있게함.
- 텍스트 분석과 토큰화:
    - 전문 검색 인덱스는 텍스트를 단어(토큰)로 분리하고 분석함.
    - 대소문자 구분 없이 검색이 가능함.
- 검색 문법 지원:
    - 와일드카드: star*는 "star", "starship", "stargate" 등을 검색할 수 있음.
    - 부정 검색: -war는 "war"가 포함되지 않은 결과를 반환함.
    - 필수 검색어: +lord +rings는 두 단어가 모두 포함된 결과만 반환함.
    - 구문 검색: "lord of the rings"는 정확한 구문을 포함하는 결과를 반환함.
- 그래프 구조와의 통합:
    - 텍스트 검색 결과를 첫 단계로 사용하고, 이후 그래프 탐색을 통해 관련 데이터를 추출할 수 있음.
    - 이는 관계형 데이터베이스에서는 구현하기 어려운 강력한 기능임.
- 관련성 점수(Relevance Score):
    - 검색 결과는 관련성 점수와 함께 제공되어 가장 적합한 결과를 우선 표시할 수 있음.
    - 이 점수는 검색어와 문서 내용의 일치도, 단어 빈도 등을 고려하여 계산됨.

## 실습4
- 파일 : 4.neo4j_movie_vector_search.ipynb
### 내용 :  임베딩 필드 추가 및 벡터 인덱스 생성
- 영화 노드에 텍스트 데이터를 벡터화한 임베딩 필드를 추가함
- 영화 제목, 줄거리 등의 텍스트 정보를 고차원 벡터로 변환하여 저장함
- 벡터화된 데이터를 효율적으로 검색하기 위한 벡터 인덱스를 생성함
- 인덱스 생성 시 벡터 차원, 유사도 계산 방식, 거리 함수 등을 지정함
- 임베딩과 벡터 인덱스를 통해 의미적 검색의 기반을 구축함

## 실습5
- 파일 : 5.neo4j_movie_text2cypher.ipynb
### 내용 : Text-to-Cypher
- 자연어 질의를 Neo4j 데이터베이스 쿼리 언어인 Cypher로 변환하여 지식 그래프를 효과적으로 검색할 수 있는 기술
- LLM을 활용하여 자연어 질의를 Cypher 쿼리로 변환하는 방법
```
from langchain_openai import ChatOpenAI
from langchain_neo4j import GraphCypherQAChain
```

## 실습6
- 파일 : 6.neo4j_movie_graphVector_RAG.ipynb
### 내용 : Graph RAG와 Vector RAG, Vector Ggraph RAG
- Neo4j에 저장된 임베딩 벡터를 활용한 문서 유사도 검색 방법 
- 벡터 검색(Semantic Search)
- MMR(Maximal Marginal Relevance) 알고리즘을 활용한 다양성 검색
    - 질의와의 관련성 + 결과 간 중복 최소화(다양성)를 동시에 만족하는 문서 5개를 선택하는 과정
    - 사용 하는 이유
        - 상위 결과가 거의 동일한 내용의 문서들로 채워짐
        - RAG에서 → 컨텍스트 낭비, 추론 다양성 감소
- 벡터 검색후 그래프 경로를 활용한 검색 확장

## 실습7
- 파일 : 7.neo4j_movie_graphRAG_hybrid.ipynb

### Neo4j 기반 하이브리드 RAG
- Vector RAG + Graph RAG를 활용한 서비스 구현하기
- Vector Graph Hybrid RAG : 구조적 하이브리드
    - 검색의 시작은 벡터(비정형)
    - 확장은 그래프(정형)
- 단편적인 정보 검색을 넘어 데이터 간의 관계와 연결성을 활용하기 위함

[핵심 프로세스]
- Entry Point (진입점) 찾기
    - 사용자의 질문과 가장 유사한 노드를 벡터 검색으로 빠르게 찾아냄
- Knowledge Expansion (지식 확장)
    - 찾아낸 노드를 기점으로 관계(:ACTED_IN)를 따라가며 인간의 기억 모델처럼 정보를 확장함.
- Context Enrichment (문맥 풍부화)
    - 단순 검색 결과뿐만 아니라 관련 배우의 필모그래피까지 포함하여 LLM에게 풍부한 '배경지식'을 제공함.
<img src="images/vector_graph_hybrid.png" alt="처리순서">

