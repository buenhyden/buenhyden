import logging
from pathlib import Path

import feedparser  # RSS 피드 파싱 (RSS Feed Parsing)
import requests  # HTTP 요청 처리 (HTTP Request Handling)

# 로깅 설정: GitHub Actions 로그에서 실행 과정을 확인하기 위함
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def fetch_blog_posts(rss_url: str, limit: int = 5):
    """RSS 피드에서 최신 포스트를 가져와 마크다운 리스트로 반환합니다."""
    try:
        # User-Agent를 설정하여 봇 차단을 방지하고 타임아웃을 설정합니다.
        response = requests.get(
            rss_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        feed = feedparser.parse(response.text)

        if not feed.entries:
            logging.warning("No entries found in the RSS feed.")
            return ""

        posts = []
        for entry in feed.entries[:limit]:
            # 날짜 형식을 'YYYY-MM-DD'로 깔끔하게 추출합니다.
            date = entry.get("published", "No Date")[:10]
            posts.append(f"- [{entry.title}]({entry.link}) - `{date}`")

        return "\n".join(posts)
    except Exception as e:
        logging.error(f"Failed to fetch RSS feed: {e}")
        return None


def update_readme(new_content: str):
    """README.md 파일의 특정 영역을 새로운 내용으로 교체합니다."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        logging.error("README.md not found.")
        return

    content = readme_path.read_text(encoding="utf-8")

    start_marker = ""
    end_marker = ""

    # 마커 위치 찾기
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        logging.error("Markers not found in README.md.")
        return

    # 새로운 내용 구성
    updated_content = (
        content[: start_idx + len(start_marker)]
        + "\n"
        + new_content
        + "\n"
        + content[end_idx:]
    )

    readme_path.write_text(updated_content, encoding="utf-8")
    logging.info("Successfully updated README.md with latest blog posts.")


if __name__ == "__main__":
    # 조현윤 님의 블로그 RSS URL (Hugo 기반인 경우 index.xml)
    RSS_URL = "https://buenhyden.github.io/index.xml"

    post_list = fetch_blog_posts(RSS_URL)
    if post_list:
        update_readme(post_list)
