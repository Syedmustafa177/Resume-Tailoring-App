import streamlit as st
import pdfplumber
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from typing import Dict, List, Optional
import json

load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ResumeFormatter:
    def __init__(self):
        self.section_templates = {
            'header': '''
{name}
{location}
Mobile: {phone} | Email: {email}
LinkedIn: {linkedin}
Website: {website}
''',
            'profile_summary': '''
PROFILE SUMMARY
{content}
''',
            'areas_of_excellence': '''
AREAS OF EXCELLENCE
{content}
''',
            'technical_skills': '''
TECHNICAL SKILLS
{content}
''',
            'work_experience': '''
WORK EXPERIENCE
{content}
''',
            'projects': '''
PROJECTS
{content}
''',
            'education': '''
EDUCATION
{content}
'''
        }
        
    def format_section(self, section_name: str, content: str) -> str:
        """Format a section using its template"""
        return self.section_templates[section_name].format(content=content)

class ResumeParser:
    def __init__(self):
        self.contact_patterns = {
            'name': r'^([A-Za-z\s]+)$',
            'location': r'([A-Za-z\s]+,\s*[A-Za-z\s]+,\s*[A-Za-z\s]+)',
            'phone': r'Mobile:\s*([+\d-]+)',
            'email': r'Email:\s*([\w\.-]+@[\w\.-]+)',
            'linkedin': r'LinkedIn:\s*(https?://[\w\./]+)',
            'website': r'Website:\s*(https?://[\w\./]+)'
        }

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information using regex patterns"""
        contact_info = {}
        for key, pattern in self.contact_patterns.items():
            match = re.search(pattern, text, re.MULTILINE)
            contact_info[key] = match.group(1) if match else ''
        return contact_info

    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract main sections from resume text"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in text.split('\n'):
            if re.match(r'^[A-Z\s]+$', line.strip()) and len(line.strip()) > 2:
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip()
                current_content = []
            elif current_section:
                current_content.append(line)
                
        if current_section:
            sections[current_section] = '\n'.join(current_content)
            
        return sections

def extract_resume_text(uploaded_file) -> Optional[str]:
    """Extract text from uploaded PDF file"""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting PDF: {str(e)}")
        return None

def analyze_resume_format(resume_text: str) -> Dict:
    """Analyze formatting patterns in the resume"""
    return {
        'bullet_style': '●' if '●' in resume_text else ('•' if '•' in resume_text else '-'),
        'section_spacing': 2,
        'indent_pattern': '    ',
        'heading_style': 'UPPERCASE'
    }

def analyze_resume(resume_text: str, job_description: str) -> tuple:
    """Analyze resume and generate insights"""
    model = genai.GenerativeModel('gemini-pro')
    
    # Analyze experience level
    experience_prompt = """
    Analyze this resume and extract:
    1. Total years of experience
    2. Current seniority level
    3. Primary technical domain
    
    RESUME:
    {resume_text}
    
    Provide only these three data points in a concise format.
    """.format(resume_text=resume_text)
    
    experience_info = model.generate_content(experience_prompt).text
    
    # Analyze format
    format_analysis = analyze_resume_format(resume_text)
    
    # Generate comprehensive analysis
    analysis_prompt = """
    You are an expert resume consultant. Provide a comprehensive analysis:
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Provide:
    1. SKILLS ALIGNMENT
       - Matching skills
       - Missing critical skills
       - Suggested skill additions
    
    2. EXPERIENCE ANALYSIS
       - Relevant experience
       - Areas needing enhancement
       - Suggested focus points
    
    3. PROJECT RECOMMENDATIONS
       - Which existing projects to keep (if any)
       - Types of projects needed
       - Suggested project complexities
    """.format(resume_text=resume_text, job_description=job_description)
    
    analysis = model.generate_content(analysis_prompt).text
    
    return analysis, experience_info, format_analysis

def generate_tailored_content(section_name: str, job_description: str, 
                            experience_level: str, format_analysis: Dict) -> str:
    """Generate content for a specific section"""
    model = genai.GenerativeModel('gemini-pro')
    
    prompts = {
        'profile_summary': """
        Create a professional profile summary for a {experience_level}-year experienced professional.
        Format using bullet points with '{bullet_style}'.
        
        JOB DESCRIPTION:
        {job_description}
        
        Focus on key achievements and skills relevant to the job.
        """,
        'technical_skills': """
        List technical skills relevant to this job description, grouped by category.
        Use bullet point style '{bullet_style}'.
        
        JOB DESCRIPTION:
        {job_description}
        
        EXPERIENCE LEVEL: {experience_level} years
        """,
        'projects': """
        Create 3-4 relevant projects matching these job requirements.
        Format each project as:
        
        Project Name | Technologies link
        o Key achievement/feature
        o Technical implementation detail
        o Impact or result
        
        JOB DESCRIPTION:
        {job_description}
        
        Use appropriate complexity for {experience_level} years of experience.
        """
    }
    
    if section_name in prompts:
        prompt = prompts[section_name].format(
            experience_level=experience_level,
            job_description=job_description,
            bullet_style=format_analysis['bullet_style']
        )
        return model.generate_content(prompt).text
    
    return ""

def generate_tailored_resume(resume_text: str, job_description: str, 
                           analysis: str, experience_info: str, 
                           format_analysis: Dict) -> str:
    """Generate complete tailored resume"""
    # Initialize formatter and parser
    formatter = ResumeFormatter()
    parser = ResumeParser()
    
    # Extract contact info and sections
    contact_info = parser.extract_contact_info(resume_text)
    original_sections = parser.extract_sections(resume_text)
    
    # Get experience level
    experience_level = "5"  # Default
    try:
        experience_level = re.search(r'(\d+)', experience_info).group(1)
    except:
        pass
    
    # Generate new content for each section
    sections_content = {}
    
    # Header (keep original)
    header = formatter.section_templates['header'].format(**contact_info)
    
    # Generate new content for main sections
    for section in ['profile_summary', 'technical_skills', 'projects']:
        sections_content[section] = generate_tailored_content(
            section,
            job_description,
            experience_level,
            format_analysis
        )
    
    # Combine all sections
    tailored_resume = f"""
{header}

{formatter.format_section('profile_summary', sections_content['profile_summary'])}

{formatter.format_section('technical_skills', sections_content['technical_skills'])}

{original_sections.get('WORK EXPERIENCE', '')}

{formatter.format_section('projects', sections_content['projects'])}

{original_sections.get('EDUCATION', '')}
""".strip()
    
    return tailored_resume

def main():
    st.set_page_config(page_title="AI Resume Tailor", layout="wide")
    st.title("Professional Resume Tailoring Assistant")
    
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Please set your Google API key in the .env file")
        st.stop()
    
    # Initialize session state
    for key in ['analysis_done', 'analysis_result', 'experience_info', 
                'format_analysis', 'resume_text', 'tailored_resume']:
        if key not in st.session_state:
            st.session_state[key] = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Documents")
        resume_file = st.file_uploader("Upload your current resume (PDF)", type="pdf")
        job_description = st.text_area("Paste the job description", height=300)
        
        if resume_file and job_description:
            if st.button("Analyze Resume"):
                with st.spinner("Analyzing resume..."):
                    resume_text = extract_resume_text(resume_file)
                    if resume_text:
                        analysis, experience_info, format_analysis = analyze_resume(
                            resume_text, 
                            job_description
                        )
                        st.session_state.analysis_result = analysis
                        st.session_state.experience_info = experience_info
                        st.session_state.format_analysis = format_analysis
                        st.session_state.analysis_done = True
                        st.session_state.resume_text = resume_text
    
    with col2:
        st.subheader("Analysis & Enhanced Resume")
        
        if st.session_state.analysis_done:
            st.write("### Analysis Results")
            st.write(st.session_state.analysis_result)
            
            if st.button("Generate Enhanced Resume"):
                with st.spinner("Generating enhanced resume..."):
                    st.session_state.tailored_resume = generate_tailored_resume(
                        st.session_state.resume_text,
                        job_description,
                        st.session_state.analysis_result,
                        st.session_state.experience_info,
                        st.session_state.format_analysis
                    )
        
        if st.session_state.tailored_resume:
            st.write("### Enhanced Resume")
            st.write(st.session_state.tailored_resume)
            
            st.download_button(
                "Download Enhanced Resume",
                st.session_state.tailored_resume,
                file_name="enhanced_resume.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()