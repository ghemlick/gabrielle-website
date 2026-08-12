#!/usr/bin/env python3
"""Create Buttondown emails when new items appear in feed.xml."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

API_URL = "https://api.buttondown.com/v1/emails"


def parse_items(xml_content: str) -> list[dict[str, str]]:
    root = ET.fromstring(xml_content)
    items: list[dict[str, str]] = []

    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        description = (item.findtext("description") or "").strip()
        guid = (item.findtext("guid") or link or title).strip()

        if title and link:
            items.append(
                {
                    "title": title,
                    "link": link,
                    "description": description,
                    "guid": guid,
                }
            )

    return items


def load_items(path: str | None) -> list[dict[str, str]]:
    if not path or not os.path.isfile(path):
        return []

    with open(path, encoding="utf-8") as handle:
        return parse_items(handle.read())


def create_email(post: dict[str, str], status: str, api_key: str) -> None:
    body_lines = [
        f"New on the blog: **{post['title']}**",
        "",
    ]

    if post["description"]:
        body_lines.append(post["description"])
        body_lines.append("")

    body_lines.append(f"[Read the full post]({post['link']})")

    payload = {
        "subject": post["title"],
        "body": "\n".join(body_lines),
        "status": status,
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    print(f"Created {status} email: {result.get('id', 'unknown')} — {post['title']}")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: notify-subscribers.py [old_feed.xml] new_feed.xml", file=sys.stderr)
        return 1

    old_path = sys.argv[1] if len(sys.argv) > 2 else None
    new_path = sys.argv[-1]

    old_items = load_items(old_path)
    new_items = load_items(new_path)

    if not old_items:
        print("No previous feed.xml found. Skipping to avoid emailing old posts.")
        return 0

    old_guids = {item["guid"] for item in old_items}
    new_posts = [item for item in new_items if item["guid"] not in old_guids]

    if not new_posts:
        print("No new posts in feed.xml.")
        return 0

    api_key = os.environ.get("BUTTONDOWN_API_KEY", "").strip()
    if not api_key:
        print("BUTTONDOWN_API_KEY is not set.", file=sys.stderr)
        return 1

    status = os.environ.get("EMAIL_STATUS", "draft").strip().lower()
    if status not in {"draft", "about_to_send"}:
        print('EMAIL_STATUS must be "draft" or "about_to_send".', file=sys.stderr)
        return 1

    for post in new_posts:
        try:
            create_email(post, status, api_key)
        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            print(f"Buttondown API error for '{post['title']}': {details}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
