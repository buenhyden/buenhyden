import os
import re

import feedparser

# 1. 설정 관리 (Configuration)
# YAML에서 주입한 환경 변수를 읽어옵니다.
RSS_URL = os.environ.get("RSS_URL")
# 리드미 파일의 상대 경로 설정
README_PATH = os.path.join(os.path.dirname(__file__), "../README.md")
MAX_POSTS = 5  # 노출할 최대 포스트 수


def fetch_blog_posts():
    """RSS 피드로부터 최신 기술 포스트를 파싱하여 마크다운 리스트로 반환합니다."""
    if not RSS_URL:
        print("Error: RSS_URL environment variable is not set.")
        return None

    try:
        # RSS 피드 파싱 실행
        feed = feedparser.parse(RSS_URL)
        if feed.bozo:
            print(f"Warning: RSS feed parsing issue at {RSS_URL}")

        posts = []
        for entry in feed.entries[:MAX_POSTS]:
            title = entry.title
            link = entry.link
            posts.append(f"- [{title}]({link})")

        return "\n".join(posts) if posts else "업데이트된 포스트가 없습니다."

    except Exception as e:
        print(f"Exception during RSS fetching: {e}")
        return None


def update_readme(new_content):
    """README.md 내의 전용 주석 마커 사이의 내용을 동적으로 교체합니다."""
    if new_content is None:
        return

    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()

        # 정규 표현식 기반 치환 (Regex-based Replacement)
        start_tag = ""
        end_tag = ""
        pattern = f"{start_tag}.*?{end_tag}"
        replacement = f"{start_tag}\n{new_content}\n{end_tag}"

        # 마커 존재 여부 검증
        if not re.search(pattern, readme, flags=re.DOTALL):
            print("Error: Automation markers not found in README.md")
            return

        # 내용 반영 및 저장
        updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print("Successfully updated README.md")

    except Exception as e:
        print(f"Error during file writing: {e}")


if __name__ == "__main__":
    # 메인 실행 로직
    content = fetch_blog_posts()
    update_readme(content)
