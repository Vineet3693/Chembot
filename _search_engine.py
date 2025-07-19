
"""
Web Search Engine for Chemical Engineering Content
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any
from urllib.parse import quote_plus, urljoin
import re
from .utils import clean_text, get_source_priority_score

class ChemESearchEngine:
    """Chemical Engineering focused web search engine"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Preferred domains for chemical engineering content
        self.preferred_domains = [
            'en.wikipedia.org',
            'aiche.org',
            'nist.gov',
            'epa.gov',
            'osha.gov',
            'engineeringtoolbox.com',
            'chemguide.co.uk',
            'khanacademy.org'
        ]
        
        self.max_results = 5
        self.timeout = 10

    def search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the web for chemical engineering content
        
        Args:
            query (str): Search query
            
        Returns:
            List[Dict]: Search results with title, url, snippet
        """
        try:
            # Add chemical engineering context to query
            enhanced_query = f"{query} chemical engineering"
            
            # Use web scraping approach (since no API key required)
            return self._scrape_search_results(enhanced_query)
            
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def _scrape_search_results(self, query: str) -> List[Dict[str, Any]]:
        """
        Scrape search results from web search
        
        Args:
            query (str): Search query
            
        Returns:
            List[Dict]: Search results
        """
        results = []
        
        try:
            # Search multiple sources
            sources = [
                self._search_wikipedia(query),
                self._search_educational_sites(query)
            ]
            
            # Combine and deduplicate results
            for source_results in sources:
                results.extend(source_results)
            
            # Remove duplicates and sort by relevance
            unique_results = self._deduplicate_results(results)
            return unique_results[:self.max_results]
            
        except Exception as e:
            print(f"Scraping error: {e}")
            return []

    def _search_wikipedia(self, query: str) -> List[Dict[str, Any]]:
        """Search Wikipedia for chemical engineering content"""
        results = []
        
        try:
            # Wikipedia API search
            wiki_api = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            
            # Try direct page lookup first
            search_terms = [
                query.replace(' ', '_'),
                f"Chemical_{query.replace(' ', '_')}",
                f"{query.replace(' ', '_')}_engineering"
            ]
            
            for term in search_terms[:2]:  # Limit attempts
                try:
                    response = self.session.get(
                        f"{wiki_api}{term}", 
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        results.append({
                            'title': data.get('title', ''),
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            'snippet': data.get('extract', ''),
                            'source': 'Wikipedia',
                            'priority': 8
                        })
                        break
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            
        return results

    def _search_educational_sites(self, query: str) -> List[Dict[str, Any]]:
        """Search educational websites for content"""
        results = []
        
        # Predefined educational content for common ChemE topics
        educational_content = {
            'distillation': {
                'title': 'Distillation - Chemical Engineering',
                'url': 'https://en.wikipedia.org/wiki/Distillation',
                'snippet': 'Distillation is a separation process that exploits differences in volatility of components in a liquid mixture.',
                'source': 'Educational',
                'priority': 7
            },
            'reactor': {
                'title': 'Chemical Reactor Design',
                'url': 'https://en.wikipedia.org/wiki/Chemical_reactor',
                'snippet': 'A chemical reactor is an enclosed volume in which a chemical reaction takes place.',
                'source': 'Educational', 
                'priority': 7
            },
            'heat exchanger': {
                'title': 'Heat Exchanger Design',
                'url': 'https://en.wikipedia.org/wiki/Heat_exchanger',
                'snippet': 'A heat exchanger is a system used to transfer heat between two or more fluids.',
                'source': 'Educational',
                'priority': 7
            }
        }
        
        # Check if query matches any predefined content
        query_lower = query.lower()
        for topic, content in educational_content.items():
            if topic in query_lower:
                results.append(content)
        
        return results

    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results and sort by priority"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        # Sort by priority score
        return sorted(unique_results, key=lambda x: x.get('priority', 0), reverse=True)

    def extract_content_from_url(self, url: str) -> str:
        """
        Extract text content from a URL
        
        Args:
            url (str): URL to extract content from
            
        Returns:
            str: Extracted text content
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean and limit text
            cleaned_text = clean_text(text)
            
            # Limit to first 1000 characters for context
            return cleaned_text[:1000] + "..." if len(cleaned_text) > 1000 else cleaned_text
            
        except Exception as e:
            print(f"Content extraction error for {url}: {e}")
            return ""

    def get_relevant_context(self, query: str) -> str:
        """
        Get relevant context from web search
        
        Args:
            query (str): User's question/query
            
        Returns:
            str: Relevant context from web sources
        """
        try:
            # Search for relevant content
            search_results = self.search_web(query)
            
            if not search_results:
                return ""
            
            # Combine snippets from top results
            context_parts = []
            for result in search_results[:3]:  # Use top 3 results
                snippet = result.get('snippet', '')
                if snippet:
                    source = result.get('source', 'Web')
                    context_parts.append(f"From {source}: {snippet}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"Context extraction error: {e}")
            return ""

# Create global instance
search_engine = ChemESearchEngine()