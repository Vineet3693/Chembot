
"""
Core Chemical Engineering Bot Engine
Integrates Gemini API with web search and chemical engineering expertise
"""

import google.generativeai as genai
import streamlit as st
from typing import Optional, Dict, Any, List
import time
import re

from .prompts import get_chemE_prompt, SAFETY_KEYWORDS, CHEME_TERMS
from .utils import (
    clean_text, 
    categorize_question, 
    validate_input,
    format_response_for_display,
    log_interaction
)
from .search_engine import search_engine

class ChemEBot:
    """Main Chemical Engineering Bot Class"""
    
    def __init__(self, api_key: str):
        """
        Initialize the Chemical Engineering Bot
        
        Args:
            api_key (str): Gemini API key
        """
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.conversation_history = []
            self.is_initialized = True
            
        except Exception as e:
            st.error(f"Failed to initialize Gemini API: {e}")
            self.is_initialized = False

    def ask(self, question: str, include_web_search: bool = True) -> Dict[str, Any]:
        """
        Process a chemical engineering question
        
        Args:
            question (str): User's question
            include_web_search (bool): Whether to include web search context
            
        Returns:
            Dict: Response with answer, sources, and metadata
        """
        # Validate input
        is_valid, error_message = validate_input(question)
        if not is_valid:
            return {
                'answer': error_message,
                'sources': [],
                'question_type': 'error',
                'processing_time': 0
            }
        
        start_time = time.time()
        
        try:
            # Categorize question type
            question_type = categorize_question(question)
            
            # Get web search context if enabled
            web_context = ""
            sources = []
            
            if include_web_search:
                web_context = search_engine.get_relevant_context(question)
                if web_context:
                    # Extract sources from context (simplified)
                    sources = self._extract_sources_from_context(web_context)
            
            # Generate AI response
            ai_response = self._generate_ai_response(
                question=question,
                question_type=question_type,
                web_context=web_context
            )
            
            # Format response for display
            formatted_response = format_response_for_display(ai_response)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Log interaction
            log_interaction(question, ai_response, sources)
            
            # Store in conversation history
            self.conversation_history.append({
                'question': question,
                'answer': formatted_response,
                'question_type': question_type,
                'sources': sources,
                'timestamp': time.time()
            })
            
            return {
                'answer': formatted_response,
                'sources': sources,
                'question_type': question_type,
                'processing_time': processing_time,
                'web_context_used': bool(web_context)
            }
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error while processing your question: {str(e)}"
            
            return {
                'answer': error_response,
                'sources': [],
                'question_type': 'error',
                'processing_time': time.time() - start_time,
                'error': str(e)
            }

    def _generate_ai_response(self, question: str, question_type: str, web_context: str = "") -> str:
        """
        Generate AI response using Gemini API
        
        Args:
            question (str): User's question
            question_type (str): Categorized question type
            web_context (str): Context from web search
            
        Returns:
            str: AI-generated response
        """
        if not self.is_initialized:
            return "Sorry, the AI system is not properly initialized. Please check the API configuration."
        
        try:
            # Create specialized prompt
            prompt = get_chemE_prompt(
                question=question,
                question_type=question_type,
                search_context=web_context
            )
            
            # Generate response with safety settings
            response = self.model.generate_content(
                prompt,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            )
            
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response to your question. Please try rephrasing it or asking a different question."
                
        except Exception as e:
            return f"I encountered an error while generating the response: {str(e)}. Please try again."

    def _extract_sources_from_context(self, web_context: str) -> List[str]:
        """Extract source information from web context"""
        sources = []
        
        # Simple extraction based on "From [source]:" pattern
        source_pattern = r'From ([^:]+):'
        matches = re.findall(source_pattern, web_context)
        
        for match in matches:
            sources.append(match.strip())
        
        return list(set(sources))  # Remove duplicates

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_statistics(self) -> Dict[str, Any]:
        """Get bot usage statistics"""
        if not self.conversation_history:
            return {
                'total_questions': 0,
                'question_types': {},
                'average_response_time': 0
            }
        
        question_types = {}
        total_time = 0
        
        for conv in self.conversation_history:
            q_type = conv.get('question_type', 'unknown')
            question_types[q_type] = question_types.get(q_type, 0) + 1
        
        return {
            'total_questions': len(self.conversation_history),
            'question_types': question_types,
            'recent_questions': len([c for c in self.conversation_history if time.time() - c.get('timestamp', 0) < 3600])
        }

    def is_safety_related(self, question: str) -> bool:
        """Check if question is safety-related"""
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in SAFETY_KEYWORDS)

    def is_cheme_related(self, question: str) -> bool:
        """Check if question is chemical engineering related"""
        question_lower = question.lower()
        return any(term in question_lower for term in CHEME_TERMS)

    def suggest_related_topics(self, question: str) -> List[str]:
        """Suggest related topics based on the question"""
        suggestions = []
        question_lower = question.lower()
        
        # Topic-based suggestions
        topic_suggestions = {
            'distillation': ['McCabe-Thiele method', 'Raoult\'s law', 'VLE diagrams', 'Packed columns'],
            'reactor': ['CSTR design', 'PFR design', 'Reaction kinetics', 'Reactor sizing'],
            'heat exchanger': ['LMTD method', 'Heat transfer coefficients', 'Shell and tube design'],
            'safety': ['HAZOP analysis', 'Risk assessment', 'Safety systems', 'Emergency procedures'],
            'thermodynamics': ['Phase equilibria', 'Gibbs free energy', 'Enthalpy calculations']
        }
        
        for topic, related in topic_suggestions.items():
            if topic in question_lower:
                suggestions.extend(related[:2])  # Add top 2 suggestions
        
        return suggestions[:3]  # Return max 3 suggestions