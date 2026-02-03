# PreTeXt Deployment Fix Summary

## Issues Fixed

### 1. Incorrect Directory References in Workflows
**Problem**: All three GitHub Actions workflow files (`.github/workflows/pretext.yml`, `.github/workflows/pretext-cli.yml`, and `.github/workflows/pretext-deploy.yml`) referenced a `PreText` directory that doesn't exist in the repository.

**Solution**: Removed all `cd PreText &&` commands from the workflows. The PreTeXt project files (`project.ptx`, `source/`, `publication/`) are located in the repository root, so builds should run from there.

### 2. Incompatible `project.ptx` Configuration
**Problem**: The `project.ptx` file used a newer format with child elements (`<source>`, `<publication>`, `<output-dir>`) that isn't compatible with PreTeXt 2.32.0.

**Solution**: 
- Converted the configuration to use attributes on `<target>` elements instead
- Removed the `output-dir` attribute entirely to use PreTeXt's default behavior
- Now each target builds to `output/<target-name>` (e.g., `output/web`)

### 3. Incorrect Output Paths
**Problem**: The workflows expected output at `PreText/output/web` but the build was producing output elsewhere.

**Solution**: With the fixed configuration, builds now correctly output to `output/web`, matching what the main workflow (`pretext.yml`) expects.

## Changes Made

### Modified Files:
1. `.github/workflows/pretext.yml` - Removed `cd PreText &&` reference
2. `.github/workflows/pretext-cli.yml` - Removed `cd PreText &&` and fixed artifact path
3. `.github/workflows/pretext-deploy.yml` - Removed `cd PreText &&` references
4. `project.ptx` - Restructured for PreTeXt 2.32.0 compatibility
5. `GITHUB_PAGES_SETUP.md` - Updated URL and workflow filename

## Next Steps for Deployment

To complete the deployment setup, you need to:

### 1. Merge This PR
Merge this pull request into the `main` branch.

### 2. Configure GitHub Pages
**This is the critical step that was likely causing the 404 error!**

Go to your repository settings:
1. Navigate to **Settings** → **Pages**
2. Under **Build and deployment** → **Source**
3. Select **"GitHub Actions"** (not "Deploy from a branch")
4. Click **Save**

### 3. Trigger the Workflow
The workflow will automatically run when you merge to `main`, or you can manually trigger it:
1. Go to **Actions** tab
2. Select "Build and Deploy PreTeXt" workflow
3. Click "Run workflow"
4. Select the `main` branch
5. Click "Run workflow"

### 4. Verify Deployment
After the workflow completes successfully, visit:
**https://lilyclements.github.io/statsthinking21-core/**

The site should now display your PreTeXt book instead of a 404 error.

## Build Verification

The PreTeXt build has been tested locally and produces:
- Valid HTML output in `output/web/`
- An `index.html` entry point
- All chapter files
- Static assets (CSS, JavaScript)

The workflow is correctly configured to:
1. Install PreTeXt 2.32.0
2. Initialize system resources
3. Create Runestone cache workaround
4. Build the web target
5. Upload to GitHub Pages
6. Deploy via GitHub Pages Actions

## Troubleshooting

If you still see a 404 error after deployment:
1. Verify GitHub Pages source is set to "GitHub Actions" (most common issue)
2. Check the Actions tab for any workflow failures
3. Ensure the workflow ran to completion
4. Wait a few minutes for GitHub Pages to propagate changes

If the workflow fails:
1. Check the workflow logs in the Actions tab
2. Look for any PreTeXt build errors
3. Verify all source files are valid PreTeXt XML
