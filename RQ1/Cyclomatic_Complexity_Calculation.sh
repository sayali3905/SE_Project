CSV_FILE="Final_repositories.csv"
CSV_DIR=$(dirname "$(realpath "$CSV_FILE")")  
OUTPUT_FILE="$CSV_DIR/cyclomatic_complexity.csv"  
REPO_DIR="/d/SE_Project/repos"
LIZARD_CMD="lizard"

if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Repository,Month,Avg. CC, Avg. NLOC" > "$OUTPUT_FILE"
fi

while IFS=, read -r repo_name stars issues open_prs closed_prs total_prs language is_fork url size_mb uses_travis travis_start_date travis_end_date travis_duration_days
do
    [[ -z "$repo_name" || -z "$url" ]] && continue

    repo_name=$(basename "$url" .git)
    repo_path="$REPO_DIR/$repo_name"
    
    if [ ! -d "$repo_path/.git" ]; then
        echo "❌ Skipping $repo_name. Repository not cloned."
        continue
    fi

    echo "📆 Travis CI Start Date for $repo_name: $travis_start_date"
    travis_start_month=$(date -d "${travis_start_date:0:10}" +%Y-%m)

    cd "$repo_path" || continue

    for i in {-12..12}; do
        month=$(date -d "$travis_start_month-01 $i months" +%Y-%m)
        start_date=$(date -d "$month-01" +%Y-%m-%d)
        end_date=$(date -d "$month-01 +1 month -1 day" +%Y-%m-%d)

        commits_this_month=$(git log --all --no-merges --after="$start_date" --before="$end_date 23:59:59" --pretty=format:"%H" -- \
        $(git ls-tree -r HEAD --name-only | grep -E ".*(Test\.java|Spec\.js|test_.*\.py|test_.*\.php|test_.*\.c|test_.*\.cpp|test_.*\.rb)$"))

        commits_count=$(echo "$commits_this_month" | wc -l)

        if [ "$commits_count" -eq 0 ]; then
            echo "⚠️ No commits found for $month in $repo_name"
            continue
        fi

        total_cc=0
        total_nloc=0
        total_files=0
        commit_counter=0

        while read -r commit_hash; do
            [[ -z "$commit_hash" ]] && continue

            git reset --hard &>/dev/null
            git clean -fd &>/dev/null
            git checkout "$commit_hash" --quiet

            test_files=$(git ls-tree -r HEAD --name-only | grep -E ".*(Test\.java|Spec\.js|test_.*\.py|test_.*\.php|test_.*\.c|test_.*\.cpp|test_.*\.rb)$")
            files_count=$(echo "$test_files" | wc -l)

            if [ "$files_count" -eq 0 ]; then
                echo "⚠️ No test files found in commit $commit_hash, skipping..."
                continue
            fi

            cc_output=$($LIZARD_CMD $test_files 2>/dev/null | tail -n 1)
            nloc=$(echo "$cc_output" | awk '{print $2}')
            complexity=$(echo "$cc_output" | awk '{print $3}')

            if [[ ! "$complexity" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
                complexity=0
            fi
            if [[ ! "$nloc" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
                nloc=0
            fi

            total_cc=$(awk "BEGIN {print $total_cc + $complexity}")
            total_nloc=$(awk "BEGIN {print $total_nloc + $nloc}")
            total_files=$(awk "BEGIN {print $total_files + $files_count}")
            commit_counter=$((commit_counter + 1))

        done <<< "$commits_this_month"

        if [ "$commit_counter" -gt 0 ]; then
            avg_cc=$(awk "BEGIN {print $total_cc / $commit_counter}")
            avg_nloc=$(awk "BEGIN {print $total_nloc / $commit_counter}")
            avg_files=$(awk "BEGIN {print $total_files / $commit_counter}")

            if [[ "$month" < "$travis_start_month" ]]; then
                echo "$repo_name,$month,,${avg_cc},${avg_nloc},${avg_files},,,,,$commits_count" >> "$OUTPUT_FILE"
            else
                echo "$repo_name,$month,,,,,${avg_cc},${avg_nloc},${avg_files},$commits_count" >> "$OUTPUT_FILE"
            fi
        else
            echo "⚠️ No valid commits for $repo_name in $month. Skipping entry."
        fi

    done

    git reset --hard &>/dev/null
    git checkout master --quiet
    cd "$REPO_DIR" || continue
    
done < <(tail -n +2 "$CSV_FILE") 
echo "📊 Results saved in: $OUTPUT_FILE"






