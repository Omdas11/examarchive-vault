# INGESTION RUNBOOK — examarchive-vault → live site

How an admin ingests the curated markdown files in this vault into the live
ExamArchive site (`examarchive.dev`). Generated 2026-10-01.

## Prerequisites

- Admin account on the live site (the `/admin/ingest-md` page and the
  `/api/admin/ingest-md` endpoint both require an admin role; non-admins get
  rejected).
- The markdown files below, as committed in this repo (`main` branch).

## Ingestion order (important)

1. **Syllabus files first** (`*-syllabus.md`). Question entries auto-link to
   syllabus entries by `paper_code`, so syllabi must exist before questions.
2. **Question files next** (`*-questions-<year>.md`).

## Step-by-step

1. Sign in to `https://examarchive.dev` with an admin account.
2. Open `https://examarchive.dev/admin/ingest-md`.
3. Upload the syllabus `.md` files (the page accepts multiple files; they are
   POSTed one-by-one to `/api/admin/ingest-md` as multipart form `file`).
   Recommended batches (syllabus):
   - Batch S1 — Physics DSC theory (25 files): `PHYSICS/PHYDSC101T-syllabus.md`
     through `PHYSICS/PHYDSC454T-syllabus.md` (incl. `PHYDSC453AT`, `PHYDSC453BT`).
   - Batch S2 — Physics DSM + SEC + IDC (16 files): `PHYSICS/PHYDSM*-syllabus.md`,
     `PHYSICS/PHYSEC*-syllabus.md`, `PHYSICS/PHYIDC*-syllabus.md`.
4. Watch the ingestion log on the same page; every file should report success
   with `paperCode` and rows affected. Re-upload any file that reports an error.
5. Verify linkage: open a paper (e.g. PHYDSC101T) and confirm the syllabus table
   renders and `syllabus_pdf_url` was auto-generated.
6. Upload question files (`QUESTION/**`), then spot-check that each question
   paper shows `link_status: linked` to its syllabus entry.

## Batch S1+S2 file list (Physics — 41 files, committed 2026-10-01)

All under `PHYSICS/`:
PHYDSC101T, PHYDSC102T, PHYDSC151T, PHYDSC152P, PHYDSC201T, PHYDSC202T,
PHYDSC251T, PHYDSC252T, PHYDSC253P, PHYDSC301T, PHYDSC302T, PHYDSC303P,
PHYDSC351T, PHYDSC352T, PHYDSC353T, PHYDSC354P, PHYDSC401T, PHYDSC402T,
PHYDSC403T, PHYDSC404P, PHYDSC451T, PHYDSC452T, PHYDSC453AT, PHYDSC453BT,
PHYDSC454T, PHYDSM101T, PHYDSM151T, PHYDSM201T, PHYDSM251P, PHYDSM252T,
PHYDSM301T, PHYDSM302T, PHYDSM351P, PHYDSM401T, PHYDSM451T,
PHYSEC101T, PHYSEC151T, PHYSEC201T, PHYIDC101T, PHYIDC151T, PHYIDC201T
(each as `{CODE}-syllabus.md`).

## Known caveats for the admin

- **Do NOT ingest these 8 phantom files** — they are auto-generated, do not
  correspond to any paper in the official AU syllabus, and must be excluded
  (or deleted from the vault):
  `PHYSICS/PHYDSC152T`, `PHYSICS/PHYDSC253T`, `PHYSICS/PHYDSC303T`,
  `PHYSICS/PHYDSC354T`, `PHYSICS/PHYDSC404T`, `PHYSICS/PHYDSC453T`,
  `PHYSICS/PHYDSM251T`, `PHYSICS/PHYDSM351T` (all `-syllabus.md`).
- **PHYDSC352T attribution**: the official PDF prints the Statistical Mechanics
  + Plasma Physics units immediately after the PHYDSC351T block under one
  header; they are filed under PHYDSC352T per the official semester-wise paper
  list (see `notes` in the file).
- **Hyphenated official codes**: the vault uses validator-safe codes
  (`PHYSEC101T`); the official hyphenated forms (`PHYSEC-101` etc.) are kept in
  the `aliases` field. If a future validator accepts hyphens, prefer the
  official forms.
- **Question files**: to be added (see below).

## Pending

- [ ] Chemistry syllabus entries (awaiting official AU FYUG Chemistry syllabus)
- [ ] Mathematics syllabus entries (awaiting official AU FYUG Mathematics syllabus)
- [ ] Question entries for verified Chemistry/Mathematics FYUG papers
      (awaiting `~/workspace/examarchive/papers/manifest.json` from the
      extraction pipeline)
