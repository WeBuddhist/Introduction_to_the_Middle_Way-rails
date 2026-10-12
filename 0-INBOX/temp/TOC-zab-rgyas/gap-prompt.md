# Gap-fill placement task — locate specific ས་བཅད tree nodes in a narrow line range (ISOLATED)

Your ONLY task. A previous pass placed most nodes of the sa bcad tree in the commentary
but left a few unplaced (or mis-placed). Locate exactly the nodes you are given.

## Inputs (read by path)
- Tree (read IN FULL): `0-INBOX/TOCs/toc-tree-zab-rgyas.md` — one node per line,
  `* <decimal id> <label>`, nodes in DOCUMENT ORDER; labels are paraphrases, not quotes.
- Guide: `4-SYSTEM/Skills/toc-generate/references/sachad-recognition.md`.
- Source snapshot (1-based line numbers; one paragraph per line):
  `0-INBOX/temp/TOC-zab-rgyas/snapshot.md`. Use Read with offset/limit.
- The task message gives: the node IDs to locate, and a line range LO–HI. The nodes'
  announcements lie between those lines (bounded by already-placed neighbours: the node
  just before the first target is announced at/after LO, the node just after the last
  target at/before HI). Read LO-3 … HI+3. Read the tree lines around the targets too —
  parents/siblings/children tell you which passage announces which node.

## Rules
1. Place each target heading directly before the clause that announces it.
   - Announcement starts the paragraph line → anchor `-`.
   - Mid-paragraph → `anchor` = verbatim substring copied from that line (10–40 chars)
     beginning exactly at the announcing clause's start (after a `།`, or after `དང་།`),
     unique within the line. Never start inside an unbroken clause.
2. Node IDs MUST be copied character-for-character from the tree file. Rows with an ID
   that is not in the tree are machine-discarded. Do not abbreviate or renumber.
3. Document order must hold: each node's position is ≥ the previous node's. A parent is
   announced at or before its first child (same position allowed — stacked headings).
4. Never guess. If you cannot find a node's announcement, omit it and add a `#!` comment
   with the node ID and why.
5. `anchor`/`evidence` are machine-verified as substrings of the stated line.

## Output
Write to the path in the task message. First line `# gap NN | lines LO-HI | rows N`, then
one TAB-separated row per node:
`<decimal id>	<line>	<anchor or ->	<conf high|med|low>	<evidence 10-40 chars verbatim from that line>`
Reply with only the path and row count.
