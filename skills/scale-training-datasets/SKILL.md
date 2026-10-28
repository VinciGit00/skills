---
name: scale-training-datasets
description: Safely enlarge or reduce machine-learning datasets and data-window counts while preserving split isolation and reproducibility. Use when modifying dataset size, sample limits, sliding-window stride, train/validation/test proportions, DataLoaders, or CPU/GPU training profiles in Python scripts and notebooks.
---

# Scale Training Datasets

Scale the number of useful training examples deliberately and verify the effective result rather than changing only a nominal limit.

## Inspect the data pipeline

1. Identify the raw corpus or records, split boundaries, dataset class, sample limits, window length, stride, and DataLoaders.
2. Distinguish raw-data size from generated-example count. Increasing `max_windows` cannot help when the corpus and stride produce fewer windows.
3. Preserve train, validation, and test isolation. Never create windows across split boundaries.

## Choose the scaling method

- Increase sample caps when enough unused examples already exist.
- Reduce sliding-window stride when more overlapping windows are needed from a fixed sequential corpus.
- Add genuinely new source data when greater diversity is required; duplicated or heavily overlapping samples increase count but not information proportionally.
- Scale CPU and GPU profiles separately when the notebook provides both.
- Keep validation and test sets large enough for stable metrics, but do not train on them.

For a sequence of length `N`, window length `L`, and stride `S`, estimate the available windows with:

```python
available_windows = len(range(0, N - L, S))
effective_windows = min(available_windows, configured_limit)
```

To approximately double sliding windows, halve the stride and double the limits, then compute actual counts. Boundary effects may prevent an exact multiple.

## Apply the change

1. Update configuration defaults and any reduced local or CPU profile consistently.
2. Update stride or source data only when limits alone cannot reach the target.
3. Add a short code comment when overlap changes because correlated windows affect how the larger dataset should be interpreted.
4. Preserve deterministic seeds, split boundaries, shuffling behavior, and tensor types.
5. Clear stale notebook output for changed cells or regenerate the notebook when practical.

## Verify

- Print or assert the effective sample count for every split.
- Confirm the requested multiplier using actual dataset lengths, not configuration values alone.
- Check that no split is empty and no sample crosses a split boundary.
- Validate notebook JSON and code-cell syntax after edits.
- State the expected change in batches per epoch, runtime, and storage or memory use.

## Guardrails

- Do not describe duplicated or overlapping windows as equivalent to new independent data.
- Do not silently alter validation or test data to improve reported metrics.
- Do not assume doubling examples exactly doubles runtime; batch size, I/O, caching, and hardware also matter.
- Do not download a new external dataset unless the user authorized it or the existing workflow already does so.
