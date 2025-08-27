import math
from Aircraft_input import Aircraft # Importa a classe Aircraft do arquivo aircraft.py

class LongitudinalStaticStability:
    """
    Realiza os cálculos de estabilidade estática longitudinal.
    """
    def __init__(self, aircraft: Aircraft):
        """
        Inicializa o analisador com um objeto Aircraft.
        """
        self.aircraft = aircraft
        self.wing = self.aircraft.data['components']['wing']
        self.mass_props = self.aircraft.data['mass_properties']

    def calculate_wing_contribution(self):
        """
        Calcula a contribuição da asa para a estabilidade estática longitudinal (Cm_alpha_asa).
        """
        c_bar = self.wing['mean_aerodynamic_chord_m']
        AR = self.wing['aspect_ratio']
        cl_alpha_2d = self.wing['aerodynamics']['cl_alpha_per_rad']
        
        C_L_alpha_wing_rad = cl_alpha_2d / (1 + (cl_alpha_2d / (math.pi * AR)))

        x_lemac = self.wing['x_lemac_m']
        xcg_frac = self.mass_props['xcg_percent_mac'] / 100.0
        x_cg = x_lemac + xcg_frac * c_bar

        x_ac_wing_frac = self.wing['aerodynamic_center_local_x_mac']
        x_ac_wing = x_lemac + x_ac_wing_frac * c_bar

        Cm_alpha_wing_rad = C_L_alpha_wing_rad * (x_cg - x_ac_wing) / c_bar

        results = {
            'C_L_alpha_wing_per_rad': C_L_alpha_wing_rad,
            'x_cg_m': x_cg,
            'x_ac_wing_m': x_ac_wing,
            'Cm_alpha_wing_per_rad': Cm_alpha_wing_rad
        }
        return results
