#!/usr/bin/env python

import sys
import json

def read_patser_matrix(infile):
    matrix = {}
    for line in open(infile, 'r'):
        parts = line.split()
        assert parts[1] == '|', "Invalid input file"
        assert parts[0] in ('A', 'T', 'G', 'C'), "invalid input file"
        matrix[parts[0]] = map(int, parts[2:])

    return matrix

def convert_probabilities(a, c, g, t):
    total = a + c + g + t
    factor = 100.0 / total
    return (a * factor, c * factor, g * factor, t * factor)

def write_patscan_pattern(outfile, matrix):
    prob_a = matrix['A']
    prob_c = matrix['C']
    prob_g = matrix['G']
    prob_t = matrix['T']
    with open(outfile, 'w') as h:
        h.write('{')
        for i in range(0, len(prob_a)):
            h.write("(%d, %d, %d, %d)" %
              convert_probabilities(prob_a[i], prob_c[i], prob_g[i], prob_t[i]))

        h.write('} > %s' % (50 * len(prob_a)))


def write_patscanui_json(outfile, matrix):
    elements = []
    pattern = {
        'type': 'weight',
        'named': False
    }
    js_matrix = []

    prob_a = matrix['A']
    prob_c = matrix['C']
    prob_g = matrix['G']
    prob_t = matrix['T']

    for i in range(0, len(prob_a)):
        a, c, g, t = convert_probabilities(prob_a[i], prob_c[i],
                                           prob_g[i], prob_t[i])
        js_matrix.append({'a': a, 'c': c, 'g': g, 't': t})

    pattern['matrix'] = js_matrix
    pattern['weight'] = 50 * len(prob_a)

    elements.append(pattern)

    with open(outfile, 'w') as h:
        h.write(json.dumps(dict(elements=elements, molecule_type="DNA")))


def main():
    matrix = read_patser_matrix(sys.argv[1])
    write_patscan_pattern(sys.argv[2], matrix)
    write_patscanui_json(sys.argv[3], matrix)

if __name__ == "__main__":
    main()
