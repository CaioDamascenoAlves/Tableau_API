import os
import logging
from datetime import datetime

class Logger:
    """Classe para gerenciar logs da aplicação."""
    
    def __init__(self, name="TableauAPI", log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configura os handlers de log."""
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Handler para arquivo
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, f"tableau_api_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Formato dos logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Adicionar handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log de informação."""
        self.logger.info(message)
    
    def error(self, message):
        """Log de erro."""
        self.logger.error(message)
    
    def warning(self, message):
        """Log de aviso."""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log de debug."""
        self.logger.debug(message)

class FileManager:
    """Classe para gerenciar operações com arquivos."""
    
    @staticmethod
    def ensure_directory(directory_path):
        """Garante que um diretório existe."""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            return True
        return False
    
    @staticmethod
    def file_exists(file_path):
        """Verifica se um arquivo existe."""
        return os.path.exists(file_path)
    
    @staticmethod
    def get_file_size(file_path):
        """Retorna o tamanho do arquivo em bytes."""
        if FileManager.file_exists(file_path):
            return os.path.getsize(file_path)
        return 0
    
    @staticmethod
    def delete_file(file_path):
        """Remove um arquivo se ele existir."""
        if FileManager.file_exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    @staticmethod
    def get_file_extension(file_path):
        """Retorna a extensão do arquivo."""
        return os.path.splitext(file_path)[1].lower()

class ValidationHelper:
    """Classe com métodos de validação."""
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """Valida se todos os campos obrigatórios estão presentes."""
        missing_fields = []
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Campos obrigatórios ausentes: {', '.join(missing_fields)}")
        
        return True
    
    @staticmethod
    def validate_file_extension(file_path, allowed_extensions):
        """Valida se a extensão do arquivo é permitida."""
        extension = FileManager.get_file_extension(file_path)
        if extension not in allowed_extensions:
            raise ValueError(f"Extensão '{extension}' não permitida. Extensões aceitas: {', '.join(allowed_extensions)}")
        
        return True
