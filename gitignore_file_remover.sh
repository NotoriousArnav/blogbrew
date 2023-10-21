#!/bin/bash

# Define the path to your project directory
PROJECT_DIR="./"

# Get the list of ignored files and directories from .gitignore
ignored_items=$(cat "$PROJECT_DIR/.gitignore")

# Loop through each ignored item and remove the corresponding directory
IFS=$'\n'
for item in $ignored_items; do
  # Build the full path to the item
  item_path="$PROJECT_DIR/$item"

  # Check if the item exists and is a directory
  if [ -d "$item_path" ]; then
    echo "Deleting $item_path"
    # rm -rf "$item_path"
  fi
done
