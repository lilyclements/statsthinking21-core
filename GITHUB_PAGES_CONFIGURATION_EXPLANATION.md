# Understanding the GitHub Pages Configuration Issue

## What the Screenshot Shows

The screenshot from the issue shows the GitHub Pages settings page with two workflow options:
- **GitHub Pages Jekyll** - Package a Jekyll site with GitHub Pages dependencies preinstalled
- **Static HTML** - Deploy static files in a repository without a build

## The Problem

The image shows that the repository is looking at suggested workflows, which indicates that:
1. GitHub Pages was not properly configured yet, OR
2. The source was set to "Deploy from a branch" instead of "GitHub Actions"

For PreTeXt to work, the GitHub Pages source **must** be set to "GitHub Actions" because:
- PreTeXt requires a custom build process (not Jekyll or static HTML)
- Our workflows handle the building and deployment
- The workflows use the `actions/deploy-pages` action to deploy

## Why PreTeXt Wasn't Rendering

There were TWO issues preventing PreTeXt from rendering:

### Issue 1: Wrong Branch Configuration (FIXED in this PR)
- Repository default branch: `master`
- Workflow trigger branches: `main`
- **Result**: Workflows never triggered, content never built

### Issue 2: GitHub Pages Source Configuration (REQUIRES MANUAL SETUP)
- GitHub Pages needs to be configured to use "GitHub Actions" as source
- Without this, even if workflows run, the content won't deploy
- **Action Required**: Repository owner must configure this setting

## How to Fix Issue 2

After merging this PR, the repository owner must:

1. Navigate to repository **Settings**
2. Click **Pages** in the left sidebar
3. Under **Build and deployment** → **Source**:
   - If it shows "Deploy from a branch" → Change to "GitHub Actions"
   - If it shows workflow suggestions → Select "GitHub Actions"
4. Click **Save**

## What Happens After Both Fixes

1. ✅ **PR Merged** - Workflows now trigger on `master` branch
2. ✅ **Pages Configured** - GitHub Pages uses GitHub Actions
3. ✅ **Workflow Runs** - PreTeXt builds on push to `master`
4. ✅ **Content Deploys** - Built HTML deployed to GitHub Pages
5. ✅ **Site Live** - PreTeXt book available at GitHub Pages URL

## Verification Steps

After both fixes are applied:

1. **Check Workflow Runs**:
   - Go to **Actions** tab
   - Look for "Build and Deploy PreTeXt" workflow
   - Verify it completed successfully

2. **Check GitHub Pages**:
   - Go to **Settings** → **Pages**
   - Verify source is "GitHub Actions"
   - Verify "Your site is live at..." message appears

3. **Visit the Site**:
   - Navigate to: https://lilyclements.github.io/statsthinking21-core/
   - Verify PreTeXt book content displays correctly

## Summary

The image in the issue showed GitHub Pages configuration screen, indicating that:
- GitHub Pages source wasn't configured for GitHub Actions
- This is **separate** from the workflow branch mismatch issue

**This PR fixes**: The workflow branch mismatch (main → master)
**Manual setup required**: GitHub Pages source configuration (Deploy from branch → GitHub Actions)

Both fixes are necessary for PreTeXt to render properly.
