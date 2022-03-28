
def get_variable_list(munch, keyword): #these 2 functions are to make the data handleable
    result = []
    for element in munch:
        result.append(element[keyword])
    return result


def get_variable_dict(munch, keyword):
    i = 0
    result = []
    for element in munch:
        result.append({'index': i, keyword: element[keyword]})
        i += 1
    return result

def ODEfunc(t, concs, constants, reacts, matrices, names): #lots of string replacement to get usable python code
    species_replace = [] #replace species with their corresponding current concentrations for arithmetic
    for reaction in reacts:
        res = reaction
        for entry in names:
            if entry['name'] in reaction:
                res = res.replace(entry['name'], f"concs[{entry['index']}]")
        species_replace.append(res)
    reacts = species_replace

    const_replacements = [] #replace the constants in the string with the user defined value
    for const in constants:
        for reaction in reacts:
            if f"k{const['index'] + 1}" in reaction:
                res = reaction.replace(f"k{const['index'] + 1}", f"constants[{const['index']}]['rate_constant']")
                const_replacements.append(res)
    reacts = const_replacements

    for constant in constants: #convert the strings to floats
        constant['rate_constant'] = float(constant['rate_constant'])

    reaction_dict = {} #calculate the value of the separate reactions
    i = 0
    for reaction in reacts:
        reaction_dict[f'r{i + 1}'] = str(eval(reaction))
        i += 1

    matrices_replace = [] #calculate the change is species per species by arithmetic of applicable individual reaction
    for matrix in matrices:
        res = matrix
        for react in reaction_dict.keys():
            if react in matrix:
                res = res.replace(react, eval(f"reaction_dict['{react}']"))
        matrices_replace.append(eval(res))
    matrices = matrices_replace

    return matrices