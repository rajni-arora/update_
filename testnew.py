import pandas as pd

# =========================
# 1. Load CSV Files
# =========================

tax_df = pd.read_csv("tax_return.csv")
missing_df = pd.read_csv("missing_info.csv")
emp_df = pd.read_csv("employee.csv")

# =========================
# 2. Clean Column Names
# =========================

tax_df.columns = tax_df.columns.str.strip()
missing_df.columns = missing_df.columns.str.strip()
emp_df.columns = emp_df.columns.str.strip()

# =========================
# 3. Create Nodes
# =========================

nodes = []

# ---- Employee Nodes ----
for _, row in emp_df.iterrows():
    node = {
        "~id": f"emp_{row['EmployeeNumber']}",
        "~label": "Employee",
        "employeeId": row['EmployeeNumber'],
        "firstName": row.get("FirstName", ""),
        "lastName": row.get("LastName", ""),
        "workCountryCode": row.get("WorkCountryCode", ""),
        "workStateCode": row.get("WorkStateCode", "")
    }
    nodes.append(node)

# ---- TaxReturn Nodes ----
for _, row in tax_df.iterrows():
    emp_id = row["Globalemployeeid"]

    node = {
        "~id": f"tax_{emp_id}_{row['Year']}",
        "~label": "TaxReturn",
        "employeeId": emp_id,
        "projectType": row.get("ProjectType", ""),
        "country": row.get("Country", ""),
        "year": row.get("Year", ""),
        "currentStatus": row.get("CurrentStatus", ""),
        "daysAtStatus": row.get("DaysAtStatus", ""),
        "daysAtStatusTotal": row.get("DaysAtStatus.1", "")
    }
    nodes.append(node)

# ---- Document Nodes ----
for _, row in missing_df.iterrows():
    node = {
        "~id": f"doc_{row['MissingInformationId']}",
        "~label": "Document",
        "documentType": row.get("DocumentType", ""),
        "missingInformationId": row.get("MissingInformationId", ""),
        "neededFrom": row.get("NeededFrom", "")
    }
    nodes.append(node)

# Convert to DataFrame
nodes_df = pd.DataFrame(nodes)

# Remove duplicates
nodes_df = nodes_df.drop_duplicates(subset=["~id"])

# =========================
# 4. Create Edges
# =========================

edges = []
edge_id = 1

# ---- Employee -> TaxReturn ----
for _, row in tax_df.iterrows():
    emp_id = row["Globalemployeeid"]
    tax_id = f"tax_{emp_id}_{row['Year']}"

    edges.append({
        "~id": f"e{edge_id}",
        "~from": f"emp_{emp_id}",
        "~to": tax_id,
        "~label": "FILES_TAX_RETURN"
    })
    edge_id += 1

# ---- Employee -> Document ----
for _, row in missing_df.iterrows():
    emp_id = row["Globalemployeeid"]
    doc_id = f"doc_{row['MissingInformationId']}"

    edges.append({
        "~id": f"e{edge_id}",
        "~from": f"emp_{emp_id}",
        "~to": doc_id,
        "~label": "MISSING_DOCUMENT"
    })
    edge_id += 1

# ---- TaxReturn -> Document ----
# (link based on employee + year assumption)
for _, row in missing_df.iterrows():
    emp_id = row["Globalemployeeid"]
    doc_id = f"doc_{row['MissingInformationId']}"

    # Assuming 2024 as default year (adjust if needed)
    tax_id = f"tax_{emp_id}_2024"

    edges.append({
        "~id": f"e{edge_id}",
        "~from": tax_id,
        "~to": doc_id,
        "~label": "REQUIRES_DOCUMENT"
    })
    edge_id += 1

edges_df = pd.DataFrame(edges)

# =========================
# 5. Save Files
# =========================

nodes_df.to_csv("nodes.csv", index=False)
edges_df.to_csv("edges.csv", index=False)

print("✅ nodes.csv and edges.csv generated successfully!")