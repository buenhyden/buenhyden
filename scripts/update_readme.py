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

        if not feed.entries:
            print("No entries found in RSS feed.")
            return None  # None을 반환하여 README 업데이트를 건너뜁니다.

        if feed.bozo:
            print(f"Warning: RSS feed parsing issue at {RSS_URL}")
            
        # 2. 날짜 기준 정렬 (Sorting Logic)
        # published_parsed가 없는 경우 updated_parsed를 사용하거나 현재 시간을 기본값으로 설정하여 런타임 에러 방지
        entries = feed.entries
        entries.sort(
            key=lambda x: x.get(
                "published_parsed", x.get("updated_parsed", datetime.now().timetuple())
            ),
            reverse=True,
        )

        posts = []
        for entry in entries[:MAX_POSTS]:
            title = entry.title
            link = entry.link
            posts.append(f"- [{title}]({link})  ")

        return "\n".join(posts) if posts else "업데이트된 포스트가 없습니다."

    except Exception as e:
        print(f"Exception during RSS fetching: {e}")
        return None


def update_readme(new_content):
    """내용이 있을 때만 README를 업데이트함 (Defensive Coding)"""
    if not new_content:
        print("SKIP: Nothing to update. Keeping current README content.")
        return

    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_content = f.read()

        # 정규표현식 마커 정의
        start_marker = (
            '<h2 align="center"> 📝 Recent Blog Posts (최신 기술 블로그) </h2>'
        )
        end_marker = "---"

        # 마커를 포함한 전체 영역을 찾아서 교체하는 정규식 패턴
        # re.DOTALL: 줄바꿈 문자를 포함하여 매칭
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n{new_content}\n{end_marker}"

        if re.search(pattern, readme_content, flags=re.DOTALL):
            new_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(new_readme)
            print("SUCCESS: README.md has been updated.")
        else:
            print("ERROR: Could not find markers in README.md. Please check the tags.")

    except Exception as e:
        print(f"ERROR: Failed to update file: {e}")


if __name__ == "__main__":
    content = fetch_blog_posts()
    update_readme(content)
