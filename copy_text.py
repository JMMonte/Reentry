
import streamlit as st

HELP_TEXT =r'''
    This app aims to simulate the complex dynamics of a spacecraft orbits around the Earth taking into account the Earth's rotation, J2 perturbations, atmospheric drag, the sun's gravity and the Moon's gravity while predicting the spacecraft's trajectory.
    
    Before running your simulation, you can edit the spacecraft's initial state and the simulation parameters.👇 
    
    The simulation uses the amazing [poliastro](https://docs.poliastro.space/en/stable/) library, as well as [astropy](https://www.astropy.org/).
    
    To learn more about reentry astrodynamics I really reccommend this summary from the Aerostudents website: [Reentry](https://www.aerostudents.com/courses/rocket-motion-and-reentry-systems/ReEntrySummary.pdf).
    
    Made with ❤️ by [João Montenegro](https://monte-negro.space/).
    '''

INPUTS = {
    "mass": {
        "default_value":5000.0,
        "min_value": 0.0,
        "help_text": "Spacecraft mass (kg) denotes the total weight of a spacecraft, including its structure, fuel, and payload. It plays a vital role in orbital and reentry trajectory planning, as it influences propulsion requirements, momentum, and heating rates. A lower mass can ease maneuvering and reduce fuel consumption (e.g., Sputnik 1), while a higher mass can pose challenges for propulsion and deceleration (e.g., International Space Station). Accurate knowledge of spacecraft mass is essential for efficient trajectory planning and mission success."
    },
    "area": {
        "default_value": 14.0,
        "min_value": 0.0,
        "help_text": "The cross-sectional area (A) refers to a spacecraft's projected area perpendicular to the direction of motion during orbital and reentry trajectories. By adjusting A in the number input, you can evaluate its influence on drag forces, deceleration, heating, and trajectory accuracy.:s Smaller cross-sectional areas lead to reduced drag forces (e.g., Mercury capsule, A ~ 1.2 m²), promoting stability and requiring less deceleration. Larger cross-sectional areas increase drag (e.g., SpaceX's Starship, A ~ 354.3 m²), aiding in deceleration but potentially increasing heating rates.:sProperly managing cross-sectional area based on the spacecraft's design ensures optimized flight paths and successful mission outcomes."
    },
    "codrag": {
        "default_value": 1.3,
        "min_value": 0.0,
        "help_text": "The drag coefficient (Cd) quantifies a spacecraft's aerodynamic resistance during orbital and reentry trajectories. By adjusting Cd in the number input, you can explore its impact on the spacecraft's deceleration, heating, and trajectory accuracy.:s Lower Cd values indicate reduced aerodynamic drag (e.g., Mars Science Laboratory, Cd ~ 0.9), leading to smoother reentry and longer deceleration times. Higher Cd values result in increased drag (e.g., Apollo Command Module, Cd ~ 1.3), causing more rapid deceleration and potentially higher heating rates.:s Optimizing Cd based on the spacecraft's shape and design helps ensure efficient trajectory planning and mission success.",
    },
    "selected_material": {
        "help_text": "The heat shield material (M) refers to the material used to protect a spacecraft from the intense heat generated during reentry. By adjusting M in the dropdown menu, you can analyze its impact on the spacecraft's heating rate, deceleration, and trajectory accuracy.:s For example, the Apollo Command Module used an ablative heat shield (M ~ Avcoat), which gradually burned away during reentry to dissipate heat. The Space Shuttle, on the other hand, used a reusable heat shield (M ~ Reinforced Carbon-Carbon), which could withstand multiple reentries.:s Selecting an appropriate heat shield material based on the spacecraft's design and mission requirements ensures efficient trajectory planning and mission success."
    },
    "v": {
        "default_value": 7540.0,
        "help_text": "Orbital velocity (V) is the speed required for a spacecraft to maintain a stable orbit around a celestial body. By adjusting V in the number input, you can analyze its impact on orbit design, altitude, period, and mission objectives.:s For example, geostationary satellites orbit at a higher altitude than low Earth orbit spacecraft, but they have a lower orbital velocity (e.g., V ~ 3.07 km/s). The geostationary transfer orbit, on the other hand, is a high-velocity maneuver orbit used to transfer a spacecraft from low Earth orbit to geostationary orbit. This transfer orbit has a higher velocity than geostationary orbit (e.g., V ~ 10.3 km/s at perigee).:s Selecting an appropriate orbital velocity based on mission requirements and spacecraft capabilities ensures efficient orbit design and mission success."
    },
    "azimuth": {
        "default_value": 90.0,
        "min_value": 0.0,
        "max_value": 360.0,
        "help_text": "Azimuth represents the spacecraft's angle relative to a reference direction during orbital and reentry trajectories. By adjusting the azimuth in the number input, you can simulate how the spacecraft's orientation affects its mission outcome.:s Properly managing the spacecraft's azimuth is crucial for achieving optimal trajectory accuracy and minimizing aerodynamic drag. For example, during reentry, a steeper azimuth angle can result in higher heating rates due to increased deceleration, while a shallower angle can lead to a longer reentry duration.:s Historic missions such as Apollo 11 and the Space Shuttle program used specific azimuth angles to achieve their mission objectives. Apollo 11 had a roll angle of 69.5 degrees during reentry, while the Space Shuttle typically used an azimuth angle of around 40 degrees for its deorbit burn.:s Selecting the appropriate azimuth angle depends on the spacecraft's objectives and design. Properly managing the azimuth angle can help ensure safe and accurate trajectory planning for successful missions."
    },
    "gamma": {
        "default_value": -2.0,
        "min_value": -90.0,
        "max_value": 90.0,
        "help_text": "The flight path angle or gamma (degrees) represents the angle between the spacecraft's velocity vector and the local horizontal during orbital and reentry trajectories. By adjusting the flight path angle in the number input, you can simulate how the spacecraft's angle affects its mission outcome.:s Lower flight path angles (e.g., SpaceX's Dragon spacecraft, gamma ~ -12 degrees) result in steeper trajectories, leading to higher deceleration and increased heating rates during reentry. Higher flight path angles (e.g., Apollo Command Module, gamma ~ -6 degrees) result in shallower trajectories, leading to lower deceleration and reduced heating rates during reentry.:s Properly managing the flight path angle ensures optimized trajectory planning for successful missions, balancing the need for deceleration and minimizing heating effects."
    },
    "alt": {
        "default_value": 100000.0,
        "min_value": 0.0,
        "max_value": 1000000.0,
        "help_text": "Orbital altitude refers to the distance between the spacecraft and the Earth's surface during orbital trajectory planning. By changing the orbital altitude in the number input, you can simulate how it affects the spacecraft's orbital period, velocity, and energy requirements.:s Lower orbital altitudes (e.g., Low Earth Orbit, ~400 km) result in shorter orbital periods and higher spacecraft velocities. Higher orbital altitudes (e.g., Geostationary Orbit, ~36,000 km) lead to longer orbital periods and lower spacecraft velocities.:s The selected orbital altitude must consider the mission objectives, such as Earth observation, communication, or space exploration, and the spacecraft's capabilities, such as propulsion and power requirements. Careful planning of the orbital altitude ensures the successful accomplishment of the mission goals."
    },
    "clock": {
        "help_text": "The start time of the mission simulation."
    },
    "calendar": {
        "help_text": "The start date of the mission simulation."
    },
    "tf": {
        "help_text": "How long do you want to simulate the spacecraft?"
    },
    "dt": {
        "help_text": "The simulation will be broken down into a time step. Shorter timesteps give more precision but will increase the processing time.",
    },
    "sim_type": {
        "help_text": "The integration method to be used by the simulation physics solver. Explicit Runge-Kutta methods ('RK23', 'RK45', 'DOP853') should be used for non-stiff problems and implicit methods ('Radau', 'BDF') for stiff problems. Among Runge-Kutta methods, 'DOP853' is recommended for solving with high precision (low values of `rtol` and `atol`).:s If not sure, first try to run 'RK45'. If it makes unusually many iterations, diverges, or fails, your problem is likely to be stiff and you should use 'Radau' or 'BDF'. 'LSODA' can also be a good universal choice, but it might be somewhat less convenient to work with as it wraps old Fortran code.:s You can also pass an arbitrary class derived from `OdeSolver` which implements the solver."
    },
    "iter_fact": {
        "help_text": "Advanced: The iteration slowdown factor is used to slow down the temperature algorithm iterator. It has the purpose of fine tunning experimental data with simulation results. The default value is 2.0. If you are not sure, leave it as is."
    },
    "max_points": {
        "help_text": "max_points"
    },
}

ALTITUDE_VS_TIME = r'''
    Here you can see the altitude of the spacecraft over time.
    The red line is the trendline of the altitude over time. The blue line is the altitude over time.
    The Karman line is the unnofficial altitude that some consider to be the begining of space. The Karman line is at 100km.
    
    In this simulation we are using the _COESA76_ atmospheric model that considers the Earth's atmosphere to be composed of 6 layers.
    The first layer is the troposphere, the second layer is the stratosphere, the third layer is the mesosphere, the fourth layer is the thermosphere, the fifth layer is the exosphere, and the sixth layer is the ionosphere.
    The Karman line is located in the thermosphere layer.
    
    The model considers the atmosphere from 0 to 1000km, after that the atmosphere is considered to be a vacuum.
    '''
DOWNRAGE_VS_ALTITUDE = r'''
    Here you can see the downrange distance of the spacecraft from the launch site as a function of altitude.
    Downrange is being measured in absolute distance from the starting point.
    '''
GROUNDTRACK = r'''
    Here you can see the groundtrack of the spacecraft as a function of time.
    Groundtrack's are a way to visualize the path of a spacecraft on a map in reference to the Earth's surface.
    
    To do this we need to adjust our original frame of reference (Earth-Centered Inertial) to a new frame of reference (Earth-Centered Earth-Fixed).
    '''
VELOCITY_VS_TIME = r'''
    Here you can see the velocity of the spacecraft both in absolute magnitude as well as in the x, y, and z directions.
    One particularly useful measure is the ground velocity vs the orbital velocity.
    '''
PERTURBATIONS_TEXT = r'''
    Let's visualize the perturbations that are affecting the spacecraft's trajectory.
    This will show us how the acceleration changes over time. We can see that the acceleration is initially very high, but then decreases as the spacecraft gets further away from the Earth.
    In this simulation we are taking into account:

    - Earth's gravitational acceleration
    - Drag acceleration
    - Moon's gravitational acceleration
    - Sun's gravitational acceleration
    - J2 acceleration
     
    In our starting scenario (in Low Earth Orbit), you can see that the total acceleration is mainly affected by the Earth's gravitational acceleration. However, you can click on the legend to hide the total acceleration to adjust the graphs y axis so the other accelerations are visible.
    '''
TEMPERATURE_MODEL_TEXT = r'''
    The spacecraft temperature model is a simplified model that calculates the temperature change of the spacecraft during its trajectory through the atmosphere.
    This model was selected because it approximates the heat generated by the spacecraft performing work against Earth's atmosphere.
    
    The model considers the following heat transfer mechanisms:

    **I) Heat generated (Q) due to the work done (W) by the drag force on the spacecraft.**

    $$Q = ablation\_efficiency \times W$$

    where $ablation\_efficiency$ is the ablation efficiency factor.


    **II) Conductive heat transfer (Qc) between the spacecraft and the atmosphere.**

    $$Q_c = thermal\_conductivity \times \frac{T_s - atmo\_T}{capsule\_length}$$

    where $thermal\_conductivity$ is the thermal conductivity of the heat shield material, $T_s$ is the spacecraft temperature, $atmo\_T$ is the atmospheric temperature, and $capsule\_length$ is the length of the capsule.


    **III) Radiative heat transfer (Qr) between the spacecraft and the atmosphere.**

    $$Q_r = emissivity \times \sigma \times (T_s^4 - atmo\_T^4)$$

    where $emissivity$ is the emissivity of the heat shield material, $\sigma$ is the Stefan-Boltzmann constant, $T_s$ is the spacecraft temperature, and $atmo\_T$ is the atmospheric temperature.

    ---
    
    The net heat transfer (Q_net) is the sum of the heat generated minus the conductive and radiative heat transfers: 
    
    $$Q_{net} = Q - Q_c - Q_r$$

    ---
    
    The temperature change (dT) is calculated as the net heat transfer divided by the product of the spacecraft mass and specific heat capacity: 
    
    $$dT = \frac{Q_{net}}{spacecraft\_m \times specific\_heat\_capacity}$$

    ---
    
    The updated spacecraft temperature is obtained by adding the temperature change to the current temperature: 
    
    $$T_s = T_s + dT$$
    
    The model iterates through these calculations for a specified number of iterations, taking into account the altitude, velocity, atmospheric temperature, and drag acceleration experienced by the spacecraft.
    The final output includes the conductive, radiative, and net heat transfers, as well as the updated spacecraft temperature and the temperature change.
    
    '''
ATMOSPHERIC_MODEL_TEXT = r'''
    This atmospheric model is a simplified version of the NRLMSISE-00 model.
    It estimates the density and temperature of Earth's atmosphere as a function of altitude, latitude, and solar activity.
    
    The model divides the atmosphere into different layers, with each layer having specific temperature gradients and base pressures:

    - Troposphere (0 to 11 km)
    - Stratosphere (11 to 47 km)
    - Mesosphere (47 to 84.8 km)
    - Thermosphere (84.8 km to 150 km)
    
    ---

    The temperature at a given altitude is calculated using the temperature gradient and the base temperature for the corresponding layer:
    
    $$T = T_{base} + \Delta h * \frac{dT}{dh}$$
    
    where: 
    - $T_{base}$ is the base temperature for the layer 
    - $\Delta h$ is the altitude difference from the base altitude of the layer 
    - $\frac{dT}{dh}$ is the temperature gradient for the layer

    ---
    
    The pressure at the given altitude is computed using either the barometric formula or the hypsometric equation, depending on whether the temperature gradient is zero:
    
    If the temperature gradient is zero st.latex($\frac{dT}{dh} = 0$), the pressure is calculated using the barometric formula:
    
    $$P = P_{base} * \exp \left( -\frac{g M \Delta h}{R T_{base}} \right)$$

    ---
    
    Otherwise, if the temperature gradient is not zero, the pressure is calculated using the hypsometric equation:
    
    $$P = P_{base} * \left( \frac{T}{T_{base}} \right) ^{-\frac{g M}{R \frac{dT}{dh}}}$$
     
    where:
    - $P_{base}$ is the base pressure for the layer
    - $g$ is Earth's gravity
    - $M$ is the molar mass of Earth's air
    - $R$ is the specific gas constant for Earth's air
    - $T_{base}$ is the base temperature for the layer
    - $\frac{dT}{dh}$ is the temperature gradient for the layer

    ---
    
    In the exosphere (above 150 km), the pressure is exponentially decreased with altitude based on a scale height parameter:
    
    $$P *= \exp \left( -\frac{h - h_{exo}}{H} \right)$$
    
    where:
    - $h_{exo}$ is the altitude where the exosphere begins (150 km)
    - $H$ is the scale height


    ---
    
    The latitude factor is applied to account for the variation in atmospheric pressure due to latitude:
    
    $$P *= 1 + \frac{0.01 * |latitude|}{90}$$

    ---
    
    The density is then computed from the pressure and temperature:
    
    $$\rho = \frac{P}{R_{gas} * T}$$
    
    where:
    - $R_{gas}$ is the specific gas constant for Earth's air

    ---
    '''
SOLAR_CYCLE_TEXT = r'''
    To account for the effect of solar activity, a solar activity factor is calculated based on the F10.7 index. A simple sinusoidal model is used to estimate the F10.7 value from the Julian date:

    $$F10.7 = F10.7_{avg} + A * \sin \left( \frac{t_{cycle}}{T_{cycle}} * 2\pi \right)$$
    
    where:
    - $F10.7_{avg}$ is the average F10.7 value
    - $A$ is the amplitude of the solar cycle
    - $t_{cycle}$ is the time since the last solar minimum in months
    - $T_{cycle}$ is the solar cycle period in months
    
    The solar activity factor is then calculated:
    
    $$factor = 1 + \frac{F10.7 - F10.7_{avg}}{F10.7_{avg}}$$
    
    Finally, the solar activity factor is applied to the calculated density:
    
    $$\rho *= factor$$
    
    The `atmosphere_model` function returns the density and temperature at the given altitude, latitude, and solar activity.
    '''
DISCLAIMER = r'''
    That's it for this dashboard. Try more combinations to see the effects of different parameters on the trajectory. Also, try landing with low Gs (your spacecraft will thank you...)!
    
    You can reach me on [Twitter](https://twitter.com/JohnMontenegro) or [Github](https://github.com/JMMonte) or [Linkedin](https://www.linkedin.com/in/jmontenegrodesign/).
    You can also visit my [personal website](https://monte-negro.space/).
    '''
ABOUT_APP = r'''
    **About this app**
    
    This app means to show the power of mixing streamlit, plotly, poliastro with scipy as the simulation engine.

    All the code is available on Github and is free to use.

    Many of these equations are a best effort to implement and are likely not the most accurate in their current form.

    Therefore, any feedback is greatly welcome.
    You can reach me on [Twitter](https://twitter.com/JohnMontenegro) or [Github](https://github.com/JMMonte) or [Linkedin](https://www.linkedin.com/in/jmontenegrodesign/).
    
    You can also visit my [personal website](https://monte-negro.space/).
    '''