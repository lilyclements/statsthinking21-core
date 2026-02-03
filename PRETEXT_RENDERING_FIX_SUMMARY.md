# PreTeXt Rendering Fix - Summary

## Problem
PreTeXt content was not rendering on GitHub Pages despite having proper workflow configurations.

## Root Cause
The repository's default branch is `master`, but all three PreTeXt deployment workflows were configured to trigger on the `main` branch:
- `.github/workflows/pretext.yml` - triggered on `main`
- `.github/workflows/pretext-deploy.yml` - triggered on `main`
- `.github/workflows/pretext-cli.yml` - referenced `main` in comments

Because the workflows never triggered on pushes to `master`, the PreTeXt content was never built or deployed to GitHub Pages.

## Solution
Updated all workflow files to trigger on the correct branch (`master` instead of `main`):

### Files Changed:
1. **`.github/workflows/pretext.yml`** - Changed trigger from `main` to `master`
2. **`.github/workflows/pretext-deploy.yml`** - Changed trigger from `main` to `master`
3. **`.github/workflows/pretext-cli.yml`** - Updated comments to reference `master`
4. **`GITHUB_PAGES_SETUP.md`** - Updated all branch references from `main` to `master`
5. **`PRETEXT_DEPLOYMENT_FIX.md`** - Updated all branch references from `main` to `master`

## Expected Outcome
After merging this PR to `master`, the PreTeXt build and deployment workflows will:
1. Trigger automatically on pushes to `master`
2. Build the PreTeXt content from the `source/` directory
3. Deploy the built HTML to GitHub Pages
4. Make the book available at: https://lilyclements.github.io/statsthinking21-core/

## Additional Requirements
**Important:** Ensure GitHub Pages is configured to use "GitHub Actions" as the deployment source:
1. Go to repository **Settings** → **Pages**
2. Under **Build and deployment** → **Source**
3. Select **"GitHub Actions"** (not "Deploy from a branch")
4. Click **Save**

This configuration is required for the workflow to successfully deploy to GitHub Pages.

## Testing
After merging:
1. The workflow should automatically trigger on the `master` branch
2. Check the **Actions** tab to see the workflow running
3. Once complete, visit https://lilyclements.github.io/statsthinking21-core/ to verify the book is deployed

Alternatively, you can manually trigger the workflow:
1. Go to **Actions** tab
2. Select "Build and Deploy PreTeXt" workflow
3. Click "Run workflow"
4. Select the `master` branch
5. Click "Run workflow"
