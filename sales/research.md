# Walk-in sales research: NFC review stands, Business Profile tune-ups, takeaway websites
Stone · Newcastle-under-Lyme · Tamworth. Compiled 26 Sep 2026.

**Method and limits.** Sections A and B come from web-search results (fetching pages was blocked in the
cloud session), so figures marked "via search summary" should be checked before quoting them to a customer.
"Unverified" = background knowledge, no source opened. Section C comes from the FSA hygiene register
(open data, via a public daily GitHub mirror); Google ratings, delivery apps and websites were **not** checked.
The prospect list is in `prospects.json` (85 independents), rebuilt by `build_prospects.py`.

## A. Suppliers and tools (UK)

### A1. Blank NFC cards (NTAG213/215, white PVC)
- Amazon UK: https://www.amazon.co.uk/s?k=ntag213+nfc+card+white+pvc · https://www.amazon.co.uk/s?k=ntag215+nfc+card+white+pvc
- Seritag (UK, TabDesk Ltd): gloss white PVC NTAG213, CR80, printable in desktop card printers; slotted, adhesive and custom-printed versions.
  https://seritag.com/nfc-tags/pvc-cards-gloss-ntag213 · https://seritag.com/nfc-tags/cards · https://seritag.com/nfc-tags/pvc-card-adhesive
- ZipNFC (UK): NTAG215 white PVC card **£0.42 each (£0.38 bulk)** (via search summary); custom printing from 1 card.
  https://zipnfc.com/nfc-tag-pvc-card-credit-card-size-ntag215.html · https://zipnfc.com/nfc-pvc-card-bespoke-custom-branded-printed-cards-ntag215.html
- ID Cards Direct (UK): https://www.idcardsdirect.co.uk/ntag213-rfid-nfc-blank-white-iso-pvc-card.html
- NTAG213 (144 bytes) is plenty for a review link.

### A2. NFC stickers
- Amazon UK NTAG213 25 mm, 100: https://www.amazon.co.uk/NTAG213-NFC-Stickers-Ntag213-Compatible/dp/B0F2F9KFDY · 50: https://www.amazon.co.uk/NTAG213-NFC-Stickers-Ntag213-Compatible/dp/B0F2FBZT42
- Search: https://www.amazon.co.uk/s?k=ntag213+nfc+stickers
- Seritag 29 mm: https://seritag.com/nfc-tags/29mm-white-ntag213 · **on-metal** disc for steel counters: https://seritag.com/nfc-tags/30mm-on-metal-pvc-disc-ntag213

### A3. Acrylic sign holders (A6 / A5 / 10x15 cm)
- Amazon UK A6 slanted 3-pack: https://www.amazon.co.uk/A6-Acrylic-Sign-Holder-Slanted/dp/B00MUTWKHU · Kurtzy A6 6-pack: https://www.amazon.co.uk/A6-Acrylic-Sign-Holder-Slanted/dp/B07PQJ2XBS
- Searches: https://www.amazon.co.uk/s?k=a5+acrylic+sign+holder · https://www.amazon.co.uk/s?k=10x15cm+acrylic+sign+holder
- Stationery Wholesale A5 L-shape £1.94 inc VAT (via search summary): https://www.stationerywholesale.co.uk/a5-vertical-design-l-shape-transparent-acrylic-label-sign-holder/
- 3D Displays A6 angled: https://www.3ddisplays.co.uk/literature-displays-c16/sign-holders-c20/angled-c117/a6-angle-portrait-sign-holder-counter-counter-sign-holder-p88

### A4. The market price you compete with (ready-made NFC review stands/cards)
- Tap To Review stand **£35**: https://taptoreview.co.uk/products/google-review-stands-nfc
- Tap and Rate stand **£39.95**: https://tapandrate.co.uk/products/google-reviews-one-tap-google-reviews-stand
- OneTap Review bundle **from £28**: https://onetapreview.co.uk/product/tap-nfc-google-review-stands/
- Local Insights bundles **£49**: https://reviews.localinsights.co.uk/
- Etsy UK custom stands **£10–£75**: https://www.etsy.com/uk/market/google_review_stand_nfc
- Seritag stand (encodes your link free): https://seritag.com/nfc-tags/google-review-stand
- **Conclusion:** £30 is on-market. Your edge is setting it up on the spot with the right link, and bundling it with the Business Profile tune-up.

### A5. Card readers (take payment on the spot)
- **Square Reader £19 + VAT**, 1.75% in person, no monthly fee: https://squareup.com/gb/en/hardware/reader · https://squareup.com/gb/en/pricing
- **Zettle Reader 2 £29 + VAT** (first reader, new users), 1.75%: https://www.zettle.com/gb/payments/card-reader
- **SumUp** Air/Solo Lite ~£19–£59 + VAT depending on promo, 1.69%: https://store.sumup.com/en-GB/product-selection/card_reader.air

### A6. Print
- Vistaprint UK, 100 business cards £11.99: https://www.vistaprint.co.uk/business-cards/standard/templates/custom/inexpensive · flyers: https://www.vistaprint.co.uk/marketing-materials/flyers-folded-leaflets
- Solopress cards "from £4.99": https://www.solopress.com/business-cards/ · A5 leaflets: https://www.solopress.com/flyers-leaflets/a5/
- Instantprint A5: https://www.instantprint.co.uk/flyers-leaflets/a5

### A7. Domains and hosting
- Porkbun .co.uk ~$4.66 (renewal ~$5.66): https://porkbun.com/products/domains · Namecheap .co.uk ~$5.18 first year: https://www.namecheap.com/domains/registration/cctld/co-uk/
- Cloudflare Registrar lists .uk domains: https://developers.cloudflare.com/registrar/top-level-domains/uk-domains/
- **Cloudflare Pages (free)** for client sites: https://developers.cloudflare.com/pages/platform/limits/index.md (Netlify's free tier now pauses sites when credits run out: https://www.netlify.com/changelog/2026-04-14-pricing-updates-april-2026/)

### A8. Website builders
- Carrd Pro Standard **$19/yr** (custom domain): https://carrd.com/pro · Framer from $10/mo · Squarespace UK from £12/mo · Wix UK from £9/mo
- Margin: Carrd or Pages + a domain ≈ £20/yr, so a £25/month care plan is nearly all profit.

### A9. Online ordering platforms (the "stop paying 30%" upsell)
- **Square Online**: free plan, **1.4% + 25p** per UK-card order: https://squareup.com/gb/en/online-ordering
- Flipdish: subscription (from ~€69/month annual): https://www.flipdish.com/gb/pricing
- Slerp (commission-free, monthly fee): https://www.slerp.com/
- Foodhub (0% commission, flat fee): https://global.foodhub.com/
- OrderYOYO (branded app; diners pay a £0.75 service fee): https://www.orderyoyo.com/
- Budget: Swiftorder £12.50/week: https://www.swiftorder.co.uk/ · Eatzy from £2/day: https://www.eatzyepos.com/commission-free-online-ordering-system-for-uk-restaurants-takeaways-eatzy

### A10. NFC writing apps
- NXP TagWriter: Android https://play.google.com/store/apps/details?id=com.nxp.nfc.tagwriter · iOS https://apps.apple.com/us/app/nfc-tagwriter-by-nxp/id1246143221
- NFC Tools: Android https://play.google.com/store/apps/details?id=com.wakdev.wdnfc · https://www.wakdev.com/en/apps.html
- Test on an iPhone and an Android, then lock the tag read-only (unverified tip).

### A11. The Google review link
1. **Best (owner's phone):** Business Profile → Read reviews → Get more reviews → Copy (`g.page/r/XXXX/review`). https://support.google.com/business/answer/16816815?hl=en
2. **Without owner access:** Place ID Finder https://developers.google.com/maps/documentation/javascript/examples/places-placeid-finder → `https://search.google.com/local/writereview?placeid=PLACE_ID`. The customer must be signed in; iOS Safari may open the profile instead of the form.
3. Pro move: point the chip at a redirect on **your** domain (e.g. `yourdomain.co.uk/r/priory`), so you can fix a broken link without re-writing the chip. That is also a reason for the care plan.

## B. Pitch stats and rules

- **Luca (Harvard Business School, 2011):** one extra Yelp star = **5–9% more revenue** for *independent* restaurants (no effect for chains).
  https://www.hbs.edu/ris/Publication%20Files/12-016_a7e4a5a2-03f9-490d-b093-8f951238dba2.pdf
- **BrightLocal Local Consumer Review Survey 2026** (US panel, via search summaries): 97% read reviews before choosing a local business;
  **68% need at least 4 stars**; **47% won't consider a business with fewer than 20 reviews**; **74% look only at reviews from the last three months**;
  **88% would use a business that replies to all reviews vs 47% if it replies to none**. https://www.brightlocal.com/research/local-consumer-review-survey/
- **Google** (local ranking help): complete, accurate information makes a business more likely to show in local results; reviews help prominence.
  https://support.google.com/business/answer/7091?hl=en · The widely quoted "2.7x more reputable / 70% more visits" is an old Google/Ipsos figure; say "Google's own research found…" only loosely.
- **Delivery-app commission** (2026 ranges via search summary, check per platform): Uber Eats 15–30%, Deliveroo 14–30%, Just Eat 14–22%.
  Worked example: moving 10 app orders a week at £25 from 25% commission to ~2% card fees saves ~£57/week (~£3k/year).
- **FSA hygiene ratings:** display is voluntary in England, mandatory in Wales and Northern Ireland (unverified here; check food.gov.uk).
  Every business has a page: `https://ratings.food.gov.uk/business/{FHRSID}`.
- **Rules (keep the business safe):** Google prohibits incentives for reviews ("fake engagement"): https://support.google.com/business/answer/3474050?hl=en.
  No review gating (don't ask only happy customers). UK DMCC Act 2024 bans fake and concealed-incentive reviews from April 2025 (check CMA guidance on gov.uk).
  **Product rules:** never write reviews for clients, no discounts for reviews, ask every customer.

## C. Prospects (FSA register; independents only)
Stone 25 · Newcastle town centre 32 · Tamworth 28. 16 are new since Nov 2025 and 3 await a first inspection (warmest leads).
Low hygiene ratings (0–2): lead with the Business Profile tune-up and a website, not reviews.
Sources: https://raw.githubusercontent.com/food-hygiene-uk/data/main/public/files/open-data-files/FHRS292en-GB.json (Stafford, covers Stone) ·
FHRS290 (Newcastle-under-Lyme) · FHRS295 (Tamworth, extract 24 Jul 2026). Just Eat area pages: https://www.just-eat.co.uk/area/st15 · /st5 · /b77 · /b78 · /b79 (format confirmed, pages not opened).
Record on each visit: Google rating, review count, date of latest review, whether the owner replies, whether hours are right,
whether there's a website with a menu, which apps they're on.
