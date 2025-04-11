Key Deliverables:
	1.	API Development (FastAPI):
	•	A new API endpoint was created using FastAPI to process data files from S3 and return processed output.
	•	The API is built to be scalable, lightweight, and easily extendable for future requirements.
	2.	Deployment to Dihydra:
	•	The service was packaged and deployed to the Dihydra platform.
	•	Deployment scripts were modified to support the new service structure.
	•	Environment variables and necessary configurations were added to ensure a seamless deployment.
	3.	S3 Integration:
	•	The service fetches input files directly from an S3 bucket.
	•	After processing, the output is written back to a designated output path on S3.
	•	This enables a smooth, cloud-native, and serverless workflow.
	4.	Metadata Enhancement:
	•	The service originally handled 6 metadata fields.
	•	We enhanced this by adding 2 additional metadata fields, bringing the total to 8, improving the depth and traceability of the output data.
	5.	Repository Update:
	•	The project has been pushed from a personal repository to the main MXLumos GitHub repository for official use and team collaboration.
