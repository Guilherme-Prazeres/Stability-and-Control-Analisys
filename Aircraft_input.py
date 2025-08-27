import yaml
import math
from pprint import pprint

class Aircraft:
    """
    Classe para carregar e processar dados de uma aeronave a partir de um arquivo YAML.
    Calcula propriedades geométricas e aerodinâmicas derivadas.
    """
    def __init__(self, config_file_path):
        """
        Inicializa o objeto da aeronave.

        Args:
            config_file_path (str): O caminho para o arquivo de configuração .yaml.
        """
        print(f"INFO: Carregando dados da aeronave de '{config_file_path}'...")
        try:
            with open(config_file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"ERRO: Arquivo de configuração '{config_file_path}' não encontrado.")
            # Encerra a execução se o arquivo não for encontrado
            raise SystemExit 
        
        self._calculate_properties()
        print("INFO: Cálculos de propriedades derivadas concluídos.")

    def _calculate_properties(self):
        """
        Método central para calcular todas as propriedades que dependem
        dos dados de entrada primários do arquivo YAML.
        """
        # --- Propriedades da Asa (wing) ---
        wing = self.data['components']['wing']
        mass_props = self.data['mass_properties']
        
        # A área (S) é derivada da carga alar (W/S) e do peso máximo (W)
        wing['area_m2'] = mass_props['MTOW_kg'] / mass_props['wing_loading_kg_per_m2']
        
        # A envergadura (b) é derivada da área (S) e da razão de aspecto (AR)
        wing['span_m'] = math.sqrt(wing['area_m2'] * wing['aspect_ratio'])
        
        # A corda (c) é derivada da área (S) e da envergadura (b)
        wing['root_chord_m'] = wing['area_m2'] / wing['span_m']
        wing['tip_chord_m'] = wing['root_chord_m'] * wing['taper_ratio']
        
        # A corda média aerodinâmica (CMA) para uma asa retangular é a própria corda
        wing['CMA_m'] = 2/3 * wing['root_chord_m'] * ((1 + wing['taper_ratio']**2 + wing['taper_ratio']) / \
                                                                         (1 + wing['taper_ratio']))
        
        # Posição do centro aerodinâmico (CA) em 25% da CMA (padrão)
        wing['aerodynamic_center_local_x_mac'] = 0.25 * wing['CMA_m']

        # --- Propriedades do Aileron ---
        aileron = wing['aileron']
        aileron['start_pos'] = (wing['span_m']/2) * aileron['start_eta']
        aileron['end_pos'] = (wing['span_m']/2) * aileron['end_eta']
        aileron['chord'] = wing['CMA_m'] * aileron['aileron_chord_percentage']
        aileron['span_m'] = aileron['end_eta'] - aileron['start_eta']

        # Área total (considerando os dois ailerons)
        aileron['area_m2'] = 2 * (aileron['span_m'] * aileron['chord'])
        aileron['area_ratio_Sa_Sw'] = aileron['area_m2'] / wing['area_m2']
        
        # --- Propriedades da Fuselagem (fuselage) ---
        fuselage = self.data['components']['fuselage']
        fuselage['fineness_ratio'] = fuselage['length_m'] / fuselage['width_m']

        # --- Empenagem Horizontal (horizontal_stabilizer) ---
        h_stab = self.data['components']['horizontal_stabilizer']
        h_stab['area_m2'] = h_stab['span_m'] * h_stab['root_chord_m']
        h_stab['tip_chord_m'] = h_stab['taper_ratio'] * h_stab['root_chord_m']
        h_stab['CMA_m'] = 2/3 * h_stab['root_chord_m'] * ((1 + h_stab['taper_ratio']**2 + h_stab['taper_ratio']) / \
                                                            (1 + h_stab['taper_ratio']))
        # Coeficiente de volume da empenagem horizontal
        h_stab['volume_coefficient'] = (h_stab['area_m2'] * h_stab['tail_arm_m']) / \
                                       (wing['area_m2'] * wing['CMA_m'])

        # --- Profundor (elevator) ---
        elevator = h_stab['elevator']
        elevator['chord_m'] = h_stab['CMA_m'] * elevator['chord_percentage']
        elevator['span_m'] = h_stab['span_m'] * elevator['span_percentage']

        # --- Empenagem Vertical (vertical_stabilizer) ---
        v_stab = self.data['components']['vertical_stabilizer']
        v_stab['area_m2'] = v_stab['span_m'] * v_stab['root_chord_m']
        v_stab['CMA_m'] = v_stab['root_chord_m']
        
        # Coeficiente de volume da empenagem vertical (usa envergadura da asa na fórmula)
        v_stab['volume_coefficient'] = (v_stab['area_m2'] * v_stab['tail_arm_m']) / \
                                       (wing['area_m2'] * wing['span_m'])

        # --- Leme (rudder) ---
        rudder = v_stab['rudder']
        rudder['span_m'] = v_stab['span_m'] * rudder['span_percentage']
        rudder['root_chord_m'] = v_stab['CMA_m'] * rudder['chord_percentage']
        rudder['tip_chord_m'] = rudder['root_chord_m'] * v_stab['taper_ratio']
        rudder['CMA_m'] = 2/3 * rudder['root_chord_m'] * ((1 + v_stab['taper_ratio']**2 + v_stab['taper_ratio']) / \
                                                            (1 + v_stab['taper_ratio']))

        rudder['mean_chord_m'] = v_stab['root_chord_m'] * rudder['chord_percentage']

    def print_summary(self):
        """
        Imprime um resumo formatado de todos os dados da aeronave,
        incluindo os valores calculados.
        """
        print("\n" + "="*50)
        print(f" Resumo Completo da Aeronave: {self.data.get('aircraft_name')}")
        print("="*50)
        pprint(self.data)
        print("="*50 + "\n")

    def save_results_to_yaml(self, output_file_path):
        """
        Salva o dicionário de dados completo
        em um novo arquivo YAML.

        Args:
            output_file_path (str): O caminho do arquivo de saída.
        """
        print(f"INFO: Salvando resultados completos em '{output_file_path}'...")
        try:
            with open(output_file_path, 'w', encoding='utf-8') as file:
                # yaml.dump escreve o dicionário no arquivo
                # sort_keys=False mantém a ordem original dos dados
                # allow_unicode=True para garantir a codificação correta
                yaml.dump(self.data, file, sort_keys=False, allow_unicode=True)
            print("INFO: Arquivo de resultados salvo com sucesso.")
        except IOError as e:
            print(f"ERRO: Não foi possível salvar o arquivo. Razão: {e}")

# # --- Ponto de Execução do Script ---
# if __name__ == "__main__":
#     # Arquivo de entrada com os dados primários
#     input_file = 'Aircraft_input.yaml'
#     # Arquivo de saída que conterá todos os dados
#     output_file = 'Aircraft.yaml'
    
#     # 1. Crie uma instância da aeronave.
#     my_aircraft = Aircraft(input_file)
    
#     # 2. Imprima o resumo no console (opcional).
#     # my_aircraft.print_summary()
    
#     # =========================================================
#     # NOVA CHAMADA DE FUNÇÃO AQUI
#     # =========================================================
#     # 3. Salve o estado completo em um novo arquivo YAML.
#     my_aircraft.save_results_to_yaml(output_file)