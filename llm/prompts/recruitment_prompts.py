def get_classification_prompt(cv_text: str, job_context: str = "") -> str:
    job_section = f'\nHere is the job description for context:\n"""\n{job_context}\n"""' if job_context else ''
    
    return (
        f'You are an HR assistant tasked with classifying candidates into one of three categories: High, Medium, or Low potential.\n\n'
        f'Candidate CV:\n"""\n{cv_text}\n"""{job_section}\n\n'
        'Please do the following:\n'
        '1. Classify the candidate as High, Medium, or Low potential.\n'
        '2. Provide a brief justification for your classification.\n'
        '3. If the candidate is High or Medium potential, list 3–5 relevant interview questions that would help assess their fit, technical skills, or motivation.\n\n'
        'Respond with the classification, justification, and the interview questions (if applicable).'
    )


def get_offer_prompt(hr_input: str) -> str:
    return (
        "You are a professional HR recruiter in QUANTEAM. Based on the following need, generate a complete and structured job description including: "
        "title, responsibilities, required skills, and experience.\n\n"
        f"HR input: {hr_input}\n\n"
        "Return the result in the following format:\n"
        "Title: <Job Title>\n"
        "Responsibilities:\n- ...\n- ...\n"
        "Required Skills:\n- ...\n- ...\n"
        "Experience:\n- ...\n"
    )


def get_interview_prompt(cv_text: str, job_context: str = "") -> str:
    job_description_block = f'\nJob Description:\n"""\n{job_context}\n"""' if job_context else ''
    
    return f"""
You are an HR assistant helping prepare for a job interview.

Based on the following candidate's CV and job description (if available), generate a list of **5 personalized interview questions** that will help evaluate the candidate’s fit for the role.

Candidate CV:
\"\"\"
{cv_text}
\"\"\"
{job_description_block}

Please return only the questions in a numbered list.
"""
def get_report_prompt(cv_text: str, position: str) -> str:
    return f"""
You are a recruiter evaluating a candidate for the position of **{position}**.

Please analyze the CV and produce a structured evaluation following this structure.

**Format your answer as follows (bullet points):**

1. **POINTS FORTS** (Strengths)
   - List the key strengths or standout qualities in the candidate’s profile (e.g., technical skills, achievements, experience).

2. **COMPÉTENCES MÉTIER** (Business Skills)
   - Highlight the candidate's business-related competencies (e.g., risk analysis, process automation, team management).

3. **NIVEAU D'INTERVENTION** (Level of Intervention)
   - Describe the level at which the candidate has worked (e.g., junior, intermediate, senior roles, leadership responsibilities).

4. **COMPÉTENCES TECHNIQUES** (Technical Skills)
   - List the technical tools, programming languages, or technologies the candidate is proficient in.

5. **EXPÉRIENCE** (Experience)
   - Copy as is from the cv provided .

6. **SOFT SKILLS** (Soft Skills)
   - Highlight interpersonal, communication, leadership, and organizational skills.

7. **POINTS DE VIGILANCE** (Watchpoints)
   - Mention any possible concerns or gaps that a recruiter should be aware of (e.g., short durations, lack of specific experience).

Here is the CV:
\"\"\"
{cv_text}
\"\"\"

Return only the structured report.
"""
