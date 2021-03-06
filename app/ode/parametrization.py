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

from viktor.parametrization import Lookup
from viktor.parametrization import NumberField
from viktor.parametrization import Parametrization
from viktor.parametrization import Section
from viktor.parametrization import Table
from viktor.parametrization import TextField
from viktor.parametrization import ToggleButton


class ODEParametrization(Parametrization):
    """For providing the input fields to users"""
    section_reaction_array = Section('Reaction data')
    section_reaction_array.reactions = Table('reaction data')
    section_reaction_array.reactions.reaction = TextField('Reaction')
    section_reaction_array.reactions.rate_constant = NumberField('Rate constant')

    species_array = Section('Species data')
    species_array.species = Table('Species data')
    species_array.species.name = TextField('Species name')
    species_array.species.concentration = NumberField('Species Concentration')
    species_array.species.matrix = TextField('Applicable reactions')

    time = Section('Time')
    time.begin = NumberField('Begin', default=0)
    time.end = NumberField('End', default=10)
    time.resolution = NumberField('Resolution', default= 10)

    plot_names = Section('Plot names')
    plot_names.toggle = ToggleButton('Change plot names?', default=False)
    plot_names.table = Table('Translations', visible=Lookup('plot_names.toggle'))
    plot_names.table.original = TextField('from')
    plot_names.table.to = TextField('to')
