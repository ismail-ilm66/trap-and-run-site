# Trap & Run website

The public site for the Trap & Run game: landing page, Privacy Policy, Terms
of Service, account-deletion instructions and support. Static files, no build
tools beyond Python 3 for the legal pages. Hosted on GitHub Pages.

```
index.html            landing page (edit directly)
src/*.md              Privacy, Terms, Delete account, Support (edit these)
src/page.html         the shared shell for those four pages
build.py              turns src/*.md into privacy.html, terms.html, …
assets/               logo, icon, feature graphic, screenshots, style.css
.well-known/          invite-link files once the domain exists
.nojekyll             serve files as they are (and the .well-known folder)
```

## Before publishing

1. In `build.py`, set `STUDIO` and `SUPPORT_EMAIL`, then run `python3 build.py`.
2. In `src/privacy.md`, fill the hosting region (§8) and the address (§10);
   in `src/terms.md`, the governing law and courts (§13). Rebuild.
3. When the app is live, replace the "Coming to Google Play" pill in
   `index.html` with the official Play badge linking to the listing.

## Deploy on GitHub Pages

1. Create a public repository (e.g. `trap-and-run-site`) and push this
   folder to its `main` branch.
2. Repository *Settings → Pages → Build and deployment*: source *Deploy
   from a branch*, branch `main`, folder `/ (root)`.
3. Pages are live a minute later at `https://<user>.github.io/<repo>/`.
   Paste `…/privacy.html` into Play Console → App content → Privacy
   policy, and `…/delete-account.html` into the account-deletion field.

Custom domain later: *Settings → Pages → Custom domain*, add the DNS
records GitHub shows, tick *Enforce HTTPS*, and put the domain in a `CNAME`
file here. Then `.well-known/assetlinks.json` and
`.well-known/apple-app-site-association` go in this repository, and the
invite-link host in the app changes from `invite.example.com` to the domain.

## Screenshots and graphics

Copies of the Play Store assets in the game repository (`art/store/`).
Regenerate there, then copy over.
