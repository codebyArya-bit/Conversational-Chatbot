@echo off
echo ========================================
echo GitHub Direct Sync Deployment Setup
echo ========================================
echo.

echo [1/5] Checking if git is initialized...
if not exist ".git" (
    echo Initializing git repository...
    git init
    echo Git repository initialized.
) else (
    echo Git repository already exists.
)

echo.
echo [2/5] Adding all files to git...
git add .

echo.
echo [3/5] Creating commit...
set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" set commit_message=Deploy with GitHub sync - automated deployment setup
git commit -m "%commit_message%"

echo.
echo [4/5] Setting up remote repository...
echo Please make sure you have created a GitHub repository first.
set /p repo_url="Enter your GitHub repository URL (https://github.com/username/repo.git): "

if "%repo_url%"=="" (
    echo No repository URL provided. Skipping remote setup.
    goto :skip_remote
)

git remote remove origin 2>nul
git remote add origin %repo_url%
echo Remote repository set to: %repo_url%

:skip_remote
echo.
echo [5/5] Pushing to GitHub...
set /p branch_name="Enter branch name (default: main): "
if "%branch_name%"=="" set branch_name=main

git branch -M %branch_name%
git push -u origin %branch_name%

echo.
echo ========================================
echo Deployment Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Go to your GitHub repository
echo 2. Set up deployment platform:
echo    - Render: Connect repository and deploy with render.yaml
echo    - Netlify: New site from Git, auto-detects netlify.toml
echo    - Vercel: Import project, set root to 'frontend'
echo.
echo 3. Your app will auto-deploy on every push to GitHub!
echo.
echo Backend URL (Render): https://conversational-chatbot.onrender.com
echo Frontend URL: Will be provided by your chosen platform
echo.
echo For detailed instructions, see GITHUB_DEPLOYMENT.md
echo.
pause