import requests
import os
from typing import Optional, Dict, Any
from .utils import Logger, FileManager, ValidationHelper
from .progress import TaskProgress

class CombustivelAPIClient:
    """Cliente para integração com a API de Combustível."""
    
    def __init__(self, base_url: str, auth_token: str):
        """
        Inicializa o cliente da API.
        
        Args:
            base_url (str): URL base da API
            auth_token (str): Token de autenticação
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.logger = Logger("CombustivelAPIClient")
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Configura a sessão HTTP com headers padrão."""
        self.session.headers.update({
            "Authorization": f"Bearer {self.auth_token}",
            "Accept": "application/json"
        })
    
    def upload_excel_file(self, file_path: str, timeout: int = 300) -> Dict[str, Any]:
        """
        Faz upload de um arquivo Excel para a API de combustível.
        
        Args:
            file_path (str): Caminho absoluto para o arquivo Excel
            timeout (int): Timeout da requisição em segundos
            
        Returns:
            Dict[str, Any]: Resposta da API
            
        Raises:
            Exception: Em caso de erro no upload
        """
        with TaskProgress("Enviando arquivo para API", 100) as progress:
            try:
                progress.update(10, "Validando arquivo")
                self._validate_file(file_path)
                
                progress.update(20, "Preparando upload")
                file_size = FileManager.get_file_size(file_path)
                self.logger.info(f"Iniciando upload do arquivo: {file_path} ({file_size:,} bytes)")
                
                progress.update(30, "Abrindo arquivo")
                with open(file_path, 'rb') as file:
                    files = {'file': (os.path.basename(file_path), file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                    
                    progress.update(30, "Enviando dados")
                    response = self._make_upload_request(files, timeout)
                
                progress.update(10, "Processando resposta")
                return self._handle_response(response, file_path)
                
            except Exception as e:
                self.logger.error(f"Erro no upload do arquivo: {str(e)}")
                raise Exception(f"Erro no upload do arquivo: {str(e)}")
    
    def _validate_file(self, file_path: str):
        """Valida se o arquivo existe e tem a extensão correta."""
        if not FileManager.file_exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        ValidationHelper.validate_file_extension(file_path, ['.xlsx', '.xls'])
        
        file_size = FileManager.get_file_size(file_path)
        if file_size == 0:
            raise ValueError(f"Arquivo está vazio: {file_path}")
        
        # Verificar se o arquivo não é muito grande (limite de 50MB por exemplo)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            raise ValueError(f"Arquivo muito grande ({file_size:,} bytes). Máximo permitido: {max_size:,} bytes")
    
    def _make_upload_request(self, files: Dict, timeout: int) -> requests.Response:
        """Realiza a requisição HTTP de upload."""
        url = f"{self.base_url}/importacao-excel/upload"
        
        try:
            response = self.session.post(
                url=url,
                files=files,
                timeout=timeout
            )
            return response
            
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout na requisição após {timeout} segundos")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Erro de conexão com a API: {self.base_url}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição HTTP: {str(e)}")
    
    def _handle_response(self, response: requests.Response, file_path: str) -> Dict[str, Any]:
        """
        Processa a resposta da API.
        
        Note: A API de Combustível retorna status 201 (Created) para uploads bem-sucedidos,
        que é o padrão REST para operações de criação. Também suportamos 200 para compatibilidade.
        """
        self.logger.info(f"Status da resposta: {response.status_code}")
        
        try:
            response_data = response.json()
        except ValueError:
            response_data = {"message": response.text}
        
        if response.status_code == 201:
            self.logger.info(f"Upload realizado com sucesso: {file_path}")
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Upload realizado com sucesso",
                "data": response_data,
                "file_path": file_path
            }
        
        elif response.status_code == 200:
            # Algumas APIs podem retornar 200 em vez de 201
            self.logger.info(f"Upload realizado com sucesso: {file_path}")
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Upload realizado com sucesso",
                "data": response_data,
                "file_path": file_path
            }
        
        elif response.status_code == 401:
            error_msg = "Erro de autenticação. Verifique o token de autorização."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        elif response.status_code == 413:
            error_msg = "Arquivo muito grande para upload."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        elif response.status_code == 422:
            error_msg = f"Erro de validação: {response_data.get('message', 'Dados inválidos')}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        elif response.status_code >= 500:
            error_msg = f"Erro interno do servidor: {response_data.get('message', 'Erro desconhecido')}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        
        else:
            error_msg = f"Erro no upload (HTTP {response.status_code}): {response_data.get('message', 'Erro desconhecido')}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def test_connection(self) -> bool:
        """Testa a conexão com a API."""
        try:
            with TaskProgress("Testando conexão com API", 100) as progress:
                progress.update(50, "Verificando conectividade")
                
                # Tenta uma requisição simples para verificar conectividade
                response = self.session.get(f"{self.base_url}/", timeout=10)
                
                progress.update(50, "Analisando resposta")
                
                self.logger.info(f"Teste de conexão - Status: {response.status_code}")
                
                # Considera sucesso para qualquer status que não seja erro de cliente/servidor
                # ou para códigos específicos que indicam que a API está respondendo
                success_codes = [200, 201, 204, 404]  # 404 pode indicar que a API existe mas a rota raiz não
                if response.status_code in success_codes or response.status_code < 500:
                    return True
                else:
                    return False
                
        except Exception as e:
            self.logger.error(f"Falha no teste de conexão: {str(e)}")
            return False
    
    def get_upload_status(self, upload_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Verifica o status de um upload (se a API suportar).
        
        Args:
            upload_id (str): ID do upload para verificar status
            
        Returns:
            Dict[str, Any]: Status do upload
        """
        if not upload_id:
            return {"message": "ID do upload não fornecido"}
        
        try:
            url = f"{self.base_url}/importacao-excel/status/{upload_id}"
            response = self.session.get(url, timeout=30)
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return {
                    "error": f"Erro ao verificar status (HTTP {response.status_code})",
                    "details": response.text
                }
                
        except Exception as e:
            self.logger.error(f"Erro ao verificar status do upload: {str(e)}")
            return {"error": str(e)}
    
    def close(self):
        """Fecha a sessão HTTP."""
        if self.session:
            self.session.close()
            self.logger.info("Sessão HTTP fechada")
    
    def __enter__(self):
        """Context manager - entrada."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - saída."""
        self.close()

class CombustivelAPIUploader:
    """Classe simplificada para upload de arquivos Excel."""
    
    def __init__(self, api_url: str, auth_token: str):
        """
        Inicializa o uploader.
        
        Args:
            api_url (str): URL da API de Combustível
            auth_token (str): Token de autenticação
        """
        if not api_url:
            raise ValueError("URL da API de Combustível é obrigatória")
        if not auth_token:
            raise ValueError("Token de autenticação é obrigatório")
            
        self.api_url = api_url
        self.token = auth_token
        self.logger = Logger("CombustivelUploader")
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload simplificado de arquivo.
        
        Args:
            file_path (str): Caminho para o arquivo Excel
            
        Returns:
            Dict[str, Any]: Resultado do upload
        """
        with CombustivelAPIClient(base_url=self.api_url, auth_token=self.token) as client:
            return client.upload_excel_file(file_path)
    
    def test_api_connection(self) -> bool:
        """Testa a conexão com a API."""
        with CombustivelAPIClient(base_url=self.api_url, auth_token=self.token) as client:
            return client.test_connection()
