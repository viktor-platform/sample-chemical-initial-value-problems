from viktor.core import ViktorController
from viktor.views import DataResult, DataGroup, DataView, DataItem, PlotlyResult, PlotlyView

from scipy.integrate import solve_ivp
import numpy as np
import plotly.graph_objects as go

from .parametrization import ODEParametrization
from .helper_functions import get_variable_list, get_variable_dict, ODEfunc

class ODEController(ViktorController):
    label = 'ODE'
    parametrization = ODEParametrization

    def executeODE(self,params):
        time = [params.time.begin, params.time.end]
        timespan = np.linspace(params.time.begin, params.time.end, params.time.resolution)

        initial_concs = get_variable_list(params.species_array.species, 'concentration')
        applied_reactions = get_variable_list(params.species_array.species, 'matrix')
        reactions = get_variable_list(params.section_reaction_array.reactions, 'reaction')
        names = get_variable_dict(params.species_array.species, 'name')
        constants = get_variable_dict(params.section_reaction_array.reactions, 'rate_constant')
        print(initial_concs)
        print(applied_reactions)
        print(reactions)
        print(names)
        print(constants)
        sol = solve_ivp(ODEfunc, time , initial_concs, t_eval = timespan, args=[constants,reactions,applied_reactions,names])
        return sol


    @DataView('Results numbers', duration_guess=1)
    def get_data(self, params, **kwargs):
        i = 0
        names = []
        for species in params.species_array.species:
            names.append(species['name'])
            i += 1

        for replacement in params.plot_names.table:
            i = 0
            for element in names:
                if element == replacement.original:
                    names[i] = replacement.to
                i+=1

        ODE_result = self.executeODE(params)
        runs = []
        i = 0
        for profile in ODE_result.y:
            runs.append(DataGroup(DataItem(label=names[i], value = list(profile))))
            i+= 1

        result = DataGroup.from_data_groups(runs)

        return DataResult(result)


    @PlotlyView("Plotly view", duration_guess=5)
    def get_plotly_view(self, params, **kwargs):
        ODE_result = self.executeODE(params)
        fig = go.Figure()

        names = []
        for element in params.species_array.species:
            names.append(element['name'])

        for replacement in params.plot_names.table:
            i = 0
            for element in names:
                if element == replacement.original:
                    names[i] = replacement.to
                i+=1

        i = 0
        for profile in ODE_result.y:
            fig.add_trace(go.Scatter(x=ODE_result.t, y=profile, name=names[i]))
            i += 1
        return PlotlyResult(fig.to_json())