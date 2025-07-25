from tqdm import tqdm
import time
from typing import Optional, Any

class ProgressManager:
    """Classe para gerenciar barras de progresso com tqdm."""
    
    def __init__(self):
        self.current_bar: Optional[tqdm] = None
    
    def create_progress_bar(self, total: int, description: str, unit: str = "it") -> tqdm:
        """Cria uma nova barra de progresso."""
        self.current_bar = tqdm(
            total=total,
            desc=description,
            unit=unit,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
            colour='green'
        )
        return self.current_bar
    
    def update_progress(self, n: int = 1, description: Optional[str] = None):
        """Atualiza a barra de progresso atual."""
        if self.current_bar:
            self.current_bar.update(n)
            if description:
                self.current_bar.set_description(description)
    
    def finish_progress(self, final_message: Optional[str] = None):
        """Finaliza a barra de progresso atual."""
        if self.current_bar:
            if final_message:
                self.current_bar.set_description(final_message)
            self.current_bar.close()
            self.current_bar = None
    
    def set_postfix(self, **kwargs):
        """Define informações adicionais na barra de progresso."""
        if self.current_bar:
            self.current_bar.set_postfix(**kwargs)

class TaskProgress:
    """Context manager para barras de progresso de tarefas."""
    
    def __init__(self, description: str, total_steps: int = 100, unit: str = "%"):
        self.description = description
        self.total_steps = total_steps
        self.unit = unit
        self.progress_bar = None
        self.current_step = 0
    
    def __enter__(self):
        self.progress_bar = tqdm(
            total=self.total_steps,
            desc=self.description,
            unit=self.unit,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
            colour='blue'
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.progress_bar:
            if exc_type is None:
                # Completa a barra se não houve erro
                self.progress_bar.n = self.total_steps
                self.progress_bar.set_description(f"{self.description} - Concluído")
                self.progress_bar.refresh()
            else:
                # Marca como erro se houve exceção
                self.progress_bar.set_description(f"{self.description} - Erro")
                self.progress_bar.colour = 'red'
                self.progress_bar.refresh()
            
            time.sleep(0.5)  # Pequena pausa para visualizar o resultado
            self.progress_bar.close()
    
    def update(self, steps: int = 1, message: Optional[str] = None):
        """Atualiza o progresso."""
        if self.progress_bar:
            self.current_step = min(self.current_step + steps, self.total_steps)
            self.progress_bar.n = self.current_step
            if message:
                self.progress_bar.set_description(f"{self.description} - {message}")
            self.progress_bar.refresh()
    
    def set_progress(self, percentage: float, message: Optional[str] = None):
        """Define o progresso como uma porcentagem."""
        if self.progress_bar:
            self.current_step = int((percentage / 100) * self.total_steps)
            self.progress_bar.n = self.current_step
            if message:
                self.progress_bar.set_description(f"{self.description} - {message}")
            self.progress_bar.refresh()

def simulate_work_with_progress(description: str, steps: int, work_function=None):
    """Simula trabalho com barra de progresso."""
    with TaskProgress(description, steps) as progress:
        for i in range(steps):
            if work_function:
                work_function(i)
            else:
                time.sleep(0.1)  # Simula trabalho
            progress.update(1, f"Processando item {i+1}/{steps}")
