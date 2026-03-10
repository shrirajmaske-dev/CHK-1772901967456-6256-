import json
from pathlib import Path

# Load company data
with open('data/company_roles_db.json', 'r') as f:
    data = json.load(f)

# Your resume skills (replace with your actual skills)
my_skills = [
    'Python', 'Java', 'JavaScript', 'React', 'SQL', 
    'AWS', 'Docker', 'Git', 'Data Structures',
    'Machine Learning', 'Communication'
]

my_experience = 3  # years
my_level = "Mid Level" if my_experience < 5 else "Advanced"

print("📊 YOUR PROFILE")
print(f"Experience: {my_experience} years ({my_level})")
print(f"Skills: {', '.join(my_skills[:10])}")
print("\n" + "="*60)

def calculate_match(my_skills, required_skills):
    matches = sum(1 for s in required_skills if s in my_skills)
    return (matches / len(required_skills)) * 100 if required_skills else 0

# Analyze each company
all_results = []

for company in data['companies']:
    print(f"\n🏢 {company['name']}")
    print("-"*40)
    
    for role in company['roles']:
        skill_match = calculate_match(my_skills, role['required_skills'])
        level_match = (role['level'] == my_level)
        
        overall = skill_match
        if level_match:
            overall += 20
        
        missing = [s for s in role['required_skills'] if s not in my_skills]
        
        if overall >= 50:  # Show only good matches
            print(f"\n  📍 {role['title']}")
            print(f"     Match: {overall:.1f}%")
            print(f"     Skills: {skill_match:.1f}%")
            if missing:
                print(f"     Need: {', '.join(missing[:3])}")
    
    # Store best match
    best_match = max(company['roles'], 
                    key=lambda r: calculate_match(my_skills, r['required_skills']) + 
                                 (20 if r['level'] == my_level else 0))
    
    best_score = calculate_match(my_skills, best_match['required_skills'])
    if best_match['level'] == my_level:
        best_score += 20
    
    all_results.append({
        'company': company['name'],
        'role': best_match['title'],
        'score': best_score
    })

print("\n" + "="*60)
print("🏆 BEST COMPANY FOR YOU")
print("="*60)

all_results.sort(key=lambda x: x['score'], reverse=True)
print(f"\n🥇 {all_results[0]['company']} - {all_results[0]['role']} ({all_results[0]['score']:.1f}%)")
print(f"🥈 {all_results[1]['company']} - {all_results[1]['role']} ({all_results[1]['score']:.1f}%)")
print(f"🥉 {all_results[2]['company']} - {all_results[2]['role']} ({all_results[2]['score']:.1f}%)")