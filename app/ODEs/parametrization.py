from viktor.parametrization import Parametrization, Section, NumberField, TextField, Table, ToggleButton, Lookup


class ODEParametrization(Parametrization):
    section_reaction_array = Section('Reaction data')
    section_reaction_array.reactions = Table('reaction data')
    section_reaction_array.reactions.reaction = TextField('Reaction')
    section_reaction_array.reactions.rate_constant = TextField('Rate constant')

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


