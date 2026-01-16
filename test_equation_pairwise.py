"""
Tests Unittest pour l'équation du second degré avec Pairwise Testing
INF563 - Test Logiciel

Ce module teste la fonction solve_quadratic en utilisant des cas de test
générés par l'approche pairwise pour réduire le nombre de tests tout
en maintenant une bonne couverture.
"""

import unittest
import math
from equation_solver import solve_quadratic, get_discriminant, verify_solution
from pairwise_generator import generate_pairwise_tests, VALUES


class TestEquationSolverBasic(unittest.TestCase):
    """Tests unitaires de base pour le solveur d'équations."""
    
    def test_two_real_roots(self):
        """Test: Deux racines réelles distinctes (discriminant > 0)."""
        # x² - 3x + 2 = 0 => (x-1)(x-2) = 0, solutions: 1, 2
        solutions = solve_quadratic(1, -3, 2)
        self.assertEqual(len(solutions), 2)
        self.assertAlmostEqual(max(solutions), 2.0)
        self.assertAlmostEqual(min(solutions), 1.0)
    
    def test_double_root(self):
        """Test: Une racine double (discriminant = 0)."""
        # x² - 2x + 1 = 0 => (x-1)² = 0, solution: 1
        solutions = solve_quadratic(1, -2, 1)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0], 1.0)
    
    def test_complex_roots(self):
        """Test: Racines complexes (discriminant < 0)."""
        # x² + 1 = 0 => x = ±i
        solutions = solve_quadratic(1, 0, 1)
        self.assertEqual(len(solutions), 2)
        self.assertTrue(isinstance(solutions[0], complex))
        self.assertAlmostEqual(solutions[0].imag, 1.0)
        self.assertAlmostEqual(solutions[1].imag, -1.0)
    
    def test_linear_equation(self):
        """Test: Équation linéaire (a = 0, b != 0)."""
        # 0*x² + 2x + 4 = 0 => x = -2
        solutions = solve_quadratic(0, 2, 4)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0], -2.0)
    
    def test_infinite_solutions(self):
        """Test: Infinité de solutions (a = b = c = 0)."""
        result = solve_quadratic(0, 0, 0)
        self.assertIsNone(result)
    
    def test_no_solution(self):
        """Test: Pas de solution (a = b = 0, c != 0)."""
        with self.assertRaises(ValueError):
            solve_quadratic(0, 0, 5)


class TestEquationSolverPairwise(unittest.TestCase):
    """Tests pairwise pour le solveur d'équations."""
    
    @classmethod
    def setUpClass(cls):
        """Génère les cas de test pairwise une seule fois."""
        cls.test_cases = generate_pairwise_tests()
        print(f"\n=== Tests Pairwise: {len(cls.test_cases)} cas de test ===")
    
    def test_all_pairwise_cases(self):
        """
        Exécute tous les cas de test pairwise.
        
        Vérifie que:
        1. La fonction ne lève pas d'exception non attendue
        2. Les solutions retournées sont correctes (vérification)
        """
        passed = 0
        errors = []
        
        for i, case in enumerate(self.test_cases):
            a, b, c = case['a'], case['b'], case['c']
            
            try:
                result = solve_quadratic(a, b, c)
                
                # Vérifier les solutions si disponibles
                if result is not None:
                    for x in result:
                        self.assertTrue(
                            verify_solution(a, b, c, x),
                            f"Solution incorrecte pour a={a}, b={b}, c={c}: x={x}"
                        )
                
                passed += 1
                
            except ValueError as e:
                # ValueError est attendu pour certains cas (a=b=0, c!=0)
                if a == 0 and b == 0 and c != 0:
                    passed += 1
                else:
                    errors.append(f"Cas {i}: a={a}, b={b}, c={c} - Erreur inattendue: {e}")
            
            except Exception as e:
                errors.append(f"Cas {i}: a={a}, b={b}, c={c} - Exception: {e}")
        
        if errors:
            for err in errors[:5]:  # Afficher les 5 premières erreurs
                print(err)
        
        self.assertEqual(len(errors), 0, f"{len(errors)} erreurs sur {len(self.test_cases)} tests")
        print(f"✓ {passed}/{len(self.test_cases)} cas passés")


class TestDiscriminantCases(unittest.TestCase):
    """Tests pour les différents types de discriminant."""
    
    def setUp(self):
        """Configuration des valeurs de test."""
        self.values = VALUES
    
    def test_positive_discriminant_cases(self):
        """Test des cas avec discriminant positif."""
        # a=1, b=5, c=4 => delta = 25 - 16 = 9 > 0
        delta = get_discriminant(1, 5, 4)
        self.assertGreater(delta, 0)
        
        solutions = solve_quadratic(1, 5, 4)
        self.assertEqual(len(solutions), 2)
        # Vérifier que les solutions sont réelles
        for x in solutions:
            self.assertIsInstance(x, float)
    
    def test_zero_discriminant_cases(self):
        """Test des cas avec discriminant nul."""
        # a=1, b=2, c=1 => delta = 4 - 4 = 0
        delta = get_discriminant(1, 2, 1)
        self.assertEqual(delta, 0)
        
        solutions = solve_quadratic(1, 2, 1)
        self.assertEqual(len(solutions), 1)
    
    def test_negative_discriminant_cases(self):
        """Test des cas avec discriminant négatif."""
        # a=1, b=1, c=1 => delta = 1 - 4 = -3 < 0
        delta = get_discriminant(1, 1, 1)
        self.assertLess(delta, 0)
        
        solutions = solve_quadratic(1, 1, 1)
        self.assertEqual(len(solutions), 2)
        for x in solutions:
            self.assertIsInstance(x, complex)


class TestEdgeCases(unittest.TestCase):
    """Tests des cas limites."""
    
    def test_large_coefficients(self):
        """Test avec de grands coefficients."""
        solutions = solve_quadratic(10, 10, -10)
        self.assertIsNotNone(solutions)
        for x in solutions:
            self.assertTrue(verify_solution(10, 10, -10, x))
    
    def test_small_coefficients(self):
        """Test avec de petits coefficients."""
        solutions = solve_quadratic(0.5, -0.5, 0)
        self.assertIsNotNone(solutions)
        # x(0.5x - 0.5) = 0 => x = 0 ou x = 1
        self.assertTrue(0.0 in solutions or any(abs(x) < 1e-10 for x in solutions))
    
    def test_negative_a(self):
        """Test avec a négatif."""
        # -x² + 4 = 0 => x² = 4 => x = ±2
        solutions = solve_quadratic(-1, 0, 4)
        self.assertEqual(len(solutions), 2)
        solutions_abs = sorted([abs(x) for x in solutions])
        self.assertAlmostEqual(solutions_abs[0], 2.0)
        self.assertAlmostEqual(solutions_abs[1], 2.0)
    
    def test_all_negative_coefficients(self):
        """Test avec tous les coefficients négatifs."""
        solutions = solve_quadratic(-1, -2, -1)
        # Discriminant = 4 - 4 = 0
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0], -1.0)


class TestVerifySolution(unittest.TestCase):
    """Tests pour la fonction de vérification."""
    
    def test_valid_real_solution(self):
        """Test de vérification avec solution réelle valide."""
        # x² - 4 = 0 => x = 2 est une solution
        self.assertTrue(verify_solution(1, 0, -4, 2.0))
        self.assertTrue(verify_solution(1, 0, -4, -2.0))
    
    def test_invalid_solution(self):
        """Test de vérification avec solution invalide."""
        # x² - 4 = 0 => x = 3 n'est pas une solution
        self.assertFalse(verify_solution(1, 0, -4, 3.0))
    
    def test_complex_solution(self):
        """Test de vérification avec solution complexe."""
        # x² + 1 = 0 => x = i est une solution
        self.assertTrue(verify_solution(1, 0, 1, 1j))
        self.assertTrue(verify_solution(1, 0, 1, -1j))


if __name__ == "__main__":
    # Configuration du runner avec plus de verbosité
    unittest.main(verbosity=2)
