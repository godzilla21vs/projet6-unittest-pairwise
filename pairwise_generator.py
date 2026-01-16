"""
Générateur de cas de test Pairwise pour l'équation du second degré
INF563 - Test Logiciel

Implémente l'algorithme IPOG pour la génération pairwise.
Réduit les 9×9×9 = 729 combinaisons à environ 81 cas de test.
"""

from itertools import product, combinations
from typing import List, Tuple, Set, Dict, Any


# Valeurs pour a, b, c (9 valeurs chacun)
VALUES = [-10, -2, -1, -0.5, 0, 0.5, 1, 2, 10]


def get_all_pairs(values_a: List, values_b: List, values_c: List) -> Set[Tuple]:
    """
    Génère toutes les paires possibles entre les paramètres.
    
    Returns:
        Set de tuples représentant toutes les paires (param, value1, param, value2)
    """
    pairs = set()
    
    # Paires (a, b)
    for a in values_a:
        for b in values_b:
            pairs.add(('a', a, 'b', b))
    
    # Paires (a, c)
    for a in values_a:
        for c in values_c:
            pairs.add(('a', a, 'c', c))
    
    # Paires (b, c)
    for b in values_b:
        for c in values_c:
            pairs.add(('b', b, 'c', c))
    
    return pairs


def check_test_covers_pair(test: Dict[str, Any], pair: Tuple) -> bool:
    """
    Vérifie si un cas de test couvre une paire donnée.
    """
    param1, val1, param2, val2 = pair
    return test[param1] == val1 and test[param2] == val2


def covers_any_uncovered(test: Dict[str, Any], uncovered: Set[Tuple]) -> int:
    """
    Compte le nombre de paires non couvertes que ce test couvre.
    """
    count = 0
    for pair in uncovered:
        if check_test_covers_pair(test, pair):
            count += 1
    return count


def generate_pairwise_tests() -> List[Dict[str, float]]:
    """
    Génère les cas de test pairwise en utilisant un algorithme glouton.
    
    L'objectif est de couvrir toutes les paires possibles avec un minimum
    de cas de test.
    
    Returns:
        Liste de dictionnaires {a, b, c} représentant les cas de test
    """
    values_a = VALUES.copy()
    values_b = VALUES.copy()
    values_c = VALUES.copy()
    
    # Obtenir toutes les paires à couvrir
    all_pairs = get_all_pairs(values_a, values_b, values_c)
    uncovered = all_pairs.copy()
    
    tests = []
    
    while uncovered:
        best_test = None
        best_coverage = 0
        
        # Chercher le meilleur cas de test (celui qui couvre le plus de paires)
        for a in values_a:
            for b in values_b:
                for c in values_c:
                    test = {'a': a, 'b': b, 'c': c}
                    coverage = covers_any_uncovered(test, uncovered)
                    if coverage > best_coverage:
                        best_coverage = coverage
                        best_test = test
        
        if best_test:
            tests.append(best_test)
            # Retirer les paires couvertes
            uncovered = {p for p in uncovered if not check_test_covers_pair(best_test, p)}
    
    return tests


def generate_all_combinations() -> List[Dict[str, float]]:
    """
    Génère toutes les combinaisons possibles (9×9×9 = 729).
    Utilisé pour comparaison avec l'approche pairwise.
    """
    return [
        {'a': a, 'b': b, 'c': c}
        for a, b, c in product(VALUES, VALUES, VALUES)
    ]


def validate_pairwise_coverage(tests: List[Dict[str, float]]) -> Tuple[bool, float]:
    """
    Valide que les cas de test pairwise couvrent toutes les paires.
    
    Returns:
        (complete_coverage, coverage_percentage)
    """
    values_a = VALUES.copy()
    values_b = VALUES.copy()
    values_c = VALUES.copy()
    
    all_pairs = get_all_pairs(values_a, values_b, values_c)
    covered = set()
    
    for test in tests:
        for pair in all_pairs:
            if check_test_covers_pair(test, pair):
                covered.add(pair)
    
    coverage = len(covered) / len(all_pairs) * 100
    return len(covered) == len(all_pairs), coverage


def print_pairwise_stats():
    """
    Affiche les statistiques de la génération pairwise.
    """
    print("=== Statistiques Pairwise ===\n")
    
    # Génération exhaustive vs pairwise
    all_tests = generate_all_combinations()
    pairwise_tests = generate_pairwise_tests()
    
    print(f"Valeurs par paramètre: {len(VALUES)}")
    print(f"Paramètres: a, b, c")
    print()
    print(f"Combinaisons exhaustives: {len(all_tests)}")
    print(f"Cas de test pairwise: {len(pairwise_tests)}")
    print(f"Réduction: {100 - (len(pairwise_tests) / len(all_tests) * 100):.1f}%")
    print()
    
    # Validation de la couverture
    complete, coverage = validate_pairwise_coverage(pairwise_tests)
    print(f"Couverture pairwise: {coverage:.2f}%")
    print(f"Couverture complète: {'Oui' if complete else 'Non'}")


if __name__ == "__main__":
    print_pairwise_stats()
    print("\n=== Premiers cas de test pairwise ===")
    tests = generate_pairwise_tests()
    for i, test in enumerate(tests[:10], 1):
        print(f"{i}. a={test['a']:6}, b={test['b']:6}, c={test['c']:6}")
    print(f"... et {len(tests) - 10} autres cas")
