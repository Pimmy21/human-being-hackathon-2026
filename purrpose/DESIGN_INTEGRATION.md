# Connected home design

Source design: Josh Christian's merged logo/light home PR, upstream commit2a2c4d203d9ccfe256f0f9f11ef1e1a43be45cc5 (`design/home/index.html` and two SVG favicons). Retrieved in a separate no-checkout review directory; the development checkout was not reset, merged or overwritten. No remote code/build script was executed. This adapter preserves the design layout/inline vector logo/glow/cool-warm controls while connecting the existing API.

## Open

Run the local server, then open http://127.0.0.1:8766/home.html . The existing full workspace remains at `/`. There is a reciprocal link between them. For rescues navigates to `/#organization`, which now opens that view. This is local only, not a public site.

## What changed from the static preview

- Form submits to the existing bounded-intent chat API, using the same local client,65second deadline and no automatic retries.
- Real default discovery, city preference/expansion, Lucy evidence/gaps/allocation, explicit refresh, official H-MEM receipt/history and organization checklist render from backend responses.
- Known exact Lucy article URLs open their saved research; this does not silently fetch them. Arbitrary/private URLs are rejected locally without a request. Explicit source refresh remains restricted server-side to configured articles.
- Removed fake sign-in, unsupported claims of arbitrary/social-page retrieval and made-up example appeal chips. The replacement chips represent actual supported requests. Click fills the prompt; Send submits it.
- CSS and JavaScript are external local assets for existing CSP; no inline script/style, Google font requests or new packages. The wordmark's vector paths remain; text uses system fallback typography.
- Source/user/provider text renders via textContent. Clickable source URLs use a restricted HTTPS host list. No untrusted HTML, provider credentials or payment forms rendered.
- Original upstream design remains unchanged. Functional adaptation is in `purrpose/web/design-home.*` plus local favicons; it is not a merged GitHub update.

## Actual checks

161full application tests passed with official H-MEM configured. JavaScript syntax check passed. Browser exercised designed-page donor request→preference→real pending lead→unknown amount, warm-theme switching and unsupported/private-URL handling.390px viewport had no horizontal overflow. No page errors and zero external asset requests. Screenshots in workspace outputs/purrpose/designed-home-desktop.png and designed-home-mobile.png. No new inference/SQL/live-source calls were needed for this verification.

The original full workspace remains available. This is an initial working design integration, not final approved UI/UX. Nightshift remains unconnected, and models do not write chat answers (since 25 Oct an optional configured model classifies chat intent; see MODEL_PROVIDER_VERIFICATION.md); the real case remains pending. A design does not expand backend evidence coverage. Local uncommitted changes require explicit upload authority and safe synchronization before they become shared work.

Organization entry now links to `/organizations.html`, a separate, clearly labeled fictional walkthrough: review public information, explain gaps, prepare a website update, simulate publication, recheck, and preview the supporter result. No backend/API/model call occurs. Better documentation does not itself confer qualification. The real Lucy checklist remains separate.
