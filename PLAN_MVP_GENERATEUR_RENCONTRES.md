# 📋 PLAN FINAL MVP - Générateur de Rencontres D&D 5e

**Date** : 2026-05-08  
**Status** : Planification complète  
**Version** : 1.0

---

## 🎯 Vue d'ensemble

Création d'une **application web moderne** pour générer des rencontres D&D 5e équilibrées en filtrant un bestiaire de ~4500 créatures traduites en français. 

**Tech Stack** :
- Framework : Astro (Static + Islands)
- Interactivité : Alpine.js
- Styling : CSS moderne
- Données : JSON bundlés statiquement (~4500 créatures)
- Hébergement : VPS personnel
- Export : JSON complet (rencontres sauvegardées)

**Public cible** : Meneur de jeu D&D 5e francophones

---

## 📦 Stack Technique

### Framework & Runtime
- **Astro** : Static Site Generator avec Islands Architecture
  - Meilleure performance (HTML précompilé)
  - Progressive enhancement avec Alpine.js
  - Déploiement statique simple

- **Alpine.js** : Framework léger (15kb)
  - Interactivité minimale (filtres, générateur)
  - Parfait pour Islands pattern
  - Pas de build step complexe

### Styling & UI
- **CSS moderne** (custom + optionnel Tailwind)
- Variables CSS pour thème/theming
- Design system cohérent
- Support dark mode

### Build & Dev
- Node.js >= 24
- npm pour dépendances
- ESLint + Prettier (optionnel)
- TypeScript pour typage

### Données & Storage
- JSON 5etools du repo existant (/data-fr/bestiary)
- LocalStorage pour sauvegarde rencontres
- Export JSON en standard

### Déploiement
- VPS personnel
- Astro static build
- GitHub Actions ou manuel

---

## 🏗️ Architecture Détaillée

### Structure des Dossiers

```
encounter-generator/
├── src/
│   ├── components/
│   │   ├── Islands/
│   │   │   ├── FilterPanel.astro           # Island #1 - Filtrage
│   │   │   ├── EncounterGenerator.astro    # Island #2 - Générateur
│   │   │   ├── SavedEncounters.astro       # Island #3 - Sauvegarde
│   │   │   └── ExportPanel.astro           # Island #4 - Export
│   │   └── Common/
│   │       ├── StatBlock.astro             # Affichage créatures
│   │       ├── Navigation.astro
│   │       ├── Footer.astro
│   │       └── Header.astro
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── GeneratorLayout.astro
│   ├── pages/
│   │   ├── index.astro                     # Accueil
│   │   ├── generator.astro                 # Page principale
│   │   ├── bestiary.astro                  # Liste créatures
│   │   └── creature/[id].astro             # Fiche créature
│   ├── lib/
│   │   ├── creatures.ts                    # Loader données
│   │   ├── filters.ts                      # Logique filtrage
│   │   ├── encounter.ts                    # Calcul rencontres
│   │   ├── storage.ts                      # LocalStorage wrapper
│   │   ├── export.ts                       # Export JSON
│   │   └── types.ts                        # TypeScript interfaces
│   ├── styles/
│   │   ├── global.css                      # Reset + variables
│   │   ├── components.css                  # Styles composants
│   │   └── stat-block.css                  # Styles stat blocks
│   └── data/
│       └── bestiary/                       # JSON 5etools-src-fr
├── public/
│   └── assets/                             # Images, icônes
├── astro.config.mjs                        # Config Astro
├── tsconfig.json                           # Config TypeScript
├── package.json
├── .prettierrc
├── .eslintrc
└── README.md
```

---

## 🎯 PHASES D'IMPLÉMENTATION

### **Phase 1 : Infrastructure & Setup** (45 min)

**Objectif** : Créer une base Astro solide et fonctionnelle

#### Tâches

1. **Créer projet Astro**
   ```bash
   npm create astro@latest encounter-generator
   # Template: minimal ou blank
   # TypeScript: yes
   ```

2. **Configurer Astro pour Islands**
   - `astro.config.mjs` :
     ```javascript
     export default defineConfig({
       integrations: [alpineIntegration()],
       output: 'static',
     });
     ```

3. **Installer dépendances**
   - Alpine.js
   - TypeScript utilities
   - Dev tools (prettier, eslint)

4. **Importer données bestiaire**
   - Copier `/data-fr/bestiary` depuis repo 5etools-src-fr
   - Ou configurer comme monorepo/symlink

5. **Setup structure CSS**
   - Reset CSS
   - Variables CSS (couleurs, spacing, fonts)
   - Grid/layout de base

6. **Vérifier build & dev**
   ```bash
   npm run dev      # Serveur local
   npm run build    # Build production
   ```

#### Livrables

- ✅ Projet Astro initialisé et opérationnel
- ✅ Astro.config.mjs configuré (Islands, Alpine.js)
- ✅ Structure CSS de base
- ✅ Données bestiaire importées et accessible
- ✅ Dev server fonctionne

#### ⏱️ Temps estimé : 45 min

---

### **Phase 2 : Modèle de Données & Parseur** (1-2h)

**Objectif** : Créer abstraction data robuste et performante

#### 2.1 - TypeScript Types (`src/lib/types.ts`)

```typescript
// Structure d'une créature complète
interface Creature {
  // Identité
  name: string;
  source: string;
  page?: number;
  
  // Classification
  type: string;              // "Dragon", "Humanoid", etc.
  size: string;              // "Small", "Medium", etc.
  alignment: string;
  
  // Combat
  ac: AC[];                   // { ac: 15, from: "leather" }
  hp: HP;                     // { average: 27, formula: "5d8+5" }
  speed: Record<string, number>; // { walk: 30, fly: 60 }
  
  // Capacités
  abilityScores: AbilityScores;  // { str: 18, dex: 14, ... }
  savingThrows?: Record<string, number>;
  skills?: Record<string, number>;
  
  // Résistances et immunités
  damageResistances?: string[];
  damageImmunities?: string[];
  conditionImmunities?: string[];
  
  // Senses
  senses: Record<string, string>;
  languages: string[];
  
  // Challenge
  cr: number;                // Challenge Rating
  
  // Capacités spéciales
  traits?: Trait[];          // Traits spéciaux
  actions?: Action[];        // Actions
  legendaryActions?: Action[];
  spellcasting?: Spellcasting[];
}

interface Trait {
  name: string;
  text: string;
}

interface Action extends Trait {
  // Optionnel : attack details
  attack?: Attack;
}

interface Spellcasting {
  type: string;
  dc?: number;
  modifier?: number;
  spells: Spell[];
}

// Critères de filtrage
interface FilterCriteria {
  types: string[];           // Types sélectionnés
  crRange: [number, number]; // Min/max CR
  sizes: string[];           // Tailles sélectionnées
  hasFlying: boolean;
  hasSwimming: boolean;
  hasSpellcasting: boolean;
  alignments?: string[];
}

// Rencontre générée
interface Encounter {
  id: string;
  name: string;
  creatures: EncounterCreature[]; // Créatures + quantité
  partyLevel: number;
  partySize: number;
  difficulty: 'easy' | 'medium' | 'hard' | 'deadly';
  totalXP: number;
  adjustedXP: number;
  createdAt: Date;
  notes: string;
}

interface EncounterCreature {
  creature: Creature;
  quantity: number;
}

// Export JSON
interface ExportedEncounter {
  metadata: {
    name: string;
    partyLevel: number;
    partySize: number;
    difficulty: string;
    createdAt: string;
  };
  creatures: {
    name: string;
    source: string;
    quantity: number;
    statBlock: Creature;
  }[];
  notes: string;
  xp: {
    total: number;
    adjusted: number;
  };
}
```

#### 2.2 - Loader de Créatures (`src/lib/creatures.ts`)

```typescript
// Charger toutes les créatures
export async function loadAllCreatures(): Promise<Creature[]>

// Index par ID, type, CR pour quick lookup
export class CreatureIndex {
  private creatures: Map<string, Creature>;
  private creaturesByType: Map<string, Creature[]>;
  private creaturesByCR: Map<number, Creature[]>;
  
  get(id: string): Creature | undefined
  getByType(type: string): Creature[]
  getByCR(cr: number): Creature[]
  getAll(): Creature[]
}

// Singleton instance
export const creatureIndex = new CreatureIndex();

// Stats
export function getCreatureStats() {
  return {
    total: number;
    byType: Record<string, number>;
    byCR: Record<number, number>;
  };
}
```

#### 2.3 - Module de Filtrage (`src/lib/filters.ts`)

```typescript
// Filtrer créatures par critères
export function filterCreatures(
  creatures: Creature[],
  criteria: FilterCriteria
): Creature[]

// Valeurs disponibles pour filtres (pour dropdowns)
export function getAvailableFilters() {
  return {
    types: string[];
    crRange: { min: number; max: number };
    sizes: string[];
    alignments: string[];
  };
}

// Cache pour perf
const filterCache = new Map<string, Creature[]>();
```

#### Livrables

- ✅ `types.ts` complet avec tous les types
- ✅ `creatures.ts` avec chargement efficace
- ✅ `filters.ts` avec logique filtrage robuste
- ✅ Tests : 4500 créatures chargées ✅
- ✅ Console logging du nombre de créatures

#### ⏱️ Temps estimé : 1-2h

---

### **Phase 3 : Island #1 - Filtrage Avancé** (1-2h)

**Objectif** : Créer interface de filtrage réactive

#### Composant : `src/components/Islands/FilterPanel.astro`

```astro
---
// Props optionnels
interface Props {
  initialFilters?: FilterCriteria;
}

const { initialFilters } = Astro.props;
---

<div class="filter-panel" x-data="filterPanelData()" x-init="init()">
  <!-- Type selector -->
  <div class="filter-group">
    <h3>Type de créature</h3>
    <div class="filter-options">
      <template x-for="type in availableTypes">
        <label>
          <input type="checkbox" x-model="filters.types" :value="type">
          <span x-text="type"></span>
        </label>
      </template>
    </div>
  </div>

  <!-- CR range slider -->
  <div class="filter-group">
    <h3>Facteur de Défi (FD)</h3>
    <div class="range-slider">
      <input 
        type="range" 
        x-model="filters.crRange[0]" 
        min="0" 
        max="30"
        @change="applyFilters()"
      >
      <input 
        type="range" 
        x-model="filters.crRange[1]" 
        min="0" 
        max="30"
        @change="applyFilters()"
      >
      <span x-text="`${filters.crRange[0]} - ${filters.crRange[1]}`"></span>
    </div>
  </div>

  <!-- Size selector -->
  <div class="filter-group">
    <h3>Taille</h3>
    <div class="filter-options">
      <template x-for="size in availableSizes">
        <label>
          <input type="checkbox" x-model="filters.sizes" :value="size">
          <span x-text="size"></span>
        </label>
      </template>
    </div>
  </div>

  <!-- Special traits -->
  <div class="filter-group">
    <h3>Traits spéciaux</h3>
    <label>
      <input type="checkbox" x-model="filters.hasFlying" @change="applyFilters()">
      <span>Peut voler</span>
    </label>
    <label>
      <input type="checkbox" x-model="filters.hasSwimming" @change="applyFilters()">
      <span>Peut nager</span>
    </label>
    <label>
      <input type="checkbox" x-model="filters.hasSpellcasting" @change="applyFilters()">
      <span>Lance des sorts</span>
    </label>
  </div>

  <!-- Counter -->
  <div class="filter-counter">
    <strong x-text="`${matchingCount} créatures`"></strong>
  </div>

  <!-- Reset button -->
  <button @click="resetFilters()" class="btn-secondary">
    Réinitialiser filtres
  </button>
</div>

<script>
function filterPanelData() {
  return {
    filters: {
      types: [],
      crRange: [0, 30],
      sizes: [],
      hasFlying: false,
      hasSwimming: false,
      hasSpellcasting: false,
    },
    matchingCount: 0,
    availableTypes: [],
    availableSizes: [],

    async init() {
      // Charger filtres disponibles
      const available = await getAvailableFilters();
      this.availableTypes = available.types;
      this.availableSizes = available.sizes;
      
      // Initial count
      this.applyFilters();
    },

    async applyFilters() {
      // Appeler API filtrage
      const filtered = await filterCreatures(this.filters);
      this.matchingCount = filtered.length;
      
      // Émettre event vers generateur (Alpine store)
      window.dispatchEvent(
        new CustomEvent('filtersChanged', { detail: filtered })
      );
    },

    resetFilters() {
      this.filters = {
        types: [],
        crRange: [0, 30],
        sizes: [],
        hasFlying: false,
        hasSwimming: false,
        hasSpellcasting: false,
      };
      this.applyFilters();
    }
  }
}
</script>

<style scoped>
.filter-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--color-bg-secondary);
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.filter-group h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-options label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.filter-counter {
  padding: 1rem;
  background: var(--color-accent);
  color: white;
  border-radius: 4px;
  text-align: center;
}

.range-slider {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.range-slider input {
  width: 100%;
}
</style>
```

#### Tâches

1. ✅ Créer composant Astro
2. ✅ Implémenter logique Alpine.js
3. ✅ UI pour filtres (checkboxes, sliders, selects)
4. ✅ Appel au module `filters.ts`
5. ✅ Compteur en temps réel
6. ✅ Styles modernes et responsive

#### Livrables

- ✅ FilterPanel.astro complet et fonctionnel
- ✅ Logique filtrage connectée
- ✅ Badge compteur mise à jour en temps réel
- ✅ Reset filtres working

#### ⏱️ Temps estimé : 1-2h

---

### **Phase 4 : Island #2 - Générateur de Rencontres** (2-3h)

**Objectif** : Créer interface génération rencontres équilibrées

#### 4.1 - Module Calcul Rencontres (`src/lib/encounter.ts`)

```typescript
// XP budget par niveau et difficulté
const XP_THRESHOLDS: Record<number, Record<string, number>> = {
  1: { easy: 25, medium: 50, hard: 75, deadly: 100 },
  2: { easy: 50, medium: 100, hard: 150, deadly: 200 },
  3: { easy: 75, medium: 150, hard: 225, deadly: 400 },
  // ... jusqu'à niveau 20
};

// Multiplier selon nombre de créatures
function getEncounterMultiplier(creatureCount: number): number {
  if (creatureCount === 1) return 1;
  if (creatureCount === 2) return 1.5;
  if (creatureCount <= 6) return 2;
  if (creatureCount <= 10) return 2.5;
  return 3;
}

// Générer rencontre équilibrée
export function generateEncounter(
  creatures: Creature[],
  partyLevel: number,
  partySize: number,
  difficulty: 'easy' | 'medium' | 'hard' | 'deadly'
): Encounter {
  const budget = XP_THRESHOLDS[partyLevel][difficulty];
  const selectedCreatures: EncounterCreature[] = [];
  let spentXP = 0;

  // Sélection aléatoire jusqu'au budget
  while (spentXP < budget && creatures.length > 0) {
    const creature = creatures[Math.floor(Math.random() * creatures.length)];
    const crXP = getCRValue(creature.cr);
    
    if (spentXP + crXP <= budget) {
      // Ajouter ou incrémenter quantité
      const existing = selectedCreatures.find(e => e.creature.name === creature.name);
      if (existing) {
        existing.quantity++;
      } else {
        selectedCreatures.push({ creature, quantity: 1 });
      }
      spentXP += crXP;
    } else {
      creatures = creatures.filter(c => c.name !== creature.name);
    }
  }

  const totalXP = selectedCreatures.reduce(
    (sum, ec) => sum + getCRValue(ec.creature.cr) * ec.quantity,
    0
  );

  const multiplier = getEncounterMultiplier(
    selectedCreatures.reduce((sum, ec) => sum + ec.quantity, 0)
  );

  return {
    id: generateId(),
    name: `Rencontre ${new Date().toLocaleDateString()}`,
    creatures: selectedCreatures,
    partyLevel,
    partySize,
    difficulty,
    totalXP,
    adjustedXP: Math.floor(totalXP * multiplier),
    createdAt: new Date(),
    notes: '',
  };
}

// Helper : convertir CR en XP
function getCRValue(cr: number): number {
  const xpByCR: Record<number, number> = {
    0: 10,
    0.125: 25,
    0.25: 50,
    0.5: 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    // ... jusqu'à 30
  };
  return xpByCR[cr] || 0;
}
```

#### 4.2 - Composant Alpine (`src/components/Islands/EncounterGenerator.astro`)

```astro
---
// Composant interactif avec Alpine.js
---

<div class="encounter-generator" x-data="generatorData()">
  <!-- Input Section -->
  <div class="generator-inputs">
    <h2>Nouvelle rencontre</h2>

    <!-- Party Level -->
    <div class="input-group">
      <label for="partyLevel">Niveau du groupe</label>
      <input 
        id="partyLevel"
        type="range" 
        x-model="partyLevel" 
        min="1" 
        max="20"
        @change="updateEstimate()"
      >
      <span x-text="partyLevel"></span>
    </div>

    <!-- Party Size -->
    <div class="input-group">
      <label for="partySize">Nombre de PJs</label>
      <select x-model="partySize" @change="updateEstimate()">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6+</option>
      </select>
    </div>

    <!-- Difficulty Toggle -->
    <div class="input-group">
      <label>Difficulté</label>
      <div class="difficulty-toggle">
        <template x-for="diff in ['easy', 'medium', 'hard', 'deadly']">
          <button
            :class="difficulty === diff && 'active'"
            @click="setDifficulty(diff)"
            x-text="getDifficultyLabel(diff)"
          ></button>
        </template>
      </div>
    </div>

    <!-- XP Budget Estimate -->
    <div class="xp-estimate">
      <span>Budget XP estimé :</span>
      <strong x-text="getXPBudget()"></strong>
    </div>

    <!-- Generate Button -->
    <button @click="generateEncounter()" class="btn-primary btn-large">
      Générer une rencontre
    </button>
  </div>

  <!-- Output Section -->
  <div class="encounter-output" x-show="currentEncounter">
    <div class="encounter-header">
      <h2 x-text="currentEncounter?.name"></h2>
      <div class="encounter-meta">
        <span x-text="`Difficulté: ${getDifficultyLabel(currentEncounter?.difficulty)}`"></span>
        <span x-text="`XP: ${currentEncounter?.totalXP} (ajusté: ${currentEncounter?.adjustedXP})`"></span>
      </div>
    </div>

    <!-- Creatures List -->
    <div class="creatures-list">
      <h3>Créatures</h3>
      <template x-for="(ec, idx) in (currentEncounter?.creatures || [])">
        <div class="creature-entry">
          <div class="creature-info">
            <strong x-text="ec.creature.name"></strong>
            <span x-text="`FD ${ec.creature.cr}`" class="badge-cr"></span>
            <span x-text="`× ${ec.quantity}`" class="badge-quantity"></span>
          </div>
          <button @click="removeCreature(idx)" class="btn-small">Retirer</button>
        </div>
      </template>
    </div>

    <!-- Notes field -->
    <div class="input-group">
      <label for="notes">Notes tactiques</label>
      <textarea 
        id="notes"
        x-model="currentEncounter.notes"
        placeholder="Ajouter des notes pour cette rencontre..."
      ></textarea>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <button @click="generateEncounter()" class="btn-secondary">
        Régénérer
      </button>
      <button @click="saveEncounter()" class="btn-success">
        Sauvegarder
      </button>
      <button @click="exportEncounter()" class="btn-primary">
        Exporter JSON
      </button>
    </div>

    <!-- Stat Blocks -->
    <div class="stat-blocks">
      <h3>Fiches des créatures</h3>
      <template x-for="ec in (currentEncounter?.creatures || [])">
        <details class="stat-block-accordion">
          <summary x-text="ec.creature.name"></summary>
          <StatBlock :creature="ec.creature" />
        </details>
      </template>
    </div>
  </div>
</div>

<script>
function generatorData() {
  return {
    partyLevel: 5,
    partySize: 4,
    difficulty: 'medium',
    currentEncounter: null,
    filteredCreatures: [],

    init() {
      // Écouter changements de filtres
      window.addEventListener('filtersChanged', (e) => {
        this.filteredCreatures = e.detail;
      });
    },

    getXPBudget() {
      const budget = XP_THRESHOLDS[this.partyLevel]?.[this.difficulty] || 0;
      return budget;
    },

    async generateEncounter() {
      if (this.filteredCreatures.length === 0) {
        alert('Aucune créature ne correspond aux filtres');
        return;
      }

      this.currentEncounter = await generateEncounterAsync(
        this.filteredCreatures,
        this.partyLevel,
        this.partySize,
        this.difficulty
      );
    },

    setDifficulty(diff) {
      this.difficulty = diff;
    },

    removeCreature(idx) {
      this.currentEncounter.creatures.splice(idx, 1);
    },

    async saveEncounter() {
      if (!this.currentEncounter) return;
      await saveEncounter(this.currentEncounter);
      alert('Rencontre sauvegardée !');
    },

    async exportEncounter() {
      if (!this.currentEncounter) return;
      const json = formatExportJSON(this.currentEncounter);
      downloadJSON(json, `encounter-${Date.now()}.json`);
    },

    updateEstimate() {
      // Update XP budget display
    },

    getDifficultyLabel(diff) {
      const labels = {
        easy: 'Facile',
        medium: 'Moyen',
        hard: 'Difficile',
        deadly: 'Mortel'
      };
      return labels[diff] || diff;
    }
  }
}

// XP Thresholds (à définir)
const XP_THRESHOLDS = {
  1: { easy: 25, medium: 50, hard: 75, deadly: 100 },
  2: { easy: 50, medium: 100, hard: 150, deadly: 200 },
  // ... etc
};
</script>

<style scoped>
.encounter-generator {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.generator-inputs {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: var(--color-bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.difficulty-toggle {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.difficulty-toggle button {
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
}

.difficulty-toggle button.active {
  background: var(--color-accent);
  color: white;
  border-color: var(--color-accent);
}

.encounter-output {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.creatures-list {
  background: var(--color-bg-secondary);
  padding: 1rem;
  border-radius: 8px;
}

.creature-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-bottom: 1px solid var(--color-border);
}

.creature-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.badge-cr,
.badge-quantity {
  padding: 0.25rem 0.5rem;
  background: var(--color-accent);
  color: white;
  border-radius: 3px;
  font-size: 0.875rem;
}

.stat-blocks {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-block-accordion {
  border: 1px solid var(--color-border);
  border-radius: 4px;
  overflow: hidden;
}

.stat-block-accordion summary {
  padding: 1rem;
  background: var(--color-bg-secondary);
  cursor: pointer;
  font-weight: 600;
}

.stat-block-accordion summary:hover {
  background: var(--color-bg-tertiary);
}

@media (max-width: 1024px) {
  .encounter-generator {
    grid-template-columns: 1fr;
  }
}
</style>
```

#### Livrables

- ✅ `encounter.ts` complet avec calculs
- ✅ `EncounterGenerator.astro` fonctionnel
- ✅ Génération aléatoire équilibrée
- ✅ Affichage stat blocks complets
- ✅ Modification créatures (ajouter/retirer)

#### ⏱️ Temps estimé : 2-3h

---

### **Phase 5 : Gestion Sauvegarde & Export** (1-1.5h)

**Objectif** : Sauvegarder et exporter rencontres

#### 5.1 - Module LocalStorage (`src/lib/storage.ts`)

```typescript
const STORAGE_KEY = 'dnd-encounters';

export function saveEncounter(encounter: Encounter): void {
  const existing = getAllEncounters();
  existing.push(encounter);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(existing));
}

export function loadEncounter(id: string): Encounter | null {
  const all = getAllEncounters();
  return all.find(e => e.id === id) || null;
}

export function getAllEncounters(): Encounter[] {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

export function deleteEncounter(id: string): void {
  const all = getAllEncounters();
  const filtered = all.filter(e => e.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
}

export function updateEncounter(id: string, updates: Partial<Encounter>): void {
  const all = getAllEncounters();
  const idx = all.findIndex(e => e.id === id);
  if (idx >= 0) {
    all[idx] = { ...all[idx], ...updates };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
  }
}
```

#### 5.2 - Module Export (`src/lib/export.ts`)

```typescript
export function formatExportJSON(encounter: Encounter): string {
  const exported: ExportedEncounter = {
    metadata: {
      name: encounter.name,
      partyLevel: encounter.partyLevel,
      partySize: encounter.partySize,
      difficulty: encounter.difficulty,
      createdAt: encounter.createdAt.toISOString(),
    },
    creatures: encounter.creatures.map(ec => ({
      name: ec.creature.name,
      source: ec.creature.source,
      quantity: ec.quantity,
      statBlock: ec.creature,
    })),
    notes: encounter.notes,
    xp: {
      total: encounter.totalXP,
      adjusted: encounter.adjustedXP,
    },
  };

  return JSON.stringify(exported, null, 2);
}

export function downloadJSON(json: string, filename: string): void {
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function parseImportJSON(json: string): Encounter | null {
  try {
    const exported: ExportedEncounter = JSON.parse(json);
    return {
      id: generateId(),
      name: exported.metadata.name,
      creatures: exported.creatures.map(c => ({
        creature: c.statBlock,
        quantity: c.quantity,
      })),
      partyLevel: exported.metadata.partyLevel,
      partySize: exported.metadata.partySize,
      difficulty: exported.metadata.difficulty as any,
      totalXP: exported.xp.total,
      adjustedXP: exported.xp.adjusted,
      createdAt: new Date(exported.metadata.createdAt),
      notes: exported.notes,
    };
  } catch {
    return null;
  }
}
```

#### 5.3 - Island SavedEncounters (`src/components/Islands/SavedEncounters.astro`)

```astro
<div class="saved-encounters" x-data="savedData()">
  <h3>Rencontres sauvegardées</h3>
  
  <div class="encounters-list">
    <template x-for="encounter in encounters">
      <div class="encounter-item">
        <div>
          <strong x-text="encounter.name"></strong>
          <div class="meta">
            <span x-text="`Niveau ${encounter.partyLevel}`"></span>
            <span x-text="`${encounter.creatures.length} types`"></span>
          </div>
        </div>
        <div class="actions">
          <button @click="loadEncounter(encounter.id)" class="btn-small">
            Charger
          </button>
          <button @click="deleteEncounter(encounter.id)" class="btn-small btn-danger">
            Supprimer
          </button>
        </div>
      </div>
    </template>
  </div>

  <input type="file" @change="importJSON($event)" accept=".json">
</div>

<script>
function savedData() {
  return {
    encounters: [],

    init() {
      this.loadEncounters();
    },

    loadEncounters() {
      this.encounters = getAllEncounters();
    },

    loadEncounter(id) {
      const encounter = loadEncounter(id);
      if (encounter) {
        window.dispatchEvent(
          new CustomEvent('encounterLoaded', { detail: encounter })
        );
      }
    },

    deleteEncounter(id) {
      if (confirm('Supprimer cette rencontre ?')) {
        deleteEncounter(id);
        this.loadEncounters();
      }
    },

    importJSON(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        const json = e.target.result;
        const encounter = parseImportJSON(json);
        if (encounter) {
          window.dispatchEvent(
            new CustomEvent('encounterLoaded', { detail: encounter })
          );
        }
      };
      reader.readAsText(file);
    }
  }
}
</script>
```

#### 5.4 - Island ExportPanel (`src/components/Islands/ExportPanel.astro`)

```astro
<div class="export-panel" x-data="{ includeStats: true }">
  <h3>Exporter</h3>
  
  <label>
    <input type="checkbox" x-model="includeStats">
    Inclure les stat blocks complets
  </label>

  <button @click="exportJSON()" class="btn-primary">
    Télécharger en JSON
  </button>
</div>

<script>
function exportJSON() {
  if (!window.currentEncounter) {
    alert('Pas de rencontre à exporter');
    return;
  }

  const json = formatExportJSON(window.currentEncounter);
  downloadJSON(json, `rencontre-${Date.now()}.json`);
}
</script>
```

#### Livrables

- ✅ `storage.ts` avec localStorage API
- ✅ `export.ts` avec JSON formatting
- ✅ SavedEncounters Island avec CRUD
- ✅ ExportPanel avec download/upload
- ✅ Persistance localStorage working

#### ⏱️ Temps estimé : 1-1.5h

---

### **Phase 6 : Pages Statiques & Layout** (1-2h)

**Objectif** : Créer structure pages et navigation

#### 6.1 - Layout Principal (`src/layouts/GeneratorLayout.astro`)

```astro
---
import BaseLayout from './BaseLayout.astro';
---

<BaseLayout title="Générateur de Rencontres">
  <div class="generator-container">
    <aside class="sidebar">
      <FilterPanel client:load />
      <SavedEncounters client:load />
    </aside>

    <main class="main-content">
      <EncounterGenerator client:load />
      <ExportPanel client:load />
    </main>
  </div>
</BaseLayout>

<style>
.generator-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  padding: 2rem;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .generator-container {
    grid-template-columns: 1fr;
  }
}
</style>
```

#### 6.2 - Page d'Accueil (`src/pages/index.astro`)

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Générateur de Rencontres D&D 5e">
  <section class="hero">
    <h1>Générateur de Rencontres D&D 5e</h1>
    <p>Créez des rencontres équilibrées en secondes</p>
    <a href="/generator" class="btn-primary btn-large">
      Commencer
    </a>
  </section>

  <section class="features">
    <h2>Fonctionnalités</h2>
    <div class="feature-grid">
      <div class="feature-card">
        <h3>4500+ créatures</h3>
        <p>Tout le bestiaire D&D 5e en français</p>
      </div>
      <div class="feature-card">
        <h3>Filtrage avancé</h3>
        <p>Par type, FD, taille, traits spéciaux</p>
      </div>
      <div class="feature-card">
        <h3>Équilibrage automatique</h3>
        <p>Calcul XP et ajustement difficulté</p>
      </div>
      <div class="feature-card">
        <h3>Sauvegarde & Export</h3>
        <p>Vos rencontres à portée de main</p>
      </div>
    </div>
  </section>

  <section class="cta">
    <h2>Prêt à créer votre rencontre ?</h2>
    <a href="/generator" class="btn-primary btn-large">
      Aller au générateur
    </a>
  </section>
</BaseLayout>

<style>
.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-dark));
  color: white;
  border-radius: 8px;
  margin-bottom: 3rem;
}

.features {
  margin-bottom: 3rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-card {
  padding: 1.5rem;
  background: var(--color-bg-secondary);
  border-radius: 8px;
  border-left: 4px solid var(--color-accent);
}
</style>
```

#### 6.3 - Page Générateur (`src/pages/generator.astro`)

```astro
---
import GeneratorLayout from '../layouts/GeneratorLayout.astro';
---

<GeneratorLayout />
```

#### 6.4 - Page Bestiaire (`src/pages/bestiary.astro`)

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { creatureIndex } from '../lib/creatures';

const creatures = creatureIndex.getAll();
const pageSize = 50;
const page = 1;
const paged = creatures.slice(0, pageSize);
---

<BaseLayout title="Bestiaire D&D 5e">
  <div class="bestiary-container">
    <h1>Bestiaire D&D 5e</h1>
    <p class="subtitle">{creatures.length} créatures disponibles</p>

    <div class="creatures-grid">
      {paged.map(creature => (
        <a href={`/creature/${creature.name.toLowerCase().replace(/\s+/g, '-')}`}>
          <div class="creature-card">
            <h3>{creature.name}</h3>
            <div class="creature-meta">
              <span class="type">{creature.type}</span>
              <span class="cr">FD {creature.cr}</span>
            </div>
          </div>
        </a>
      ))}
    </div>

    <div class="pagination">
      <!-- Pagination controls -->
    </div>
  </div>
</BaseLayout>

<style>
.bestiary-container {
  padding: 2rem;
}

.creatures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.creature-card {
  padding: 1rem;
  background: var(--color-bg-secondary);
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.creature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.creature-meta {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.type, .cr {
  padding: 0.25rem 0.5rem;
  background: var(--color-accent);
  color: white;
  border-radius: 3px;
}
</style>
```

#### 6.5 - Fiche Créature (`src/pages/creature/[id].astro`)

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import StatBlock from '../../components/Common/StatBlock.astro';
import { creatureIndex } from '../../lib/creatures';

const { id } = Astro.params;
const creature = creatureIndex.get(id);

if (!creature) {
  return Astro.redirect('/bestiary');
}
---

<BaseLayout title={creature.name}>
  <div class="creature-page">
    <a href="/bestiary" class="back-link">← Retour au bestiaire</a>

    <StatBlock :creature={creature} />

    <div class="actions">
      <a href="/generator" class="btn-primary">
        Utiliser dans le générateur
      </a>
    </div>
  </div>
</BaseLayout>

<style>
.creature-page {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: var(--color-accent);
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
</style>
```

#### Livrables

- ✅ Layout responsive principal
- ✅ Page d'accueil avec features
- ✅ Page générateur opérationnelle
- ✅ Page bestiaire avec grille créatures
- ✅ Fiche créature avec stat block complet
- ✅ Navigation cohérente

#### ⏱️ Temps estimé : 1-2h

---

### **Phase 7 : Composant StatBlock** (1h)

**Objectif** : Afficher stat blocks complets et formatés

#### Composant : `src/components/Common/StatBlock.astro`

```astro
---
interface Props {
  creature: Creature;
}

const { creature } = Astro.props;

// Helper pour formater ability scores
function getAbilityModifier(score: number): number {
  return Math.floor((score - 10) / 2);
}

// Helper pour formater traits
function parseText(text: string): string {
  // Convertir **gras** en <strong>, etc.
  return text
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
}
---

<div class="stat-block">
  <!-- Header -->
  <div class="stat-block-header">
    <h1 class="name">{creature.name}</h1>
    <div class="type-line">
      <em>
        {creature.size} {creature.type},
        {creature.alignment}
      </em>
    </div>
  </div>

  <!-- Divider -->
  <hr class="divider" />

  <!-- Quick Stats -->
  <div class="quick-stats">
    <div class="stat-line">
      <strong>Class d'armure</strong>
      {creature.ac[0]?.ac || '10'}
    </div>
    <div class="stat-line">
      <strong>Points de vie</strong>
      {creature.hp.average || 0}
      <span class="formula">({creature.hp.formula})</span>
    </div>
    <div class="stat-line">
      <strong>Vitesse</strong>
      {creature.speed.walk || 0} pi,
      {creature.speed.fly ? `vol ${creature.speed.fly} pi,` : ''}
      {creature.speed.swim ? `nage ${creature.speed.swim} pi` : ''}
    </div>
  </div>

  <hr class="divider" />

  <!-- Ability Scores -->
  <div class="abilities">
    <div class="ability">
      <div class="ability-score">
        {creature.abilityScores.str}
      </div>
      <div class="ability-label">FOR</div>
      <div class="ability-modifier">
        {getAbilityModifier(creature.abilityScores.str) > 0 ? '+' : ''}
        {getAbilityModifier(creature.abilityScores.str)}
      </div>
    </div>
    <div class="ability">
      <div class="ability-score">{creature.abilityScores.dex}</div>
      <div class="ability-label">DEX</div>
      <div class="ability-modifier">
        {getAbilityModifier(creature.abilityScores.dex) > 0 ? '+' : ''}
        {getAbilityModifier(creature.abilityScores.dex)}
      </div>
    </div>
    <div class="ability">
      <div class="ability-score">{creature.abilityScores.con}</div>
      <div class="ability-label">CON</div>
      <div class="ability-modifier">
        {getAbilityModifier(creature.abilityScores.con) > 0 ? '+' : ''}
        {getAbilityModifier(creature.abilityScores.con)}
      </div>
    </div>
    <div class="ability">
      <div class="ability-score">{creature.abilityScores.int}</div>
      <div class="ability-label">INT</div>
      <div class="ability-modifier">
        {getAbilityModifier(creature.abilityScores.int) > 0 ? '+' : ''}
        {getAbilityModifier(creature.abilityScores.int)}
      </div>
    </div>
    <div class="ability">
      <div class="ability-score">{creature.abilityScores.wis}</div>
      <div class="ability-label">SAG</div>
      <div class="ability-modifier">
        {getAbilityModifier(creature.abilityScores.wis) > 0 ? '+' : ''}
        {getAbilityModifier(creature.abilityScores.wis)}
      </div>
    </div>
    <div class="ability">
      <div class="ability-score">{creature.abilityScores.cha}</div>
      <div class="ability-label">CHA</div>
      <div class="ability-modifier">
        {getAbilityModifier(creature.abilityScores.cha) > 0 ? '+' : ''}
        {getAbilityModifier(creature.abilityScores.cha)}
      </div>
    </div>
  </div>

  <hr class="divider" />

  <!-- Additional Info -->
  <div class="additional-info">
    {creature.savingThrows && (
      <div class="stat-line">
        <strong>Jets de sauvegarde</strong>
        {Object.entries(creature.savingThrows)
          .map(([ability, mod]) => `${ability.toUpperCase()} ${mod > 0 ? '+' : ''}${mod}`)
          .join(', ')}
      </div>
    )}
    {creature.skills && (
      <div class="stat-line">
        <strong>Compétences</strong>
        {Object.entries(creature.skills)
          .map(([skill, mod]) => `${skill} ${mod > 0 ? '+' : ''}${mod}`)
          .join(', ')}
      </div>
    )}
    {creature.damageResistances && (
      <div class="stat-line">
        <strong>Résistances aux dégâts</strong>
        {creature.damageResistances.join(', ')}
      </div>
    )}
    {creature.damageImmunities && (
      <div class="stat-line">
        <strong>Immunités aux dégâts</strong>
        {creature.damageImmunities.join(', ')}
      </div>
    )}
    {creature.conditionImmunities && (
      <div class="stat-line">
        <strong>Immunités aux états</strong>
        {creature.conditionImmunities.join(', ')}
      </div>
    )}
    <div class="stat-line">
      <strong>Sens</strong>
      {Object.entries(creature.senses)
        .map(([sense, value]) => `${sense} ${value}`)
        .join(', ')}
    </div>
    <div class="stat-line">
      <strong>Langues</strong>
      {creature.languages?.join(', ') || 'Aucune'}
    </div>
    <div class="stat-line">
      <strong>Facteur de défi</strong>
      {creature.cr}
    </div>
  </div>

  <hr class="divider" />

  <!-- Traits -->
  {creature.traits && creature.traits.length > 0 && (
    <div class="traits-section">
      {creature.traits.map(trait => (
        <div class="trait">
          <strong>{trait.name}.</strong>
          <span set:html={parseText(trait.text)} />
        </div>
      ))}
    </div>
  )}

  <!-- Actions -->
  {creature.actions && creature.actions.length > 0 && (
    <div class="actions-section">
      <h3>Actions</h3>
      {creature.actions.map(action => (
        <div class="action">
          <strong>{action.name}.</strong>
          <span set:html={parseText(action.text)} />
        </div>
      ))}
    </div>
  )}

  <!-- Legendary Actions -->
  {creature.legendaryActions && creature.legendaryActions.length > 0 && (
    <div class="legendary-section">
      <h3>Actions légendaires</h3>
      <p>
        La créature peut faire {creature.legendaryActions.length} actions
        légendaires par round, à choisir parmi les options ci-dessous.
      </p>
      {creature.legendaryActions.map(action => (
        <div class="action">
          <strong>{action.name}.</strong>
          <span set:html={parseText(action.text)} />
        </div>
      ))}
    </div>
  )}

  <!-- Spellcasting -->
  {creature.spellcasting && creature.spellcasting.length > 0 && (
    <div class="spellcasting-section">
      <h3>Lancer des sorts</h3>
      {creature.spellcasting.map(sc => (
        <div class="spellcasting">
          <p set:html={parseText(sc.type)} />
          {sc.spells && (
            <div class="spells-list">
              {sc.spells.map(spell => (
                <div class="spell">
                  <strong>{spell.name}</strong>
                  {spell.dc && <span class="dc">DD {spell.dc}</span>}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )}
</div>

<style>
.stat-block {
  background: var(--color-bg);
  color: var(--color-text);
  font-family: 'Georgia', serif;
  padding: 1.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  line-height: 1.6;
}

.stat-block-header {
  text-align: center;
  margin-bottom: 0.5rem;
}

.name {
  margin: 0;
  color: var(--color-accent);
  font-size: 2rem;
}

.type-line {
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.divider {
  border: none;
  border-top: 2px solid var(--color-accent);
  margin: 0.75rem 0;
}

.quick-stats {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.stat-line {
  display: flex;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.stat-line strong {
  color: var(--color-accent);
}

.formula {
  font-style: italic;
  font-size: 0.85em;
  color: var(--color-text-secondary);
}

.abilities {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
  text-align: center;
  margin-bottom: 0.5rem;
}

.ability {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ability-score {
  font-weight: bold;
  font-size: 1.5rem;
  color: var(--color-accent);
}

.ability-label {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.ability-modifier {
  font-size: 0.9rem;
  font-weight: bold;
}

.additional-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.traits-section,
.actions-section,
.legendary-section,
.spellcasting-section {
  margin-bottom: 1rem;
}

.trait,
.action {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.trait strong,
.action strong {
  color: var(--color-accent);
}

h3 {
  margin: 0.75rem 0 0.5rem 0;
  color: var(--color-accent);
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.spells-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.85rem;
}

.spell {
  display: flex;
  justify-content: space-between;
  padding-left: 1rem;
}

@media (max-width: 640px) {
  .abilities {
    grid-template-columns: repeat(3, 1fr);
  }

  .stat-block {
    padding: 1rem;
  }

  .name {
    font-size: 1.5rem;
  }
}
```

#### Livrables

- ✅ Composant StatBlock.astro complet
- ✅ Formatage traits/actions/spells
- ✅ Layout style 5etools modernisé
- ✅ Responsive design
- ✅ Support abilities, skills, saves

#### ⏱️ Temps estimé : 1h

---

### **Phase 8 : Polish, Tests & Déploiement** (1-2h)

**Objectif** : Finaliser et déployer

#### Tâches

1. **Tests navigateurs**
   - Chrome, Firefox, Safari
   - Vérifier interactivité Alpine.js
   - Vérifier localStorage

2. **Tests responsive**
   - Desktop (1920px)
   - Tablet (768px)
   - Mobile (375px)

3. **Performance**
   - Lighthouse audit
   - Optimiser images
   - Minify CSS/JS

4. **Accessibilité**
   - WCAG 2.1 AA
   - Vérifier contraste
   - Tester avec lecteur d'écran

5. **Build production**
   ```bash
   npm run build
   ```

6. **Setup déploiement VPS**
   - GitHub Actions (optionnel)
   - ou déploiement manuel
   - Configuration domaine + SSL

7. **Documentation**
   - README.md
   - Guide utilisateur
   - Guide développeur

#### Livrables

- ✅ Build production testée
- ✅ Tous navigateurs compatibles
- ✅ Score Lighthouse > 80
- ✅ Accessible WCAG 2.1 AA
- ✅ Déploiement VPS configuré
- ✅ Documentation complète

#### ⏱️ Temps estimé : 1-2h

---

## 📊 RÉSUMÉ TEMPS TOTAL

| Phase | Temps estimé |
|-------|-------------|
| 1. Infrastructure | 45 min |
| 2. Modèle données | 1-2h |
| 3. Island Filtres | 1-2h |
| 4. Island Générateur | 2-3h |
| 5. Sauvegarde/Export | 1-1.5h |
| 6. Pages & Layout | 1-2h |
| 7. StatBlock | 1h |
| 8. Polish & Deploy | 1-2h |
| **TOTAL MVP** | **9-15.5h** |

---

## ✅ CHECKLIST MVP FINAL

- ✅ Infrastructure Astro + Alpine.js
- ✅ Données bestiaire (~4500 créatures) chargées
- ✅ Filtrage avancé (types, CR, taille, traits, alignement)
- ✅ Génération rencontres équilibrées (XP budget)
- ✅ Affichage stat blocks complets
- ✅ Sauvegarde LocalStorage
- ✅ Export JSON avec données complètes
- ✅ Import rencontres depuis JSON
- ✅ Pages bestiaire + fiche créature
- ✅ Design moderne et responsive
- ✅ Dark mode ready
- ✅ Tests et déploiement VPS
- ✅ Documentation complète

---

## 🚀 PHASES FUTURES (Phase 9+)

1. **Export PDF** - Rencontres formattées PDF
2. **Mode Multi-RPG** - Support Pathfinder, Warhammer, etc.
3. **Traductions** - Anglais, espagnol, allemand
4. **PWA** - Support offline
5. **Historique** - Toutes les rencontres générées
6. **Partage** - URL courtes pour partager rencontres
7. **Créatures custom** - Upload créatures personnalisées
8. **Statistiques** - Analyses sur rencontres générées

---

## 📝 NOTES IMPORTANTES

### Dépendances
- Vérifier formatage des données 5etools (40+ champs)
- Assurer compatibilité JSON parsing

### Performance
- 4500 créatures = ~10-15MB JSON
- Considérer lazy loading par source si trop lourd
- Index en mémoire pour quick lookups

### UX
- Bien différencier les Islands (zones interactives)
- Garder filtres et générateur synchronisés
- Confirmation avant supprimer rencontres

### Accessibilité
- Labels explicites sur inputs
- ARIA pour stat blocks
- Contraste suffisant (AA minimum)

---

## 🎨 Design System (À définir)

### Couleurs (Variables CSS)
```css
--color-accent: #8B0000;        /* Accent D&D rouge sang */
--color-accent-dark: #600000;
--color-bg: #FDFBF7;            /* Parchemin clair */
--color-bg-secondary: #F5F2ED;
--color-text: #2C1810;          /* Marron foncé */
--color-text-secondary: #5C4033;
--color-border: #D4A574;        /* Or/bronze */
```

### Typographie
- **Serif** (Georgia, Garamond) : Stat blocks, headings
- **Sans-serif** (Inter, Roboto) : UI, buttons

### Spacing
- Base : 8px
- Grid : 4px

---

**Plan finalisé et prêt pour implémentation ! 🚀**

Version 1.0 | 2026-05-08
