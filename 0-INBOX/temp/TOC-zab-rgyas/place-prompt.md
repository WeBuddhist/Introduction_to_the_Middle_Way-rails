# Placement task — find where each ས་བཅད tree node is announced (ISOLATED)

This is your ONLY task. You are given one window of a Tibetan commentary and the
finished sa bcad (ས་བཅད) tree of that commentary. For every tree node whose announcement
begins inside your window, report exactly where. You do not edit any file but your own
output file.

## Inputs (read by path)

- Tree (read it IN FULL first): `0-INBOX/TOCs/toc-tree-zab-rgyas.md` — nested list, one
  node per line, `* <decimal id> <label>`. Nodes are in DOCUMENT ORDER. Labels are
  *paraphrased/abbreviated* titles, NOT verbatim quotes — expect the text to word the
  same division differently (e.g. label `དང་པོ་དགག་པ་` ↔ text `དང་པོ་དགག་པ་ནི།` or `དང་པོ་ལ། ... བཀག་པ་ནི།`).
- Recognition guide: `4-SYSTEM/Skills/toc-generate/references/sachad-recognition.md`.
- Source (snapshot, 1-based line numbers; one paragraph per line, blank lines between):
  `0-INBOX/temp/TOC-zab-rgyas/snapshot.md`. Use the Read tool with `offset`/`limit`.
  Your CORE range is given in the task message. Also read ~12 lines before and after it
  for context, but report only announcements that BEGIN inside the core range.

## What to do

1. Read the tree. Read the core range (+context).
2. Walk the core in order. Wherever the author announces a division, labels a part
   ("as for the second, X …"), or opens a sub-part that corresponds to a tree node,
   decide WHICH node it is. Use content words, the ordinal, and the parent chain —
   labels repeat often (`དང་པོ་དགག་པ་` appears many times), so identify the node by its
   position in the nesting (parent topic must be the one currently being discussed).
   A hint only: nodes run in document order, and a window at X% of the file usually
   (not always) lies near X% of the tree — locate by content, not by percentage.
3. For each matched node output one row (format below). One passage may announce a
   whole chain of nested nodes at once (e.g. 3, 3.1, 3.1.1 …): output a row for EACH node,
   all with the same position.
4. Place the heading **directly before the sentence/clause that announces that section.**
   - Announcement starts at the beginning of the paragraph line → anchor `-`.
   - Announcement starts MID-paragraph (the paragraph first finishes the previous
     section's content, then opens the next one) → give `anchor`: a verbatim substring
     copied from that line, starting exactly at the beginning of the announcing clause
     (a clause boundary: right after a `།`/`་།`, or after a `དང་།` connector), 10–40
     characters, and unique within that line. Never start inside an unbroken clause.
5. NEVER guess. If a node's announcement is not in your core, do not output it. If you
   see an announcement but cannot tell which node it is, output it as a `#?` comment
   line with line number and the quoted clause. If the text clearly states a division
   whose node you cannot find in the tree, output `#!` with the line and quote.
6. Copy `anchor` and `evidence` VERBATIM from the source — they are machine-verified
   as substrings of the stated line; a non-matching row is discarded.

## Output

Write to the path given in the task message. First line:
`# window NNN | core A-B | rows N`
then one tab-separated row per node, sorted by line number then decimal id depth:

```
<decimal id>	<line>	<anchor or ->	<conf: high|med|low>	<evidence: verbatim announcing words, 10-40 chars from that line>
```

Optional `#?` / `#!` comment lines after the rows. If the core has no announcements, the
file is just the header line with `rows 0`. Tibetan text only in `anchor`/`evidence`.
Reply with the output path and the row count — nothing else.
