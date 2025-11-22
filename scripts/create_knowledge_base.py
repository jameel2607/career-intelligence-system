#!/usr/bin/env python3
"""
Script to create a comprehensive knowledge base for the Career Intelligence System
"""

import pandas as pd
import os
from pathlib import Path

def create_knowledge_base():
    """Create a comprehensive knowledge base with real job data"""
    
    # Define the job data
    job_data = [
        {
            'cluster': 'Technology',
            'job_family': 'Software Development',
            'job_role': 'Frontend Developer',
            'level': 'Entry',
            'qualifications': "Bachelor's in Computer Science, IT, or related field",
            'technical_skills': 'HTML, CSS, JavaScript, React, Vue.js, Angular, Git, Responsive Design',
            'soft_skills': 'Communication, Problem Solving, Attention to Detail, Teamwork',
            'domain_skills': 'Web Development, UI/UX Design, Cross-browser Compatibility',
            'experience_range': '0-2 years',
            'job_index': '15-1254.00',
            'description': 'Develops user interfaces and client-side applications using modern web technologies',
            'average_salary': '₹4-8 LPA (India), $50-70k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1254.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Software Development',
            'job_role': 'Backend Developer',
            'level': 'Entry',
            'qualifications': "Bachelor's in Computer Science, IT, or related field",
            'technical_skills': 'Python, Java, Node.js, SQL, MongoDB, PostgreSQL, REST APIs, Git',
            'soft_skills': 'Problem Solving, Logical Thinking, Communication, Teamwork',
            'domain_skills': 'Server-side Development, Database Management, API Design',
            'experience_range': '0-2 years',
            'job_index': '15-1253.00',
            'description': 'Builds server-side logic, databases, and APIs for web applications',
            'average_salary': '₹5-9 LPA (India), $55-75k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1253.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Software Development',
            'job_role': 'Full Stack Developer',
            'level': 'Mid',
            'qualifications': "Bachelor's in Computer Science + 2-3 years experience",
            'technical_skills': 'JavaScript, React, Node.js, Python, SQL, MongoDB, Git, Docker',
            'soft_skills': 'Problem Solving, Communication, Time Management, Adaptability',
            'domain_skills': 'Full Stack Development, DevOps, System Architecture',
            'experience_range': '2-5 years',
            'job_index': '15-1252.00',
            'description': 'Develops both frontend and backend components of web applications',
            'average_salary': '₹8-15 LPA (India), $70-95k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1252.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Software Development',
            'job_role': 'Software Engineer',
            'level': 'Mid',
            'qualifications': "Bachelor's in Computer Science + 3-5 years experience",
            'technical_skills': 'Java, Python, C++, SQL, Git, Algorithms, Data Structures, Testing',
            'soft_skills': 'Problem Solving, Critical Thinking, Communication, Collaboration',
            'domain_skills': 'Software Architecture, System Design, Code Review',
            'experience_range': '3-6 years',
            'job_index': '15-1251.00',
            'description': 'Designs, develops, and maintains software systems and applications',
            'average_salary': '₹10-18 LPA (India), $80-110k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1251.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Software Development',
            'job_role': 'Senior Software Engineer',
            'level': 'Senior',
            'qualifications': "Bachelor's + 5+ years experience or Master's + 3+ years",
            'technical_skills': 'Advanced Programming, System Design, Architecture, Leadership, Mentoring',
            'soft_skills': 'Leadership, Communication, Strategic Thinking, Problem Solving',
            'domain_skills': 'Technical Leadership, System Architecture, Code Quality',
            'experience_range': '5-10 years',
            'job_index': '15-1250.00',
            'description': 'Leads development teams and makes architectural decisions for complex software systems',
            'average_salary': '₹18-35 LPA (India), $110-150k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1250.00'
        },
        {
            'cluster': 'Data',
            'job_family': 'Analytics',
            'job_role': 'Data Analyst',
            'level': 'Entry',
            'qualifications': "Bachelor's in Statistics, Mathematics, Computer Science, or related field",
            'technical_skills': 'SQL, Python, R, Excel, Tableau, Power BI, Statistics, Data Visualization',
            'soft_skills': 'Analytical Thinking, Communication, Attention to Detail, Curiosity',
            'domain_skills': 'Data Analysis, Statistical Analysis, Business Intelligence',
            'experience_range': '0-2 years',
            'job_index': '15-2041.00',
            'description': 'Analyzes data to identify trends, patterns, and insights for business decisions',
            'average_salary': '₹4-7 LPA (India), $45-65k (Global)',
            'sources': 'https://www.onetonline.org/link/15-2041.00'
        },
        {
            'cluster': 'Data',
            'job_family': 'Analytics',
            'job_role': 'Data Scientist',
            'level': 'Mid',
            'qualifications': "Bachelor's in quantitative field + 2-3 years experience or Master's",
            'technical_skills': 'Python, R, SQL, Machine Learning, Statistics, Pandas, Scikit-learn, TensorFlow',
            'soft_skills': 'Problem Solving, Critical Thinking, Communication, Creativity',
            'domain_skills': 'Machine Learning, Statistical Modeling, Data Mining',
            'experience_range': '2-5 years',
            'job_index': '15-2051.01',
            'description': 'Builds predictive models and extracts insights from complex datasets',
            'average_salary': '₹8-16 LPA (India), $75-105k (Global)',
            'sources': 'https://www.onetonline.org/link/15-2051.01'
        },
        {
            'cluster': 'Data',
            'job_family': 'Analytics',
            'job_role': 'Senior Data Scientist',
            'level': 'Senior',
            'qualifications': "Master's/PhD + 4+ years experience",
            'technical_skills': 'Advanced ML, Deep Learning, MLOps, Cloud Platforms, Leadership',
            'soft_skills': 'Leadership, Strategic Thinking, Communication, Innovation',
            'domain_skills': 'Advanced Analytics, AI Strategy, Team Leadership',
            'experience_range': '4-8 years',
            'job_index': '15-2051.00',
            'description': 'Leads data science initiatives and develops advanced analytical solutions',
            'average_salary': '₹16-30 LPA (India), $105-140k (Global)',
            'sources': 'https://www.onetonline.org/link/15-2051.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'AI/ML',
            'job_role': 'Machine Learning Engineer',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/Engineering + ML experience",
            'technical_skills': 'Python, TensorFlow, PyTorch, Kubernetes, Docker, MLOps, Cloud (AWS/GCP/Azure)',
            'soft_skills': 'Problem Solving, Innovation, Communication, Collaboration',
            'domain_skills': 'ML Engineering, Model Deployment, Production Systems',
            'experience_range': '2-5 years',
            'job_index': '15-2031.00',
            'description': 'Deploys and maintains machine learning models in production environments',
            'average_salary': '₹10-20 LPA (India), $85-120k (Global)',
            'sources': 'https://www.onetonline.org/link/15-2031.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'AI/ML',
            'job_role': 'AI Engineer',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/AI + 3+ years experience",
            'technical_skills': 'Python, Deep Learning, NLP, Computer Vision, TensorFlow, PyTorch, MLOps',
            'soft_skills': 'Innovation, Problem Solving, Research Skills, Communication',
            'domain_skills': 'Artificial Intelligence, Deep Learning, Neural Networks',
            'experience_range': '3-6 years',
            'job_index': '15-2032.00',
            'description': 'Develops AI systems and implements advanced machine learning algorithms',
            'average_salary': '₹12-22 LPA (India), $90-130k (Global)',
            'sources': 'https://www.onetonline.org/link/15-2032.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Cloud/DevOps',
            'job_role': 'DevOps Engineer',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/IT + 2-3 years experience",
            'technical_skills': 'Docker, Kubernetes, AWS/Azure/GCP, Jenkins, Terraform, Linux, Git, CI/CD',
            'soft_skills': 'Problem Solving, Communication, Adaptability, Teamwork',
            'domain_skills': 'Cloud Computing, Infrastructure Automation, System Administration',
            'experience_range': '2-5 years',
            'job_index': '15-1244.00',
            'description': 'Manages infrastructure, deployment pipelines, and ensures system reliability',
            'average_salary': '₹8-16 LPA (India), $70-100k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1244.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Cloud/DevOps',
            'job_role': 'Cloud Engineer',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/IT + Cloud certifications",
            'technical_skills': 'AWS/Azure/GCP, Terraform, Kubernetes, Docker, Python, Networking',
            'soft_skills': 'Problem Solving, Communication, Learning Agility, Attention to Detail',
            'domain_skills': 'Cloud Architecture, Infrastructure as Code, Security',
            'experience_range': '2-5 years',
            'job_index': '15-1245.00',
            'description': 'Designs and manages cloud infrastructure and services',
            'average_salary': '₹9-18 LPA (India), $75-110k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1245.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Cybersecurity',
            'job_role': 'Cybersecurity Analyst',
            'level': 'Entry',
            'qualifications': "Bachelor's in Cybersecurity, IT, or related field + Security certifications",
            'technical_skills': 'Network Security, SIEM Tools, Incident Response, Risk Assessment, Compliance',
            'soft_skills': 'Analytical Thinking, Attention to Detail, Communication, Integrity',
            'domain_skills': 'Information Security, Threat Analysis, Compliance',
            'experience_range': '0-3 years',
            'job_index': '15-1122.00',
            'description': 'Monitors and protects organizational systems from cyber threats',
            'average_salary': '₹5-10 LPA (India), $50-75k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1122.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Mobile Development',
            'job_role': 'Mobile App Developer',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/IT + Mobile development experience",
            'technical_skills': 'iOS (Swift), Android (Kotlin/Java), React Native, Flutter, Git, API Integration',
            'soft_skills': 'Problem Solving, Creativity, Communication, User Focus',
            'domain_skills': 'Mobile Development, UI/UX Design, Cross-platform Development',
            'experience_range': '1-4 years',
            'job_index': '15-1256.00',
            'description': 'Develops mobile applications for iOS and Android platforms',
            'average_salary': '₹6-14 LPA (India), $65-90k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1256.00'
        },
        {
            'cluster': 'Design',
            'job_family': 'UX/UI',
            'job_role': 'UX Designer',
            'level': 'Mid',
            'qualifications': "Bachelor's in Design, HCI, or related field + Portfolio",
            'technical_skills': 'Figma, Sketch, Adobe Creative Suite, Prototyping, User Research, Wireframing',
            'soft_skills': 'Empathy, Creativity, Communication, Problem Solving, Collaboration',
            'domain_skills': 'User Experience Design, Human-Computer Interaction, Design Thinking',
            'experience_range': '1-4 years',
            'job_index': '15-1255.00',
            'description': 'Designs user experiences and interfaces for digital products',
            'average_salary': '₹5-12 LPA (India), $55-80k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1255.00'
        },
        {
            'cluster': 'Design',
            'job_family': 'UX/UI',
            'job_role': 'UI Designer',
            'level': 'Entry',
            'qualifications': "Bachelor's in Design, Visual Arts, or related field + Portfolio",
            'technical_skills': 'Figma, Sketch, Adobe Creative Suite, CSS, HTML, Design Systems',
            'soft_skills': 'Creativity, Attention to Detail, Communication, Visual Thinking',
            'domain_skills': 'Visual Design, Interface Design, Brand Guidelines',
            'experience_range': '0-3 years',
            'job_index': '15-1257.00',
            'description': 'Creates visual designs and user interfaces for digital applications',
            'average_salary': '₹4-9 LPA (India), $45-70k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1257.00'
        },
        {
            'cluster': 'Business',
            'job_family': 'Product Management',
            'job_role': 'Product Manager',
            'level': 'Mid',
            'qualifications': "Bachelor's in Business, Engineering, or related field + 3+ years experience",
            'technical_skills': 'Analytics Tools, SQL, Project Management, Agile/Scrum, Market Research',
            'soft_skills': 'Leadership, Communication, Strategic Thinking, Problem Solving',
            'domain_skills': 'Product Strategy, Market Analysis, Stakeholder Management',
            'experience_range': '3-6 years',
            'job_index': '11-3031.01',
            'description': 'Defines product strategy and manages product development lifecycle',
            'average_salary': '₹12-25 LPA (India), $85-120k (Global)',
            'sources': 'https://www.onetonline.org/link/11-3031.01'
        },
        {
            'cluster': 'Business',
            'job_family': 'Project Management',
            'job_role': 'Project Manager',
            'level': 'Mid',
            'qualifications': "Bachelor's + PMP/Agile certifications + 3+ years experience",
            'technical_skills': 'Project Management Tools, Agile/Scrum, Risk Management, Budgeting',
            'soft_skills': 'Leadership, Communication, Organization, Problem Solving',
            'domain_skills': 'Project Planning, Resource Management, Stakeholder Communication',
            'experience_range': '3-6 years',
            'job_index': '11-3021.00',
            'description': 'Plans, executes, and manages projects to deliver results on time and budget',
            'average_salary': '₹8-18 LPA (India), $70-95k (Global)',
            'sources': 'https://www.onetonline.org/link/11-3021.00'
        },
        {
            'cluster': 'Business',
            'job_family': 'Sales',
            'job_role': 'Sales Executive',
            'level': 'Entry',
            'qualifications': "Bachelor's in Business, Marketing, or any field + Sales aptitude",
            'technical_skills': 'CRM Software, Sales Analytics, Lead Generation, Presentation Skills',
            'soft_skills': 'Communication, Persuasion, Resilience, Relationship Building',
            'domain_skills': 'Sales Process, Customer Relationship Management, Market Knowledge',
            'experience_range': '0-2 years',
            'job_index': '41-3031.00',
            'description': 'Generates leads, manages customer relationships, and closes sales deals',
            'average_salary': '₹3-8 LPA (India), $40-60k (Global)',
            'sources': 'https://www.onetonline.org/link/41-3031.00'
        },
        {
            'cluster': 'Business',
            'job_family': 'Marketing',
            'job_role': 'Digital Marketing Specialist',
            'level': 'Entry',
            'qualifications': "Bachelor's in Marketing, Communications, or related field",
            'technical_skills': 'Google Analytics, SEO/SEM, Social Media Marketing, Content Marketing, Email Marketing',
            'soft_skills': 'Creativity, Communication, Analytical Thinking, Adaptability',
            'domain_skills': 'Digital Marketing, Content Strategy, Campaign Management',
            'experience_range': '0-3 years',
            'job_index': '11-2031.00',
            'description': 'Develops and executes digital marketing campaigns across various channels',
            'average_salary': '₹4-9 LPA (India), $45-65k (Global)',
            'sources': 'https://www.onetonline.org/link/11-2031.00'
        },
        {
            'cluster': 'Finance',
            'job_family': 'Financial Analysis',
            'job_role': 'Financial Analyst',
            'level': 'Entry',
            'qualifications': "Bachelor's in Finance, Accounting, Economics, or related field",
            'technical_skills': 'Excel, Financial Modeling, SQL, Tableau, Bloomberg Terminal',
            'soft_skills': 'Analytical Thinking, Attention to Detail, Communication, Problem Solving',
            'domain_skills': 'Financial Analysis, Valuation, Risk Assessment',
            'experience_range': '0-3 years',
            'job_index': '13-2051.00',
            'description': 'Analyzes financial data and provides insights for investment and business decisions',
            'average_salary': '₹4-8 LPA (India), $50-70k (Global)',
            'sources': 'https://www.onetonline.org/link/13-2051.00'
        },
        {
            'cluster': 'Healthcare',
            'job_family': 'Healthcare IT',
            'job_role': 'Health Informatics Specialist',
            'level': 'Mid',
            'qualifications': "Bachelor's in Health Informatics, IT, or Healthcare + IT experience",
            'technical_skills': 'EHR Systems, Healthcare Databases, SQL, Data Analysis, HIPAA Compliance',
            'soft_skills': 'Communication, Problem Solving, Attention to Detail, Empathy',
            'domain_skills': 'Healthcare Systems, Medical Data Management, Regulatory Compliance',
            'experience_range': '2-5 years',
            'job_index': '15-1121.01',
            'description': 'Manages healthcare information systems and ensures data quality and compliance',
            'average_salary': '₹6-12 LPA (India), $60-85k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1121.01'
        },
        {
            'cluster': 'Education',
            'job_family': 'EdTech',
            'job_role': 'Instructional Designer',
            'level': 'Mid',
            'qualifications': "Bachelor's in Education, Psychology, or related field + EdTech experience",
            'technical_skills': 'Learning Management Systems, E-learning Authoring Tools, Multimedia Design',
            'soft_skills': 'Creativity, Communication, Empathy, Problem Solving',
            'domain_skills': 'Curriculum Design, Learning Theory, Educational Technology',
            'experience_range': '2-5 years',
            'job_index': '25-9031.00',
            'description': 'Designs educational content and learning experiences for digital platforms',
            'average_salary': '₹5-10 LPA (India), $55-75k (Global)',
            'sources': 'https://www.onetonline.org/link/25-9031.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Quality Assurance',
            'job_role': 'QA Engineer',
            'level': 'Entry',
            'qualifications': "Bachelor's in CS/IT or related field",
            'technical_skills': 'Manual Testing, Automation Testing, Selenium, JIRA, Test Planning',
            'soft_skills': 'Attention to Detail, Problem Solving, Communication, Patience',
            'domain_skills': 'Software Testing, Quality Assurance, Bug Tracking',
            'experience_range': '0-3 years',
            'job_index': '15-1253.01',
            'description': 'Tests software applications to ensure quality and identify defects',
            'average_salary': '₹3-7 LPA (India), $45-65k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1253.01'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Database',
            'job_role': 'Database Administrator',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/IT + Database certifications + 2+ years experience",
            'technical_skills': 'SQL, MySQL, PostgreSQL, Oracle, MongoDB, Database Design, Backup/Recovery',
            'soft_skills': 'Problem Solving, Attention to Detail, Communication, Reliability',
            'domain_skills': 'Database Management, Performance Tuning, Data Security',
            'experience_range': '2-6 years',
            'job_index': '15-1141.00',
            'description': 'Manages and maintains database systems to ensure optimal performance and security',
            'average_salary': '₹6-14 LPA (India), $65-90k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1141.00'
        },
        {
            'cluster': 'Technology',
            'job_family': 'Systems',
            'job_role': 'Systems Administrator',
            'level': 'Mid',
            'qualifications': "Bachelor's in CS/IT + System administration experience",
            'technical_skills': 'Linux, Windows Server, Networking, Virtualization, Scripting, Security',
            'soft_skills': 'Problem Solving, Communication, Reliability, Learning Agility',
            'domain_skills': 'System Administration, Network Management, Infrastructure',
            'experience_range': '2-5 years',
            'job_index': '15-1142.00',
            'description': 'Maintains and manages computer systems, networks, and IT infrastructure',
            'average_salary': '₹5-12 LPA (India), $55-80k (Global)',
            'sources': 'https://www.onetonline.org/link/15-1142.00'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(job_data)
    
    # Ensure the knowledge_base directory exists
    kb_dir = Path(__file__).parent.parent / 'knowledge_base'
    kb_dir.mkdir(exist_ok=True)
    
    # Save to Excel file
    excel_path = kb_dir / 'career_intelligence_kb.xlsx'
    df.to_excel(excel_path, index=False, engine='openpyxl')
    
    print(f"Knowledge base created successfully at: {excel_path}")
    print(f"Total job roles: {len(df)}")
    print(f"Clusters: {df['cluster'].unique()}")
    print(f"Job families: {df['job_family'].nunique()}")
    
    return excel_path

if __name__ == "__main__":
    create_knowledge_base()
