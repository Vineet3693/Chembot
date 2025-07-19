
"""
Utility functions for Chemical Engineering Bot
"""

import re
import string
from typing import List, Dict, Any
import streamlit as st

def clean_text(text: str) -> str:
    """
    Clean and format text for better readability
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep chemical formulas
    # Keep: letters, numbers, spaces, parentheses, +, -, =, /, \, degrees, subscripts
    text = re.sub(r'[^\w\s\(\)\+\-=\/\\°₀₁₂₃₄₅₆₇₈₉→←↔]', ' ', text)
    
    # Fix multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_chemical_formulas(text: str) -> List[str]:
    """
    Extract chemical formulas from text
    
    Args:
        text (str): Text containing chemical formulas
        
    Returns:
        List[str]: List of detected chemical formulas
    """
    # Pattern for chemical formulas (e.g., H2SO4, CaCO3, etc.)
    formula_pattern = r'\b[A-Z][a-z]?[0-9]*(?:[A-Z][a-z]?[0-9]*)*\b'
    
    # Common chemical formulas
    common_chemicals = [
        'H2O', 'CO2', 'NH3', 'H2SO4', 'HCl', 'NaOH', 'CaCO3', 'NaCl',
        'CH4', 'C2H6', 'C3H8', 'C2H4', 'C2H2', 'CO', 'NO', 'NO2', 'SO2'
    ]
    
    formulas = re.findall(formula_pattern, text)
    
    # Filter to likely chemical formulas
    valid_formulas = []
    for formula in formulas:
        if (len(formula) >= 2 and 
            any(c.isupper() for c in formula) and 
            any(c.islower() or c.isdigit() for c in formula)):
            valid_formulas.append(formula)
    
    # Add common chemicals if mentioned
    for chemical in common_chemicals:
        if chemical in text:
            valid_formulas.append(chemical)
    
    return list(set(valid_formulas))

def format_equations(text: str) -> str:
    """
    Format mathematical equations for better display
    
    Args:
        text (str): Text containing equations
        
    Returns:
        str: Formatted text with improved equation display
    """
    # Add LaTeX formatting for common mathematical expressions
    # This is a simplified version - could be expanded
    
    # Format fractions
    text = re.sub(r'(\w+)/(\w+)', r'$\\frac{\1}{\2}$', text)
    
    # Format subscripts (chemical formulas)
    text = re.sub(r'([A-Za-z])([0-9]+)', r'\1$_{\2}$', text)
    
    # Format superscripts (powers)
    text = re.sub(r'\^([0-9]+)', r'$^{\1}$', text)
    
    return text

def categorize_question(question: str) -> str:
    """
    Categorize the type of chemical engineering question
    
    Args:
        question (str): User's question
        
    Returns:
        str: Question category
    """
    question_lower = question.lower()
    
    # Safety-related keywords
    safety_words = ['safe', 'hazard', 'danger', 'toxic', 'risk', 'accident', 'emergency']
    if any(word in question_lower for word in safety_words):
        return "safety"
    
    # Calculation keywords
    calc_words = ['calculate', 'compute', 'find', 'determine', 'solve', 'how much', 'what is the']
    if any(word in question_lower for word in calc_words):
        return "calculation"
    
    # Design keywords
    design_words = ['design', 'size', 'select', 'choose', 'optimize', 'specify']
    if any(word in question_lower for word in design_words):
        return "design"
    
    # Theory keywords
    theory_words = ['explain', 'what is', 'how does', 'why', 'difference', 'compare']
    if any(word in question_lower for word in theory_words):
        return "theory"
    
    return "general"

def validate_input(question: str) -> tuple[bool, str]:
    """
    Validate user input
    
    Args:
        question (str): User's question
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Please enter a question."
    
    if len(question.strip()) < 3:
        return False, "Please enter a more detailed question."
    
    if len(question) > 1000:
        return False, "Question is too long. Please keep it under 1000 characters."
    
    # Check for inappropriate content (basic check)
    inappropriate_words = ['spam', 'test123', 'asdf']
    if any(word in question.lower() for word in inappropriate_words):
        return False, "Please enter a genuine chemical engineering question."
    
    return True, ""

def format_response_for_display(response: str) -> str:
    """
    Format AI response for better display in Streamlit
    
    Args:
        response (str): Raw AI response
        
    Returns:
        str: Formatted response
    """
    if not response:
        return "No response generated."
    
    # Split into sections
    sections = response.split('\n\n')
    formatted_sections = []
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Format headers (lines starting with **)
        if section.startswith('**') and section.endswith('**'):
            section = f"\n### {section[2:-2]}\n"
        
        # Format bullet points
        lines = section.split('\n')
        formatted_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                formatted_lines.append(line)
            elif line.startswith('• '):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        formatted_sections.append('\n'.join(formatted_lines))
    
    return '\n\n'.join(formatted_sections)

def get_source_priority_score(url: str) -> int:
    """
    Assign priority score to different source types
    
    Args:
        url (str): URL of the source
        
    Returns:
        int: Priority score (higher = better)
    """
    url_lower = url.lower()
    
    # Educational institutions (.edu)
    if '.edu' in url_lower:
        return 10
    
    # Government sites (.gov)
    if '.gov' in url_lower:
        return 9
    
    # Professional organizations
    professional_orgs = ['aiche.org', 'acs.org', 'asme.org', 'api.org']
    if any(org in url_lower for org in professional_orgs):
        return 8
    
    # Wikipedia and similar
    if 'wikipedia' in url_lower:
        return 6
    
    # General websites
    return 5

def log_interaction(question: str, response: str, sources: List[str] = None):
    """
    Log user interactions (for debugging and improvement)
    
    Args:
        question (str): User question
        response (str): Bot response
        sources (List[str]): Sources used
    """
    # In a production environment, you might want to log to a file or database
    # For now, we'll just use Streamlit's session state
    
    if 'interaction_log' not in st.session_state:
        st.session_state.interaction_log = []
    
    log_entry = {
        'question': question[:100],  # Limit length
        'response_length': len(response),
        'sources_count': len(sources) if sources else 0,
        'timestamp': str(st.session_state.get('current_time', 'unknown'))
    }
    
    st.session_state.interaction_log.append(log_entry)
    
    # Keep only last 50 interactions
    if len(st.session_state.interaction_log) > 50:
        st.session_state.interaction_log = st.session_state.interaction_log[-50:]