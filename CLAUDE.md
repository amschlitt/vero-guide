# 1381 3rd Court: four outputs that must always stay in sync

Any change Andrea asks for (wording, a place, an address, a link, a rule) must be applied to ALL FOUR outputs, in any conversation:

1. **Website welcome book** (this repo, GitHub Pages: https://amschlitt.github.io/vero-guide/). Pages: `welcome/` (menu), `welcome/house/`, `welcome/stay/`, `welcome/eat/`, `welcome/explore/`, `welcome/vero/`, `how-to/` (index) and `how-to/<guide>/`. Edit the HTML directly, commit, push to `main`.
2. **Welcome book PDF**: generated from the site pages. Run `python3 tools/build_welcome_pdf.py /path/Welcome_Book_1381_3rd_Court.pdf` (needs Google Chrome). Never hand-edit the PDF.
3. **Owner's manual PDF** (Airbnb listing and owner launch checklist): PRIVATE, never put it in this public repo. Its source and build script live in the claude.ai Project "1381 3rd court" as docs `claude/owners-manual-source.html` and `claude/build_owners_manual.py` (read with the Projects tool, write to disk, run `python3 build_owners_manual.py SOURCE POOL_JPG OUT_PDF`, using `welcome/pool.jpg` from this repo). After changing the source, write the updated source back to the Project doc.
4. **QR code printable sheet**: `python3 tools/build_qr_sheet.py /path/QR_Codes_1381_3rd_Court.pdf` (pip install segno reportlab). Update the `items` list in that script when sections or guides are added, removed or renamed. Scan-check a few codes after building.

## Workflow for every request
- Clone this repo (add_repo with push access if needed), make the edit on the site, then rebuild PDFs 2-4 as needed and send them with SendUserFile. Push the site changes unless Andrea says to hold.
- Check the owner's manual for the same wording (house rules, summary, title) even when the request sounds website-only.
- Keep the guest copy consistent everywhere: "cozy two-bedroom, one-bathroom cottage"; no smoking of any kind indoors; pets: pick up after them and never leave them unattended outside; guests contact the host through the Airbnb or VRBO app; every address is a Google Maps link on the site, full address at the end of the entry with city and state; never start a sentence with a number.
- The site is public. Do not publish owner-only content or placeholders with private details.
