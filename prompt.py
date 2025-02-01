REFINE_PROMPT = """
You will be given a list of history messages and the current user question.  
Your task is to refine the user question based on the previous user question.  
If the current question is not related to the {num} previous user questions, please return the original question.  
Otherwise, refine the current question to better capture the user's intent.

When refining, consider that the database has the following tables:  
- **Company**: Stores company details.  
- **User**: Stores user details, including their associated company.  

Example:  
History:  
- user: Công ty "ABC Corp" có bao nhiêu nhân viên?  

Question: Nguyễn Văn A làm việc ở đâu?  
After refining: Nguyễn Văn A làm việc ở công ty nào?  

History:  
- user: Danh sách các công ty có trong hệ thống?  

Question: Có người dùng nào thuộc công ty này không?  
After refining: Có người dùng nào thuộc các công ty trong hệ thống không?  

""" 