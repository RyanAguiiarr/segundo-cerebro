---
name: skill-moc-update
trigger: "update mocs" / after any batch of new permanent notes
description: "Updates MOC files to reflect new permanent notes added to each cluster."
---

# Skill: Update MOCs

## Steps
1. Read all files in `negocio/permanent/` (all subfolders)
2. Group by domain tag (medico, decisoes, produto)
3. For each MOC in `negocio/mocs/`:
   - Add any new permanent note that belongs to this cluster
   - Remove any link to a note that was deleted
   - Keep entries sorted by relevance, not alphabetically
4. Update `index.md` to reflect new permanent notes
5. Append to `log.md`
