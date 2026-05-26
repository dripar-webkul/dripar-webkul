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
echo "📝 Checking README placeholders..."
echo ""

if grep -q "{{TOTAL_CONTRIBUTIONS}}" README.md; then
  echo "✅ Found {{TOTAL_CONTRIBUTIONS}}"
else
  echo "❌ Missing {{TOTAL_CONTRIBUTIONS}}"
  all_good=false
fi

if grep -q "{{COMMITS}}" README.md; then
  echo "✅ Found {{COMMITS}}"
else
  echo "❌ Missing {{COMMITS}}"
  all_good=false
fi

if grep -q "{{REPOSITORIES}}" README.md; then
  echo "✅ Found {{REPOSITORIES}}"
else
  echo "❌ Missing {{REPOSITORIES}}"
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
