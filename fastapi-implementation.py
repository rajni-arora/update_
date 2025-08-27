The function knowledge_recall is responsible for retrieving relevant knowledge snippets and examples given a user’s question.
It combines semantic search results (already computed and passed in) with TF-IDF keyword search, filters them, deduplicates them, and finally builds:
	1.	A knowledge representation string (kg_repr)
	2.	A dynamic examples string (dynamic_examples_repr)

These outputs are later injected into your query rewrite prompt.

⸻

🛠️ Inputs

knowledge_recall(qn, k1=3, threshold_k1=0.49, k2=4, docs_knowledge_meta=None, docs_knowledge_full=None, knowledge_base=None, dynamic_examples=None, knowledge=None)
	1.	qn → The user’s query (string).
	2.	k1 → Number of top results to keep from semantic search.
	3.	threshold_k1 → Confidence threshold for semantic search hits.
	4.	k2 → Number of top results to fetch in TF-IDF keyword search.
	5.	docs_knowledge_meta → Set of “meta” documents (usually titles).
	6.	docs_knowledge_full → Set of “full” documents (descriptions).
	7.	knowledge_base → A dictionary containing structured knowledge (e.g., {title: {description: ..., example: ...}}).
	8.	dynamic_examples → Dictionary mapping example IDs → actual example text.
	9.	knowledge → Semantic search results (list of dicts with page_content + metadata).

⸻

📤 Outputs

The function returns a tuple:
	1.	kg_repr → A single string that contains all relevant knowledge snippets (joined with newlines).
	2.	dynamic_examples_repr → A single string that contains all relevant dynamic few-shot examples (joined with newlines).

⸻

⚙️ Processing Steps
	1.	Semantic Search Recall
	•	Convert each semantic hit (knowledge) into a Document object.
	•	Add to a recall list (kg_recall).
	2.	TF-IDF Keyword Recall
	•	Run TF-IDF over docs_knowledge_meta (titles) and docs_knowledge_full (descriptions).
	•	Cross-check matches so only docs whose title appears in both meta and full results are kept.
	•	Add unique TF-IDF matches into kg_recall.
	3.	Deduplication
	•	Normalize text (remove whitespace) so duplicates aren’t added twice.
	4.	Reordering
	•	Reverse the final recall list (priority adjustment).
	5.	Build kg_repr
	•	Concatenate all recalled page_content separated by blank lines.
	6.	Select Examples
	•	For each recalled doc, check if its title exists in knowledge_base.
	•	If yes, get the linked example field, look up its text in dynamic_examples, and add it to a set (example_sel).
	•	Deduplicate via set and join them into a single string.
	7.	Return
	•	Return (kg_repr, dynamic_examples_repr).

⸻

✅ In short:
knowledge_recall = Semantic hits + TF-IDF hits → cleaned + deduped → stitched into one knowledge string + one example string.
