# GitHub Actions Deployment for PreTeXt Book

This repository uses GitHub Actions to automatically build and deploy the PreTeXt book to GitHub Pages.

## How It Works

The deployment workflow (`.github/workflows/deploy-pretext.yml`) automatically:
1. Builds the PreTeXt book using the `web` target
2. Deploys the built HTML to GitHub Pages

### Triggers

The workflow runs automatically when:
- Changes are pushed to the `main` branch
- Manually triggered via the GitHub Actions interface

## GitHub Pages Setup

**IMPORTANT**: For the book to deploy correctly, GitHub Pages must be configured to use "GitHub Actions" as the source.

### Configuration Steps:

1. Go to repository **Settings** → **Pages**
2. Under **Build and deployment** → **Source**:
   - Select **"GitHub Actions"**
   - **DO NOT** select "Deploy from a branch"
3. Save the setting

Once the workflow runs successfully, the book will be available at:
https://lilyclements.github.io/statsthinking21-core/

## Local Development

To build and preview the book locally:

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Initialize PreTeXt

```bash
pretext init --system
```

### Build the Book

```bash
# Build for web deployment
pretext build web

# Or build as regular HTML
pretext build html
```

### Preview Locally

```bash
# Preview the web build
pretext view web

# Or preview the HTML build
pretext view html
```

## Files

- **project.ptx** - Main project configuration defining build targets
- **requirements.txt** - Python dependencies (PreTeXt CLI)
- **.github/workflows/deploy-pretext.yml** - GitHub Actions workflow
- **.github/scripts/setup-pretext-cache.sh** - Cache workaround script
- **source/** - PreTeXt source files
- **publication/** - Publication settings
- **output/** - Generated output (excluded from git)

## Troubleshooting

### Runestone Services Cache Error

The workflow includes a cache workaround script that handles the Runestone services cache file. This is automatically applied during the build process.

If you encounter this error locally, run:

```bash
bash .github/scripts/setup-pretext-cache.sh
```

### Build Failures

Check the GitHub Actions logs:
1. Go to the **Actions** tab in the repository
2. Click on the failed workflow run
3. Examine the build logs for error messages

Common issues:
- Syntax errors in PreTeXt source files
- Missing dependencies
- Invalid project.ptx configuration

## More Information

- [PreTeXt Guide](https://pretextbook.org/documentation.html)
- [PreTeXt CLI Documentation](https://github.com/PreTeXtBook/pretext-cli)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
