#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}     Syntax Motion - Repository Cleanup     ${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

echo -e "${YELLOW}This script will remove virtual environment files and media files from git tracking.${NC}"
echo -e "${YELLOW}These files will still exist on your local system but will be ignored by git.${NC}"
echo ""
echo -e "${RED}Make sure you have committed and pushed any important changes before running this script.${NC}"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Cleanup aborted.${NC}"
    exit 1
fi

echo -e "${YELLOW}Cleaning up repository...${NC}"

# Remove .venv directory from git tracking
echo "Removing virtual environment files from git tracking..."
git rm -r --cached backend/.venv/ 2>/dev/null
git rm -r --cached backend/venv/ 2>/dev/null

# Remove media files from git tracking
echo "Removing media files from git tracking..."
git rm -r --cached backend/media/ 2>/dev/null

# Remove temporary files from git tracking
echo "Removing temporary files from git tracking..."
git rm -r --cached backend/tmp*/ 2>/dev/null
git rm -r --cached backend/temp*/ 2>/dev/null

# Commit the changes
echo "Committing changes..."
git add .gitignore
git commit -m "Remove virtual environment and media files from git tracking"

echo -e "${GREEN}Cleanup complete!${NC}"
echo -e "${YELLOW}To push these changes to your remote repository, run:${NC}"
echo -e "  ${BLUE}git push${NC}"
echo ""
echo -e "${YELLOW}Note: This only stops Git from tracking these files. The files still exist on your system.${NC}"
echo -e "${YELLOW}To remove them completely, delete them manually.${NC}" 