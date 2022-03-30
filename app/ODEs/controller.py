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

import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp
from viktor.core import ViktorController
from viktor.views import DataGroup
from viktor.views import DataItem
from viktor.views import DataResult
from viktor.views import DataView
from viktor.views import PlotlyResult
from viktor.views import PlotlyView

from .helper_functions import ODEfunc
from .helper_functions import get_variable_dict
from .helper_functions import get_variable_list
from .parametrization import ODEParametrization


class ODEController(ViktorController):
    label = 'ODE'
    parametrization = ODEParametrization

    def executeODE(self,params): # function for solving the differential profiles based on user input
        time = [params.time.begin, params.time.end]
        timespan = np.linspace(params.time.begin, params.time.end, params.time.resolution)

        initial_concs = get_variable_list(params.species_array.species, 'concentration')
        applied_reactions = get_variable_list(params.species_array.species, 'matrix')
        reactions = get_variable_list(params.section_reaction_array.reactions, 'reaction')
        names = get_variable_dict(params.species_array.species, 'name')
        constants = get_variable_dict(params.section_reaction_array.reactions, 'rate_constant')

        sol = solve_ivp(ODEfunc, time , initial_concs, t_eval=timespan, args=[constants,
                                                                                reactions,
                                                                                applied_reactions,
                                                                                names])
        return sol


    @DataView('Results numbers', duration_guess=1) #get the changes at all time points for all species
    def get_value_changes(self, params, **kwargs):
        # i = 0
        # names = []
        # for species in params.species_array.species:
        #     names.append(species['name'])
        #     i += 1
        names = [species['name'] for species in params.species_array.species]

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
            runs.append(DataGroup(DataItem(label=names[i], value=list(profile))))
            i+= 1

        result = DataGroup.from_data_groups(runs)

        return DataResult(result)


    @PlotlyView("Plotly view", duration_guess=5) #for viualizing all differential profiles in a plot
    def get_progression_plot(self, params, **kwargs):
        ODE_result = self.executeODE(params)
        fig = go.Figure()

        # names = []
        # for element in params.species_array.species:
        #     names.append(element['name'])
        names = [species['name'] for species in params.species_array.species]

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
