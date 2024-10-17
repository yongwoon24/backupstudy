import oracledb
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Oracle Instant Client 경로 설정
oracledb.init_oracle_client(lib_dir="C:/Users/3calss_15/Downloads/instantclient_11_2")  # Instant Client의 경로로 바꿔주세요

# 오라클 DB 연결 설정
connection = oracledb.connect(user='mainproject', password='mainproject', dsn='localhost:1521/xe')

# SQL 쿼리로 데이터베이스에서 필요한 데이터 불러오기
def fetch_data():
    try:
        print("데이터베이스에서 제품 데이터 가져오는 중...")
        query = """
        SELECT p.product_id, p.product_name, p.category_id, p.brand, p.price, p.stock_quantity
        FROM products p
        """
        products_df = pd.read_sql(query, con=connection)
        print("제품 데이터:")
        print(products_df.head())

        print("데이터베이스에서 사용자 조회 데이터 가져오는 중...")
        query_user_views = """
        SELECT uv.user_id, uv.product_id 
        FROM user_views uv
        """
        user_views_df = pd.read_sql(query_user_views, con=connection)
        print("사용자 조회 데이터:")
        print(user_views_df.head())

        print("데이터베이스에서 장바구니 내역 데이터 가져오는 중...")
        query_cart_history = """
        SELECT ch.user_id, ch.product_id
        FROM cart_history ch
        """
        cart_history_df = pd.read_sql(query_cart_history, con=connection)
        print("장바구니 내역 데이터:")
        print(cart_history_df.head())

        return products_df, user_views_df, cart_history_df
    except Exception as e:
        print(f"데이터를 가져오는 중 오류 발생: {e}")

# 데이터 전처리 및 모델 생성
def preprocess_and_recommend(user_id, products_df, user_views_df, cart_history_df):
    try:
        print(f"사용자 {user_id}에 대한 추천 준비 중...")
        print("제품 속성 결합 (카테고리, 브랜드) 중...")
        products_df['combined_features'] = products_df['CATEGORY_ID'].astype(str) + ' ' + products_df['BRAND']
        print("결합된 속성 데이터:")
        print(products_df[['PRODUCT_ID', 'combined_features']].head())

        print("TF-IDF 벡터화 중...")
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(products_df['combined_features'])
        print(f"TF-IDF 매트릭스 크기: {tfidf_matrix.shape}")

        print("코사인 유사도 계산 중...")
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        print("코사인 유사도 계산 완료.")

        print("사용자가 조회하거나 장바구니에 담은 제품 추출 중...")
        user_interactions = pd.concat([
            user_views_df[user_views_df['USER_ID'] == user_id],
            cart_history_df[cart_history_df['USER_ID'] == user_id]
        ])
        user_products = user_interactions['PRODUCT_ID'].unique()
        print(f"사용자가 상호작용한 제품 ID: {user_products}")

        print("사용자가 상호작용한 제품과 유사한 제품 추천 중...")
        product_indices = products_df[products_df['PRODUCT_ID'].isin(user_products)].index
        sim_scores = list(enumerate(cosine_sim[product_indices].mean(axis=0)))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        print(f"추천 제품 수: {len(sim_scores)}")

        top_product_indices = [i[0] for i in sim_scores[:10]]
        recommended_products = products_df.iloc[top_product_indices]

        print("추천된 제품 목록:")
        print(recommended_products[['PRODUCT_ID', 'PRODUCT_NAME', 'BRAND', 'PRICE']])

        return recommended_products
    except KeyError as ke:
        print(f"KeyError 발생: {ke}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")

from mpl_toolkits.mplot3d import Axes3D  # 3D 그래프를 그리기 위한 라이브러리 추가

import seaborn as sns
import matplotlib.pyplot as plt

# 코사인 유사도 히트맵을 그리는 함수
def visualize_cosine_similarity(cosine_sim, products_df):
    try:
        print("코사인 유사도 히트맵을 생성하는 중...")

        # 제품 이름을 축 라벨로 사용하여 히트맵 그리기
        plt.figure(figsize=(12, 8))
        sns.heatmap(cosine_sim, xticklabels=products_df['PRODUCT_NAME'], 
                    yticklabels=products_df['PRODUCT_NAME'], cmap="coolwarm", annot=False, linewidths=0.5)

        plt.title("Product Cosine Similarity Heatmap")
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"코사인 유사도 시각화 중 오류 발생: {e}")

# 메인 함수에서 코사인 유사도 히트맵 호출 추가
def main(user_id):
    print("데이터를 불러오는 중...")
    products_df, user_views_df, cart_history_df = fetch_data()

    print(f"사용자 {user_id}에 대한 추천 작업을 시작합니다.")
    recommendations = preprocess_and_recommend(user_id, products_df, user_views_df, cart_history_df)

    if recommendations is not None:
        print("추천 상품 목록:")
        print(recommendations[['PRODUCT_ID', 'PRODUCT_NAME', 'BRAND', 'PRICE']])

        # TF-IDF 매트릭스 생성 및 코사인 유사도 계산
        products_df['combined_features'] = products_df['CATEGORY_ID'].astype(str) + ' ' + products_df['BRAND']
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(products_df['combined_features'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # 코사인 유사도 히트맵 시각화 호출
        visualize_cosine_similarity(cosine_sim, products_df)
    else:
        print("추천 상품을 생성하는 데 문제가 발생했습니다.")

# 예시 실행 (user_id가 2인 사용자에게 추천)
main(7)

