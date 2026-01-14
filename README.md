# graph_rag
# neo4j graph rag movie

### Neo4j 기반 질의 응답 시스템 (GraphRAG) 구현하기
- Graph 데이터베이스를 기반으로 한 질의 응답 시스템(GraphRAG)은 전통적인 벡터 기반 RAG 시스템보다 더 정확하고 연관성 있는 답변을 제공함. 
- 자연어 질문을 Neo4j Cypher 쿼리로 변환하여 지식 그래프를 효과적으로 탐색하기

### 특장점:
- 정확한 관계 검색: 그래프 데이터베이스의 관계 중심 구조를 활용해 복잡한 연결 패턴을 찾을 수 있습니다
- 컨텍스트 유지: 엔티티 간의 관계를 유지하여 더 풍부한 컨텍스트를 제공합니다
구조화된 정보 검색: 단순 텍스트 검색이 아닌 구조화된 방식으로 정보를 검색합니다

# 설치 라이브러리
```
pip install langchain, langchain-neo4j, langchain-openai
pip install pandas
```

