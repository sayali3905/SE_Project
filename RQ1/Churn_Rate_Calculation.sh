#!/bin/bash

CSV_FILE="../Final_repositories.csv"
OUTPUT_FILE="churn_results.csv"

rm -f "$OUTPUT_FILE"

tail -n +2 "$CSV_FILE" | while IFS=, read -r repo_name stars issues open_prs closed_prs total_prs language is_fork url size_mb uses_travis travis_start_date travis_end_date travis_duration_days; do
  repo_name=$(basename "$url" .git)

  #clone repo if not already present
  if [ ! -d "$repo_name" ]; then
    git clone --quiet "$url" "$repo_name"
  fi

  cd "$repo_name" || continue

  #initial commit before Travis CI adoption
  initial_commit=$(git rev-list -1 --before="$travis_start_date" HEAD)

  #test files based on directory structure and file naming patterns
  test_files=$(git ls-tree -r "$initial_commit" --name-only | grep -E "(/|^)(test[s]?|spec|src|app|script)/.*|.*(Test.java|Spec.js|test_.*\.py|test_.*\.php|test_.*\.c|test_.*\.cpp|test_.*\.rb)$")

  #initial LOC
  initial_loc=$(echo "$test_files" | xargs -I {} git show "$initial_commit:{}" 2>/dev/null | wc -l)

  echo "$repo_name,Initial LOC,$initial_loc"
  echo "$repo_name,N/A,Initial LOC,$initial_loc" >> "$OUTPUT_FILE"

  for i in {-12..12}; do
    month=$(date -d "$(date -d "$travis_start_date" +%Y-%m-01) $i months" +%Y-%m)
    [ -z "$month" ] && continue

    echo "Processing: $repo_name - $month"

    #additions & deletions in test files
    stats=$(git log --since="$month-01" --until="$(date -d "$month-01 +1 month" +%Y-%m-%d)" --numstat -- \
      -- "*Test.java" "*Spec.js" "test_*.py" "test_*.php" "test_*.c" "test_*.cpp" "test_*.rb" \
      $(echo "$test_files" | xargs -I {} echo "-- {}") | awk 'NF==3 && $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ {added+=$1; deleted+=$2} END {print added, deleted}')

    additions=$(echo "$stats" | awk '{print ($1+0)}')  
    deletions=$(echo "$stats" | awk '{print ($2+0)}')  

    echo "Debug: $repo_name - $month - Additions: $additions - Deletions: $deletions"

    #avoid insane numbers by capping deletions
    if [ "$deletions" -ge 1000000 ]; then
      echo "Warning: Unusually high deletion count ($deletions), resetting to 0"
      deletions=0
    fi

    #avoid division errors
    if [ "$initial_loc" -gt 0 ]; then
      churn_rate=$(awk "BEGIN {print ($additions + $deletions) / $initial_loc}")
    else
      churn_rate=0
    fi

    echo "$repo_name,$month,Churn Rate,$churn_rate" >> "$OUTPUT_FILE"
  done

  cd ..
done
