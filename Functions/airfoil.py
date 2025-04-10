import numpy as np
import plotly.graph_objects as go
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='airfoil.log',
                    encoding='utf-8', level=logging.DEBUG)


class Airfoil:
    """A glider airfoil representation"""

    def __init__(self, airfoil_name="Generic Airfoil", chord_length=1.0, upper_surface=None, lower_surface=None) -> None:
        self.airfoil_name: str = airfoil_name
        self.chord_length: float = chord_length
        self.upper_surface: list[np.ndarray] | None = upper_surface
        self.lower_surface: list[np.ndarray] | None = lower_surface

        if self.lower_surface is None:
            self.lower_surface = []

        if self.upper_surface is None:
            self.upper_surface = []

    def generate_upper_lower_surfaces(self, filepath: str):
        try:
            converted_string_array = self._read_xflr_file(filepath)

            upper_to_lower_threshold = [i for i, arr in enumerate(
                converted_string_array) if np.array_equal(arr, np.array([0.0, 0.0]))][0]
            self.upper_surface = converted_string_array[0:upper_to_lower_threshold+1]
            self.lower_surface = converted_string_array[upper_to_lower_threshold:]

            # Ensure that airfoil end points
            if not np.array_equal(self.upper_surface[0], np.array([1.0, 0.0])):
                self.upper_surface[0] = np.array([1.0, 0.0])

            if not np.array_equal(self.lower_surface[-1], np.array([1.0, 0.0])):
                self.lower_surface[-1] = np.array([1.0, 0.0])

        except FileNotFoundError:
            logger.error("File not found")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def adjust_chord_length(self, new_chord_length: float) -> None:
        self.upper_surface = [point * new_chord_length /
                              self.chord_length for point in self.upper_surface]
        self.lower_surface = [point * new_chord_length /
                              self.chord_length for point in self.lower_surface]

    def _print_points(self) -> None:
        for point in self.upper_surface:
            print(f"Upper: {point}")
        for point in self.lower_surface:
            print(f"Lower: {point}")

    def _plot_airfoil(self, title="") -> None:
        fig = go.Figure()
        # fig.add_trace(go.Scatter(x=[point[0] for point in self.points], y=[point[1] for point in self.points], mode="lines"))
        fig.add_trace(go.Scatter(x=[point[0] for point in self.upper_surface], y=[
                      point[1] for point in self.upper_surface], mode="lines"))
        fig.add_trace(go.Scatter(x=[point[0] for point in self.lower_surface], y=[
                      point[1] for point in self.lower_surface], mode="lines"))

        x_figure_range = np.array([-0.5, 1.5])
        y_figure_range = np.array([-1, 1])*9/16
        fig.update_layout(xaxis_range=x_figure_range,
                          yaxis_range=y_figure_range*9/16,
                          title=title)
        fig.show()

    def _read_xflr_file(self, filepath: str) -> list[np.ndarray]:
        with open(filepath, "r") as file:
            content: list[str] = file.readlines()
            self.airfoil_name: str = content[0].strip()
            converted_string_array: list[str] = []

            for line in content[1:]:
                split_line = line.strip().split()
                point = np.array(
                    [float(split_line[0]), float(split_line[1])])
                converted_string_array.append(point)

        return converted_string_array

if __name__ == "__main__":
    airfoil = Airfoil()
    airfoil.generate_upper_lower_surfaces(
        "/home/christian/Documents/Python_Projects/PGLineTrim/Airfoils/NACA 2412.dat")
    airfoil._plot_airfoil()
    # airfoil.adjust_chord_length(2.0)
    # airfoil._plot_airfoil()
