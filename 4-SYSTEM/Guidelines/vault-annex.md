# Vault Annex — Introduction to the Middle Way conventions

The methodology guidelines (`0-VAULT-Structure.md`, `../../1-SOURCES/About Sources.md`, `../../2-RAILS/About Rails.md`, `../../3-TRANSFORMATIONS/About Transformations.md`) are **text-agnostic** — they apply to any Railroads vault built on any classical text. This annex records the conventions that are specific to *this* vault: **Introduction to the Middle Way** (དབུ་མ་ལ་འཇུག་པ).

When the Guidelines and this annex disagree on a vault-specific detail, this annex wins — **for the points it actually states**. Everything it does not state follows the defaults unchanged.

This file may be renamed for its text (`<text-slug>-annex.md`) as long as `README.md` and `4-SYSTEM/CLAUDE.md` link to it.

---

## 1. The text

This vault serves **Introduction to the Middle Way** (*དབུ་མ་ལ་འཇུག་པ*), a Tibetan-language Madhyamaka treatise whose own colophon (`^a-1`) names its author as སློབ་དཔོན་ཟླ་བ་གྲགས་པ, studied through four Tibetan commentaries.

Source-text files in `1-SOURCES/Text/` correspond to the following books / volumes:

| Order | Book / Volume | Filename |
| ----- | ------------- | -------- |
| 1 | དབུ་མ་ལ་འཇུག་པ། (11 chapters, plus an intro and a back-matter zone) | `དབུ་མ་འཇུག་པ།.md` |

Source filenames are kept in Tibetan script, exactly as ingested. This departs from the lowercase-hyphenated naming rule in `4-SYSTEM/CLAUDE.md` §4; the `registered_id` (§3) is the ASCII handle used everywhere in `2-RAILS/`.

Only books that have been ingested are present in the folder. The primary text currently being railed out is **the whole of དབུ་མ་ལ་འཇུག་པ, chapters 1–11** — at present the TOC trees of the four commentaries (`2-RAILS/Sections/Raw/toc-tree/`).

---

## 2. Addressing scheme

The root text is addressed by chapter and verse: `^chapter-verse`, with chapter numbers 1–11 and verse numbers counted from 1 inside each chapter. Two extra zones sit outside the chapters (see the registered deviation below).

**`verse_id_format`:** `chapter-verse`

**Format example:** `^6-33` (chapter 6, block 33)

### Heading hierarchy

Root text (`1-SOURCES/Text/དབུ་མ་འཇུག་པ།.md`):

| Markdown | Role | Anchor |
| -------- | ---- | ------ |
| `##` | Title (`^0`), intro zone (`^I-0`), chapter (`^N-0`), back-matter zone (`^a-0`) | `^0`, `^I-0`, `^1-0` … `^11-0`, `^a-0` |
| `###` | Sub-heading inside a zone (`^I-1-0`, `^I-2-0`, `^a-2-0`) | `^[zone]-[n]-0` |

Commentaries follow the default convention in `annotation-conventions.md` §2: each `##` section carries a hand-assigned label (`^1-0`, `^I-0`, `^a-0`, …); every deeper heading takes the **full decimal path of the commentary's own TOC tree** plus the `-0` slot (for example `^3-2-1-3-2-2-3-5-0`), with no segment cap; body blocks are `^label-n`, counted from 1 inside the `##` section. A commentary's own `verse_id_format` is therefore `section-paragraph`.

### Verse numbering rule

Verse numbers restart at 1 in every chapter of the root text. Transclusion lines never take an ID and never advance a counter. Commentary body IDs restart at 1 in every `##` section.

### ⚑ Registered deviations — overrides of the default conventions

### ⚑ Intro / back-matter zones — overrides `annotation-conventions.md` §7 (registered 2026-10-13)

The default has chapters only. This vault keeps front matter and back matter addressable apart from the chapters:

- **Root text:** `^0` (title), `^I-1`–`^I-3` (Indian-language title, Tibetan title, homage to Mañjuśrī-kumārabhūta), `^a-1`–`^a-3` (author colophon, translation colophon, editorial note on the colophons). Headings `^I-0`, `^I-1-0`, `^I-2-0`, `^a-0`, `^a-2-0`.
- **Commentaries:** `^I-*` for the opening homage and pledge to compose; `^a-*` for the closing dedication and colophon. `shel-phreng` also has `^b-*` (an appendix on difficult points) and `^c-*` (the closing statement of the commentary) because its own structure has those sections.

Why: the colophons carry author, translator and edition information that metadata and rails must cite apart from any chapter.

### ⚑ `zab-rgyas` opens without a title or `##` heading — overrides `annotation-conventions.md` §1b/§2 (registered 2026-10-13)

The file has no `#` title line and no `##` heading before its first section. Its twelve opening blocks (title line, homage, praise verses, statement of purpose) carry IDs `^0-1`–`^0-12` directly, ahead of the first `##` section `^1-0`. This is how the file was ingested; no heading was invented for it. A human contributor may decide to add a `##` heading with the label `0` later; doing so does not change any of those IDs.

### Re-segmentation and ID-migration log

No rail in `2-RAILS/` cites any block ID of these files yet, so none of the changes below invalidate a citation.

**2026-10-06 to 2026-10-13 — commentaries re-segmented and re-stamped (git history).** The four commentaries were re-segmented, given TOC headings and stamped with block IDs over this period; the intermediate versions I checked had no block IDs. The coworker's original imports (mostly line-per-clause) remain in git history from `8d78ebc` (2026-09-28).

**2026-10-13 — `shel-phreng` heading IDs re-nested.** The sections "གཙོ་བོར་འདོད་པ་འཐད་པའི་ཚུལ" and its two children were mis-nested in the TOC tree. The two child headings changed from `^3-2-1-1-2-2-2-3-1-1-1-1-2-2-2-2-2-1-2-2-2-1-1-0` and `…-1-2-0` to `…-2-1-0` and `…-2-2-0`. Backup: `0-INBOX/temp/fix-backups-2026-10-13/shel-phreng.source.before.md`.

**2026-10-13 — empty headings inserted.** `zab-rgyas` `^3-2-1-1-2-3-5-2-2-2-2-1-4-0` and `shel-phreng` `^3-2-1-1-2-2-2-3-1-2-2-2-1-2-1-2-0`: both nodes are announced in the text but have no passage of their own, so they are empty sections. No existing ID changed. Backups: `0-INBOX/temp/fix-backups-2026-10-13/*.before-empty-headings.md`.

**2026-10-13 — `dbu-ma-la-hjug-pa-bshad-pa` body IDs renumbered.** 13 blocks had no ID; they were stamped and the body IDs in chapters 1, 3 and 6 were renumbered so each `##` section runs 1…N with no gaps (13 added, 517 changed; headings and text unchanged). Backup: `0-INBOX/temp/fix-backups-2026-10-13/bshad-pa.source.before.md`. Any note taken before this date that cites a body ID in chapter 1 (after `^1-26`), chapter 3 (after `^3-14`) or chapter 6 (after `^6-313`) of this file must be re-checked.

**2026-10-13 — frontmatter added** to the root text and the four commentaries. Total line numbers shift by 13–17 lines; block IDs are unaffected.

---

## 3. Registered commentary IDs

Every commentary file in `1-SOURCES/Commentaries/` declares a `registered_id` in its frontmatter. That short ID is the only string used to attribute claims to the commentary throughout `2-RAILS/`.

Once assigned, a `registered_id` never changes. New commentaries must be added to the roster below before their `registered_id` is used in any rail.

| `registered_id` | Author / Title | Tier | School or tradition | `book_id` | Language | File |
| --------------- | -------------- | ---- | ------------------- | --------- | -------- | ---- |
| `zab-rgyas` | ཐུབ་བསྟན་དགེ་ལེགས་རྒྱ་མཚོ — དབུ་མ་ལ་འཇུག་པའི་ཊཱི་ཀ་ཟབ་རྒྱས་ལམ་མཆོག་རབ་གསལ་སྣང་བའི་རྒྱན། | commentary (its colophon, `^4-21`, says it expands the wording of དགོངས་པ་རབ་གསལ and another work) | to be supplied | to be supplied | Tibetan | `1-SOURCES/Commentaries/དབུ་མ་ལ་འཇུག་པའི་ཊཱི་ཀ་ཟབ་རྒྱས་ལམ་མཆོག་རབ་གསལ་སྣང་བའི་རྒྱན།.md` |
| `shel-phreng` | སི་ཏུ་པ་ཆོས་ཀྱི་རྒྱ་མཚོ (compiler, from the notes of མི་ཕམ་འཇམ་དབྱངས་རྣམ་པར་རྒྱལ་བ) — དབུ་མ་ལ་འཇུག་པའི་འགྲེལ་བ་ཟླ་བའི་ཞལ་ལུང་དྲི་མེད་ཤེལ་ཕྲེང་། | commentary | to be supplied | to be supplied | Tibetan | `1-SOURCES/Commentaries/དབུ་མ་ལ་འཇུག་པའི་འགྲེལ་བ་ཟླ་བའི་ཞལ་ལུང་དྲི་མེད་ཤེལ་ཕྲེང་།.md` |
| `dgongs-pa-rab-gsal` | ཤར་ཙོང་ཁ་པ་བློ་བཟང་གྲགས་པའི་དཔལ — དབུ་མ་ལ་འཇུག་པའི་རྒྱ་ཆེར་བཤད་པ་དགོངས་པ་རབ་གསལ། | commentary | to be supplied | to be supplied | Tibetan | `1-SOURCES/Commentaries/དབུ་མ་ལ་འཇུག་པའི་རྒྱ་ཆེར་བཤད་པ་དགོངས་པ་རབ་གསལ།.md` |
| `dbu-ma-la-hjug-pa-bshad-pa` | author not named in the file — དབུ་མ་ལ་འཇུག་པའི་བཤད་པ། | commentary (the colophon, `^a-2`, records its translators) | to be supplied | to be supplied | Tibetan | `1-SOURCES/Commentaries/དབུ་མ་ལ་འཇུག་པའི་བཤད་པ།.md` |

"To be supplied" means the file does not state it; a human contributor fills these in. Authors above are taken from each file's own colophon, not from outside knowledge.

**Tier ordering** within a verse package's Traditional Interpretation section: not yet decided — to be set by a human contributor before the verse packages are built.

**ID migrations.** None.

---

## 4. Language tracks

| Tag | Language | Translation track | Plan stream |
| --- | -------- | ----------------- | ----------- |
| `bo` | Tibetan | — (source) | — |

No translation tracks exist yet.

### Analysis language per rail section

Not yet decided; the defaults in `4-SYSTEM/CLAUDE.md` §10 apply (English for the per-commentary paraphrases and translation notes, original language everywhere else).

---

## 5. Bilingual glossary pairs

None yet.

---

## 6. Active transformation tracks

None yet.

---

## 7. Source-language tags used in this vault

| Tag | Script / System | Use in this vault |
| --- | --------------- | ----------------- |
| `-bo` | Unicode Tibetan | The root text and all four commentaries |

The default for every Tibetan source is `-bo`.

---

## 8. Where to look next

- [`0-VAULT-Structure.md`](0-VAULT-Structure.md) — the architecture in full.
- [`../../1-SOURCES/About Sources.md`](../../1-SOURCES/About%20Sources.md) — source-file rules.
- [`../../2-RAILS/About Rails.md`](../../2-RAILS/About%20Rails.md) — rails schema.
- [`../../3-TRANSFORMATIONS/About Transformations.md`](../../3-TRANSFORMATIONS/About%20Transformations.md) — track and output rules.
- [`annotation-conventions.md`](annotation-conventions.md) — the default block-ID conventions this annex may register deviations from.
- [`vault-variants.md`](vault-variants.md) — the three documented vault shapes, if this vault is not the common case.
- [`../CLAUDE.md`](../CLAUDE.md) — the operational quick-reference. *This annex overrides it on the points recorded above.*
- [Top-level `README.md`](../../README.md) — pipeline overview and reading paths.
