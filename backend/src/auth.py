import tableauserverclient as TSC
from .config import Config
from .progress import TaskProgress
import time

class TableauAuthenticator:
    """Classe responsável pela autenticação no Tableau Cloud."""
    
    def __init__(self, config: Config):
        self.config = config
        self.server = None
    
    def authenticate(self):
        """Autentica no Tableau Cloud usando um Personal Access Token."""
        with TaskProgress("Autenticando no Tableau", 100) as progress:
            try:
                progress.update(20, "Criando token de autenticação")
                tableau_auth = TSC.PersonalAccessTokenAuth(
                    token_name=self.config.TABLEAU_TOKEN_NAME,
                    personal_access_token=self.config.TABLEAU_TOKEN_VALUE,
                    site_id=self.config.TABLEAU_SITE_ID
                )
                
                progress.update(30, "Conectando ao servidor")
                self.server = TSC.Server(self.config.TABLEAU_SERVER, use_server_version=True)
                
                progress.update(40, "Realizando login")
                self.server.auth.sign_in(tableau_auth)
                
                progress.update(10, "Verificando versão da API")
                print(f"Versão da API do servidor: {self.server.version}")
                
                return self.server
                
            except Exception as e:
                raise Exception(f"Erro na autenticação: {str(e)}")
    
    def get_server(self):
        """Retorna o servidor autenticado."""
        if self.server is None:
            raise Exception("Servidor não autenticado. Chame authenticate() primeiro.")
        return self.server