import numpy as np

class earth:
    r_equator = 6.3781e6 # m
    r_pole = 6.3568e6 # m
    r_mean = 6.371008e6
    GRAVITATIONAL_CONSTANTS = 6.6740831e-11 # Nm^2kg^2
    mass = 5.9722e24 # kg
    GAS_CONSTANT = 8.314459848 # J⋅/ (mol⋅K)
    R_SPECIFIC_DRY_AIR = 287.058 # J / (kg*K)

    def getGeopotential(altitude_km):
        """
        Input:
        altitude: km

        Output:
        GeoPotential Height: km

        Comment:
        geopot_height = earth_radius * altitude / (earth_radius + altitude) /// All in km
        Wiki: ...it can be considered a "gravity-adjusted height"...
        """
        EARTH_RADIUS =  6356.766 # km
        return EARTH_RADIUS * altitude_km / (EARTH_RADIUS + altitude_km)

    def getStandardTemperature(geopot_height):
        """
        Input:
        geopot_height: km

        Output:
        return value: Kelvin

        Comment:

        Thermosphere has high kinetic temperature (500 C to 2000 C) but temperature
        as measured by a thermometer would be very low because of almost vacuum.
        Temperature is in kelvins = 273.15 + Celsius
        """


        if (geopot_height <= 11):          # Troposphere
            return 288.15 - (6.5 * geopot_height)
        elif (geopot_height <= 20):     # Stratosphere starts
            return 216.65
        elif (geopot_height <= 32):
            return 196.65 + geopot_height
        elif (geopot_height <= 47):
            return 228.65 + 2.8 * (geopot_height - 32)
        elif (geopot_height <= 51):     # Mesosphere starts
            return 270.65
        elif (geopot_height <= 71):
            return 270.65 - 2.8 * (geopot_height - 51)
        elif (geopot_height <= 84.85):
            return 214.65 - 2 * (geopot_height - 71)
        else:
            raise ValueError("geopot_height must be less than 84.85 km.")

    def getStandardPressure(altitude_km):
        """
        Input:
        altitude: km

        Output:
        return value: Pascal

        Comment:

        Below 51 km: Practical Meteorology by Roland Stull, pg 12
        Above 51 km: http://www.braeunig.us/space/atmmodel.htm
        Validation data: https://www.avs.org/AVS/files/c7/c7edaedb-95b2-438f-adfb-36de54f87b9e.pdf
        """

        geopot_height = earth.getGeopotential(altitude_km)

        t = earth.getStandardTemperature(geopot_height);

        if (geopot_height <= 11):
            return  101325 * pow(288.15 / t, -5.255877)
        elif (geopot_height <= 20):
            return 22632.06 * np.exp(-0.1577 * (geopot_height - 11))
        elif (geopot_height <= 32):
            return 5474.889 * pow(216.65 / t, 34.16319)
        elif (geopot_height <= 47):
            return 868.0187 * pow(228.65 / t, 12.2011)
        elif (geopot_height <= 51):
            return 110.9063 * np.exp(-0.1262 * (geopot_height - 47))
        elif (geopot_height <= 71):
            return 66.93887 * pow(270.65 / t, -12.2011)
        elif (geopot_height <= 84.85):
            return 3.956420 * pow(214.65 / t, -17.0816)
        else:
            raise ValueError("altitude must be less than 86 km.")
    def SelfTest():
        assert earth.getStandardPressure(0)==101325., 'Wrong Pressure at 0 km'
        assert round(earth.getStandardPressure(5),2)==54048.28, 'Wrong Pressure at 5 km'
        assert round(earth.getGeopotential(1),5) == 0.99984, 'Wrong GeoPotential at 1 km'
        assert round(earth.getGeopotential(20),5) == 19.93727, 'Wrong GeoPotential at 20 km'
        assert round(earth.density_dry_air(0),4) == 1.225, "Wrong Air Density at 0 m"
        assert round(earth.density_dry_air(10000),4) == 0.4137, "Wrong Air Density at 10 km"
        assert earth.getStandardTemperature(0) == 288.15, 'Wrong Standard Temperature 0 km at'
        assert round(earth.getStandardTemperature(10),4) == 223.15 , "Wrong Temperature at 10 km"
        assert round(earth.getGravityByHeight(0),5) == 9.81996 , "Wrong gravity at 0 km"
        assert round(earth.getGravityByHeight(50000),5) == 9.66762 , "Wrong gravity at 0 km"
        print('Everyting seems ok')

    def getGravityByHeight(height_in_m):
        """
        Input:
        height above earth surface (mean earth radius): m
        Output:
        gravity: m/s^2
        """
        return (earth.GRAVITATIONAL_CONSTANTS * earth.mass) / np.square(earth.r_mean + height_in_m)

    def density_dry_air(altitude_in_m):
        """
        Input:
        height above earth surface: m

        Output:
        density of dry air: kg/m^3

        Comment:
        Using the U.S. Standard Atmosphere for calculation
        """
        altitude = altitude_in_m / 1000. #convert m to km
        return earth.getStandardPressure(altitude) / (earth.R_SPECIFIC_DRY_AIR * earth.getStandardTemperature(altitude))
