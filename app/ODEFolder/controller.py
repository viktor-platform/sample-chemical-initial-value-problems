from viktor.core import ViktorController


class ODEFolderController(ViktorController):
    label = 'ODE Folder'
    children = ['ODE'] #add all entities
    show_children_as = 'Cards'  # or 'Table'

    viktor_convert_entity_field = True
