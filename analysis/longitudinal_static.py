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
        c_bar = self.wing['CMA_m']
        AR = self.wing['aspect_ratio']
        cl_alpha_2d = self.wing['aerodynamics']['cl_alpha_per_rad']
        c_l_0 = self.wing['aerodynamics']['c_l_0']
        c_m_0 = self.wing['aerodynamics']['c_m_0']
        x_cg = c_bar * self.mass_props['xcg_percent_mac']
        x_ac = 0.25 * c_bar
        
        C_L_alpha_wing_rad = cl_alpha_2d / (1 + (cl_alpha_2d / (math.pi * AR)))

        C_m0_w = c_m_0 + c_l_0 * ((x_cg/c_bar) - (x_ac/c_bar))

        C_ma_w = C_L_alpha_wing_rad * ((x_cg/c_bar) - (x_ac/c_bar)) 

        results = {
            'C_L_alpha_wing_per_rad': C_L_alpha_wing_rad,
            'C_m0_w': C_m0_w,
            'C_ma_w': C_ma_w
        }
        return results
