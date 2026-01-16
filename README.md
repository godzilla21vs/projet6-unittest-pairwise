# Projet 6 - Tests Unitaires Python avec Pairwise Testing

## 📋 Description

Ce projet implémente un **solveur d'équation du second degré** (ax² + bx + c = 0) avec des tests unitaires Python utilisant l'approche **Pairwise Testing**. Cette technique de test combinatoire permet de réduire drastiquement le nombre de cas de test tout en maintenant une couverture efficace.

Ce projet fait partie du cours **INF563 - Test Logiciel**.

## 🎯 Objectifs Pédagogiques

- Comprendre et appliquer le **Pairwise Testing** (All-Pairs Testing)
- Implémenter des tests unitaires avec **unittest**
- Tester une fonction mathématique avec multiples entrées
- Générer automatiquement des cas de test optimisés
- Analyser la couverture combinatoire

## 📁 Structure du Projet

```
projet6-unittest-pairwise/
├── equation_solver.py          # Module de résolution d'équation
├── pairwise_generator.py       # Générateur de cas pairwise
├── test_equation_pairwise.py   # Tests unittest
└── README.md
```

## 🧮 Problématique Mathématique

### Équation du Second Degré

L'équation **ax² + bx + c = 0** admet :

| Discriminant (Δ) | Type de Solutions |
|------------------|-------------------|
| Δ > 0 | Deux racines réelles distinctes |
| Δ = 0 | Une racine double (réelle) |
| Δ < 0 | Deux racines complexes conjuguées |

### Cas Spéciaux

| Condition | Résultat |
|-----------|----------|
| a = 0, b ≠ 0 | Équation linéaire : x = -c/b |
| a = 0, b = 0, c = 0 | Infinité de solutions |
| a = 0, b = 0, c ≠ 0 | Aucune solution (contradiction) |

## 🔬 Approche Pairwise Testing

### Le Problème Combinatoire

Avec **3 paramètres** (a, b, c) et **9 valeurs** pour chaque :
- Valeurs testées : `{-10, -2, -1, -0.5, 0, 0.5, 1, 2, 10}`
- Combinaisons exhaustives : **9 × 9 × 9 = 729 cas** ❌

### La Solution Pairwise

L'approche pairwise garantit que **chaque paire** de valeurs (a,b), (a,c), (b,c) est testée **au moins une fois** :

```
Réduction obtenue :
├── Tests exhaustifs : 729 cas
├── Tests pairwise : ~81 cas
└── Réduction : ~89% 🎉
```

### Pourquoi Ça Fonctionne ?

La plupart des bugs sont causés par l'interaction de **2 paramètres** (et rarement 3+). Le pairwise testing couvre toutes les interactions binaires avec un minimum de tests.

## 🔧 Prérequis

- **Python** 3.8+
- Aucune dépendance externe (utilise les modules standards)

## 📦 Installation

1. **Cloner le projet**
```bash
git clone https://github.com/godzilla21vs/projet6-unittest-pairwise.git
cd projet6-unittest-pairwise
```

2. **Vérifier Python**
```bash
python --version  # Python 3.8+
```

## 🚀 Exécution

### Lancer les tests unitaires

```bash
# Avec unittest (verbeux)
python -m unittest test_equation_pairwise.py -v

# Avec pytest (si installé)
pytest test_equation_pairwise.py -v

# Lancer un test spécifique
python -m unittest test_equation_pairwise.TestQuadraticPairwise.test_two_real_roots -v
```

### Voir les statistiques pairwise

```bash
python pairwise_generator.py
```

**Sortie attendue :**
```
=== Statistiques Pairwise ===
Paramètres : 3 (a, b, c)
Valeurs par paramètre : 9
Combinaisons exhaustives : 729
Cas pairwise générés : 81
Réduction : 88.9%
Toutes les paires couvertes : ✓
```

### Tester le solveur directement

```bash
python equation_solver.py
```

## 📝 Architecture du Code

### equation_solver.py

```python
def solve_quadratic(a: float, b: float, c: float):
    """
    Résout ax² + bx + c = 0
    
    Returns:
        - Tuple(x1, x2) : deux racines réelles
        - Tuple(x,) : racine double ou linéaire
        - Tuple(complex1, complex2) : racines complexes
        - None : infinité de solutions
    
    Raises:
        ValueError : si équation impossible (a=b=0, c≠0)
    """
```

### pairwise_generator.py

```python
def generate_pairwise_cases(values_a, values_b, values_c):
    """
    Génère les cas de test couvrant toutes les paires.
    
    Algorithme : 
    1. Énumère toutes les paires possibles (a,b), (a,c), (b,c)
    2. Sélectionne goulûment les triplets couvrant le max de paires
    3. Répète jusqu'à couverture complète
    """
```

### test_equation_pairwise.py

```python
class TestQuadraticPairwise(unittest.TestCase):
    """Tests pairwise pour le solveur d'équation."""
    
    def test_two_real_roots(self):
        """Δ > 0 : deux racines réelles distinctes"""
        
    def test_double_root(self):
        """Δ = 0 : une racine double"""
        
    def test_complex_roots(self):
        """Δ < 0 : racines complexes"""
        
    def test_all_pairwise_combinations(self):
        """Teste tous les cas pairwise générés"""
```

## 📊 Cas de Test

### Tests de Base (6 tests)

| Test | Condition | Résultat Attendu |
|------|-----------|------------------|
| `test_two_real_roots` | Δ > 0 | (x1, x2) réels |
| `test_double_root` | Δ = 0 | (x,) réel |
| `test_complex_roots` | Δ < 0 | (z1, z2) complexes |
| `test_linear_equation` | a = 0, b ≠ 0 | (x,) réel |
| `test_infinite_solutions` | a = b = c = 0 | None |
| `test_no_solution` | a = b = 0, c ≠ 0 | ValueError |

### Tests Pairwise (~81 tests)

Générés automatiquement avec vérification :
```python
for a, b, c in pairwise_cases:
    result = solve_quadratic(a, b, c)
    # Vérifie que chaque solution satisfait l'équation
    if result and not isinstance(result, type(None)):
        for x in result:
            self.assertTrue(verify_solution(a, b, c, x))
```

## 📈 Couverture des Tests

```
Total des tests : ~87
├── Tests unitaires de base : 6
└── Tests pairwise : ~81

Couverture des paires :
├── Paires (a, b) : 81/81 (100%) ✓
├── Paires (a, c) : 81/81 (100%) ✓
└── Paires (b, c) : 81/81 (100%) ✓

Valeurs testées pour chaque paramètre :
{-10, -2, -1, -0.5, 0, 0.5, 1, 2, 10}
```

## 🔬 Vérification des Solutions

Chaque solution trouvée est vérifiée :

```python
def verify_solution(a, b, c, x):
    """Vérifie que ax² + bx + c ≈ 0"""
    result = a * x**2 + b * x + c
    return abs(result) < 1e-10  # Tolérance numérique
```

## 📚 Références

- [Pairwise Testing (Wikipedia)](https://en.wikipedia.org/wiki/All-pairs_testing)
- [PICT - Pairwise Tool by Microsoft](https://github.com/microsoft/pict)
- [Article original : "Adequacy of Pseudo-Random Testing"](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software)

## 👤 Auteur

**Cours INF563 - Test Logiciel**

---

*Ce projet démontre l'efficacité du Pairwise Testing pour la réduction des cas de test combinatoires.*
