📌 Descriptive Prompt for Entity / Community Extraction

You are an advanced entity extraction engine.
You are given a document titled “Management Policy – AEMP 70 Enterprise Data Management Operating Policy.”

Your task is to carefully analyze this document and extract all unique entities, roles, policies, standards, organizational units, committees, frameworks, and definitions mentioned.

Use the Table of Contents as a guide to ensure complete coverage. Specifically, extract entities from the following sections:

⸻

1. Overview and Purpose
	•	Identify all broad organizational entities, communities, or groups (e.g., American Express Company, AXP, “the Company”).
	•	Identify policy references (e.g., AEMP70, AEMP79).
	•	Identify any concepts or principles (e.g., Data Risk Management, Enterprise Data Management Architecture, Risk-Based Layering of Data Requirements, Data Lifecycle, Data Governance).

⸻

2. Scope
	•	Extract entities related to formats of data, data states (in motion, at rest), and data activities (creation, processing, consumption, sharing).
	•	Extract all actors (colleagues, contractors, consultants, legal entities, business units).

⸻

3. Key Definitions
	•	Extract each defined term as a distinct entity.
Examples: Authoritative Data Source (ADS), Business Unit Data Office (BU DO), Critical Data Element (CDE), Data Governance, Data Incident, Data Lifecycle, Data Management, Data Risk, Data Risk Management, Data Risk Taxonomy, Data Supply Chain, End-User Developed Application (EUDA).
	•	Capture both the term and its abbreviation if given.

⸻

4. Roles & Responsibilities

Extract all roles, offices, committees, and communities listed in this section, including but not limited to:
	•	First Line Roles: Chief Data Officer (CDO), Enterprise Data Office (EDO), Business Unit Data Office (BU DO), Data Executive, Data Steward, Data Custodian, Process Owner, AXP Technology Chief Information Security Officer (CISO), Technology Risk and Information Security (TRIS).
	•	Second Line Roles: Enterprise Data Risk Management (EDRM), Global Records Management (GRM).
	•	Third Line Role: Internal Audit Group (IAG).
	•	Approval Entities / Signatories: Enterprise Risk Management Committee, Enterprise Data Committee, Policy Signatories.

⸻

5. Policy Requirements

Extract entities related to policy domains and frameworks, including:
	•	Data Risk Management requirements.
	•	Enterprise Data Management Architecture (and its subcomponents like Enterprise Data Domain Taxonomy, Master Data Management, Reference Data Management, Authoritative Data Source).
	•	Risk-Based Layering of Data Requirements and Controls (e.g., Data Control Inventory).
	•	End-to-End Data Lifecycle Management (e.g., Data Identification, Data Classification, Data Creation, Storage, Sharing, Archiving, Disposal).

⸻

6. Related Policies, Regulatory Guidelines, and Supporting Documents

Extract all policy references and supporting standards, such as:
	•	AEMP05, AEMP08, AEMP10, AEMP15, AEMP39, AEMP40, AEMP47, AEMP48, AEMP50, AEMP54, AEMP64, AEMP68, AEMP79, AEMP80, AEMP90.
	•	TECH02.01, TECH06.48.
	•	Internal Control Framework Policy, Enterprise Data Usage Standard, Enterprise Record Risk Management Standard, Enterprise Issue Management Policy, Risk and Control Self-Assessment Policy, TRIS Program.

⸻

📌 Extraction Guidelines
	•	Extract entities in exact wording as they appear in the document (no paraphrasing).
	•	Maintain entities as distinct (e.g., “Chief Data Officer (CDO)” and “Enterprise Data Office (EDO)” should not be merged).
	•	Capture both abbreviation and full form when provided.
	•	Consider roles, offices, committees, policies, standards, programs, definitions, frameworks, and processes all as entities.
	•	Output should be structured so that each entity is clearly identifiable and separable (e.g., one per line or one per JSON key).

⸻

👉 This prompt ensures you don’t miss any community/entity and lays the groundwork for later converting them into triplets for your knowledge graph.

Would you like me to now turn this into a JSON schema-based extraction prompt (so that the model outputs directly in JSON format for easier parsing in your Python pipeline)?