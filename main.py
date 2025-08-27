# Importa as classes necessárias dos nossos módulos
from Aircraft_input import Aircraft
from analysis.longitudinal_static import LongitudinalStaticStability

def run_longitudinal_static_analysis(aircraft_config_file):
    """
    Função principal para carregar uma aeronave e rodar a análise de estabilidade.
    """
    # 1. Crie uma instância da aeronave.
    my_aircraft = Aircraft(aircraft_config_file)

    # 2. Crie uma instância do analisador de estabilidade, passando a aeronave.
    stability_analyzer = LongitudinalStaticStability(my_aircraft)
    
    # Opcional: Salvar o arquivo com todos os cálculos geométricos
    my_aircraft.save_results_to_yaml('Aircraft_calculated.yaml')

# --- Ponto de Execução do Script ---
if __name__ == "__main__":
    # Defina aqui o arquivo de configuração da aeronave que você quer analisar.
    config_file = 'Aircraft.yaml'
    run_longitudinal_static_analysis(config_file)