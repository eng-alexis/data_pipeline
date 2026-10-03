from pdv_simulator.config.paths import PDV_SALES_DIR, NUM_SIMULATIONS
from pdv_simulator.history.simulations import update_num_simulations
import shutil
import os

path =  r"/home/alexis/data_pipeline/pdv_sales"

# Apaga diretório pdv_sales e zera o numero da ultima simulação

print("=" * 60)
print("ATENÇÃO - A operação resulta na exclusão permanente")
print(f"do diretório e todos os seus arquivos...")
print("=" * 60)

confirmacao = input("Deseja continuar? Digite 'SIM' para confirmar: ").strip()

if confirmacao == "SIM":
    if os.path.exists(PDV_SALES_DIR):
        try:
            shutil.rmtree(PDV_SALES_DIR)
            print("Diretório excluído com sucesso.")
            
        except Exception as e:
            print(f"Erro ao excluir: {e}")
            
        update_num_simulations(NUM_SIMULATIONS, 0)

    else:
        print("O diretório informado não existe.")
else:
    print("Operação cancelada pelo usuário.")