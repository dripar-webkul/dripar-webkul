#!/bin/bash
# verification-checklist.sh - Verify dynamic README setup

echo "🔍 Dynamic GitHub README Setup Verification"
echo "==========================================="
echo ""

# Check for required files
echo "📋 Checking required files..."
echo ""

files=(
  ".github/workflows/update-readme.yml"
  "update_readme.py"
  "README.md"
  ".gitignore"
)

all_good=true

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file (MISSING)"
    all_good=false
  fi
done

echo ""
echo "📝 Checking README structure..."
echo ""

# Placeholders are replaced by the workflow on first run, so check section
# headers and template-handle markers — those are stable across runs.
for section in "## 📊 GitHub Stats" "## 💻 Top Languages" "## 🏆 Achievements"; do
  if grep -qF "$section" README.md; then
    echo "✅ Section present: $section"
  else
    echo "❌ Missing section: $section"
    all_good=false
  fi
done

if grep -q "<!-- LANGUAGES_START -->" README.md && grep -q "<!-- LANGUAGES_END -->" README.md; then
  echo "✅ LANGUAGES markers present"
else
  echo "❌ LANGUAGES_START/END markers missing"
  all_good=false
fi

echo ""
echo "⚙️  Checking Python script..."
echo ""

if grep -q "class GitHubStatsUpdater" update_readme.py; then
  echo "✅ GitHubStatsUpdater class found"
else
  echo "❌ GitHubStatsUpdater class missing"
  all_good=false
fi

if grep -q "def fetch_user_stats" update_readme.py; then
  echo "✅ fetch_user_stats method found"
else
  echo "❌ fetch_user_stats method missing"
  all_good=false
fi

echo ""
echo "🔄 Checking GitHub Actions workflow..."
echo ""

if grep -q "schedule:" .github/workflows/update-readme.yml; then
  echo "✅ Schedule trigger configured"
else
  echo "❌ Schedule trigger missing"
  all_good=false
fi

if grep -q "workflow_dispatch:" .github/workflows/update-readme.yml; then
  echo "✅ Manual trigger available"
else
  echo "❌ Manual trigger missing"
  all_good=false
fi

if grep -q "permissions:" .github/workflows/update-readme.yml; then
  echo "✅ Permissions configured"
else
  echo "⚠️  Permissions might need manual setup"
fi

echo ""
echo "==========================================="
if [ "$all_good" = true ]; then
  echo "✨ All checks passed! Setup is complete."
  echo ""
  echo "Next steps:"
  echo "1. Push changes to GitHub"
  echo "2. Go to your repo Settings → Actions → General"
  echo "3. Select 'Read and write permissions'"
  echo "4. Go to Actions tab and run workflow manually"
else
  echo "⚠️  Some checks failed. Review items above."
fi
echo "==========================================="
