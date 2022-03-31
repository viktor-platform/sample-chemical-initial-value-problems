"""Copyright (c) 2022 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re

def get_variable_list(munch, keyword): #these 2 functions are to make the data handleable
    result = [element[keyword] for element in munch]
    return result


def get_variable_dict(munch, keyword): #some things need to be findable by order of input
    i = 0
    result = []
    for element in munch:
        result.append({'index': i, keyword: element[keyword]})
        i += 1
    return result

def react_to_arithmetic(string, react_num, concs, constants, new_names):
  pattern = re.compile(r'[-+*]*[^-+*]+')
  matches = pattern.finditer(string)
  constant = constants[react_num]['rate_constant']
  total = constant
  for match in matches:
    value = match.group()
    if value == '0':
      total = 0
    elif value[0] == '*':
      total *= concs[new_names[value[1:]]]
    else:
      total *= concs[new_names[value]]
  return total

def matrix_to_arithmetic(string):
  total = eval(string)
  return total

def ODEfunc(t, concs, constants, reacts, matrices, names): #lots of string replacement to get usable python code
    reacts = {f'r{i + 1}': react_to_arithmetic(reacts[i], i, concs, constants, names) for i in range(len(reacts))}
    matrix_replace = []
    for matrix in matrices:
        res = matrix
        for reaction, value in reacts.items():
            if reaction in matrix:
                res = res.replace(reaction, str(reacts[reaction]))
        matrix_replace.append(res)
    matrices = matrix_replace
    changes = [matrix_to_arithmetic(matrix) for matrix in matrices]
    return changes