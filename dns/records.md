# DNS for the three Matt Jones, LLC sites

This repository is `coolmatt.games`. The other two addresses have their own repositories and are
listed here so the whole picture is in one place. Each address is its own site; none of them is a
redirect to another.

Checked against public DNS and GitHub Pages on 2026-11-22. Run `dns/check.sh` to see today's
answers. The hosting history and cutover steps are in `docs/hosting.md` in
`Matt-Jones-LLC/matt-jones.org`.

| Address            | What it is                    | Repository                        | DNS managed at |
|--------------------|-------------------------------|-----------------------------------|----------------|
| `coolmatt.games`   | The main arcade               | `Matt-Jones-LLC/cool-matt-games`  | GoDaddy        |
| `coolmattgames.io` | The lab: experimental arcade  | `Matt-Jones-LLC/coolmattgames.io` | GoDaddy        |
| `matt-jones.org`   | The company site, and email   | `Matt-Jones-LLC/matt-jones.org`   | Squarespace    |

DNS records and domain settings are Matt's to change. These notes say what the records are, not
that anyone should edit them.

## The GitHub Pages records

All three sites are served by GitHub Pages, so all three use the same apex records:

| Host | Type | Value                 |
|------|------|-----------------------|
| `@`  | A    | `185.199.108.153`     |
| `@`  | A    | `185.199.109.153`     |
| `@`  | A    | `185.199.110.153`     |
| `@`  | A    | `185.199.111.153`     |
| `@`  | AAAA | `2606:50c0:8000::153` |
| `@`  | AAAA | `2606:50c0:8001::153` |
| `@`  | AAAA | `2606:50c0:8002::153` |
| `@`  | AAAA | `2606:50c0:8003::153` |

`www` is a CNAME to the GitHub Pages host of the account that owns the repository. For the
`Matt-Jones-LLC` organization that is `matt-jones-llc.github.io`.

## coolmatt.games

GoDaddy: **Domain Portfolio → coolmatt.games → DNS → DNS Records**.

- The four `A` and four `AAAA` records above are in place.
- `www` is a CNAME to `matt-jones-org.github.io`, from when this repository belonged to Matt's
  personal account. It still resolves and `www.coolmatt.games` redirects to `coolmatt.games`.
  Pointing it at `matt-jones-llc.github.io` is the tidy-up for the next DNS maintenance.
- There must be no forwarding on this domain (the **Forwarding** tab says "Not set up"). GoDaddy
  forwarding adds two locked `A` records of its own, which would send some visitors to GoDaddy
  instead of the site.
- Leave the `NS`, `SOA`, `_domainconnect` and `_dmarc` records GoDaddy created.

GitHub Pages has `coolmatt.games` as this repository's custom domain, with HTTPS enforced.

## coolmattgames.io

GoDaddy: **Domain Portfolio → coolmattgames.io → DNS → DNS Records**.

- Public DNS returns the four `A` records above and no `AAAA` records.
- `www` is a CNAME to `matt-jones-llc.github.io`.
- This domain used to forward to `coolmatt.games`. Some resolvers were still returning GoDaddy's
  forwarding addresses on 2026-11-22; a visitor behind one of those gets GoDaddy's "Not Found"
  page until the old answer expires.

GitHub Pages has `coolmattgames.io` as the lab repository's custom domain and serves the lab over
plain HTTP. HTTPS was not available yet on 2026-11-22: no certificate had been issued, so
**Enforce HTTPS** was still off.

## matt-jones.org

Squarespace: **Settings → Domains → matt-jones.org → DNS**.

- The four `A` and four `AAAA` records above are in place.
- `www` is a CNAME to `matt-jones-org.github.io`. It resolves and `www.matt-jones.org` redirects to
  `matt-jones.org`. As with `coolmatt.games`, `matt-jones-llc.github.io` is the tidy-up.

GitHub Pages has `matt-jones.org` as the company repository's custom domain, with HTTPS enforced.
The arcade lived at this address until November 2026. Old game links such as
`matt-jones.org/games/shapes/` land on the company site's not-found page, which sends the browser
on to the same path at `coolmatt.games`.

### Email (Google Workspace): leave alone

Email for `matt-jones.org` is Google Workspace and is not affected by any of the above. Keep
whatever Google Workspace records exist. They're usually shown as the "Google Workspace" preset.
Don't touch MX, the `v=spf1` TXT, `google._domainkey`, `_dmarc`, or any `google-site-verification`
TXT. If any are missing, the target values are:

| Host                | Type | Value                                               |
|---------------------|------|-----------------------------------------------------|
| `@`                 | MX   | `1 smtp.google.com`                                 |
| `@`                 | TXT  | `v=spf1 include:_spf.google.com ~all`               |
| `google._domainkey` | TXT  | DKIM key from admin.google.com → Gmail → Authenticate email |
| `_dmarc`            | TXT  | `v=DMARC1; p=none; rua=mailto:matt@matt-jones.org`  |

## Optional: verify the domains with GitHub

To stop anyone else's GitHub repository from claiming a domain: in the `Matt-Jones-LLC`
organization's **Settings → Pages → Add a domain**, add each of the three domains. GitHub shows a
TXT record (`_github-pages-challenge-matt-jones-llc`) to add at each domain's DNS. None of the
three had that record on 2026-11-22.
