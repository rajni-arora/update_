1. Node Types (Entities)

1️⃣ Employee

Represents an employee.

Label: Employee

Properties
	•	employeeId
	•	firstName
	•	lastName
	•	workCountryCode
	•	workStateCode
    
    
example:
Employee {
  employeeId: "EMPNO7510976"
  firstName: "First10976"
  lastName: "Last10976"
  workCountryCode: "AR"
  workStateCode: null
}


2️⃣ TaxReturn

Represents a tax return project for an employee.

Label: TaxReturn

Properties
	•	projectType
	•	country
	•	year
	•	currentStatus
	•	daysAtStatus
	•	daysAtStatusTotal
	•	dataCollectionSent
	•	dataCollectionReceived
	•	informationCompletionDate
	•	daysToSendIndividual

Example

TaxReturn {
 projectType: "Tax Return"
 country: "United States"
 year: 2024
 currentStatus: "Pending Preparation"
 daysAtStatus: 509
}

3️⃣ Document

Represents required documentation.

Label: Document

Properties
	•	documentType
	•	missingInformationId
	•	neededFrom

Example
Document {
 documentType: "Engagement Letter"
 missingInformationId: "PETESTR10290422"
 neededFrom: "Individual"
}
4️⃣ Country (Optional but good for normalization)

Label: Country

Properties

countryCode
countryName


2. Relationship Types

Employee → TaxReturn

(:Employee)-[:FILES_TAX_RETURN]->(:TaxReturn)
Meaning: Employee files a tax return.

⸻

Employee → Document
(:Employee)-[:MISSING_DOCUMENT]->(:Document)

Meaning: Employee still needs to provide a document.

⸻

TaxReturn → Document
(:TaxReturn)-[:REQUIRES_DOCUMENT]->(:Document)

Meaning: Tax return requires that document.

Employee → Country
(:Employee)-[:WORKS_IN]->(:Country)


3. Graph Triples (Example)

From your Excel rows.

Example 1

Employee: 100560556

(Employee:100560556)
    └── FILES_TAX_RETURN
           └── (TaxReturn:2024_US)

(Employee:100560556)
    └── MISSING_DOCUMENT
           └── (Document:PETESTR10290422)
        
        
Triples:

(100560556) --FILES_TAX_RETURN--> (TaxReturn_2024_US)

(100560556) --MISSING_DOCUMENT--> (PETESTR10290422)

(PETESTR10290422) --DOCUMENT_TYPE--> (EngagementLetter)


4. Neptune Compatible Format

CSV Loader Structure (Recommended)

Amazon Neptune bulk loader uses nodes.csv and edges.csv

Nodes CSV

~id,~label,employeeId,firstName,lastName,workCountryCode,workStateCode,projectType,country,year,currentStatus,documentType,missingInformationId
emp_100560556,Employee,100560556,,,,,,,,
tax_100560556_2024,TaxReturn,,,,,Tax Return,United States,2024,Pending Preparation,,
doc_PETESTR10290422,Document,,,,,,,,,Engagement Letter,PETESTR10290422

Edges CSV
~id,~from,~to,~label
edge1,emp_100560556,tax_100560556_2024,FILES_TAX_RETURN
edge2,emp_100560556,doc_PETESTR10290422,MISSING_DOCUMENT
edge3,tax_100560556_2024,doc_PETESTR10290422,REQUIRES_DOCUMENT

Gremlin Example (Neptune)
g.addV('Employee').
property('employeeId','100560556').
property('firstName','First10976')

g.addV('TaxReturn').
property('year',2024).
property('country','United States').
property('status','Pending Preparation')

g.addE('FILES_TAX_RETURN').
from(g.V().has('employeeId','100560556')).
to(g.V().has('year',2024))


5. Data Cleaning Suggestions

Your Excel shows several normalization problems.

1️⃣ Duplicate Employees

Employee appears as:

100560556
EMPNO7510976

Use one canonical ID.

Recommended:

employeeId = EMPNO7510976

2️⃣ Country duplication

You have:

United States
US
AR
AU

Normalize using:

countryCode
countryName

Example
US → United States
AU → Australia
AR → Argentina



Document duplication

Document type repeats:

Engagement Letter

Better:
DocumentType node

(:Document)-[:OF_TYPE]->(:DocumentType)


Status normalization

CurrentStatus values like:
Pending Preparation

Better create:
(:TaxReturn)-[:HAS_STATUS]->(:Status)

Optimized Graph Structure (Best for Neptune)

Employee
   │
   ├── FILES_TAX_RETURN
   │          │
   │          ├── HAS_STATUS
   │          │
   │          └── REQUIRES_DOCUMENT
   │
   ├── MISSING_DOCUMENT
   │
   └── WORKS_IN
              │
              Country
