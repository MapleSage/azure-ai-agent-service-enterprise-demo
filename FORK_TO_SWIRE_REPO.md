# Fork to Swire Renewable Private Repository

## Step 1: Create New Private Repository on GitHub

### Option A: Using GitHub CLI (gh)

```bash
# Create new private repo
gh repo create swire-ops-hr-agent --private --description "Swire Renewable Operations & HR AI Agent - Enterprise documentation and policy management system"

# Add remote
git remote add swire https://github.com/YOUR_USERNAME/swire-ops-hr-agent.git

# Push to new repo
git push swire main
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `swire-ops-hr-agent`
   - **Description:** "Swire Renewable Operations & HR AI Agent - Enterprise documentation and policy management system"
   - **Visibility:** Private ✓
   - **Do NOT initialize** with README, .gitignore, or license (we already have these)
3. Click "Create repository"

4. Then in your terminal:
```bash
# Add the new remote
git remote add swire https://github.com/YOUR_USERNAME/swire-ops-hr-agent.git

# Push all branches
git push swire main

# Push all tags (if any)
git push swire --tags
```

## Step 2: Update Repository Information

After creating the repo, update these files:

### Update README.md
```bash
# Edit README.md to reflect Swire-specific information
```

### Update package.json or project metadata (if applicable)
```bash
# Update project name and description
```

## Step 3: Clean Up Original Remote (Optional)

If you want to remove the original remote and only keep Swire's:

```bash
# Remove original remote
git remote remove origin

# Rename swire remote to origin
git remote rename swire origin

# Verify
git remote -v
```

## Step 4: Set Up Repository Settings

On GitHub, configure:

1. **Collaborators:** Add Swire team members
2. **Branch Protection:** Protect main branch
3. **Secrets:** Add Azure credentials for CI/CD
4. **Topics:** Add tags like `azure`, `ai-agent`, `operations-manual`, `swire-renewable`

## Alternative Repository Names

If `swire-ops-hr-agent` doesn't work, consider:
- `swire-renewable-ops-agent`
- `swire-operations-hr-assistant`
- `swire-enterprise-agent`
- `swire-ops-manual-ai`
- `swire-renewable-assistant`

## Step 5: Update Documentation

Update these files with Swire-specific information:
- [ ] README.md - Add Swire branding and context
- [ ] CONTRIBUTING.md - Update contribution guidelines
- [ ] LICENSE.md - Verify license is appropriate
- [ ] .env.example - Already updated with Swire config

## Step 6: Remove Demo Data

Remove or replace sample data:
```bash
# Remove demo enterprise data
rm -rf enterprise-data/*

# Create Swire department structure
mkdir -p enterprise-data/{blades,pre_assembly_installation,service_maintenance,hr,company_info,general}
```

## Step 7: Initialize Git LFS (if needed for large files)

If you'll be storing large documents:
```bash
git lfs install
git lfs track "*.pdf"
git lfs track "*.docx"
git add .gitattributes
git commit -m "Configure Git LFS for large documents"
git push
```

## Verification Checklist

- [ ] New private repository created
- [ ] Code pushed to new repository
- [ ] Remote configured correctly
- [ ] Repository settings configured
- [ ] Team members added as collaborators
- [ ] README updated with Swire information
- [ ] Demo data removed/replaced
- [ ] Deployment configuration verified
