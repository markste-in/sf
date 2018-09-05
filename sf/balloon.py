import sf.earth as earth

class balloon:
    Helium_Molecular_Weight = 4.002602 # g
    def __init__(self, weight_balloon = 0.3 , weight_payload = 0.3 , Gas = 'He', thickness_uninflated = 0.2e-3, radius_uninflated = 0.5):
        self.thickness_uninflated = thickness_uninflated # m
        self.radius_uninflated = radius_uninflated # m
        self.shear_modulus = 300e3 # Pa
        self.alpha = 10. # 1
        self.weight_balloon = weight_balloon # kg
        self.weight_payload = weight_payload # kg
        self.Gas = Gas # Helium as default
    def deltaPInsideOutsideMR(self, radius_inflated):
        """
        Calculates the pressure difference between the outside and the inside oft the ballon with the help of the stress-strain relation of Mooney–Rivlin
        Input:

        Output:

        Comment:

        """
        deltaP = 2 * self.shear_modulus * (self.thickness_uninflated/self.radius_uninflated) \
                *(
                    ((self.radius_uninflated/radius_inflated) - pow((self.radius_uninflated/radius_inflated),7)) \
                    *
                    (1 + (1-self.alpha)/self.alpha*(pow((self.radius_uninflated/radius_inflated),2)))
                )
        return deltaP

    def deltaPInsideOutsideIGL(radius_inflated, helium_filling_gramms, altitude):
        deltaP = balloon.Helium_Gramms_to_Moles(helium_filling_gramms) * earth.GAS_CONSTANT  * earth.getStandardTemperature(altitude)/(4/3*np.pi*np.pow(radius_inflated,3)) - earth.getStandardPressure(altitude)
        return deltaP

    def PressureInside(altitude):
        return earth.getStandardPressure(altitude)+balloon._deltaPInsideOutsideMR(radius_inflated)

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
