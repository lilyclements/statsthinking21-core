# GitHub Pages Configuration Instructions

## ⚠️ IMPORTANT: Required Configuration

After merging this PR, you **MUST** configure GitHub Pages to use "GitHub Actions" as the deployment source. Without this configuration, the book will not deploy correctly.

## Quick Setup (2 minutes)

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in the left sidebar)
3. Under **Build and deployment** → **Source**:
   - Select **"GitHub Actions"** from the dropdown
   - **DO NOT** select "Deploy from a branch"
4. Click **Save**

That's it! Once this is configured, the workflow will automatically deploy your PreTeXt book to GitHub Pages.

## How It Works

The GitHub Actions workflow (`.github/workflows/deploy-pretext.yml`) will:
- Trigger automatically on pushes to the `main` branch
- Install PreTeXt and build the book
- Deploy the built HTML to GitHub Pages

Your book will be available at:
**https://statsthinking21.github.io/statsthinking21-core/**

## Testing the Workflow

After merging this PR and configuring GitHub Pages:

1. Go to the **Actions** tab in your repository
2. You should see the "Build and Deploy PreTeXt" workflow running
3. Wait for it to complete (usually takes 2-3 minutes)
4. Visit your GitHub Pages URL to see the deployed book

## Manual Trigger

You can also manually trigger the workflow:
1. Go to **Actions** tab
2. Select "Build and Deploy PreTeXt" workflow
3. Click "Run workflow"
4. Select the `main` branch
5. Click "Run workflow"

## Troubleshooting

### Book not showing up
- **Cause**: GitHub Pages is not configured to use "GitHub Actions"
- **Solution**: Follow the Quick Setup instructions above

### Workflow fails
- **Cause**: Build errors in PreTeXt source files
- **Solution**: Check the workflow logs in the Actions tab for error details

### 404 error on GitHub Pages
- **Cause**: Workflow hasn't completed yet or Pages isn't configured
- **Solution**: Wait for workflow to complete, then check Pages configuration

## Local Development

To build and preview the book locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize PreTeXt
pretext init --system

# Build the web target
pretext build web

# Preview the build
pretext view web
```

For more details, see [DEPLOYMENT.md](DEPLOYMENT.md).
