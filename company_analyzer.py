"""
Company Role Analyzer Module
Input: Resume skills, experience years
Output: Matched company roles with scores
"""

import json
from pathlib import Path

class CompanyAnalyzer:
    def __init__(self):
        """Load company database"""
        self.data_path = Path(__file__).parent / 'data' / 'company_roles_db.json'
        with open(self.data_path, 'r') as f:
            data = json.load(f)
            self.companies = {c['name']: c for c in data['companies']}
    
    def get_all_companies(self):
        """Return list of all companies"""
        return list(self.companies.keys())
    
    def get_experience_level(self, years):
        """Convert years to level"""
        if years < 2:
            return "Entry Level"
        elif years < 5:
            return "Mid Level"
        else:
            return "Advanced"
    
    def calculate_match(self, resume_skills, required_skills):
        """Calculate skill match percentage"""
        if not required_skills:
            return 0
        
        resume_lower = [s.lower() for s in resume_skills]
        required_lower = [s.lower() for s in required_skills]
        
        matches = sum(1 for req in required_lower 
                     if any(req in res for res in resume_lower))
        
        return (matches / len(required_skills)) * 100
    
    def analyze_for_company(self, resume_skills, experience_years, company_name=None):
        """
        Analyze resume against companies
        
        Args:
            resume_skills: list of skills from resume
            experience_years: float
            company_name: optional specific company
        
        Returns:
            dict with matched roles
        """
        user_level = self.get_experience_level(experience_years)
        
        if company_name and company_name != "All Companies":
            # Analyze single company
            company = self.companies.get(company_name)
            if not company:
                return {"error": "Company not found"}
            
            results = []
            for role in company['roles']:
                skill_match = self.calculate_match(resume_skills, role['required_skills'])
                level_match = (role['level'] == user_level)
                
                overall = skill_match
                if level_match:
                    overall += 20
                
                results.append({
                    'title': role['title'],
                    'level': role['level'],
                    'skill_match': round(skill_match, 1),
                    'overall_match': round(min(overall, 100), 1),
                    'missing_skills': [s for s in role['required_skills'] 
                                     if s.lower() not in [r.lower() for r in resume_skills]][:5]
                })
            
            results.sort(key=lambda x: x['overall_match'], reverse=True)
            return {
                'company': company_name,
                'user_level': user_level,
                'matches': results[:5]
            }
        
        else:
            # Compare all companies
            all_results = []
            for comp_name, company in self.companies.items():
                best_match = None
                best_score = 0
                
                for role in company['roles']:
                    skill_match = self.calculate_match(resume_skills, role['required_skills'])
                    level_match = (role['level'] == user_level)
                    
                    overall = skill_match
                    if level_match:
                        overall += 20
                    
                    if overall > best_score:
                        best_score = overall
                        best_match = {
                            'title': role['title'],
                            'skill_match': round(skill_match, 1),
                            'overall_match': round(min(overall, 100), 1),
                            'missing_skills': [s for s in role['required_skills'] 
                                             if s.lower() not in [r.lower() for r in resume_skills]][:3]
                        }
                
                if best_match:
                    all_results.append({
                        'company': comp_name,
                        'best_role': best_match['title'],
                        'match_score': best_match['overall_match'],
                        'details': best_match
                    })
            
            all_results.sort(key=lambda x: x['match_score'], reverse=True)
            return all_results


# Create single instance for import
analyzer = CompanyAnalyzer()

def get_company_matches(resume_skills, experience_years, company_name=None):
    """Public function to be imported by app.py"""
    return analyzer.analyze_for_company(resume_skills, experience_years, company_name)