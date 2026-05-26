#!/usr/bin/env python3
"""
GitHub Profile README Auto-Updater
Fetches live GitHub stats and updates README.md with current data
"""

import os
import re
import requests
from datetime import datetime, timedelta


class GitHubStatsUpdater:
    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN", "")
        self.repo = os.environ.get("GITHUB_REPOSITORY", "")
        self.username = self.repo.split('/')[0] if '/' in self.repo else ""
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.stats = {}

    def fetch_user_stats(self):
        """Fetch basic user statistics via GraphQL"""
        query = """
        {
          user(login: "%s") {
            contributionsCollection {
              contributionCalendar {
                totalContributions
              }
            }
            repositories(first: 100, orderBy: {field: STARGAZERS, direction: DESC}) {
              totalCount
              nodes {
                stargazers {
                  totalCount
                }
              }
            }
            followers {
              totalCount
            }
            following {
              totalCount
            }
          }
        }
        """ % self.username

        try:
            resp = requests.post(
                "https://api.github.com/graphql",
                json={"query": query},
                headers=self.headers,
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()

            if "errors" in data:
                print(f"GraphQL Error: {data['errors']}")
                return False

            user_data = data.get("data", {}).get("user", {})
            contributions = user_data.get("contributionsCollection", {})
            self.stats["total_contributions"] = contributions.get("contributionCalendar", {}).get("totalContributions", 0)
            self.stats["followers"] = user_data.get("followers", {}).get("totalCount", 0)
            self.stats["following"] = user_data.get("following", {}).get("totalCount", 0)

            # Calculate total stars
            repos = user_data.get("repositories", {}).get("nodes", [])
            self.stats["total_stars"] = sum(repo.get("stargazers", {}).get("totalCount", 0) for repo in repos)
            self.stats["repo_count"] = user_data.get("repositories", {}).get("totalCount", 0)

            return True
        except Exception as e:
            print(f"Error fetching user stats: {e}")
            return False

    def fetch_commit_count(self):
        """Fetch total commit count"""
        try:
            # This endpoint requires authentication
            url = f"https://api.github.com/search/commits?q=author:{self.username}"
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            self.stats["commits"] = data.get("total_count", 0)
            return True
        except Exception as e:
            print(f"Error fetching commit count: {e}")
            # Fallback if search fails
            self.stats["commits"] = self.stats.get("total_contributions", 0)
            return False

    def fetch_languages(self, limit=6):
        """Fetch top programming languages from all repositories"""
        try:
            url = f"https://api.github.com/users/{self.username}/repos?per_page=100"
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            repos = resp.json()

            lang_counts = {}

            for repo in repos:
                if repo.get("fork"):
                    continue

                lang_url = repo.get("languages_url", "")
                if lang_url:
                    lang_resp = requests.get(lang_url, headers=self.headers, timeout=10)
                    lang_resp.raise_for_status()
                    languages = lang_resp.json()

                    for lang, bytes_count in languages.items():
                        lang_counts[lang] = lang_counts.get(lang, 0) + bytes_count

            # Sort by byte count and take top N
            sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
            total_bytes = sum(count for _, count in sorted_langs)

            self.stats["languages"] = []
            for lang, bytes_count in sorted_langs:
                percentage = round((bytes_count / total_bytes) * 100) if total_bytes > 0 else 0
                self.stats["languages"].append({
                    "name": lang,
                    "percentage": percentage,
                    "bytes": bytes_count
                })

            return True
        except Exception as e:
            print(f"Error fetching languages: {e}")
            self.stats["languages"] = []
            return False

    def fetch_pull_requests(self):
        """Fetch PR and issue counts"""
        try:
            # PRs created by user
            prs_url = f"https://api.github.com/search/issues?q=author:{self.username}+type:pr"
            prs_resp = requests.get(prs_url, headers=self.headers, timeout=10)
            prs_resp.raise_for_status()
            self.stats["pull_requests"] = prs_resp.json().get("total_count", 0)

            # Issues created by user
            issues_url = f"https://api.github.com/search/issues?q=author:{self.username}+type:issue"
            issues_resp = requests.get(issues_url, headers=self.headers, timeout=10)
            issues_resp.raise_for_status()
            self.stats["issues"] = issues_resp.json().get("total_count", 0)

            return True
        except Exception as e:
            print(f"Error fetching PR/Issue counts: {e}")
            self.stats["pull_requests"] = 0
            self.stats["issues"] = 0
            return False

    def update_readme(self):
        """Read, update, and write README.md"""
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                content = f.read()

            # Replace stat placeholders
            replacements = {
                "{{TOTAL_CONTRIBUTIONS}}": str(self.stats.get("total_contributions", 0)),
                "{{COMMITS}}": str(self.stats.get("commits", 0)),
                "{{REPOSITORIES}}": str(self.stats.get("repo_count", 0)),
                "{{TOTAL_STARS}}": str(self.stats.get("total_stars", 0)),
                "{{FOLLOWERS}}": str(self.stats.get("followers", 0)),
                "{{FOLLOWING}}": str(self.stats.get("following", 0)),
                "{{PULL_REQUESTS}}": str(self.stats.get("pull_requests", 0)),
                "{{ISSUES}}": str(self.stats.get("issues", 0)),
            }

            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)

            # Update languages section
            if self.stats.get("languages"):
                lang_lines = []
                for lang in self.stats["languages"]:
                    bar_length = max(1, lang["percentage"] // 5)  # Scale 0-100 to 0-20
                    bar = "█" * bar_length + "░" * (20 - bar_length)
                    lang_lines.append(f"- **{lang['name']}** {lang['percentage']}% {bar}")

                lang_section = "\n".join(lang_lines)
                content = re.sub(
                    r"<!-- LANGUAGES_START -->.*?<!-- LANGUAGES_END -->",
                    f"<!-- LANGUAGES_START -->\n{lang_section}\n<!-- LANGUAGES_END -->",
                    content,
                    flags=re.DOTALL
                )

            # Add last update timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            content = re.sub(
                r"Last updated:.*",
                f"Last updated: {now}",
                content
            )

            with open("README.md", "w", encoding="utf-8") as f:
                f.write(content)

            print("✅ README.md updated successfully!")
            return True
        except Exception as e:
            print(f"Error updating README: {e}")
            return False

    def run(self):
        """Execute the full update pipeline"""
        print(f"🔄 Updating README for @{self.username}...")

        self.fetch_user_stats()
        self.fetch_commit_count()
        self.fetch_languages()
        self.fetch_pull_requests()

        print(f"📊 Stats collected:")
        for key, value in self.stats.items():
            if key != "languages":
                print(f"   {key}: {value}")

        self.update_readme()


if __name__ == "__main__":
    updater = GitHubStatsUpdater()
    updater.run()
