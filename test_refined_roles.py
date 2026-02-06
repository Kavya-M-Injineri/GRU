
def refine_role_logic(base_role, cleaned_text):
    ROLE_KEYWORDS = {
        'Software Development Engineer (SDE)': ['sde', 'backend', 'java', 'spring', 'microservices', 'api', 'sql', 'system design'],
        'Software Engineer (SWE)': ['swe', 'software engineer', 'coding', 'algorithms', 'data structures', 'development'],
        'Python Developer': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scripting', 'py'],
        'Machine Learning Engineer (ML)': ['ml', 'machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'deep learning', 'neural', 'ai', 'modeling'],
        'VLSI Engineer': ['vlsi', 'verilog', 'vhdl', 'fpga', 'asic', 'cmos', 'circuit', 'rtl', 'cadence'],
        'Hardware Engineer': ['hardware', 'pcb', 'circuit design', 'electronics', 'microcontroller', 'arduino', 'raspberry pi', 'embedded'],
        'Site Reliability Engineer (SRE)': ['sre', 'site reliability', 'scalability', 'monitoring', 'availability', 'infrastructure', 'on-call'],
        'Frontend Developer': ['frontend', 'react', 'angular', 'vue', 'html', 'css', 'javascript', 'js', 'ui', 'ux', 'web'],
        'Backend Developer': ['backend', 'node', 'express', 'ruby', 'rails', 'php', 'databases', 'redis', 'mongodb'],
        'Full Stack Developer': ['full stack', 'fullstack', 'mern', 'mean', 'frontend and backend'],
        'Data Scientist': ['data scientist', 'data science', 'statistics', 'r', 'tableau', 'visualization', 'analysis', 'modeling'],
        'DevOps Engineer': ['devops', 'cicd', 'docker', 'kubernetes', 'jenkins', 'ansible', 'terraform', 'cloud'],
        'Cybersecurity Analyst': ['cybersecurity', 'security', 'pentesting', 'network security', 'cryptography', 'firewall', 'threat'],
        'Mobile App Developer': ['mobile', 'android', 'ios', 'swift', 'kotlin', 'flutter', 'react native', 'app'],
        'Cloud Architect': ['cloud architect', 'aws', 'azure', 'gcp', 'cloud infrastructure', 'serverless'],
        'Embedded Systems Engineer': ['embedded', 'c', 'cpp', 'rtos', 'firmware', 'bare metal', 'stm32'],
        'Automation Engineer': ['automation', 'selenium', 'testing', 'qa', 'scripts', 'pytest', 'unittest']
    }

    refined_role = base_role
    sub_role_scores = {}

    if base_role in ['ENGINEERING', 'INFORMATION-TECHNOLOGY']:
        text_lower = cleaned_text.lower()
        for role, keywords in ROLE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                sub_role_scores[role] = score
        
        if sub_role_scores:
            refined_role = max(sub_role_scores, key=sub_role_scores.get)

    tags = []
    if 'intern' in cleaned_text.lower():
        tags.append('Intern')
    if 'freelancer' in cleaned_text.lower() or 'freelance' in cleaned_text.lower():
        tags.append('Freelancer')
    
    display_role = refined_role
    if tags:
        display_role += f" ({', '.join(tags)})"
    
    return display_role

# Test Cases
test_cases = [
    ("INFORMATION-TECHNOLOGY", "Python developer with experience in flask and django", "Python Developer"),
    ("INFORMATION-TECHNOLOGY", "SDE with java and microservices background", "Software Development Engineer (SDE)"),
    ("ENGINEERING", "VLSI design using verilog and rtl", "VLSI Engineer"),
    ("ENGINEERING", "Machine learning intern with tensorflow skills", "Machine Learning Engineer (ML) (Intern)"),
    ("INFORMATION-TECHNOLOGY", "Mobile app freelancer focused on flutter and ios", "Mobile App Developer (Freelancer)"),
    ("ENGINEERING", "Hardware engineer with pcb and arduino experience", "Hardware Engineer"),
    ("PUBLIC-RELATIONS", "PR professional", "PUBLIC-RELATIONS") # Should not refine
]

print("Running Refinement Logic Tests:")
for base, text, expected in test_cases:
    actual = refine_role_logic(base, text)
    status = "PASS" if actual == expected else f"FAIL (Expected: {expected}, Got: {actual})"
    print(f"Base: {base} | Text: {text[:30]}... | Result: {actual} | Status: {status}")
