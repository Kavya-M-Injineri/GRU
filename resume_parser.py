import os
import pdfplumber
import docx
import pytesseract
from PIL import Image
from utils import clean_text

# Configure Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

REQUIRED_SKILLS = {
    'HR': ['recruiting', 'communication', 'payroll', 'policy', 'human resources'],
    'DESIGNER': ['photoshop', 'illustrator', 'ui', 'ux', 'adobe', 'sketch'],
    'INFORMATION-TECHNOLOGY': ['python', 'java', 'sql', 'database', 'network', 'agile'],
    'TEACHER': ['teaching', 'classroom', 'curriculum', 'education', 'students'],
    'ADVOCATE': ['legal', 'law', 'litigation', 'court', 'research'],
    'BUSINESS-DEVELOPMENT': ['sales', 'marketing', 'strategy', 'client', 'negotiation'],
    'FINANCE': ['finance', 'accounting', 'audit', 'reporting', 'tax'],
    'ENGINEERING': ['engineering', 'design', 'testing', 'development', 'cad'],
    'SALES': ['sales', 'customer', 'negotiation', 'communication', 'target'],
    'Software Development Engineer (SDE)': ['java', 'spring', 'microservices', 'sql', 'system design', 'api'],
    'Software Engineer (SWE)': ['coding', 'algorithms', 'data structures', 'software engineering', 'debugging'],
    'Python Developer': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scripting'],
    'Machine Learning Engineer (ML)': ['machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'deep learning', 'neural'],
    'VLSI Engineer': ['verilog', 'vhdl', 'fpga', 'asic', 'cmos', 'circuit', 'rtl'],
    'Hardware Engineer': ['pcb', 'circuit design', 'electronics', 'microcontroller', 'arduino', 'hardware'],
    'Site Reliability Engineer (SRE)': ['kubernetes', 'monitoring', 'scalability', 'docker', 'infrastructure', 'availability'],
    'Frontend Developer': ['react', 'angular', 'vue', 'html', 'css', 'javascript', 'js', 'ui', 'ux'],
    'Backend Developer': ['node', 'express', 'databases', 'api', 'microservices', 'sql', 'no-sql'],
    'Full Stack Developer': ['react', 'node', 'sql', 'frontend', 'backend', 'javascript', 'web development'],
    'Data Scientist': ['statistics', 'r', 'python', 'visualization', 'machine learning', 'data analysis', 'modeling'],
    'DevOps Engineer': ['ci/cd', 'docker', 'kubernetes', 'jenkins', 'terraform', 'aws', 'ansible'],
    'Cybersecurity Analyst': ['security', 'penetration testing', 'network security', 'firewall', 'cryptography', 'threat analysis'],
    'Mobile App Developer': ['android', 'ios', 'swift', 'kotlin', 'flutter', 'react native', 'mobile development'],
    'Cloud Architect': ['aws', 'azure', 'gcp', 'serverless', 'cloud infrastructure', 'architecture'],
    'Embedded Systems Engineer': ['c', 'cpp', 'rtos', 'firmware', 'stm32', 'bare metal', 'embedded systems'],
    'Automation Engineer': ['selenium', 'testing', 'qa', 'automation', 'scripts', 'pytest', 'unittest']
}

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text_from_image(file_path):
    text = ""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error reading Image (OCR): {e}")
        text = ""
    return text

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""

def get_sub_role(cleaned_text, base_role):
    refined_role = base_role
    sub_role_scores = {}
    
    if base_role.upper() in ['ENGINEERING', 'INFORMATION-TECHNOLOGY']:
        text_lower = cleaned_text.lower()
        for role, keywords in ROLE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                sub_role_scores[role] = score
        
        if sub_role_scores:
            refined_role = max(sub_role_scores, key=sub_role_scores.get)
            
    return refined_role

def get_missing_skills(cleaned_text, role):
    missing_skills = []
    text_lower = cleaned_text.lower()
    
    if role in REQUIRED_SKILLS:
        for skill in REQUIRED_SKILLS[role]:
            if skill.lower() not in text_lower:
                missing_skills.append(skill)
    return missing_skills

def detect_sections(text):
    sections = []
    text_upper = text.upper()
    keywords = {
        'Education': ['EDUCATION', 'ACADEMIC', 'QUALIFICATIONS', 'SCHOLASTIC'],
        'Experience': ['EXPERIENCE', 'WORK HISTORY', 'PROFESSIONAL BACKGROUND', 'EMPLOYMENT'],
        'Skills': ['SKILLS', 'TECHNICAL SKILLS', 'STRENGTHS', 'COMPETENCIES'],
        'Projects': ['PROJECTS', 'ACADEMIC PROJECTS', 'PERSONAL PROJECTS'],
        'Certifications': ['CERTIFICATIONS', 'COURSES', 'CERTIFICATES']
    }
    for section, keys in keywords.items():
        if any(key in text_upper for key in keys):
            sections.append(section)
    return sections

def parse_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx' or ext == '.doc':
        text = extract_text_from_docx(file_path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        text = extract_text_from_image(file_path)
    elif ext == '.txt':
        text = extract_text_from_txt(file_path)
    
    cleaned_text = clean_text(text)
    
    # Analysis Metrics
    words = cleaned_text.split()
    word_count = len(words)
    char_count = len(cleaned_text)
    # Average reading speed: 200-250 wpm
    reading_time_sec = (word_count / 200) * 60
    
    sections_found = detect_sections(text)
    
    return {
        'raw_text': text,
        'cleaned_text': cleaned_text,
        'analysis': {
            'word_count': word_count,
            'char_count': char_count,
            'reading_time': f"{int(reading_time_sec // 60)}m {int(reading_time_sec % 60)}s" if reading_time_sec > 60 else f"{int(reading_time_sec)}s",
            'sections_found': sections_found,
            'complexity': "High" if word_count > 500 else "Medium" if word_count > 200 else "Low"
        }
    }
