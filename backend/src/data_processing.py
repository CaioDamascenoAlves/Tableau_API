import pandas as pd
from .progress import TaskProgress
from tqdm import tqdm

class DataProcessor:
    """Classe responsável pelo processamento e transformação de dados."""
    
    def __init__(self):
        self.expected_columns = [
            "Cidades", "Combustíveis", "Measure Names", "Origens", 
            "Medição", "Turno + Data", "Measure Values"
        ]
        
        self.measure_names_order = [
            "Estq. Dia. Ant. Utl. Medç.",
            "Estq. Ult. Medç",
            "Venda Utl. Medç",
            "Compra Dia Ult. Medç",
            "Verificação",
            "Capac.",
            "Venda Anterior",
            "Vol. Atual",
            "Carga",
            "Vendas",
            "Estoque",
            "Giro Estoque Hoje",
            "Percent. Cap. Hoje",
            "Media",
            "Estq. Final",
            "Giro Estq Final ",  # Com espaço extra
            "Percent. Cap. Final Hoje",
            "Sugest.",
            "Média",
            "Estoque ",  # Com espaço extra
            "Giro Estq",
            "Percent. Cap.",
            "Sugest. "   # Com espaço extra
        ]
    
    def transform_csv_to_xlsx(self, csv_path, xlsx_path):
        """Lê o CSV, transforma os dados e salva em XLSX."""
        with TaskProgress("Processando dados CSV para XLSX", 100) as progress:
            try:
                progress.update(10, "Carregando arquivo CSV")
                # Ler o CSV com pandas
                df = pd.read_csv(csv_path)
                
                progress.update(10, "Validando estrutura dos dados")
                # Validar colunas
                self._validate_columns(df)
                
                # Exibir valores únicos de Measure Names para depuração
                measure_names_found = df["Measure Names"].unique().tolist()
                print(f"Colunas encontradas em 'Measure Names': {measure_names_found}")
                
                progress.update(30, "Pivotando tabela de dados")
                # Pivotar a tabela
                df_pivot = self._pivot_dataframe(df)
                
                progress.update(20, "Reorganizando colunas")
                # Reorganizar as colunas
                df_pivot = self._reorder_columns(df_pivot)
                
                progress.update(20, "Processando valores numéricos")
                # Processar valores numéricos
                df_pivot = self._process_numeric_values(df_pivot)
                
                progress.update(10, "Salvando arquivo XLSX")
                # Salvar em XLSX
                self._save_to_xlsx(df_pivot, xlsx_path)
                
            except Exception as e:
                raise Exception(f"Erro ao transformar o CSV em XLSX: {str(e)}")
    
    def _validate_columns(self, df):
        """Valida se o DataFrame contém todas as colunas esperadas."""
        if not all(col in df.columns for col in self.expected_columns):
            raise Exception(f"O CSV não contém todas as colunas esperadas: {self.expected_columns}")
    
    def _pivot_dataframe(self, df):
        """Realiza o pivot do DataFrame."""
        return df.pivot_table(
            index=["Cidades", "Origens", "Turno + Data", "Combustíveis", "Medição"],
            columns="Measure Names",
            values="Measure Values",
            aggfunc="first"  # Assume um único valor por combinação
        ).reset_index()
    
    def _reorder_columns(self, df_pivot):
        """Reorganiza as colunas do DataFrame pivotado."""
        # Verificar se todas as colunas de measure_names_order estão presentes
        missing_columns = [col for col in self.measure_names_order if col not in df_pivot.columns]
        if missing_columns:
            print(f"Aviso: As seguintes colunas de Measure Names não estão no CSV: {missing_columns}")
            # Filtrar apenas colunas existentes
            available_measure_names = [col for col in self.measure_names_order if col in df_pivot.columns]
        else:
            available_measure_names = self.measure_names_order
        
        # Reorganizar as colunas
        columns_order = ["Cidades", "Origens", "Turno + Data", "Combustíveis", "Medição"] + available_measure_names
        return df_pivot[columns_order]
    
    def _process_numeric_values(self, df):
        """Processa valores numéricos de forma segura."""
        non_index_columns = ["Cidades", "Origens", "Turno + Data", "Combustíveis", "Medição"]
        
        # Usar tqdm para mostrar progresso do processamento de colunas
        numeric_columns = [col for col in df.columns if col not in non_index_columns]
        
        for col in tqdm(numeric_columns, desc="Processando colunas numéricas", leave=False):
            if df[col].dtype.name == "object":  # Apenas para colunas de strings
                df[col] = pd.to_numeric(df[col].str.replace(",", "", regex=False), errors="coerce")
            else:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        return df
    
    def _save_to_xlsx(self, df, xlsx_path):
        """Salva o DataFrame em formato XLSX."""
        df.to_excel(xlsx_path, index=False, engine="openpyxl")
        print(f"Dados transformados salvos em: {xlsx_path}")
