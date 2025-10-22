# utils/file_handler.py
"""
Módulo responsável pela leitura e escrita de arquivos
"""

import pandas as pd
from typing import Dict, BinaryIO
from io import BytesIO
import openpyxl


class FileHandler:
    """Manipulador de arquivos Excel e CSV"""
    
    @staticmethod
    def read_excel(file: BinaryIO) -> Dict[str, pd.DataFrame]:
        """
        Lê arquivo Excel e retorna dicionário com todas as abas
        
        Args:
            file: Arquivo binário do Excel
            
        Returns:
            Dicionário com {nome_aba: DataFrame}
        """
        excel_file = pd.ExcelFile(file)
        workbook_data = {}
        
        for sheet_name in excel_file.sheet_names:
            # Ler sem usar a primeira linha como header
            df = pd.read_excel(
                excel_file,
                sheet_name=sheet_name,
                header=None
            )
            workbook_data[sheet_name] = df
        
        return workbook_data
    
    @staticmethod
    def to_excel(df: pd.DataFrame, filename: str = "output.xlsx") -> bytes:
        """
        Converte DataFrame para bytes de Excel
        
        Args:
            df: DataFrame a ser convertido
            filename: Nome do arquivo (não usado, mantido para compatibilidade)
            
        Returns:
            Bytes do arquivo Excel
        """
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados')
        
        return output.getvalue()
    
    @staticmethod
    def to_csv(df: pd.DataFrame) -> str:
        """
        Converte DataFrame para string CSV
        
        Args:
            df: DataFrame a ser convertido
            
        Returns:
            String com conteúdo CSV
        """
        return df.to_csv(index=False, encoding='utf-8-sig')
    
    @staticmethod
    def get_download_button_data(df: pd.DataFrame, format: str = 'excel') -> tuple:
        """
        Prepara dados para botão de download
        
        Args:
            df: DataFrame a ser baixado
            format: 'excel' ou 'csv'
            
        Returns:
            Tuple com (data, mime_type, extension)
        """
        if format.lower() == 'excel':
            data = FileHandler.to_excel(df)
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ext = 'xlsx'
        else:  # csv
            data = FileHandler.to_csv(df)
            mime = 'text/csv'
            ext = 'csv'
        
        return data, mime, ext