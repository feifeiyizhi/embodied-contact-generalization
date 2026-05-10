# GitHub Manual Next Steps

Automatic private GitHub creation was not performed on this machine.

Detected status on 2026-05-10:

- `git` is available.
- `gh` is not available in the shell path.
- SSH authentication to GitHub failed with `Permission denied (publickey)`.
- No GitHub push was attempted.

After GitHub authentication is configured, use one of the following routes.

## Route A: GitHub CLI

```bash
cd qingmiao_embodied_generalization_github
gh auth login
gh repo create qingmiao-embodied-generalization --private --source=. --remote=origin --push
```

## Route B: SSH Remote

Create an empty private repository named `qingmiao-embodied-generalization` on GitHub, add a working SSH key, then run:

```bash
cd qingmiao_embodied_generalization_github
git remote add origin git@github.com:<your-user>/qingmiao-embodied-generalization.git
git branch -M main
git push -u origin main
```

## Route C: HTTPS Token Remote

Create an empty private repository on GitHub, then run:

```bash
cd qingmiao_embodied_generalization_github
git remote add origin https://github.com/<your-user>/qingmiao-embodied-generalization.git
git branch -M main
git push -u origin main
```

Use a GitHub personal access token if prompted for a password.
