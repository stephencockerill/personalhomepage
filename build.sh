for filename in content/*.html; do
    cat templates/top.html $filename templates/bottom.html > docs/`basename "$filename"`
done
