#!/usr/bin/env python3
"""
Script de traduction automatique du bestiaire français
Utilise glossary.json pour les traductions de termes récurrents
"""

import json
import os
import re

# Charger le glossaire
with open('glossary.json', 'r', encoding='utf-8') as f:
    GLOSSARY = json.load(f)

def translate_environment(env_list):
    """Traduit les environnements"""
    if not isinstance(env_list, list):
        return env_list
    translated = []
    for env in env_list:
        if env in GLOSSARY.get('environments', {}):
            translated.append(GLOSSARY['environments'][env])
        else:
            translated.append(env)
    return translated

def translate_creature_type(creature_type):
    """Traduit le type de créature"""
    if isinstance(creature_type, str):
        return GLOSSARY.get('creature_types', {}).get(creature_type, creature_type)
    elif isinstance(creature_type, dict):
        new_type = creature_type.get('type', '')
        if isinstance(new_type, str):
            translated_type = GLOSSARY.get('creature_types', {}).get(new_type, new_type)
            new_dict = {'type': translated_type}
            if 'tags' in creature_type:
                new_dict['tags'] = creature_type['tags']
            return new_dict
    return creature_type

def translate_trait_name(name):
    """Traduit les noms de capacités"""
    return GLOSSARY.get('traits', {}).get(name, name)

def translate_action_name(name):
    """Traduit les noms d'actions"""
    return GLOSSARY.get('actions', {}).get(name, name)

def translate_legendary_name(name):
    """Traduit les noms d'actions légendaires"""
    return GLOSSARY.get('legendary', {}).get(name, name)

def process_monster(monster):
    """Traite une créature individuelle"""
    result = dict(monster)
    
    # Traduire l'environnement
    if 'environment' in monster and monster.get('environment'):
        result['environment'] = translate_environment(monster['environment'])
    
    # Traduire le type
    if 'type' in monster:
        result['type'] = translate_creature_type(monster['type'])
    
    # Traduire les traits
    if 'trait' in monster and monster.get('trait'):
        new_traits = []
        for trait in monster['trait']:
            if isinstance(trait, dict) and 'name' in trait:
                new_trait = dict(trait)
                new_trait['name'] = translate_trait_name(trait['name'])
                new_traits.append(new_trait)
            else:
                new_traits.append(trait)
        result['trait'] = new_traits
    
    # Traduire les actions
    if 'action' in monster and monster.get('action'):
        new_actions = []
        for action in monster['action']:
            if isinstance(action, dict) and 'name' in action:
                new_action = dict(action)
                new_action['name'] = translate_action_name(action['name'])
                new_actions.append(new_action)
            else:
                new_actions.append(action)
        result['action'] = new_actions
    
    # Traduire les actions légendaires
    if 'legendary' in monster and monster.get('legendary'):
        new_legendary = []
        for leg in monster['legendary']:
            if isinstance(leg, dict) and 'name' in leg:
                new_leg = dict(leg)
                new_leg['name'] = translate_legendary_name(leg['name'])
                new_legendary.append(new_leg)
            else:
                new_legendary.append(leg)
        result['legendary'] = new_legendary
    
    return result

def process_bestiary_file(filepath):
    """Traite un fichier bestiary complet"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'monster' in data:
        new_monsters = []
        for m in data['monster']:
            new_monsters.append(process_monster(m))
        data['monster'] = new_monsters
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='\t', ensure_ascii=False)
    
    print(f"Traité: {filepath}")

def main():
    """Point d'entrée principal"""
    bestiary_dir = '.'
    
    # Traiter tous les fichiers bestiary-*.json
    for f in os.listdir(bestiary_dir):
        if f.startswith('bestiary-') and f.endswith('.json'):
            process_bestiary_file(f)
    
    print("Terminé!")

if __name__ == '__main__':
    main()