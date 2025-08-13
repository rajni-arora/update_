rewritten_query + original_question + schema + config thresholds
        │
        ▼
few_shot.get_few_shot()
        │
        ├── Retrieve similar past questions from Datastax (vector DB)
        ├── Extract & format them into few_shot_examples
        ├── Build global_mapping from synonyms in retrieved examples
        └── Determine very_similar_example by top match score
        │
        ▼
(few_shot_examples, global_mapping, very_similar_example)