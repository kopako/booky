#!/bin/bash
file_path="app/.env"
echo "Reading file: $file_path using while loop"
echo "---------------------------------"
mkdir -p "secrets" && echo "Directory 'secrets' created"
while IFS='=' read -r key value || [[ -n "$key" ]]; do
    # Skip empty lines and comments
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    echo "$value" > "secrets/$key" && echo "secrets/$key created"
done < "$file_path"
echo "---------------------------------"
echo "Secrets creation completed!"