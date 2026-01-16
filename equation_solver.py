"""
Module de résolution d'équation du second degré
INF563 - Test Logiciel

Résout l'équation ax² + bx + c = 0
"""

import math
from typing import Tuple, Optional, Union


def solve_quadratic(a: float, b: float, c: float) -> Union[Tuple[float, float], Tuple[float], Tuple[complex, complex], None]:
    """
    Résout l'équation quadratique ax² + bx + c = 0.
    
    Args:
        a: Coefficient de x²
        b: Coefficient de x
        c: Terme constant
    
    Returns:
        - Tuple de 2 racines réelles si discriminant > 0
        - Tuple d'une racine réelle (double) si discriminant = 0
        - Tuple de 2 racines complexes si discriminant < 0
        - None si a = 0 et b = 0 (pas d'équation ou équation sans solution)
        - Tuple d'une racine si a = 0 et b != 0 (équation linéaire)
    
    Raises:
        ValueError: Si a = 0 et c != 0 et b = 0 (équation impossible)
    """
    # Cas dégénéré: a = 0 (équation linéaire ou constante)
    if a == 0:
        if b == 0:
            # 0*x² + 0*x + c = 0
            if c == 0:
                # 0 = 0, infinité de solutions
                return None
            else:
                # c = 0 avec c != 0, pas de solution
                raise ValueError("Équation impossible: c != 0 avec a = b = 0")
        else:
            # bx + c = 0 => x = -c/b
            return (-c / b,)
    
    # Calcul du discriminant
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        # Deux racines réelles distinctes
        sqrt_delta = math.sqrt(discriminant)
        x1 = (-b + sqrt_delta) / (2 * a)
        x2 = (-b - sqrt_delta) / (2 * a)
        return (x1, x2)
    
    elif discriminant == 0:
        # Une racine double
        x = -b / (2 * a)
        return (x,)
    
    else:
        # Deux racines complexes conjuguées
        real_part = -b / (2 * a)
        imag_part = math.sqrt(-discriminant) / (2 * a)
        x1 = complex(real_part, imag_part)
        x2 = complex(real_part, -imag_part)
        return (x1, x2)


def get_discriminant(a: float, b: float, c: float) -> float:
    """
    Calcule le discriminant de l'équation ax² + bx + c = 0.
    
    Args:
        a: Coefficient de x²
        b: Coefficient de x
        c: Terme constant
    
    Returns:
        La valeur du discriminant (b² - 4ac)
    """
    return b**2 - 4*a*c


def get_discriminant_type(discriminant: float) -> str:
    """
    Détermine le type de discriminant.
    
    Args:
        discriminant: Valeur du discriminant
    
    Returns:
        'positive', 'zero', ou 'negative'
    """
    if discriminant > 0:
        return "positive"
    elif discriminant == 0:
        return "zero"
    else:
        return "negative"


def verify_solution(a: float, b: float, c: float, x: Union[float, complex]) -> bool:
    """
    Vérifie si x est une solution de ax² + bx + c = 0.
    
    Args:
        a, b, c: Coefficients de l'équation
        x: Valeur à vérifier
    
    Returns:
        True si x est une solution (à epsilon près)
    """
    result = a * x**2 + b * x + c
    if isinstance(result, complex):
        return abs(result) < 1e-10
    else:
        return abs(result) < 1e-10


if __name__ == "__main__":
    # Exemples d'utilisation
    print("=== Résolution d'équations du second degré ===\n")
    
    # Exemple 1: Deux racines réelles
    a, b, c = 1, -3, 2
    print(f"Équation: {a}x² + {b}x + {c} = 0")
    print(f"Solutions: {solve_quadratic(a, b, c)}")
    print()
    
    # Exemple 2: Racine double
    a, b, c = 1, -2, 1
    print(f"Équation: {a}x² + {b}x + {c} = 0")
    print(f"Solutions: {solve_quadratic(a, b, c)}")
    print()
    
    # Exemple 3: Racines complexes
    a, b, c = 1, 2, 5
    print(f"Équation: {a}x² + {b}x + {c} = 0")
    print(f"Solutions: {solve_quadratic(a, b, c)}")
