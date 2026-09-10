#!/usr/bin/env python3
"""
Improved translation script for bestiary-MM with regex patterns
Process in multiple passes for safety
"""

import json
import re

def translate_text(text):
    """Translate text entry with careful regex-based replacements"""
    if not isinstance(text, str):
        return text
    
    result = text
    
    # CRITICAL: Protect special patterns first - don't translate inside @{}
    # This must be FIRST before any other translations
    placeholders = {}
    counter = [0]
    def add_placeholder(match):
        key = f"__PLACEHOLDER_{counter[0]}__"
        counter[0] += 1
        placeholders[key] = match.group(0)
        return key
    
    # Find all @{word ...} patterns and protect them
    result = re.sub(r'\{@[^}]+\}', add_placeholder, result)
    
    # ===== TRANSLATIONS START HERE =====
    
    # Pass 1: Distance conversions (most specific first)
    # Handle ranges like "30/120 feet" → "9 m / 36 m"
    # First, translate individual numbers with ft
    distance_ranges = [
        (r'\b30/120 feet\b', '9 m / 36 m'),
        (r'\b30/90 feet\b', '9 m / 27 m'),
        (r'\b30/60 feet\b', '9 m / 18 m'),
        (r'\b15/30 feet\b', '4,50 m / 9 m'),
        (r'\b10/20 feet\b', '3 m / 6 m'),
        (r'\b10/40 feet\b', '3 m / 12 m'),
        (r'\b5/15 feet\b', '1,50 m / 4,50 m'),
    ]
    for pattern, replacement in distance_ranges:
        result = re.sub(pattern, replacement, result)
    
    # Then regular distances
    replacements = [
        # Specific distances with "feet" - MUST come first for longer matches
        (r'\b30 feet\b', '9 m'),
        (r'\b60 feet\b', '18 m'),
        (r'\b120 feet\b', '36 m'),
        (r'\b90 feet\b', '27 m'),
        (r'\b50 feet\b', '15 m'),
        (r'\b40 feet\b', '12 m'),
        (r'\b150 feet\b', '45 m'),
        (r'\b300 feet\b', '90 m'),
        (r'\b20 feet\b', '6 m'),
        (r'\b25 feet\b', '7,50 m'),
        (r'\b15 feet\b', '4,50 m'),
        (r'\b10 feet\b', '3 m'),
        (r'\b5 feet\b', '1,50 m'),
        # Abbreviations (ft.) 
        (r'\b30 ft\.', '9 m'),
        (r'\b60 ft\.', '18 m'),
        (r'\b120 ft\.', '36 m'),
        (r'\b90 ft\.', '27 m'),
        (r'\b50 ft\.', '15 m'),
        (r'\b40 ft\.', '12 m'),
        (r'\b150 ft\.', '45 m'),
        (r'\b300 ft\.', '90 m'),
        (r'\b20 ft\.', '6 m'),
        (r'\b25 ft\.', '7,50 m'),
        (r'\b15 ft\.', '4,50 m'),
        (r'\b10 ft\.', '3 m'),
        (r'\b5 ft\.', '1,50 m'),
    ]
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result)
    
    # Pass 2: Basic connecting words
    connectors = [
        (r'\bor\b', 'ou'),
        (r'\band\b', 'et'),
        (r'\bIf\b', 'Si'),
    ]
    for pattern, replacement in connectors:
        result = re.sub(pattern, replacement, result)
    
    # Pass 2: Basic terms
    terms = [
        (r'\bto hit\b', 'pour toucher'),
        (r'\breach\b', 'allonge'),
        (r'\brange\b', 'portée'),
        (r'\bone target\b', 'une cible'),
        (r'\bone creature\b', 'une créature'),
    ]
    for pattern, replacement in terms:
        result = re.sub(pattern, replacement, result)
    
    # Pass 3: Damage types - only replace standalone
    damage_types = [
        (r'\bslashing damage\b', 'dégâts tranchants'),
        (r'\bpiercing damage\b', 'dégats perforants'),
        (r'\bbludgeoning damage\b', 'dégats contondants'),
        (r'\bfire damage\b', 'dégats de feu'),
        (r'\bcold damage\b', 'dégats de froid'),
        (r'\blightning damage\b', "dégats d'électricité"),
    ]
    for pattern, replacement in damage_types:
        result = re.sub(pattern, replacement, result)
    
    # Pass 4: Conditions
    conditions = [
        (r'\bcharmed\b', 'charmé'),
        (r'\bprone\b', 'à terre'),
        (r'\bparalyzed\b', 'paralysé'),
    ]
    for pattern, replacement in conditions:
        result = re.sub(pattern, replacement, result)
    
    # Pass 5: Saving throws
    saves = [
        (r'Constitution saving throw', 'jet de sauvegarde CON'),
        (r'Wisdom saving throw', 'jet de sauvegarde SAG'),
    ]
    for pattern, replacement in saves:
        result = re.sub(pattern, replacement, result)
    
    # Pass 6: Vision
    vision_terms = [
        (r'\bdarkvision\b', 'vision dans le noir'),
        (r'\bblindsight\b', 'vision aveugle'),
    ]
    for pattern, replacement in vision_terms:
        result = re.sub(pattern, replacement, result)
    
    # Restore placeholders
    for key, value in placeholders.items():
        result = result.replace(key, value)
    
    return result

def translate_entry(entry):
    """Translate a single entry (can be string or dict)"""
    if isinstance(entry, str):
        return translate_text(entry)
    elif isinstance(entry, dict):
        result = dict(entry)
        if 'entries' in result:
            result['entries'] = [translate_entry(e) for e in result['entries']]
        if 'name' in result:
            result['name'] = translate_text(result['name'])
        return result
    elif isinstance(entry, list):
        return [translate_entry(e) for e in entry]
    return entry

def translate_monster(monster):
    """Translate a monster"""
    result = dict(monster)
    
    # Translate environment
    if 'environment' in result and result['environment']:
        env_trans = {
            'mountain': 'montagne',
            'underdark': 'souterrain',
            'forest': 'forêt',
            'swamp': 'marais',
            'desert': 'désert',
            'coastal': 'côte',
            'hill': 'colline',
            'cave': 'caverne',
            'urban': 'ville',
            'grassland': 'plaine',
            'arctic': 'arctique',
        }
        result['environment'] = [env_trans.get(e, e) for e in result['environment']]
    
    # Translate type
    if 'type' in result:
        t = result['type']
        if isinstance(t, str):
            translations = {'humanoid': 'humanoïde'}
            result['type'] = translations.get(t, t)
        elif isinstance(t, dict) and 'type' in t:
            translations = {'humanoid': 'humanoïde'}
            new_type = translations.get(t['type'], t['type'])
            result['type'] = {'type': new_type}
            if 'tags' in t:
                result['type']['tags'] = t['tags']
    
    # Translate trait names
    if 'trait' in result and result['trait']:
        trait_trans = {
            'Multiattack': 'Attaque multiple',
            'Dive Attack': 'Attaque en piqué',
            'Keen Smell': 'Odorat fin',
            'Keen Senses': 'Sens aiguisés',
        }
        new_traits = []
        for t in result['trait']:
            if isinstance(t, dict):
                new_t = dict(t)
                if 'name' in new_t:
                    new_t['name'] = trait_trans.get(new_t['name'], new_t['name'])
                if 'entries' in new_t:
                    new_t['entries'] = [translate_entry(e) for e in new_t['entries']]
                new_traits.append(new_t)
            else:
                new_traits.append(t)
        result['trait'] = new_traits
    
    # Translate action names
    if 'action' in result and result['action']:
        action_trans = {
            'Multiattack': 'Attaque multiple',
            'Talon': 'Griffe',
            'Javelin': 'Javelot',
            'Bite': 'Morsure',
            'Claw': 'Griffe',
            'Tail': 'Queue',
            'Slam': 'Coup',
        }
        new_actions = []
        for a in result['action']:
            if isinstance(a, dict):
                new_a = dict(a)
                if 'name' in new_a:
                    new_a['name'] = action_trans.get(new_a['name'], new_a['name'])
                if 'entries' in new_a:
                    new_a['entries'] = [translate_entry(e) for e in new_a['entries']]
                new_actions.append(new_a)
            else:
                new_actions.append(a)
        result['action'] = new_actions
    
    # Translate legendary
    if 'legendary' in result and result['legendary']:
        result['legendary'] = [translate_entry(l) for l in result['legendary']]
    
    return result

def main():
    input_file = 'bestiary-mm.json'
    output_file = 'bestiary-mm.json'
    
    # Load data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Translate each monster
    if 'monster' in data:
        translated = [translate_monster(m) for m in data['monster']]
        data['monster'] = translated
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='\t', ensure_ascii=False)
    
    print(f"Terminé! {len(data.get('monster', []))} créatures traduites")

if __name__ == '__main__':
    main()