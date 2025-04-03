import streamlit as st
import feedparser


def fetch_news(rss_url):
    feed = feedparser.parse(rss_url)
    news_list = []
    for entry in feed.entries:
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "published": entry.published,
            "image": entry.media_content[0]["url"] if "media_content" in entry else None
        }
        news_list.append(news_item)
    return news_list

def fnGetNews(rss_url):
    news_list = fetch_news(rss_url)

    # 뉴스 표시
    for news in news_list:
        st.markdown("---")
        with st.container():
            # 레이아웃: 가로 공간 분할
            col1, col2 = st.columns([1, 3])  # 비율로 조정

            # 왼쪽: 이미지
            with col1:
                if news["image"]:
                    st.image(news["image"], width=200)

            # 오른쪽: 제목과 요약
            with col2:
                st.markdown(f"#### [{news['title']}]({news['link']})")
                st.markdown(f"📅 {news['published']}")
                st.markdown(f"{news['summary'][:150]}...")  # 요약 부분만 표시

    st.markdown("---")