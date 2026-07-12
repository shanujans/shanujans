# Setup — GitHub Stats Terminal Card

This adds a self-hosted, animated "terminal" stats card to your profile
README, calculated from your real GitHub data — the same approach Andrew6rant
uses (a Python script + GitHub Action that regenerates an SVG on a schedule),
just with an original design and script.

## 1. Add these files to `shanujans/shanujans`

Copy this exact structure into your repo root:

```
shanujans/
├── README.md                              (replace your current one)
├── today.py
├── requirements.txt
├── light_mode.svg                         (placeholder until first run)
├── dark_mode.svg                          (placeholder until first run)
├── templates/
│   ├── light_mode.svg.template
│   └── dark_mode.svg.template
└── .github/workflows/
    └── update-stats.yml
```

## 2. Create a Personal Access Token

The script needs a token to read your GitHub data (public repo stats can be
read with a basic token; if you want private repos counted too, include the
`repo` scope).

1. Go to **GitHub → Settings → Developer settings → Personal access tokens
   → Tokens (classic) → Generate new token**.
2. Scopes needed: `repo` (or `public_repo` if you only want public repos
   counted) and `read:user`.
3. Copy the token — you won't see it again.

## 3. Add it as a repo secret

1. In `shanujans/shanujans` → **Settings → Secrets and variables → Actions
   → New repository secret**.
2. Name: `ACCESS_TOKEN`
3. Value: the token you copied.

## 4. Enable Actions (if not already)

Go to the **Actions** tab of the repo and enable workflows if prompted.

## 5. Run it

- Push these files to `main` — the workflow runs automatically on push.
- Or trigger it manually: **Actions → Update GitHub Stats SVG → Run workflow**.

It re-runs every 12 hours after that (edit the `cron` line in
`update-stats.yml` to change the frequency), and commits the refreshed
`light_mode.svg` / `dark_mode.svg` back to the repo automatically.

## Customizing

- Change your displayed name/role: edit `DISPLAY_NAME` / `DISPLAY_ROLE` in
  `.github/workflows/update-stats.yml`.
- Change colors, spacing, or wording: edit `templates/dark_mode.svg.template`
  and `templates/light_mode.svg.template` directly — placeholders like
  `{{REPOS}}` get substituted by `today.py`, everything else is plain SVG/CSS.
- `today.py` currently counts: account age on GitHub, owned public repos,
  repos contributed to, total commits, stars earned, followers, and total
  lines added/removed across your owned repos. You can extend the GraphQL
  query in `get_user_overview()` to pull more (e.g. PRs, issues) and add
  matching lines to the templates.

## Notes

- The card's fade-in/typing animation and blinking cursor are done in pure
  CSS inside the SVG — they play in any browser when the raw SVG is loaded
  directly (which is how `raw.githubusercontent.com` serves it), same as
  Andrew's.
- If `today.py` fails with a 401/403, double check the `ACCESS_TOKEN` secret
  is set and the token hasn't expired.
