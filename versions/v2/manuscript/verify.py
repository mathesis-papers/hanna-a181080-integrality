import argparse
from fractions import Fraction
import hashlib
import json
from math import comb


EXPECTED = {
    'A181080': [1, 1, 2, 4, 14, 83, 774, 10641, 255918],
    'A181070': [1, 1, 2, 4, 8, 23, 88, 379, 3044],
    'A166894': [1, 1, 2, 4, 14, 89, 1050, 28983, 2066217],
    'A181082': [1, 1, 2, 6, 34, 375, 15200, 2066401, 450054919],
    'A181074': [1, 1, 2, 5, 23, 231, 5405, 322799, 42761356],
    'A181076': [1, 1, 2, 5, 20, 168, 3659, 204644, 25503314],
    'A181078': [1, 1, 2, 5, 29, 657, 61207, 22168009, 29875987984],
    'A181084': [1, 1, 2, 10, 92, 1367, 87090, 20385333, 6633475836],
}
LOG_IDENTIFIERS = {
    'A181080': 'A181081', 'A181070': 'A181071', 'A166894': 'A166895',
    'A181082': 'A181083', 'A181074': 'A181075', 'A181076': 'A181077',
    'A181078': 'A181079', 'A181084': 'A181085',
}
PRIMES = [2, 3, 5, 7, 11, 13]


def valuation(number, prime):
    assert number > 0
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def binomial_base(identifier, row, column):
    if identifier in ['A181074', 'A181076', 'A181078']:
        return comb(row + column - 1, column)
    return comb(row, column) if column <= row else 0


def power_exponent(identifier, row, column, comparison=False):
    if identifier == 'A181080':
        return row - column + (not comparison)
    if identifier in ['A181070', 'A181074']:
        return column + (not comparison)
    if identifier in ['A166894', 'A181076']:
        return row
    if identifier == 'A181082':
        return row + column
    if identifier == 'A181078':
        return row + column - 1
    if identifier == 'A181084':
        return row + column + 1
    raise ValueError(identifier)


def array_value(identifier, row, column, comparison=False, modulus=None):
    if identifier not in ['A181074', 'A181076', 'A181078'] and column > row:
        return 0
    base = binomial_base(identifier, row, column)
    exponent = power_exponent(identifier, row, column, comparison)
    return pow(base, exponent) if modulus is None else pow(base, exponent, modulus)


def logarithm_coefficients(identifier, degree, comparison=False):
    result = [Fraction(0) for index in range(degree + 1)]
    for row in range(1, degree + 1):
        for column in range(degree - row + 1):
            result[row + column] += Fraction(array_value(identifier, row, column, comparison), row)
    return result


def exponential_recurrence(logarithm):
    result = [Fraction(1)]
    for degree in range(1, len(logarithm)):
        result.append(sum((index * logarithm[index] * result[degree - index]
                           for index in range(1, degree + 1)), Fraction(0)) / degree)
    return result


def mobius(number):
    sign = 1
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            number //= divisor
            sign = -sign
            if number % divisor == 0:
                return 0
        divisor += 1
    return -sign if number > 1 else sign


def euler_product(ghost):
    degree = len(ghost) - 1
    result = [1] + [0] * degree
    exponents = []
    for index in range(1, degree + 1):
        numerator = sum(mobius(divisor) * ghost[index // divisor]
                        for divisor in range(1, index + 1) if index % divisor == 0)
        assert numerator.denominator == 1 and numerator.numerator % index == 0
        exponent = numerator.numerator // index
        exponents.append(exponent)
        factor = [1]
        for order in range(1, degree // index + 1):
            numerator = factor[-1] * (exponent + order - 1)
            assert numerator % order == 0
            factor.append(numerator // order)
        result = [sum(result[target - order * index] * factor[order]
                      for order in range(target // index + 1)) for target in range(degree + 1)]
    return result, exponents


def direct_exponential(logarithm):
    degree = len(logarithm) - 1
    term = [Fraction(1)] + [Fraction(0)] * degree
    result = list(term)
    for order in range(1, degree + 1):
        term = [sum((term[target - index] * logarithm[index]
                     for index in range(1, target + 1)), Fraction(0)) / order
                for target in range(degree + 1)]
        result = [left + right for left, right in zip(result, term)]
    return result


def digest(values):
    return hashlib.sha256(json.dumps([str(value) for value in values], separators=(',', ':')).encode()).hexdigest()


def logarithmic_formula(identifier, degree):
    result = [Fraction(0)]
    for index in range(1, degree + 1):
        upper = index - 1 if identifier in ['A181074', 'A181076', 'A181078'] else index // 2
        total = Fraction(0)
        for column in range(upper + 1):
            row = index - column
            base = comb(index - 1, column) if upper == index - 1 and identifier in ['A181074', 'A181076', 'A181078'] else comb(row, column)
            exponent = power_exponent(identifier, row, column)
            total += Fraction(index * base ** exponent, row)
        result.append(total)
    return result


def linear_family_checks():
    degree = 12
    prime_list = [2, 3, 5]
    count = 0
    coefficient_checks = 0
    series_list = [[1, 1, 1], [1, 2, 0, 1], [1] * (5 * degree + 1)]
    parameters = [(0, 0, 1), (0, 2, 2), (1, 1, 1), (1, 0, 0),
                  (2, 1, 0), (1, 1, -1), (2, 3, -1)]
    for series in series_list:
        powers = [[1] + [0] * (5 * degree)]
        for row in range(1, 5 * degree + 1):
            powers.append([sum(powers[-1][column - offset] * series[offset]
                               for offset in range(min(column, len(series) - 1) + 1))
                           for column in range(5 * degree + 1)])
        for row_factor, column_factor, shift in parameters:
            for row in range(1, 7):
                for column in range(13):
                    base = powers[row][column]
                    exponent = row_factor * row + column_factor * column + shift
                    value = base ** exponent
                    assert column * value % row == 0
                    for prime in prime_list:
                        modulus = prime ** (valuation(row, prime) + 1)
                        scaled_exponent = row_factor * prime * row + column_factor * prime * column + shift
                        scaled = pow(powers[prime * row][prime * column], scaled_exponent, modulus)
                        assert (scaled - pow(base, exponent, modulus)) % modulus == 0
                        count += 1
            logarithm = [Fraction(0)] * (degree + 1)
            for row in range(1, degree + 1):
                for column in range(degree - row + 1):
                    exponent = row_factor * row + column_factor * column + shift
                    logarithm[row + column] += Fraction(powers[row][column] ** exponent, row)
            coefficients = exponential_recurrence(logarithm)
            assert all(value.denominator == 1 for value in coefficients)
            assert direct_exponential(logarithm) == coefficients
            product, unused = euler_product([index * value for index, value in enumerate(logarithm)])
            assert product == coefficients
            coefficient_checks += 1
    return {'series': ['1+t+t^2', '1+2t+t^3', '1/(1-t)'],
            'parameters_r_s_delta': parameters, 'rows': [1, 6], 'columns': [0, 12],
            'primes': prime_list, 'prime_scaling_checks': count,
            'integral_exponential_checks': coefficient_checks, 'coefficient_degree': degree}


def main():
    parser = argparse.ArgumentParser(description='Exact finite checks for the formal exponentials in note.tex.')
    parser.add_argument('--degree', type=int, default=48)
    arguments = parser.parse_args()
    assert 8 <= arguments.degree <= 96
    degree = arguments.degree
    families = {}
    for identifier, expected in EXPECTED.items():
        logarithm = logarithm_coefficients(identifier, degree)
        ghost = [index * value for index, value in enumerate(logarithm)]
        assert ghost == logarithmic_formula(identifier, degree)
        assert all(value.denominator == 1 for value in ghost)
        coefficients = exponential_recurrence(logarithm)
        assert all(value.denominator == 1 for value in coefficients)
        assert coefficients[:len(expected)] == expected
        product, exponents = euler_product(ghost)
        assert product == coefficients
        direct_degree = min(16, degree)
        assert direct_exponential(logarithm[:direct_degree + 1]) == coefficients[:direct_degree + 1]
        array_checks = 0
        for prime in PRIMES:
            for row in range(1, 25):
                modulus = prime ** (valuation(row, prime) + 1)
                for column in range(25):
                    assert column * array_value(identifier, row, column, modulus=row) % row == 0
                    difference = (array_value(identifier, prime * row, prime * column, modulus=modulus)
                                  - array_value(identifier, row, column, modulus=modulus))
                    assert difference % modulus == 0
                    array_checks += 1
        ghost_checks = 0
        for prime in PRIMES:
            for index in range(1, degree // prime + 1):
                modulus = prime ** (valuation(index, prime) + 1)
                assert (ghost[prime * index] - ghost[index]) % modulus == 0
                ghost_checks += 1
        families[identifier] = {
            'degrees': [0, degree], 'oeis_prefix': expected,
            'coefficient_sha256': digest(coefficients),
            'euler_exponent_sha256': digest(exponents),
            'direct_exponential_degrees': [0, direct_degree],
            'array_checks': array_checks, 'ghost_checks': ghost_checks,
            'logarithmic_sequence': LOG_IDENTIFIERS[identifier],
            'logarithmic_coefficient_sha256': digest(ghost[1:]),
            'logarithmic_prefix': [str(value) for value in ghost[1:9]],
        }
        if identifier == 'A181080':
            assert ghost[1:9] == [1, 3, 7, 39, 336, 4077, 68461, 1955295]
    comparisons = {}
    for identifier, expected in [('A181080', Fraction(327, 2)),
                                 ('A181070', Fraction(45, 2)),
                                 ('A181074', Fraction(1481, 2))]:
        logarithm = logarithm_coefficients(identifier, 6, comparison=True)
        coefficients = exponential_recurrence(logarithm)
        assert coefficients[6] == expected
        assert all(value.denominator == 1 for value in coefficients[:6])
        assert direct_exponential(logarithm) == coefficients
        comparisons[identifier] = {
            'first_nonintegral_degree': 6, 'coefficient': str(expected),
            'ghost_prefix': [str(index * logarithm[index]) for index in range(1, 7)],
        }
    correct_ghost = logarithmic_formula('A181078', 4)[4]
    other_ghost = logarithmic_formula('A181076', 4)[4]
    assert correct_ghost == 95 and other_ghost == 59
    print(json.dumps({
        'arithmetic': 'exact integers and rational numbers',
        'scope': 'Finite coefficient, Euler-product and congruence checks; the unbounded statements have written proofs in note.tex.',
        'primes': PRIMES, 'array_rows': [1, 24], 'array_columns': [0, 24],
        'families': families, 'nonintegral_comparisons': comparisons,
        'linear_exponent_families': linear_family_checks(),
        'corrected_A181079_cross_reference': {
            'index': 4, 'A181079': int(correct_ghost), 'A181077': int(other_ghost),
            'correct_exponential': 'A181078',
            'identity': 'sum(A181079(m)*x^m,m>=1)=x*A181078_prime(x)/A181078(x)',
        },
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
