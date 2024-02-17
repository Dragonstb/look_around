import numpy as np
import utils

_letters = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
_entity_type = np.array(['SE', 'Holding', 'Ltd.'])

# company description

_cd_grammar = {
    '*start': [
        ['*S', '*CD', 'in', '*CL', '.', '*BS', '*BG', '*BT', '.'],
        ['*S', '*CD', 'in', '*CL', '.', '*BSa', '*BGa', '*BT', '.'],
        ['*S', '*CD', '*BG', '*CL', '.', '*BS', '*BG', '*BT', '.'],
        ['*S', '*CD', 'in', '*CL', '.', '*BSa', '*BGa', '*BT', '.'],
        ['*S', 'are', '*BG', '*CL']
    ],
    '*S': [['we'], ['our company'], ['{company_name}']],
    '*CD': [['are a', '*CA', '*C'], ['are a', '*C'], ['are', '*CH']],
    '*CL': [
        ['the field of', '*CF'],
        ['the', '*CF', 'sector'],
        ['the', '*CF', 'markets'],
    ],
    '*BS': [['our goal is'], ['with our products we']],
    '*BSa': [['with our solutions we']],
    '*BG': [
        ['*BR', '*BA', '*BI', 'for'],
        ['*BR', '*BI', 'for'],
        ['revolutionizing']
    ],
    '*BGa': [
        ['*BRa', '*BA', '*BI', 'for'],
        ['*BRa', '*BI', 'for'],
        ['revolutionize']
    ],
    '*BT': [
        ['the use of {fields}'],
    ],
    '*CA': [['innovative'], ['family-led'], ['small'], ['large'], ['leading'], ['ambitious'], ['encouraged'], ['the leading']],
    '*C': [['company'], ['start up']],
    '*CH': [['the market leader'], ['the number one company'], ['the largest company'], ['one of the largest players']],
    '*BR': [['are providing'], ['are offering'], ['are coming up with']],
    '*BRa': [['provide'], ['offer'], ['come up with']],
    '*BA': [['novel'], ['smart'], ['outstanding'], ['innovative']],
    '*BI': [['ideas'], ['solutions'], ['products'], ['services']],
    '*CF': [['energy'], ['logistics'], ['public health'], ['business intelligence'], ['software development'], ['B2B'], ['transport'], ['automotion']]
}

# yes, it is stupid for now. In the future, there will be lists for each field
_comp_fields = ['solar energy', 'wind energy', 'oil', 'coal', 'nuclear power', 'logistics', 'transport', 'screening', 'cancer prevention', 'data analysis',
                'process analysis', 'process mining', 'coding styles', 'cloud platforms', 'SaaS', 'traffic optimization', 'public transport', 'car sharing']


def gen_company_name() -> str:
    """
    Generates a company name. Do not expect too much.

    return:
    An obviously very random company name.
    """
    rand = np.random.default_rng()
    rolls = rand.random(size=4)
    rollIdx = 0
    name = []
    # one or two individual names
    if rolls[rollIdx] < 0.8:
        numLetters = int(7 + 7 * rolls[rollIdx+1])
        name.append(
            ''.join(utils.pick_several_from_array(_letters, size=numLetters)))
    else:
        numLetters = int(4 + 3 * rolls[rollIdx+1])
        name.append(
            ''.join(utils.pick_several_from_array(_letters, size=numLetters)))
        numLetters = int(4 + 3 * rolls[rollIdx+2])
        name.append(
            ''.join(utils.pick_several_from_array(_letters, size=numLetters)))
    rollIdx = rollIdx + 3
    # entity type
    if rolls[rollIdx] < 0.8:
        name.append(utils.pick_from_array(_entity_type))

    return ' '.join(name)


def gen_company_desc(company_name: str) -> str:
    """
    Generates a description of what the company works on.
    The result might be a bit funny, though :)

    company name:
    Name of the company. It might be incorporated into the description.

    returns:
    One or two sentences what the company does.
    """
    rand = np.random.default_rng()
    sentence = ['*start']

    # resolve grammar
    while len(list(filter(lambda x: x[0] == '*', sentence))) > 0:
        # first element starting with *
        symbol = next(filter(lambda x: x[0] == '*', sentence))
        idx = sentence.index(symbol)
        options = _cd_grammar[symbol]
        insert = options[rand.integers(0, len(options))]
        sentence = sentence[:idx] + insert + sentence[idx+1:]

    # pick fields the company is working in
    numFields = rand.integers(1, 4)
    if numFields == 1:
        idx = rand.integers(0, len(_comp_fields))
        fields = _comp_fields[idx]
    elif numFields == 2:
        idx1 = rand.integers(0, len(_comp_fields))
        idx2 = rand.integers(0, len(_comp_fields))
        fields = _comp_fields[idx1] + ' and ' + _comp_fields[idx2]
    else:
        idx1 = rand.integers(0, len(_comp_fields))
        idx2 = rand.integers(0, len(_comp_fields))
        idx3 = rand.integers(0, len(_comp_fields))
        fields = _comp_fields[idx1] + ', ' + \
            _comp_fields[idx2] + ' and ' + _comp_fields[idx3]

    # assemble to single string
    description = ' '.join(sentence)
    description = description.replace(' .', '.').capitalize()

    return description.format(company_name=company_name, fields=fields)


# _______________  interactive tests  _______________

def _test_comp_desc():
    return gen_company_desc('Look Around SE')
