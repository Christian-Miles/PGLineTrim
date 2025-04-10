from airfoil import Airfoil
import numpy as np
import logging
from scipy.spatial.distance import euclidean
from customfunctions import resample_path_with_endpoints
import plotly.graph_objects as go

logger = logging.getLogger(__name__)
logging.basicConfig(filename='airfoiltools.log', encoding='utf-8', level=logging.DEBUG)

class AirfoilTools: 
    def morph_profile(self, airfoil1: Airfoil, airfoil2: Airfoil, percentage: float) -> Airfoil:
        """Morphs two airfoils together based on a percentage. The percentage is the percentage of the first airfoil in the final airfoil.

        Args:
            airfoil1 (Airfoil): The starting airfoil
            airfoil2 (Airfoil): The airfoil to morph into
            percentage (float): The percentage of morph between the starting and final airfoil

        Returns:
            Airfoil: The morph of airfoil1 into airfoil2
        """

        # Generate any errors if exist
        if not isinstance(airfoil1, Airfoil):
            raise TypeError("Airfoil1 must be an instance of Airfoil")
        if not isinstance(airfoil2, Airfoil):
            raise TypeError("Airfoil2 must be an instance of Airfoil")
        if not isinstance(percentage, (int, float)):
            raise TypeError("Percentage must be a number")
        if percentage < 0.0 or percentage > 1.0:
            raise ValueError("Percentage must be between 0.0 and 1.0")
        if len(airfoil1.upper_surface) != len(airfoil2.upper_surface) or len(airfoil1.lower_surface) != len(airfoil2.lower_surface):
            raise ValueError("Airfoils must have the same number of points")
        
        # Morph upper surface
        morphed_upper_surface = []
        for airfoil1_point, airfoil2_point in zip(airfoil1.upper_surface, airfoil2.upper_surface):
            morphed_upper_surface.append(airfoil1_point + (airfoil2_point - airfoil1_point) * percentage)
            
        # Morph lower surface
        morphed_lower_surface = []
        for airfoil1_point, airfoil2_point in zip(airfoil1.lower_surface, airfoil2.lower_surface):
            morphed_lower_surface.append(airfoil1_point + (airfoil2_point - airfoil1_point)  * percentage)
    
        # Instantiate morphed profile
        morphed_airfoil = Airfoil(upper_surface=morphed_upper_surface, lower_surface=morphed_lower_surface)

        return morphed_airfoil

    def _arc_length_resample(self, airfoil_to_resample: Airfoil, numpoints: int) -> Airfoil:
        """Applies arc length resampling to an airfoil.

        Args:
            airfoil (Airfoil): _description_
            numpoints (int): _description_

        Returns:
            resampled_airfoil (Airfoil): _description_
        """

        resampled_upper_surface: list[np.ndarray] = []
        resampled_lower_surface: list[np.ndarray] = []

        resampled_upper_surface = resample_path_with_endpoints(airfoil_to_resample.upper_surface, numpoints)
        resampled_lower_surface = resample_path_with_endpoints(airfoil_to_resample.lower_surface, numpoints)
        
        resampled_airfoil = Airfoil(airfoil_name=airfoil_to_resample.airfoil_name, upper_surface=resampled_upper_surface, lower_surface=resampled_lower_surface)

        return resampled_airfoil

if __name__=="__main__":
    # Test resampling
    numpoints = 20
    resampling_steps = 100
    airfoil = Airfoil()
    airfoil.generate_upper_lower_surfaces("/home/christian/Documents/Python_Projects/PGLineTrim/Airfoils/NACA 2412.dat")
    airfoil_tools = AirfoilTools()
    resampled_airfoil = airfoil_tools._arc_length_resample(airfoil, numpoints)
    airfoil._plot_airfoil("Airfoil 1")
    resampled_airfoil._plot_airfoil("Resampled Airfoil 1")

    # Test profile morphing
    airfoil2 = Airfoil()
    airfoil2.generate_upper_lower_surfaces("/home/christian/Documents/Python_Projects/PGLineTrim/Airfoils/test.dat")
    airfoil2._plot_airfoil("Airfoil 2")
    airfoil2 = airfoil_tools._arc_length_resample(airfoil2, numpoints)
    

    morphed_airfoil = airfoil_tools.morph_profile(resampled_airfoil, airfoil2, 0.5)
    morphed_airfoil._plot_airfoil("50% Morphed Airfoil (between 1 and 2)")
    
    fig = go.Figure()
    morphed_steps = np.arange(0, 1.01, 1/resampling_steps)  # Include 1.0 in the range

    # Create all traces but set them initially invisible
    for i, step in enumerate(morphed_steps):
        # Calculate morphed airfoil for this step first
        morphed_airfoil = airfoil_tools.morph_profile(resampled_airfoil, airfoil2, step)
        
        # Add upper surface trace
        fig.add_trace(go.Scatter(
            x=[point[0] for point in morphed_airfoil.upper_surface],
            y=[point[1] for point in morphed_airfoil.upper_surface],
            mode="lines",
            name=f"Upper {step:.1f}",
            visible=(i==0)  # Only first step visible initially
        ))
        
        # Add lower surface trace
        fig.add_trace(go.Scatter(
            x=[point[0] for point in morphed_airfoil.lower_surface],
            y=[point[1] for point in morphed_airfoil.lower_surface],
            mode="lines",
            name=f"Lower {step:.1f}",
            visible=(i==0)  # Only first step visible initially
        ))

    # Create steps for slider
    steps = []
    for i in range(len(morphed_steps)):
        step = dict(
            method="update",
            args=[
                {"visible": [False] * len(fig.data)},
                {"title": f"Morphed Airfoil: {morphed_steps[i]:.1f}"}
            ],
        )
        # Set the current pair of traces (upper and lower) to visible
        step["args"][0]["visible"][i*2] = True      # Upper surface
        step["args"][0]["visible"][i*2+1] = True    # Lower surface
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Morph Percent: "},
        pad={"t": 10},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
        title="Airfoil Morphing",
        xaxis_title="X",
        yaxis_title="Y",
        autosize=True
    )
    x_figure_range = np.array([-0.5, 1.5])
    y_figure_range = np.array([-1, 1])*9/16
    fig.update_layout(xaxis_range=x_figure_range,
                        yaxis_range=y_figure_range*9/16)
    fig.show()