from .auth import TableauAuthenticator
from .tableau_export import TableauExporter
from .data_processing import DataProcessor
from .config import Config
from .utils import Logger
from .progress import TaskProgress
from .api_integration import CombustivelAPIUploader
import os
from tqdm import tqdm

class TableauAPIApp:
    """Classe principal da aplicação Tableau API."""
    
    def __init__(self):
        self.config = Config()
        self.authenticator = TableauAuthenticator(self.config)
        self.data_processor = DataProcessor()
        self.logger = Logger("TableauAPIApp")
        
        # Inicializar uploader apenas se upload estiver habilitado e configurações estiverem presentes
        if (self.config.ENABLE_API_UPLOAD and 
            self.config.COMBUSTIVEL_API_URL and 
            self.config.COMBUSTIVEL_API_TOKEN):
            self.api_uploader = CombustivelAPIUploader(
                self.config.COMBUSTIVEL_API_URL,
                self.config.COMBUSTIVEL_API_TOKEN
            )
        else:
            self.api_uploader = None
            
        self.server = None
        self.exporter = None
    
    def initialize(self):
        """Inicializa a aplicação com configurações e autenticação."""
        with TaskProgress("Inicializando aplicação", 100) as progress:
            try:
                self.logger.info("Iniciando aplicação...")
                progress.update(10, "Carregando configurações")
                
                # Validar configurações
                self.config.validate_config()
                self.logger.info("Configurações validadas com sucesso")
                progress.update(20, "Configurações validadas")
                
                # Criar diretório de saída
                self.config.ensure_output_directory()
                progress.update(20, "Diretório de saída criado")
                
                # Autenticar no Tableau
                progress.update(30, "Iniciando autenticação")
                self.server = self.authenticator.authenticate()
                self.logger.info("Autenticação no Tableau realizada com sucesso")
                
                # Inicializar exportador
                progress.update(20, "Inicializando exportador")
                self.exporter = TableauExporter(self.server)
                
                self.logger.info("Aplicação inicializada com sucesso!")
                
            except Exception as e:
                self.logger.error(f"Erro na inicialização: {str(e)}")
                raise Exception(f"Erro na inicialização: {str(e)}")
    
    def run(self):
        """Executa o fluxo principal da aplicação."""
        try:
            print("\n🚀 Iniciando processamento dos dados do Tableau...")
            print("=" * 60)
            
            # Inicializar aplicação
            self.initialize()
            
            # Definir caminhos dos arquivos
            csv_path = os.path.join(self.config.OUTPUT_DIR, self.config.NAME_FILE_ORIGINAL)
            xlsx_path = os.path.join(self.config.OUTPUT_DIR, self.config.NAME_FILE_PROCESSED)
            
            print(f"\n📁 Arquivos de saída:")
            print(f"   CSV: {csv_path}")
            print(f"   XLSX: {xlsx_path}")
            print()
            
            # Fluxo principal com barra de progresso geral
            main_steps = [
                ("Exportando dados do Tableau", lambda: self.exporter.export_base_dados_csv(
                    self.config.WORKBOOK_ID, self.config.VIEW_ID, csv_path)),
                ("Transformando dados", lambda: self.data_processor.transform_csv_to_xlsx(csv_path, xlsx_path))
            ]
            
            # Adicionar upload da API se habilitado
            if self.config.ENABLE_API_UPLOAD and self.api_uploader:
                main_steps.append(("Enviando para API de Combustível", lambda: self._upload_to_api(xlsx_path)))
            
            for step_name, step_function in tqdm(main_steps, desc="Progresso geral", unit="etapa"):
                self.logger.info(f"Executando: {step_name}")
                step_function()
            
            print("\n✅ Processamento concluído com sucesso!")
            print("=" * 60)
            self.logger.info("Processamento concluído com sucesso!")
            
            # Mostrar informações dos arquivos gerados
            self._show_file_info(csv_path, xlsx_path)
            
        except Exception as e:
            print(f"\n❌ Erro durante a execução: {str(e)}")
            print("=" * 60)
            self.logger.error(f"Erro durante a execução: {str(e)}")
            raise
    
    def _show_file_info(self, csv_path, xlsx_path):
        """Mostra informações sobre os arquivos gerados."""
        print("\n📊 Informações dos arquivos gerados:")
        
        if os.path.exists(csv_path):
            csv_size = os.path.getsize(csv_path)
            print(f"   📄 CSV: {csv_size:,} bytes")
        
        if os.path.exists(xlsx_path):
            xlsx_size = os.path.getsize(xlsx_path)
            print(f"   📈 XLSX: {xlsx_size:,} bytes")
        
        print()
    
    def _upload_to_api(self, xlsx_path):
        """Faz upload do arquivo XLSX para a API de combustível."""
        try:
            self.logger.info(f"Iniciando upload para API: {xlsx_path}")
            
            # Verificar se o arquivo existe
            if not os.path.exists(xlsx_path):
                raise FileNotFoundError(f"Arquivo não encontrado para upload: {xlsx_path}")
            
            # Realizar upload
            result = self.api_uploader.upload_file(xlsx_path)
            
            if result.get("success"):
                self.logger.info("Upload para API realizado com sucesso!")
                print(f"✅ Arquivo enviado para API: {os.path.basename(xlsx_path)}")
                
                # Mostrar informações do resultado se disponível
                if "data" in result:
                    data = result["data"]
                    if isinstance(data, dict) and "message" in data:
                        print(f"   📤 Resposta da API: {data['message']}")
            else:
                self.logger.error("Falha no upload para API")
                print(f"❌ Falha no upload para API")
                
        except Exception as e:
            self.logger.error(f"Erro no upload para API: {str(e)}")
            print(f"⚠️  Erro no upload para API: {str(e)}")
            # Não falha o processo principal se o upload falhar
            print("   ℹ️  O processamento principal foi concluído com sucesso")

def main():
    """Função principal de entrada da aplicação."""
    try:
        app = TableauAPIApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processamento interrompido pelo usuário.")
    except Exception as e:
        print(f"\n💥 Erro fatal: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())