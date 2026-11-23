#!/usr/bin/env bash
# Shows what public DNS returns for the three Matt Jones, LLC sites and the email,
# then what each address answers. See dns/records.md for what it should say.
# Asks 8.8.8.8 directly so a stale local resolver cache does not hide a change.
for q in "NS coolmatt.games" "A coolmatt.games" "AAAA coolmatt.games" "CNAME www.coolmatt.games" \
         "NS coolmattgames.io" "A coolmattgames.io" "AAAA coolmattgames.io" "CNAME www.coolmattgames.io" \
         "NS matt-jones.org" "A matt-jones.org" "AAAA matt-jones.org" "CNAME www.matt-jones.org" \
         "MX matt-jones.org" "TXT matt-jones.org" "TXT google._domainkey.matt-jones.org" "TXT _dmarc.matt-jones.org"; do
  set -- $q; printf '%-6s %-36s ' "$1" "$2"; dig +short "$1" "$2" @8.8.8.8 | tr '\n' ' '; echo
done
# Each address is its own site: the arcade, the lab, and the company site.
# The www addresses redirect to the bare domain. An old arcade link at matt-jones.org answers 404
# and its not-found page sends the browser on to coolmatt.games.
for u in https://coolmatt.games https://www.coolmatt.games/about/ \
         http://coolmattgames.io https://coolmattgames.io \
         https://matt-jones.org https://www.matt-jones.org/ https://matt-jones.org/games/shapes/; do
  curl -sSo /dev/null --max-time 15 -w "$u -> %{http_code} %{redirect_url}\n" "$u"
done
