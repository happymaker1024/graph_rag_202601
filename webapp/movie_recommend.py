import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(override=True, dotenv_path="../.env")

import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph, Neo4jVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


# 환경 변수 로드
load_dotenv(override=True)

# Neo4j 연결 (Cypher용)
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database=os.getenv("NEO4J_DATABASE"),
    enhanced_schema=True
)

# 모델 및 DB 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Neo4j 벡터 저장소 연결 (검색용)
vector_store = Neo4jVector.from_existing_index(
    embeddings,
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="movie_content_embeddings",
    text_node_property="overview",
)

def get_movie_details_and_actors(movie_titles):
    """영화 제목 목록을 받아 상세 정보와 출연진을 조회합니다."""
    query = """
    MATCH (m:Movie)
    WHERE ANY(t IN $titles WHERE m.title CONTAINS t)
    OPTIONAL MATCH (m)<-[:ACTED_IN]-(a:Person)
    RETURN 
        m.title as title, 
        m.released as released, 
        m.rating as rating, 
        m.overview as overview,
        collect(a.name) as actor_names,
        collect(elementId(a)) as actor_ids
    """
    return graph.query(query, params={"titles": movie_titles})

def get_actor_filmography(actor_ids, exclude_titles):
    """배우들의 ID를 받아 다른 출연작들을 조회합니다."""
    if not actor_ids:
        return []
        
    query = """
    MATCH (a:Person)
    WHERE elementId(a) IN $actor_ids
    MATCH (a)-[:ACTED_IN]->(m:Movie)
    WHERE NOT m.title IN $exclude_titles   // 전달 받은 영화는 제외
    RETURN 
        a.name as actor_name, 
        collect({title: m.title, released: m.released}) as other_movies
    """
    return graph.query(query, params={"actor_ids": actor_ids, "exclude_titles": exclude_titles})

def format_context_for_llm(movies, filmographies):
    """조회된 데이터를 하나의 문자열 문맥으로 합칩니다."""
    context_parts = ["## 검색된 영화 정보"]
    
    for m in movies:
        actors = ", ".join(m['actor_names']) if m['actor_names'] else "정보 없음"
        context_parts.append(
            f"- 영화: {m['title']} ({m['released']})\n"
            f"  평점: {m['rating']}\n"
            f"  배우: {actors}\n"
            f"  줄거리: {m['overview'][:100]}..."
        )
    
    if filmographies:
        context_parts.append("\n## 출연 배우의 다른 작품들")
        for f in filmographies:
            # 최대 3개까지만 표시 (너무 길어지지 않게)
            titles = [f"{m['title']}({m['released']})" for m in f['other_movies'][:3]]
            context_parts.append(f"- {f['actor_name']}: {', '.join(titles)}")
            
    return "\n".join(context_parts)

def movie_graph_search_orchestrator(user_query):
    """벡터 검색 -> 상세 정보 조회 -> 필모그래피 조회 -> 포맷팅 과정을 총괄합니다."""
    
    # 1. 유사한 영화 제목 찾기 (Vector Search)
    docs = vector_store.similarity_search(user_query, k=3)
    found_titles = [doc.metadata.get("title") for doc in docs if doc.metadata.get("title")]
    
    if not found_titles:
        return "관련 정보를 찾을 수 없습니다."
    
    # 2. 영화 상세 정보 및 배우 ID 가져오기 (Graph Search 1)
    movie_data = get_movie_details_and_actors(found_titles)
    

    # 3. 모든 배우 ID 수집 (중복 제거)
    all_actor_ids = []
    for m in movie_data:
        all_actor_ids.extend(m['actor_ids'])
    all_actor_ids = list(set(all_actor_ids))  # 중복 제거
    
    
    # 4. 배우들의 다른 작품 가져오기 (Graph Search 2)
    film_data = get_actor_filmography(all_actor_ids, found_titles)
    
    
    # 5. 최종 텍스트 생성
    return format_context_for_llm(movie_data, film_data)

def main_chain(query: str) -> str:
    # LLM 객체 생성
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.0)

    # Prompt 템플릿 정의
    template = '''당신은 영화 추천 전문가로서 오직 주어진 정보에 기반하여 객관적이고 정확한 답변을 제공합니다.

    [주어진 영화 정보]
    {context}

    [질문]
    {question}

    # 답변 작성 지침:
    1. 제공된 영화 정보에 명시된 사실만 사용하세요.
    2. 간결하고 정확하게 답변하세요.
    3. 제공된 정보에 없는 내용은 "제공된 정보에서 해당 내용을 찾을 수 없습니다"라고 답하세요.
    4. 영화의 제목, 평점 등 주요 정보를 포함해서 답변하세요.
    5. 한국어로 자연스럽고 이해하기 쉽게 답변하세요.
    '''

    # Prompt 객체 생성
    prompt = ChatPromptTemplate.from_template(template)

    # RAG 체인 구성(딕셔너리를 체인에 넣으면 자동으로 **RunnableParallel**로 변환됨)
    rag_input = {
        "context": RunnableLambda(movie_graph_search_orchestrator),   # vector 질문 → 그래프 검색 결과
        "question": RunnablePassthrough()    # 질문 그대로 전달
    }

    graph_rag_chain = rag_input| prompt | llm | StrOutputParser()

    return graph_rag_chain.invoke(query)

if __name__ == "__main__":
    query = "2차 세계대전 영화 중에서 평점이 높은 작품과 그 배우들의 다른 작품을 알려줘"
    answer = main_chain(query)
    print(answer)