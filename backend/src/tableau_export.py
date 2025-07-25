import tableauserverclient as TSC
import os
from .progress import TaskProgress

class TableauExporter:
    """Classe responsável pela exportação de dados do Tableau."""
    
    def __init__(self, server):
        self.server = server
    
    def export_base_dados_csv(self, workbook_id, view_id, csv_path):
        """Exporta a worksheet BASE DE DADOS do Tableau Server para um arquivo CSV."""
        with TaskProgress("Exportando dados do Tableau", 100) as progress:
            try:
                progress.update(20, "Obtendo pasta de trabalho")
                # Obter a pasta de trabalho pelo ID
                workbook = self._get_workbook(workbook_id)
                
                progress.update(20, "Carregando visualizações")
                # Popula as visualizações da pasta de trabalho
                self.server.workbooks.populate_views(workbook)
                
                progress.update(20, "Localizando view específica")
                # Encontrar a view pelo ID
                view = self._get_view(workbook, view_id)
                
                progress.update(30, "Exportando dados como CSV")
                # Exportar dados da worksheet como CSV
                self._export_view_to_csv(view, csv_path)
                
                progress.update(10, "Finalização")
                
            except Exception as e:
                raise Exception(f"Erro ao exportar a worksheet BASE DE DADOS: {str(e)}")
    
    def _get_workbook(self, workbook_id):
        """Obtém a pasta de trabalho pelo ID."""
        workbook = self.server.workbooks.get_by_id(workbook_id)
        if not workbook:
            raise Exception(f"Pasta de trabalho com ID {workbook_id} não encontrada.")
        return workbook
    
    def _get_view(self, workbook, view_id):
        """Encontra a view pelo ID dentro da pasta de trabalho."""
        for view in workbook.views:
            if view.id == view_id:
                return view
        
        raise Exception(f"View com ID {view_id} não encontrada.")
    
    def _export_view_to_csv(self, view, csv_path):
        """Exporta a view para um arquivo CSV."""
        self.server.views.populate_csv(view)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        with open(csv_path, "wb") as f:
            f.write(b''.join(view.csv))
        
        print(f"Dados da worksheet 'BASE DE DADOS' exportados para: {csv_path}")
    
    def list_workbooks(self):
        """Lista todas as pastas de trabalho disponíveis."""
        with TaskProgress("Listando pastas de trabalho", 100) as progress:
            progress.update(50, "Obtendo lista do servidor")
            workbooks, _ = self.server.workbooks.get()
            progress.update(50, "Processando resultados")
            return [(wb.id, wb.name) for wb in workbooks]
    
    def list_views_in_workbook(self, workbook_id):
        """Lista todas as views de uma pasta de trabalho específica."""
        with TaskProgress("Listando views da pasta de trabalho", 100) as progress:
            progress.update(30, "Obtendo pasta de trabalho")
            workbook = self._get_workbook(workbook_id)
            progress.update(40, "Carregando views")
            self.server.workbooks.populate_views(workbook)
            progress.update(30, "Processando resultados")
            return [(view.id, view.name) for view in workbook.views]