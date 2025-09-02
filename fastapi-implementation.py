
Got it ✅ Thanks for sharing the document screenshots.
Since you want to build a descriptive prompt that extracts communities/entities from this policy document (which you’ll later use for building triplets in a knowledge graph), I’ll create a rich, detailed prompt that guides the model to capture all possible relevant entities from the document.

Here’s a draft prompt you can use:

⸻

📌 Descriptive Prompt for Entity Extraction

You are an advanced information extraction system. You are given a policy document from mgmt Policy (AEMP 70 – Enterprise Data Management Operating Policy). Your task is to carefully read the document and extract all unique entities or communities mentioned.

Entities can belong to (but are not limited to) the following categories:
	1.	Roles / Offices / Committees / Units
	•	Examples: Chief Data Officer (CDO), Enterprise Data Office (EDO), Business Unit Data Office (BU DO), Process Owner, Enterprise Data Risk Management (EDRM), Global Records Management (GRM), Internal Audit Group (IAG), Enterprise Risk Management Committee, Enterprise Data Committee, Policy Signatories, Data Executive, Data Steward, Data Custodian, AXP Technology Chief Information Security Officer (CISO), Technology Risk and Information Security (TRIS).
	2.	Policies / Policy References
	•	Examples: AEMP70 Enterprise Data Management Operating Policy, AEMP79 Enterprise Data Risk Management Policy, AEMP05 Business Continuity Management Policy, AEMP08 Record Risk Management Policy, AEMP10 Third-Party Management Policy, AEMP15 Enterprise Policy and Committee Governance Framework Policy, AEMP39 Global Compliance Risk Management, AEMP40 Merger & Acquisition Deal Approval Policy, AEMP47 Operational Risk Management Policy, AEMP48 Privacy Risk Management Policy, AEMP50 Enterprise Risk Appetite Policy, AEMP54 New or Modified Product Governance Policy, AEMP64 Information Security Management Policy, AEMP68 Internal Audit Policy, AEMP80 AI Risk Management Policy, AEMP90 Risk Governance Framework Policy.
	3.	Standards / Programs
	•	Examples: TECH02.01 Information Ownership and Classification Standard, TECH06.48 Global Automated Balancing Controls Standard, Enterprise Technology Risk & Information Security (TRIS) Program, Enterprise Data Usage Standard, Enterprise Record Risk Management Standard, Internal Control Framework Policy, Risk and Control Self-Assessment Policy, Enterprise Issue Management Policy.
	4.	Concepts / Definitions (Data-related)
	•	Examples: Authoritative Data Source (ADS), Critical Data Element (CDE), Data Governance, Data Incident, Data Lifecycle, Data Management, Data Risk, Data Risk Management, Data Risk Taxonomy, Data Supply Chain, End-User Developed Application (EUDA).
	5.	Processes / Frameworks
	•	Examples: Data Risk Management requirements, Enterprise Data Management Architecture, Enterprise Data Domain Taxonomy, Master Data Management, Reference Data Management, Data Control Inventory, End-to-End Data Lifecycle Management, Data Identification and Classification, Data Creation/Collection, Risk-Based Layering of Data Requirements and Controls.

⸻

🎯 Extraction Goal
	•	Identify and list all entities/communities explicitly or implicitly mentioned in the document.
	•	Ensure coverage across roles, policies, standards, committees, offices, risk management frameworks, data governance terms, and definitions.
	•	Do not paraphrase—extract terms in the exact wording used in the document.
	•	Keep entities distinct (no merging or grouping unless explicitly defined as such in the policy).

⸻

Would you like me to also convert this into a ready-to-use structured prompt (for example: "Extract all entities from the document and classify them into Roles, Policies, Standards, Concepts, Frameworks") that you can directly paste into an LLM for extraction?