import streamlit as st
from openai import OpenAI
import openai
from dotenv import load_dotenv
import os

# 환경 변수 로드 및 OpenAI 클라이언트 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# GPT-4 블로그 글 생성 함수
def generate_blog_text(place, location, menu, price, review):
    prompt = f"""
당신은 다양한 맛집을 소개하는 블로거입니다.
아래의 맛집 정보를 바탕으로 블로그 포스트의 첫 문단을 **조금 더 길고 상세하게** 작성해주세요.

[맛집 정보]
- 가게 이름: {place}
- 위치: {location}
- 시킨 메뉴: {menu}
- 가격: {price}원
- 후기: {review}

[작성 조건]
- 방문자에게 해당 가게를 소개하는 톤으로 시작해주세요.
- 위치, 접근성, 매장 분위기 등을 서두에서 간단히 언급하세요.
- 시킨 메뉴의 특징, 양, 맛, 플레이팅, 반찬 조화 등에 대한 설명을 자세히 추가해주세요.
- 가격 대비 만족도, 서비스 응대 등도 함께 언급해주세요.
- 단순한 평가보다는 방문자가 실제로 상상할 수 있도록 묘사형으로 작성해주세요.
- 문장 수는 5~8문장 이상으로 작성해주세요.
- 블로그 소개 스타일로 문장 끝은 “입니다”, “이에요”, “좋았어요” 등 단정한 말투로 마무리해주세요.
- 자연스럽게 이모지 1~3개 정도 사용하면 좋습니다. (예: 🍲😊🔥 등)

예시:
“서울 마포구 서교동에 위치한 ‘보승회관’은 한적한 골목길에 자리한 순대국밥 전문점입니다. 외관은 깔끔하고 오래된 식당 느낌이 나는데, 내부는 따뜻한 조명 덕분에 편안한 분위기를 줍니다. 🍲 주문한 순대국밥(10,000원)은 국물이 진하고 건더기가 푸짐해, 속을 확 풀어주는 느낌이었어요. 김치와 깍두기도 적당히 익어 국밥과 조화가 좋았고, 플레이팅도 투박하지만 정갈했습니다. 직원분들도 친절하게 맞아주셔서 전체적인 인상도 좋았습니다. 가성비 좋은 한 끼를 찾는 분들께 추천드리고 싶은 곳이에요. 😊”

이제 위 내용을 참고하여 블로그 글을 작성해주세요.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# 썸네일 이미지 생성 함수 (가게 분위기 + 음식 감상 기반)
def generate_thumbnail(menu, review, place):
    openai.api_key = api_key  # DALL·E용 키 설정
    dalle_prompt = f"""
Create an artistic thumbnail image that harmonizes the following elements:
- Dish: {menu}
- Mood and description: {review}
- Restaurant vibe: imagine the feeling or ambiance of the place, inspired by the description of '{place}'

Generate a cozy, appetizing, and blog-friendly visual that captures both the food and the atmosphere together. No text in the image.
"""
    response = openai.images.generate(
        prompt=dalle_prompt,
        n=1,
        size="512x512"
    )
    return response.data[0].url

# Streamlit 앱 UI
def main():
    st.set_page_config(page_title="맛집 블로그 자동 작성기", layout="centered")
    st.title("🍴 맛집 블로그 자동 생성기")
    st.markdown("맛집 정보를 입력하면 블로그 문단을 생성하고, DALL·E로 썸네일도 만들 수 있어요!")

    # 입력 폼
    with st.form("blog_form"):
        place = st.text_input("🍽️ 가게 이름", "")
        location = st.text_input("📍 위치 (예: 서울 마포구 서교동 392-24)", "")
        menu = st.text_input("🍲 시킨 메뉴", "")
        price = st.text_input("💰 가격 (숫자만)", "")
        review = st.text_area("📝 한줄 평가", "")
        use_dalle = st.checkbox("썸네일 이미지 생성 (DALL·E 사용)", value=True)
        submitted = st.form_submit_button("블로그 문단 생성하기")

    if submitted:
        if not all([place, location, menu, price, review]):
            st.warning("모든 항목을 입력해주세요!")
        else:
            with st.spinner("GPT가 블로그 글을 생성 중입니다..."):
                blog_text = generate_blog_text(place, location, menu, price, review)
            st.subheader("📄 생성된 블로그 문단")
            st.write(blog_text)

            if use_dalle:
                with st.spinner("DALL·E가 썸네일 생성 중입니다..."):
                    try:
                        image_url = generate_thumbnail(menu, review, place)
                        st.subheader("🖼️ 생성된 썸네일")
                        st.image(image_url, use_column_width=True)
                    except Exception as e:
                        st.error(f"DALL·E 생성 오류: {e}")

            st.download_button("📥 텍스트 파일로 저장", blog_text, file_name="blog.txt")

if __name__ == "__main__":
    main()
