from dotenv import load_dotenv
import os

class Config:
    """Classe para gerenciar configurações da aplicação."""
    
    def __init__(self):
        load_dotenv()
        self._load_config()
        
    def _load_config(self):
        """Carrega as configurações do ambiente."""
        # Configurações do Tableau Cloud
        self.TABLEAU_SERVER = os.getenv("TABLEAU_SERVER")
        self.TABLEAU_SITE_ID = os.getenv("TABLEAU_SITE_ID")
        self.TABLEAU_TOKEN_NAME = os.getenv("TABLEAU_TOKEN_NAME")
        self.TABLEAU_TOKEN_VALUE = os.getenv("TABLEAU_TOKEN_VALUE")
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
        self.WORKBOOK_ID = os.getenv("WORKBOOK_ID")
        self.VIEW_ID = os.getenv("VIEW_ID")
        self.NAME_FILE_ORIGINAL = os.getenv("NAME_FILE_ORIGINAL", "BASE_DE_DADOS.csv")
        self.NAME_FILE_PROCESSED = os.getenv("NAME_FILE_PROCESSED", "ANALISE_DE_PEDIDOS.xlsx")
    
    def ensure_output_directory(self):
        """Cria o diretório de saída caso ele não exista."""
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)
            print(f"Diretório criado: {self.OUTPUT_DIR}")
        else:
            print(f"Diretório já existe: {self.OUTPUT_DIR}")
    
    def validate_config(self):
        """Valida se todas as configurações necessárias estão definidas."""
        required_configs = [
            'TABLEAU_SERVER', 'TABLEAU_SITE_ID', 'TABLEAU_TOKEN_NAME',
            'TABLEAU_TOKEN_VALUE', 'WORKBOOK_ID', 'VIEW_ID'
        ]
        
        missing_configs = []
        for config in required_configs:
            if not getattr(self, config):
                missing_configs.append(config)
        
        if missing_configs:
            raise Exception(f"Configurações obrigatórias não definidas: {', '.join(missing_configs)}")
        
        return True