import os
import re

import feedparser

# 1. 설정 (Configuration)
RSS_URL = "https://buenhyden.github.io/feed.xml"  # 조현윤 님의 블로그 피드 주소
README_PATH = os.path.join(os.path.dirname(__file__), "../README.md")
MAX_POSTS = 5  # 노출할 최대 포스트 개수


def fetch_blog_posts():
    """기술 블로그 RSS 피드에서 최신 포스트를 추출합니다."""
    try:
        feed = feedparser.parse(RSS_URL)
        posts = []
        for entry in feed.entries[:MAX_POSTS]:
            # 제목 및 링크 추출 (Format: [Emoji] Title)
            title = entry.title
            link = entry.link
            posts.append(f"- [{title}]({link})")
        return "\n".join(posts)
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return None


def update_readme(new_content):
    """README.md의 특정 주석 사이 구간을 업데이트합니다."""
    if not new_content:
        return

    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        # 주석 기반 태그 검색 (Regex (정규 표현식) 사용)
        start_tag = ""
        end_tag = ""
        pattern = f"{start_tag}.*?{end_tag}"
        replacement = f"{start_tag}\n{new_content}\n{end_tag}"

        updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)

        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("Successfully updated README.md with latest blog posts.")

    except FileNotFoundError:
        print("Error: README.md file not found.")
    except Exception as e:
        print(f"Unexpected error during file update: {e}")


if __name__ == "__main__":
    blog_content = fetch_blog_posts()
    update_readme(blog_content)
