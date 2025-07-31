I wanted to provide you with an update regarding the issue you reported about the missing column in the E3 environment.

I have thoroughly crosschecked the schema file, and I can confirm that the column in question is indeed present in our schema definition. Additionally, I have verified across all environments — E1, E2, and E3 — and the column exists in DataStax for each of them.

To be doubly sure, I tested this locally by running the same query, and the column is showing up correctly in the results. I’ve attached screenshots below to show the results from all three environments — E1, E2, and E3 — for your reference.

However, I did notice one behavior in E3 worth mentioning. When I executed the query multiple times, I did not receive data in the first three attempts, but on the fourth attempt, I did get the expected results. This suggests that the semantic retrieval might be behaving inconsistently at times, possibly due to transient factors or load-related variance.

We are continuing to look into this further, but I wanted to share these findings with you in the meantime.

Please feel free to reach out if you have any questions or if there’s anything else you’d like us to check.