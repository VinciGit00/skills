---
name: training-loop-progress-logging
description: Add concise, informative runtime progress logging to machine-learning training and evaluation loops. Use whenever creating or modifying training code in Python scripts or notebooks, especially loops over epochs and batches, so users can see progress, current and running loss, validation results, and checkpoint improvements without excessive output.
---

# Training Loop Progress Logging

Add visible progress reporting whenever writing or editing model-training loops.

## Requirements

- Print a training-start summary with epoch count, batches per epoch, device, and useful configuration such as learning rate or accumulation steps.
- Print the epoch start.
- Report batch progress at a bounded interval, normally about five to ten times per epoch. Always include the final batch.
- Include the current loss and running mean loss in batch reports.
- Print the epoch's training and validation losses after evaluation.
- Clearly identify when validation improves and a new best state or checkpoint is selected.
- Print final test or evaluation results and the selected epoch when available.
- Use `flush=True` for long-running notebook loops so output appears promptly.

## Implementation pattern

Derive a safe interval from loader length:

```python
total_batches = len(train_loader)
log_every = max(1, total_batches // 5)

for batch_index, batch in enumerate(train_loader, start=1):
    # training step
    current_loss = loss.item()
    losses.append(current_loss)
    if batch_index % log_every == 0 or batch_index == total_batches:
        running_loss = sum(losses) / len(losses)
        print(
            f"  Batch {batch_index:>4}/{total_batches} | "
            f"loss: {current_loss:.4f} | running loss: {running_loss:.4f}",
            flush=True,
        )
```

Adapt labels to the codebase and preserve existing training semantics.

## Guardrails

- Do not print every batch unless the loader is very small or the user explicitly asks for it.
- Do not call `.item()` repeatedly for the same tensor; append once and reuse the Python value.
- Do not change gradients, optimizer cadence, mixed precision, accumulation, or evaluation behavior merely to add logging.
- Keep notebook messages short and easy to scan.
