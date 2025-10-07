openai_client = OpenAIClient(api_key=req.api_key)
result = answer_user_query(openai_client, df, req.query)