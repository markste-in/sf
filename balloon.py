import sf.earth as earth
from sympy.solvers import solve
from sympy import Symbol
import math

class balloon:
    Helium_Molecular_Weight = 4.002602 # g

    class template:
        balloon350g = {
        'weight_balloon':0.35,
        'radius_uninflated':0.625,
        'burst_radius':2.06,
        }
        balloon600g = {
        'weight_balloon':0.6,
        'radius_uninflated':0.71,
        'burst_radius':3.01
        }
        balloon1200g = {
        'weight_balloon':1.2,
        'radius_uninflated':0.895,
        'burst_radius':4.315
        }
        balloon2000g = {
        'weight_balloon':2.,
        'radius_uninflated':0.975,
        'burst_radius':5.27
        }
        balloon3000g = {
        'weight_balloon':3.,
        'radius_uninflated':1.06,
        'burst_radius':6.5
        }
        rubber_material = {
        'thickness_uninflated':0.2e-3,
        'shear_modulus':300.e3,
        's2':-30.e3,
        'alpha':10./11.
        }

    def __init__(self, weight_balloon = 0.35 , radius_uninflated = 0.625, burst_radius = 2.06, thickness_uninflated = 0.2e-3, shear_modulus = 300.e3, s2 = -30.e3, alpha = 0.90909, weight_payload = 0. , Gas = 'He'):
        self.thickness_uninflated = thickness_uninflated # m
        self.radius_uninflated = radius_uninflated # m
        self.shear_modulus = shear_modulus # Pa
        self.s2 = s2 # 1
        self.weight_balloon = weight_balloon # kg
        self.weight_payload = weight_payload # kg
        self.Gas = Gas # Helium as default
        self.alpha = alpha
        self.molesGasFilling = balloon.MolesGasFilling(self)
    # def deltaPInsideOutsideMR(self, radius_inflated):
    #     """
    #     Calculates the pressure difference between the outside and the inside oft the balloon with the help of the stress-strain relation of Mooney–Rivlin
    #     Input:
    #
    #     Output:
    #
    #     Comment:
    #
    #     """
    #     deltaP = 2 * self.shear_modulus * (self.thickness_uninflated/self.radius_uninflated) \
    #             *(
    #                 ((self.radius_uninflated/radius_inflated) - pow((self.radius_uninflated/radius_inflated),7))
    #                 *
    #                 (1 + (1-self.alpha)/self.alpha*(pow((radius_inflated/self.radius_uninflated),2)))
    #             )
    #     return deltaP
    def deltaPInsideOutsideMR(self, radius_inflated):
        """
        Calculates the pressure difference between the outside and the inside oft the balloon with the help of the stress-strain relation of Mooney–Rivlin
        Input:

        Output:

        Comment:

        """
        deltaP = 2 * self.shear_modulus * (self.thickness_uninflated/self.radius_uninflated) \
                *(
                    ((self.radius_uninflated/radius_inflated) - pow((self.radius_uninflated/radius_inflated),7))
                    *
                    (1 - (self.s2/self.shear_modulus)*(pow((radius_inflated/self.radius_uninflated),2)))
                )
        return deltaP
    def radius_inflation(self,altitude):
        """
        Returns the radius of the balloon at a given altitude
        Input: altitude in km
        Output: balloon radius in m
        """
        radius_inflated = Symbol('radius_inflated')
        result = solve(balloon.deltaPInsideOutsideMR(self,radius_inflated)-balloon._pressureBalloon(self,altitude,radius_inflated)+earth.getStandardPressure(altitude)
                ,radius_inflated)
        result = max([i for i in result if i.is_real and i >= 0])
        return result

    def _pressureBalloon(self, altitude,radius_inflated):
        """
        Internal Function! Needed for sympy solver to solve the equation for the inflated radius
        Input:
        altitude in km
        radius_inflated in m

        Output:
        Pressure inside the balloon
        """
        return (self.molesGasFilling * earth.GAS_CONSTANT * earth.getStandardTemperature(altitude))/balloon.VolumeBalloon(radius_inflated)

    def pressureBalloon(self,altitude):
        """
        Calculates the pressure inside the Balloon
        Input:
        altitude in km
        radius_inflated in m

        Output:
        Pressure inside the balloon
        """
        return (self.molesGasFilling * earth.GAS_CONSTANT * earth.getStandardTemperature(altitude))/balloon.VolumeBalloon(balloon.radius_inflation(self,altitude))

    def MolesGasFilling(self):
        """
        Returns the gas filling of the balloon in moles using the uninflated radius (at release) and the standard temperature and pressure on the ground
        Output: moles
        """
        return (balloon.VolumeBalloon(self.radius_uninflated)*earth.getStandardPressure(0)) / (earth.GAS_CONSTANT *earth.getStandardTemperature(0))

    def VolumeBalloon(radius):
        """
        Returns the volumen of the weight_balloon
        Input: radius in m
        Output: Volume in m^3
        """
        return (4./3.)*math.pi*pow(radius,3)


    def Gramms_to_Moles(Gramms, Gas = 'He'):
        """
        Converts Gramms to Moles for a given gas (default is Helium)
        Input:
        Gramms: g
        Gas: Name of the gas as string (default Helium)

        Output:
        Moles of the given gas: mol
        """
        if (Gas.lower() == 'helium' or Gas.lower() == 'he'):
            return Gramms / balloon.Helium_Molecular_Weight
        elif (Gas.lower() == 'hydrogen' or Gas.lower() == 'h2'):
            print("Hydroge not yet implemented")
            raise Exception("Not Implemented")


    def Moles_to_Gramms(Moles, Gas = 'He'):
        """
        Converts Moles to Gramms for a given gas (default is Helium)
        Input:
        Moles: mol
        Gas: Name of the gas as string (default Helium)

        Output:
        Gramms of the given gas : g
        """
        if (Gas.lower() == 'helium' or Gas.lower() == 'he'):
            return Moles * balloon.Helium_Molecular_Weight
        elif (Gas.lower() == 'hydrogen' or Gas.lower() == 'h2'):
            print("Hydroge not yet implemented")
            raise Exception("Not Implemented")
