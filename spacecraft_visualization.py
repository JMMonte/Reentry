import plotly.graph_objects as go
import numpy as np
from poliastro.bodies import Earth
from coordinate_converter import CoordinateConverter
import astropy.units as u
from astropy.coordinates import CartesianRepresentation


class SpacecraftVisualization:
    @staticmethod
    def create_geo_trace(geometry, gmst):
        lons, lats = geometry.xy
        x, y, z = CoordinateConverter.geo_to_ecef(np.deg2rad(lons), np.deg2rad(lats))
        x, y, z = CoordinateConverter.ecef_to_eci(x, y, z, gmst)
        trace = go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='blue', width=2))
        return trace

    @staticmethod
    def get_geo_traces(feature, gmst):
        trace_list = []
        for geometry in feature.geometries():
            if geometry.geom_type == 'MultiLineString':
                for line_string in geometry.geoms:
                    trace_list.append(SpacecraftVisualization.create_geo_trace(line_string, gmst))
            else:
                trace_list.append(SpacecraftVisualization.create_geo_trace(geometry, gmst))

        return trace_list
    
    @staticmethod
    def create_latitude_lines(N=50, gmst=0):
        lat_lines = []
        lon = np.linspace(-180, 180, N)
        lat_space = np.linspace(-90, 90, N // 2)
        for lat in lat_space:
            lons = np.full_like(lon, lat)
            x, y, z = CoordinateConverter.geo_to_ecef(np.deg2rad(lon), np.deg2rad(lons))
            x, y, z = CoordinateConverter.ecef_to_eci(x, y, z, gmst)
            lat_lines.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='blue', width=1)))
        return lat_lines

    @staticmethod
    def create_longitude_lines(N=50, gmst=0):
        lon_lines = []
        lat = np.linspace(-90, 90, N)
        lon_space = np.linspace(-180, 180, N)
        for lon in lon_space:
            lons = np.full_like(lat, lon)
            x, y, z = CoordinateConverter.geo_to_ecef(np.deg2rad(lons), np.deg2rad(lat))
            x, y, z = CoordinateConverter.ecef_to_eci(x, y, z, gmst)
            lon_lines.append(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='blue', width=1)))
        return lon_lines

    @staticmethod
    def create_spheroid_mesh(N=50, attractor=Earth):
        lat = np.linspace(-90, 90, N)
        lon = np.linspace(-180, 180, N)
        lat_grid, lon_grid = np.meshgrid(lat, lon)

        lat_rad_grid = np.radians(lat_grid)
        lon_rad_grid = np.radians(lon_grid)
        alt_grid = np.zeros_like(lat_rad_grid)

        x, y, z = CoordinateConverter.geo_to_ecef(lon_rad_grid, lat_rad_grid, alt_grid)

        return go.Mesh3d(
            x=x.flatten(), y=y.flatten(), z=z.flatten(),
            alphahull=0, color='rgb(0,0,100)', opacity=0.9)

    @staticmethod
    def create_3d_arrow(x_start, y_start, z_start, x_end, y_end, z_end, color, name):
        # Arrow line trace
        line_trace = go.Scatter3d(
            x=[x_start, x_end],
            y=[y_start, y_end],
            z=[z_start, z_end],
            mode='lines',
            line=dict(color=color),
            hoverinfo="none",
            name=name,
        )

        # Arrowhead trace
        arrowhead_length_ratio = 0.1  # Adjust this value to change the arrowhead length
        arrowhead_width_ratio = 0.05  # Adjust this value to change the arrowhead width

        arrow_vector = np.array([x_end - x_start, y_end - y_start, z_end - z_start])
        arrow_length = np.linalg.norm(arrow_vector)
        arrow_unit_vector = arrow_vector / arrow_length

        arrowhead_length = arrow_length * arrowhead_length_ratio
        arrowhead_base = np.array([x_end, y_end, z_end]) - arrowhead_length * arrow_unit_vector

        cross_product1 = np.cross(arrow_unit_vector, np.array([1, 0, 0]))
        if np.linalg.norm(cross_product1) == 0:
            cross_product1 = np.cross(arrow_unit_vector, np.array([0, 1, 0]))

        cross_product2 = np.cross(arrow_unit_vector, cross_product1)

        arrowhead_width = arrow_length * arrowhead_width_ratio
        corner1 = arrowhead_base + arrowhead_width * (cross_product1 / np.linalg.norm(cross_product1))
        corner2 = arrowhead_base + arrowhead_width * (cross_product2 / np.linalg.norm(cross_product2))
        corner3 = arrowhead_base - arrowhead_width * (cross_product1 / np.linalg.norm(cross_product1))
        corner4 = arrowhead_base - arrowhead_width * (cross_product2 / np.linalg.norm(cross_product2))

        arrowhead_trace = go.Mesh3d(
            x=[x_end, corner1[0], corner2[0], corner3[0], corner4[0]],
            y=[y_end, corner1[1], corner2[1], corner3[1], corner4[1]],
            z=[z_end, corner1[2], corner2[2], corner3[2], corner4[2]],
            i=[0, 0, 0, 0],
            j=[1, 2, 3, 4],
            k=[2, 3, 4, 1],
            color=color,
            name=name,
            hoverinfo="none"
        )

        return line_trace, arrowhead_trace
    
    @staticmethod
    def plot_orbit_3d(orbit, num_points=1000, color='blue', name=None):
        # Get position data
        time_values = np.linspace(0, orbit.period.to(u.s).value, num_points) * u.s
        positions = np.array([orbit.propagate(t).represent_as(CartesianRepresentation).xyz.to(u.m).value for t in time_values])

        # Create a 3D scatter plot
        scatter = go.Scatter3d(x=positions[:, 0], y=positions[:, 1], z=positions[:, 2],
                            mode='lines', line=dict(width=3, color=color), name=name)

        return scatter


    