#!/usr/bin/env python3
"""
Translation script for bestiary entries (descriptions)
"""

import json
import re
import os

# Translation dictionary for entries
TRANSLATIONS = {
    # Distance - various patterns
    " feet ": " mètres ",
    " feet.": " mètres.",
    " feet,": " mètres,",
    " foot ": " mètre ",
    " foot.": " mètre.",
    " ft.": " m",
    " ft,": " m,",
    
    # Specific distances
    "30 ft.": "9 m",
    "30 ft,": "9 m",
    "5 ft.": "1,50 m",
    "5 ft,": "1,50 m",
    "10 ft.": "3 m",
    "10 ft,": "3 m",
    "15 ft.": "4,50 m",
    "15 ft,": "4,50 m",
    "20 ft.": "6 m",
    "20 ft,": "6 m",
    "25 ft.": "7,50 m",
    "25 ft,": "7,50 m",
    "40 ft.": "12 m",
    "40 ft,": "12 m",
    "50 ft.": "15 m",
    "50 ft,": "15 m",
    "60 ft.": "18 m",
    "60 ft,": "18 m",
    "90 ft.": "27 m",
    "90 ft,": "27 m",
    "120 ft.": "36 m",
    "120 ft,": "36 m",
    "150 ft.": "45 m",
    "150 ft,": "45 m",
    "300 ft.": "90 m",
    "300 ft,": "90 m",
    "600 ft.": "180 m",
    
    # Vision
    "darkvision": "vision dans le noir",
    "blindsight": "vision aveugle",
    "truesight": "vue parfaite",
    
    # Basic terms
    " to hit": " pour toucher",
    " to hit,": " pour toucher,",
    " reach ": " allonge ",
    " reach,": " allonge,",
    " reach.": " allonge.",
    " range ": " portée ",
    " range,": " portées,",
    " range.": " portée.",
    " one target": " une cible",
    " one target.": " une cible.",
    " one creature": " une créature",
    " one creature.": " une créature.",
    "a creature": "une créature",
    "Hit ": "Touché ",
    " Hit ": " Touché ",
    " hit": "touché",
    " damage": "dégâts",
    "damage": "dégât",
    "Hitpoints": "points de vie",
    "hit points": "points de vie",
    
    # Damage types
    " slashing damage": " dégâts tranchants",
    " piercing damage": " dégats perforants",
    " bludgeoning damage": " dégâts contondants",
    " fire damage": " dégats de feu",
    " cold damage": " dégats de froid",
    " lightning damage": " dégats d'électricité",
    " acid damage": " dégats d'acide",
    " poison damage": " dégats de poison",
    " psychic damage": " dégats psychiques",
    " necrotic damage": " dégats nécrotiques",
    " radiant damage": " dégats radiants",
    " thunder damage": " dégats de tonnerre",
    " force damage": " dégats de force",
    
    # Conditions
    "charmed": "charmé",
    "frightened": "effrayé",
    "paralyzed": "paralysé",
    "petrified": "pétrifié",
    "poisoned": "empoisonné",
    "prone": "à terre",
    "grappled": "agrippé",
    "restrained": "entravé",
    "unconscious": "inconscient",
    "stunned": "étourdi",
    "blinded": "aveuglé",
    "deafened": "sourd",
    "invisible": "invisible",
    "incapacitated": "incapacité",
    "diseased": "malade",
    "exhaustion": "épuisement",
    "frightened": "effrayé",
    
    # Saving throws
    "Constitution saving throw": "jet de sauvegarde Constitution",
    "Constitution saving throw.": "jet de sauvegarde Constitution.",
    " Wisdom saving throw": "jet de sauvegarde Sagesse",
    " Wisdom saving throw.": "jet de sauvegarde Sagesse.",
    "Dexterity saving throw": "jet de sauvegarde Dextérité",
    "Dexterity saving throw.": "jet de sauvegarde Dextérité.",
    "Strength saving throw": "jet de sauvegarde Force",
    "Strength saving throw.": "jet de sauvegarde Force.",
    "Intelligence saving throw": "jet de sauvegarde Intelligence",
    "Intelligence saving throw.": "jet de sauvegarde Intelligence.",
    "Charisma saving throw": "jet de sauvegarde Charisme",
    "Charisma saving throw.": "jet de sauvegarde Charisme.",
    "DC ": "DD ",
    "{@dc ": "{@dd ",
    
    # Other terms
    " CON": " CON",
    " WIS": " SAG",
    " DEX": " DEX",
    " STR": " FOR",
    " INT": " INT",
    " CHA": " CHA",
    " CON,": " CON,",
    " WIS,": " SAG,",
    " DEX,": " DEX,",
    " STR,": " FOR,",
    " INT,": " INT,",
    " CHA,": " CHA,",
    "Constitution": "Constitution",
    "Wisdom": "Sagesse",
    "Dexterity": "Dextérité",
    "Strength": "Force",
    "Intelligence": "Intelligence",
    "Charisma": "Charisme",
    "Perception": "Perception",
    "Stealth": "Discrétion",
    "Athletics": "Athlétisme",
    "Acrobatics": "Acrobaties",
    "Survival": "Survie",
    "Medicine": "Médecine",
    "Insight": "Perspicacité",
    "Investigation": "Investigation",
    "History": "Histoire",
    "Performance": "Représentation",
    "Persuasion": "Persuasion",
    "Deception": "Tromperie",
    "Intimidation": "Intimidation",
    "Nature": "Nature",
    "Religion": "Religion",
    "Arcana": "Arcanes",
    "{@skill Perception}": "{@skill Perception}",
    "{@skill Perception": "{@skill Perception",
    "{@skill": "{@skill",
    "Skill": "Compétence",
    
    # Spell references
    "{@spell fireball}": "{@spell fireball}",
    "{@spell lightning bolt}": "{@spell lightning bolt}",
    "{@spell cure wounds}": "{@spell cure wounds}",
    "{@spell heal}": "{@spell heal}",
    "{@spell hold person}": "{@spell hold person}",
    "{@spell sleep}": "{@spell sleep}",
    "{@spell misty step}": "{@spell misty step}",
    
    # Creature references  
    "{@creature air elemental}": "{@creature élémentaire de l'air}",
    "{@creature fire elemental}": "{@creature élémentaire de feu}",
    "{@creature water elemental}": "{@creature élémentaire d'eau}",
    "{@creature earth elemental}": "{@creature élémentaire de terre}",
    
    # Time
    " 1 hour": " 1 heure",
    "1 hour": "1 heure",
    "1 minute": "1 minute",
    "1 minute.": "1 minute.",
    "1 round": "1 tour",
    "10 minutes": "10 minutes",
    "24 hours": "24 heures",
    "1 mile": "480 mètres",
    "miles": "kilomètres",
    
    # Other
    "the end of its next turn": "la fin de son prochain tour",
    "the creature": "la créature",
    "the target": "la cible",
    "If the": "Si ",
    "when": "lorsque",
    "as if": "comme si",
    "can take": "peut faire",
    "must make": "doit faire",
    "must succeed": "doit réussir",
    "has disadvantage": "désavantage",
    "has advantage": "avantage",
    "on attack rolls": "aux jets d'attaque",
    "on ability checks": "aux tests de caractéristique",
    "on saving throws": "aux jets de sauvegarde",
    "Melee Weapon Attack": "Attaque d'arme de mêlée",
    "Ranged Weapon Attack": "Attaque d'arme à distance",
}

def translate_entry(text):
    """Translate a single entry text"""
    if not isinstance(text, str):
        return text
    
    result = text
    
    # Apply all translations
    for english, french in TRANSLATIONS.items():
        result = result.replace(english, french)
    
    return result

def translate_entries(entries):
    """Translate list of entries"""
    if not isinstance(entries, list):
        return entries
    
    result = []
    for e in entries:
        if isinstance(e, str):
            result.append(translate_entry(e))
        elif isinstance(e, dict):
            # Recursively translate nested entries
            new_dict = dict(e)
            if 'entries' in new_dict:
                new_dict['entries'] = translate_entries(new_dict['entries'])
            result.append(new_dict)
        else:
            result.append(e)
    
    return result

def translate_monster(monster):
    """Translate all entries for a monster"""
    result = dict(monster)
    
    # Translate traits
    if 'trait' in monster and monster.get('trait'):
        new_traits = []
        for trait in monster['trait']:
            if isinstance(trait, dict):
                new_trait = dict(trait)
                if 'entries' in new_trait:
                    new_trait['entries'] = translate_entries(new_trait['entries'])
                new_traits.append(new_trait)
            else:
                new_traits.append(trait)
        result['trait'] = new_traits
    
    # Translate actions
    if 'action' in monster and monster.get('action'):
        new_actions = []
        for action in monster['action']:
            if isinstance(action, dict):
                new_action = dict(action)
                if 'entries' in new_action:
                    new_action['entries'] = translate_entries(new_action['entries'])
                new_actions.append(new_action)
            else:
                new_actions.append(action)
        result['action'] = new_actions
    
    # Translate legendary actions
    if 'legendary' in monster and monster.get('legendary'):
        new_legendary = []
        for leg in monster['legendary']:
            if isinstance(leg, dict):
                new_leg = dict(leg)
                if 'entries' in new_leg:
                    new_leg['entries'] = translate_entries(new_leg['entries'])
                new_legendary.append(new_leg)
            else:
                new_legendary.append(leg)
        result['legendary'] = new_legendary
    
    return result

def process_file(filepath):
    """Process a single bestiary file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'monster' in data:
        new_monsters = []
        for m in data['monster']:
            new_monsters.append(translate_monster(m))
        data['monster'] = new_monsters
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='\t', ensure_ascii=False)
    
    print(f"Traité: {filepath}")

def main():
    """Main entry point"""
    for f in os.listdir('.'):
        if f.startswith('bestiary-') and f.endswith('.json'):
            try:
                process_file(f)
            except Exception as e:
                print(f"Erreur {f}: {e}")
    
    print("Terminé!")

if __name__ == '__main__':
    main()