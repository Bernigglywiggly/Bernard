# QC: Low-Stim Phone Kit (12 Oct 2026)

Independent check of the files a buyer actually gets. All 4 zips were unzipped into fresh folders. I looked at every wallpaper, both icon sheets at 60 px and 150 px, every PDF page, and all 5 listing images, including image 01 at 340 px.

**Verdict: fix first.** The product works and the files are clean, but two things will cost sales or reviews: duplicate wallpapers counted as separate items, and wallpaper and lock screen images that look like blank black rectangles. Both need changes in make.py and mock.py.

## Findings

| # | Area | Check | Result | Detail / action |
|---|---|---|---|---|
| 1 | Zips | Open, structure, junk | PASS | All 4 open. No .DS_Store, __MACOSX or `._` files. Clear folder names. Part zips are 10.6, 12.9 and 3.2 MB. FULL zip has 237 files (24 wallpapers + 200 icons + PDF + 2 licences + folders). |
| 2 | Zips | Etsy file limit | NOTE | FULL zip is 26.7 MB, over Etsy's 20 MB per-file limit. Upload the 3 part zips to Etsy and use FULL on Gumroad only. Now noted in LISTING.md. |
| 3 | Wallpapers | Counts and sizes | PASS | 12 iPhone at 1320×2868 (6 home + 6 lock). 12 Android at 1440×3200. |
| 4 | Wallpapers | **Duplicates** | **FIX** | `01_matte` and `02_fade` home and lock files are **byte-identical**, on both iPhone and Android. So "24 wallpapers" is really 20 unique files, and only about 6 visual designs. A buyer who opens them will see padding. **make.py:** give each lock version a real difference (for example a bottom vignette, a lighter top band behind the clock, or the motif moved down), or change the claim to "6 designs, home + lock, 2 sizes". |
| 5 | Wallpapers | Banding and artefacts | PASS (minor) | Grain at about σ3.7 hides banding at normal viewing. Faint stripes show in `fade` only under extreme contrast stretch. No JPEG artefacts. |
| 6 | Wallpapers | Text strength | PASS | "one thing at a time" is about 24 px tall at grey 104 on 35. Readable, but quiet. |
| 7 | Wallpapers | Motif visibility | FIX (design) | `ring` is only about 7 to 20 levels above the background, so it looks identical to `matte` on most screens and in the listing images. `line` is also very faint. **make.py:** raise the ring and line contrast to about +30 to 40 levels. |
| 8 | Wallpapers | Lock screen clock area | PASS | Lock versions put the motif lower (`words` at 81% down, `ring`, `line` and `contour` in the lower half). Top 40% is clear. |
| 9 | Wallpapers | Home motif position | NOTE | On home versions the `words`, `line` and `ring` motifs sit at about 33 to 48% height, behind icon rows 3 and 4 of a full grid. That's fine for an 8 to 12 icon page. Consider about 60% height in make.py. |
| 10 | Icons | Count, size, tones | PASS | 100 per tone, 2 tones, all 1024×1024. Names match across tones. |
| 11 | Icons | Name vs glyph | PASS | Checked all 100 names against the pictures. All match. |
| 12 | Icons | Duplicate meaning | FIX (minor) | `passwords` and `vpn` are both keys and nearly identical at 60 px. `slides`, `video` and `live_tv` are 3 play-button glyphs. **make.py:** swap `vpn` for a shield-lock or globe-lock glyph, and `slides` for a presentation or easel glyph. |
| 13 | Icons | Centring | FIX (minor) | Wide, short glyphs sit about 64 px (6%) above centre: `code`, `vpn`, `passwords`, `quotes`, `meetings`, `reminders`. That's about 4 px at home-screen size. **make.py:** centre by ink bounding box, not font metrics. |
| 14 | Icons | Legible at 60 px | PASS | Both tones are clear at 60 px. Graphite is grey 169 on 45. Ash is grey 43 on 152. |
| 15 | Icons | Trademarks | FIX (low risk) | The `bluetooth` glyph is the Bluetooth SIG's registered figure mark. Swap or drop it to keep the "no brand logos" claim watertight. `crypto` (₿) is fine because the symbol is unregistered. No app logos anywhere. |
| 16 | PDF | Layout | FIXED | The comparison table rendered as flattened "a · b · c" lines, so I rewrote it as bullets. "Option A/B" are now headings, so Option B is no longer stranded at the bottom of page 5. "[Android, Pixel]" lines showed raw brackets; they now use the Android pill plus "Pixel:". I removed a widow page (licence moved to page 1). The guide is now 7 pages. |
| 17 | PDF | Remaining design issues | FIX (design) | guide_pdf.py strips **bold**, so troubleshooting questions look like their answers. The PDF is raster-only (no selectable text or search). There's no cover page or visuals. Add bold rendering, and ideally a cover plus 2 or 3 screenshots, in guide_pdf.py. |
| 18 | PDF | Factual risk (iOS 26/27) | FIXED / NOTE | Track 2 step 9 used to say "Default **or Dark**". iOS 26's auto-generated Dark and Tinted styles can restyle shortcut icons, so it now says Default (Dark usually OK with graphite). Colour Filters, Accessibility Shortcut, Focus › Customise Screens, Shortcuts › Add to Home Screen and Remove from Home Screen are correct. iOS 27 home-screen menus are unverified, but the copy says "iOS 26 and later" plus a menu-names disclaimer. |
| 19 | PDF | Factual risk (Android 16) | FIXED / NOTE | Pixel dark theme is now "Display (or Display & touch)". Samsung custom modes may not offer greyscale, so the copy now points to the built-in Sleep mode, which has it. Samsung's Digital Wellbeing › Bedtime mode no longer exists on One UI 6+, but the guide already gives the Modes alternative. Shortcut Maker's exact button names are unverified. |
| 20 | Copy | Medical claims | PASS | ADHD is mentioned only with "not a treatment" disclaimers, in the guide and the FAQ. "Dopamine detox" is a lifestyle term. No cure claims. PROMO.md bans results claims. |
| 21 | Copy | Trademarks in copy | PASS (note) | "iPhone", "iOS", "Android", "Pixel" and "Samsung" are used only as compatibility words. The title opens "Minimalist iPhone Home Screen Kit"; "…Home Screen Kit for iPhone" would be safer but loses keyword position. This pattern is common on Etsy, so it's low risk. |
| 22 | Copy | Licence | FIXED | The buyer licence is clear. I added a credits line (Material Symbols Apache 2.0, Inter OFL) to the guide, as Apache attribution expects, and listed `licences/` in "What's in your download". |
| 23 | Copy | Digital-download wording | FIXED | The Etsy description now says the buyer gets 3 ZIP files. The refund line now reads "returns and exchanges aren't accepted… if a file is faulty I'll fix it or make it right", in line with the UK Consumer Rights Act on faulty digital content. |
| 24 | Copy | Internal notes | FIXED | The LISTING.md mockup list didn't match the real 5 images, and the "upgrade at 100+ icons" note was stale. Both updated. |
| 25 | Value risk | Free source icons | NOTE | The glyphs are restyled Google Material Symbols, which are free. That's legal under Apache 2.0, but a buyer or a competitor reporting under Etsy's "made by me" rules could call it low effort. The wallpapers and guide are the real value-add, so they need to look distinct (see #4 and #7). |
| 26 | Listing img 01 | 340 px thumbnail | PASS with fix | The headline and the colourful "before" phone read well at thumbnail size, so it will catch the eye. But the right-hand text block (iPhone + Android / 24 wallpapers…) is unreadable at 340 px, and about 30% of the frame is empty beige. **mock.py:** make the two phones about 85% of the height, drop the small grey text, and add one bold pill at about 60 px+ type: "200 icons + 24 wallpapers + guide". |
| 27 | Listing img 04/05 | Accuracy and appeal | FIX (design) | Image 04 shows 6 near-identical black rectangles, and image 05 shows 3 lock screens that look the same. That's honest, but it undersells the product. Fix after #4 and #7, or show crops at higher contrast. Add a 6th image showing one guide page, since nothing currently shows the guide. |

## Design fixes for you (make.py / mock.py / guide_pdf.py, not changed by QC)

1. **make.py:** make the matte and fade lock versions differ from their home versions (#4).
2. **make.py:** raise ring and line contrast (#7). Consider moving home motifs to about 60% height (#9).
3. **make.py:** swap `vpn`, `slides` and `bluetooth` glyphs, and centre glyphs by ink bounding box (#12, #13, #15).
4. **mock.py:** image 01 with bigger phones and one bold pill instead of small grey text (#26). Image 04/05 at higher contrast. New image 06 showing a guide page (#27).
5. **guide_pdf.py:** render bold, and add a cover page (#17).

## Files changed by QC

- GUIDE.md: copy fixes (#16, #18, #19, #22). PDF rebuilt (7 pages).
- LISTING.md: copy fixes (#2, #23, #24).
- Re-zipped LowStim_3_icons_guide.zip and LowStim_Phone_Kit_FULL.zip from out/kit. Zips 1 and 2 are unchanged.
- Originals of both .md files backed up in the QC scratchpad.
