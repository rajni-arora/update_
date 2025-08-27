🔎 Why knowledge_recall is needed

When you rewrite a user’s query (with LLM), you don’t want the model to work blindly.
You want it to see relevant knowledge and examples from your system so that the rewrite is:
	•	Accurate (uses the right domain/business context)
	•	Grounded (not hallucinated)
	•	Consistent (uses the same examples/terminology as the KB)

That’s exactly what knowledge_recall is doing: it prepares the evidence/context for the LLM before you inject it into the prompt.

⸻

🎯 Goals of knowledge_recall
	1.	Bring in relevant knowledge
	•	From semantic search (captures meaning similarity)
	•	From TF-IDF keyword search (captures exact keyword matches)
	•	This hybrid recall improves recall (coverage) and precision (relevance).
	2.	Deduplicate & Clean
	•	Avoid redundant knowledge snippets.
	•	Normalize whitespace and text so comparison is consistent.
	3.	Prepare Few-Shot Examples
	•	Dynamically fetch examples tied to the recalled knowledge.
	•	These are injected as few-shot prompts, helping the LLM learn how to rewrite queries correctly.
	4.	Output in Model-Readable Format
	•	Stitch the results into two neat strings:
	•	kg_repr: the recalled domain knowledge.
	•	dynamic_examples_repr: related examples.

These strings then slot directly into the prompt template in get_qr_prompt.

⸻

🔗 Where it fits

👉 User query → knowledge_recall → get_qr_prompt → invoke_query_llm → rewritten query

So without knowledge_recall, your LLM would only see the raw query, without context or examples.
That would lead to weak, less accurate, and less controlled rewrites.
