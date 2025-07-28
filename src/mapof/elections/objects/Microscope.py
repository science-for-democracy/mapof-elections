import os

class Microscope:

    def __init__(self, fig, ax, experiment_id, label, object_type):
        self.fig = fig
        self.ax = ax

        if experiment_id is None:
            self.experiment_id = 'online'
        else:
            self.experiment_id = experiment_id

        if label is None:
            self.label = 'noname'
        else:
            self.label = label

        self.object_type = object_type

    def show(self):
        """ Display the microscope plot in a window. """
        self.fig.show()

    def save_to_file(self, saveas='default'):
        """ Save the microscope plot to a file. """

        path_to_folder = os.path.join(os.getcwd(), "images", self.experiment_id)
        if not os.path.isdir(path_to_folder):
            os.makedirs(path_to_folder, exist_ok=True)

        if saveas == 'default':
            saveas = f'{self.label}_{self.object_type}'

        file_name = os.path.join(os.getcwd(), "images", self.experiment_id, f'{saveas}.png')
        self.fig.savefig(file_name, bbox_inches='tight', dpi=100)

    def show_and_save(self, saveas='default'):
        """ Display the microscope plot and save it to a file. """
        self.show()
        self.save_to_file(saveas=saveas)