Hi Christina,

I wanted to share my current thinking on how to approach fine-tuning MaxToki for human heart development, drawing on what we learned from the brain-aging fine-tune.

Key design decisions:

- Time axis: Developmental time in post-conception weeks (PCW), represented as a float.
- Time grouping: Rather than using (cell type × sex) as in the brain-aging run, I propose grouping by canonical cell type alone, mapping all dataset-specific sub-types to our approved lineage tree using the harmonization dictionary I shared earlier. This keeps the grouping consistent across datasets.
- Starting weights: The foundational 94M model, since we have no prior heart-specific weights.
- Dataset: ~493K cells across four datasets (CellxGene heart-dev subset, Tyser et al., Xu et al., Lázár et al.).

Train/val/test split:

Since we don't have matched donors across datasets, I propose splitting by developmental stage rather than by donor. Three options:

Option 1 (stage-based split — my preference):
- Val: PCW 10, 20, 30 — specific age points spread across the developmental window, covering cardiomyocyte maturation onset, mid-fetal, and late fetal stages.
- Test: PCW 7, 25, 33 — interleaved with val ages for broad temporal coverage; may be combined with val if hyperparameter fine-tuning is not required.
- Train: all remaining PCW.
- Cell lineage holdout: additionally hold out 2–3 complete cell lineages (depending on total lineage count) to test generalization across cell identity as well as developmental time.
- Caveat: specific age points may have uneven cell coverage across datasets; some points may need to be relaxed to a narrow window (e.g., ±1 PCW) to ensure sufficient cells.

Option 2 (whole-dataset training, held-out cells):
- Train on the full dataset regardless of stage, then hold out specific cells per developmental stage and cell type for evaluation.
- Pro: maximizes training data. Con: risk of the model seeing all stages during training, making generalization harder to assess cleanly.

What we are predicting:
- Timelapse (developmental time gap between two cells, in PCW)
- Cell state (gene expression trajectory)

I am leaning toward Option 1 because it gives us the cleanest biological interpretation of val and test performance. Happy to discuss any of these choices.

Best,
Enock
