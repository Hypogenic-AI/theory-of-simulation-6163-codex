# Downloaded Datasets

This directory contains datasets for the research project. Data files are not committed to git due to size; the datasets are downloaded locally in this workspace and excluded via `datasets/.gitignore`.

## Dataset 1: OpinionQA

### Overview
- Source: Hugging Face `timchen0618/OpinionQA`
- Size: validation 294, test 882
- Format: Hugging Face Dataset saved with `save_to_disk`
- Task: demographic opinion alignment and population-level simulation
- Splits: validation, test
- License: see dataset card / upstream repo

### Download Instructions

Using Hugging Face:

```python
from datasets import load_dataset
dataset = load_dataset("timchen0618/OpinionQA")
dataset.save_to_disk("datasets/opinionqa")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/opinionqa")
```

### Sample Data

Saved at `datasets/opinionqa/samples/samples.json`.

### Notes
- Columns: `question`, `perspectives`, `id`
- Useful for testing whether simulated responses match group-level distributions.
- Pairs well with the `opinions_qa` repository for representativeness metrics.

## Dataset 2: Synthetic-Persona-Chat

### Overview
- Source: Hugging Face `google/Synthetic-Persona-Chat`
- Size: train 8938, validation 1000, test 968
- Format: Hugging Face Dataset saved with `save_to_disk`
- Task: persona grounding and conditional response generation
- Splits: train, validation, test
- License: see dataset card

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("google/Synthetic-Persona-Chat")
dataset.save_to_disk("datasets/synthetic_persona_chat")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/synthetic_persona_chat")
```

### Sample Data

Saved at `datasets/synthetic_persona_chat/samples/samples.json`.

### Notes
- Columns: `user 1 personas`, `user 2 personas`, `Best Generated Conversation`
- Best used as auxiliary conditioning data rather than a direct realism benchmark.
- Helpful for experiments on latent-factor capture from compact persona descriptions.

## Dataset 3: Social IQa

### Overview
- Source: Hugging Face `jet-ai/social_i_qa`
- Size: train 33410, validation 1954
- Format: Hugging Face Dataset saved with `save_to_disk`
- Task: social commonsense action and intent prediction
- Splits: train, validation
- License: see dataset card / original Social IQa release

### Download Instructions

```python
from datasets import load_dataset
dataset = load_dataset("jet-ai/social_i_qa")
dataset.save_to_disk("datasets/social_i_qa")
```

### Loading the Dataset

```python
from datasets import load_from_disk
dataset = load_from_disk("datasets/social_i_qa")
```

### Sample Data

Saved at `datasets/social_i_qa/samples/samples.json`.

### Notes
- Columns: `context`, `question`, `answerA`, `answerB`, `answerC`, `label`
- The original `allenai/social_i_qa` Hub entry relies on an old dataset script; the `jet-ai` mirror downloaded cleanly.
- Useful for scenario-level behavioral choice prediction, but weaker on long-horizon simulation.
