# 🎯 Quick Start & Troubleshooting

## ⚡ Quick Start (30 seconds)

1. **Verify your repository name is `Dripar/Dripar`**
   - Go to https://github.com/settings/profile
   - Your profile README uses a repo with your username

2. **Check workflow permissions**
   - Go to your repo → Settings → Actions → General
   - Select "Read and write permissions"
   - Click Save

3. **Trigger the workflow manually**
   - Go to your repo → Actions tab
   - Select "Update README with Live GitHub Stats"
   - Click "Run workflow" → "Run workflow"
   - Wait 1-2 minutes

4. **Done!** Your README now shows live stats ✨

---

## 🐛 Troubleshooting

### "Workflow not appearing in Actions tab"
**Solution:** Make sure the `.github/workflows/update-readme.yml` file exists and is in the correct location.

```bash
# Verify locally
ls -la .github/workflows/
# Should show: update-readme.yml
```

### "Workflow runs but README doesn't update"

**Check logs:**
1. Actions tab → Latest workflow run
2. Click the "update" job
3. Expand "Run update script" step to see errors

**Common fixes:**
- Missing workflow permissions (see Quick Start step 2)
- API rate limiting (wait 1 hour)
- Invalid `GITHUB_TOKEN` (should auto-work with GitHub Actions)

### "Error: Permission to push"

**Solution:** Update workflow permissions
1. Repo → Settings → Actions → General
2. Set: "Read and write permissions"
3. Check: "Allow GitHub Actions to create and approve pull requests"
4. Retry workflow

### "Script runs but stats show 0"

**Causes & fixes:**
- Brand new repository with no activity → Run the script again after a few minutes
- Private repositories → Only public repos are counted
- Check GitHub API token is valid (auto-handled in Actions)

Run manually to see detailed logs:
```bash
# Locally (requires GITHUB_TOKEN environment variable)
export GITHUB_TOKEN="your_token_here"
export GITHUB_REPOSITORY="Dripar/Dripar"
python update_readme.py
```

---

## 📊 Example Output

After first successful run, your README will look like:

```markdown
| Metric | Count |
|--------|-------|
| **Total Contributions** | 1,247 |
| **Commits** | 856 |
| **Repositories** | 42 |
| **Stars Received** | 189 |
| **Pull Requests** | 23 |
| **Issues Created** | 12 |
| **Followers** | 84 |
| **Following** | 156 |

💻 Top Languages

- **JavaScript** 45% █████████░░░░░░░░░░
- **Python** 30% ██████░░░░░░░░░░░░░░
- **TypeScript** 15% ███░░░░░░░░░░░░░░░░
```

Last updated: 2026-05-26 14:32:15 UTC

---

## 🔄 What Gets Updated

| Item | Frequency |
|------|-----------|
| Total Contributions | Daily (from GitHub API) |
| Commits Count | Daily |
| Repository Count | Daily |
| Stars | Daily |
| Languages | Daily (from all repos) |
| Followers/Following | Daily |
| Last Updated Timestamp | Every run |

---

## 🎨 Customizing Stats

### Want different update schedule?

Edit `.github/workflows/update-readme.yml`, line 7:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'   # Change this line
```

**Examples:**
- `'0 0 * * *'` → Daily at midnight UTC
- `'0 9 * * MON'` → Mondays at 9 AM UTC
- `'0 */3 * * *'` → Every 3 hours
- `'0 12 * * *'` → Daily at noon UTC

Use [crontab.guru](https://crontab.guru) to generate schedules.

### Want to add custom stats?

1. Add placeholder to README:
   ```markdown
   {{YOUR_CUSTOM_STAT}}
   ```

2. Edit `update_readme.py` and add to `GitHubStatsUpdater` class:
   ```python
   def fetch_custom_stat(self):
       # Your logic here
       self.stats["custom_stat"] = value
   ```

3. Call in the `run()` method:
   ```python
   self.fetch_custom_stat()
   ```

4. Add to replacements in `update_readme()`:
   ```python
   "{{YOUR_CUSTOM_STAT}}": str(self.stats.get("custom_stat", 0))
   ```

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `.github/workflows/update-readme.yml` | Automation trigger & scheduler |
| `update_readme.py` | Fetches stats and updates README |
| `README.md` | Your profile with live stats |
| `SETUP_GUIDE.md` | Detailed setup documentation |
| `.gitignore` | Ignores Python cache files |

---

## ✅ Verification Checklist

- [ ] Repository name is `YourUsername/YourUsername`
- [ ] `.github/workflows/update-readme.yml` exists
- [ ] `update_readme.py` exists in root
- [ ] `README.md` has placeholders like `{{TOTAL_CONTRIBUTIONS}}`
- [ ] Workflow permissions set to "Read and write"
- [ ] Workflow runs successfully (check Actions tab)
- [ ] README.md has been updated with real numbers

---

## 🆘 Still Stuck?

1. **Check the workflow logs** - Most errors are detailed there
2. **Verify permissions** - Workflow needs write access
3. **Check placeholders** - Make sure `{{PLACEHOLDER}}` format matches
4. **Restart workflow** - Click "Re-run all jobs" in Actions tab
5. **Clear Python cache** - `rm -rf __pycache__`

**Pro tip:** Run manually to see real-time output:
```bash
python update_readme.py  # (with GITHUB_TOKEN and GITHUB_REPOSITORY env vars)
```

---

*Last Updated: 2026-05-26*
