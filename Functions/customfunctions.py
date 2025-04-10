import numpy as np
from scipy.spatial.distance import euclidean

def point_at_arc_length_percentage(list_of_points: list[np.ndarray], percentage: float):
    """
    Returns the position vector at a given percentage along a path defined by points.
    
    Args:
        points: List of points (each point is a tuple or array of coordinates)
        percentage: Float between 0 and 1 representing the percentage along the path
    
    Returns:
        Position vector (coordinates) at the given percentage
    """
    
    # Calculate distances between consecutive points
    distances = [euclidean(list_of_points[i], list_of_points[i+1]) for i in range(len(list_of_points)-1)]
    
    # Calculate cumulative distances (arc lengths)
    cumulative_distances = np.cumsum([0] + distances)
    
    # Total path length
    total_length = cumulative_distances[-1]
    
    # Target distance along the path
    target_distance = percentage * total_length
    
    # Find the segment that contains the target distance
    segment_index = np.searchsorted(cumulative_distances, target_distance) - 1
    segment_index = max(0, min(segment_index, len(list_of_points)-2))  # Ensure valid index
    
    # Calculate how far along the segment the target is
    segment_start_distance = cumulative_distances[segment_index]
    segment_length = distances[segment_index]
    segment_percentage = (target_distance - segment_start_distance) / segment_length if segment_length > 0 else 0
    
    # Interpolate between the points
    start_point = np.array(list_of_points[segment_index])
    end_point = np.array(list_of_points[segment_index + 1])
    position = start_point + segment_percentage * (end_point - start_point)
    
    return position

def resample_path_with_endpoints(list_of_points: list[np.ndarray], num_samples: int):
    """
    Resamples a path defined by points to have exactly num_samples points,
    guaranteeing that the first and last original points are included.
    
    Args:
        points: List of points (each point is a tuple or array of coordinates)
        num_samples: Number of points in the output (must be >= 2)
    
    Returns:
        List of resampled points with exactly num_samples points
    """
    if num_samples < 2:
        raise ValueError("Number of samples must be at least 2")
    
    # Calculate distances between consecutive points
    distances = [euclidean(list_of_points[i], list_of_points[i+1]) for i in range(len(list_of_points)-1)]
    
    # Calculate cumulative distances (arc lengths)
    cumulative_distances = np.cumsum([0] + distances)
    
    # Total path length
    total_length = cumulative_distances[-1]
    
    # Initialize result with the first point
    resampled_points = [np.array(list_of_points[0])]
    
    # Calculate internal points (everything except first and last)
    if num_samples > 2:
        # Create percentages that exclude 0 and 1
        percentages = np.linspace(0, 1, num_samples)[1:-1]
        
        for percentage in percentages:
            target_distance = percentage * total_length
            
            # Find the segment that contains the target distance
            segment_index = np.searchsorted(cumulative_distances, target_distance) - 1
            segment_index = max(0, min(segment_index, len(list_of_points)-2))
            
            # Calculate how far along the segment the target is
            segment_start_distance = cumulative_distances[segment_index]
            segment_length = distances[segment_index]
            segment_percentage = (target_distance - segment_start_distance) / segment_length if segment_length > 0 else 0
            
            # Interpolate between the points
            start_point = np.array(list_of_points[segment_index])
            end_point = np.array(list_of_points[segment_index + 1])
            position = start_point + segment_percentage * (end_point - start_point)
            
            resampled_points.append(position)
    
    # Add the last point
    resampled_points.append(np.array(list_of_points[-1]))
    
    return resampled_points