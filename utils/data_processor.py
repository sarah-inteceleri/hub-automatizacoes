# utils/data_processor.py
"""
Módulo responsável pelo processamento e transformação dos dados
"""

import pandas as pd
from typing import Tuple, List, Dict
import re


class OlimpiadasProcessor:
    """Processador de dados para separação entre Olimpíadas e Paralimpíadas"""
    
    DEFICIENCIA_OLIMPIADAS = "Não possui deficiência/transtorno"
    ABA_IGNORADA = "DIVISÃO"
    
    def __init__(self):
        self.olimpiadas_data = {}
        self.paralimpiadas_data = []
        self.anos_set = set()
    
    def process_workbook(
        self, 
        workbook_data: Dict[str, pd.DataFrame]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Processa todas as abas do workbook
        
        Args:
            workbook_data: Dicionário com nome da aba e DataFrame
            
        Returns:
            Tuple com (olimpiadas_pivot, paralimpiadas_long, anos_ordenados)
        """
        for sheet_name, df in workbook_data.items():
            if sheet_name.upper() == self.ABA_IGNORADA:
                continue
            
            self._process_sheet(sheet_name, df)
        
        # Criar DataFrames finais
        olimpiadas_df = self._create_olimpiadas_pivot()
        paralimpiadas_df = self._create_paralimpiadas_long()
        anos_ordenados = self._get_anos_ordenados()
        
        return olimpiadas_df, paralimpiadas_df, anos_ordenados
    
    def _process_sheet(self, sheet_name: str, df: pd.DataFrame):
        """Processa uma única aba da planilha"""
        if df.empty or len(df) < 2:
            return
        
        # Nome da escola (primeira linha, primeira coluna)
        nome_escola = df.iloc[0, 0] if not pd.isna(df.iloc[0, 0]) else sheet_name
        
        # Headers estão na segunda linha (índice 1)
        headers = df.iloc[1].tolist()
        
        # Dados começam da terceira linha (índice 2)
        data_rows = df.iloc[2:].reset_index(drop=True)
        data_rows.columns = headers
        
        # Encontrar colunas relevantes
        ano_col = self._find_column(headers, ['ano'])
        deficiencia_col = self._find_column(
            headers, 
            ['deficiência', 'deficiencia', 'transtorno']
        )
        
        if ano_col is None:
            return
        
        # Inicializar dados da escola nas olimpíadas
        if nome_escola not in self.olimpiadas_data:
            self.olimpiadas_data[nome_escola] = {}
        
        # Processar cada linha
        for _, row in data_rows.iterrows():
            if pd.isna(row[ano_col]):
                continue
            
            ano = str(row[ano_col]).strip()
            self.anos_set.add(ano)
            
            # Verificar status de deficiência
            deficiencia_valor = ""
            if deficiencia_col is not None and not pd.isna(row[deficiencia_col]):
                deficiencia_valor = str(row[deficiencia_col]).strip()
            
            is_olimpiadas = deficiencia_valor == self.DEFICIENCIA_OLIMPIADAS
            
            if is_olimpiadas:
                # Adicionar às olimpíadas
                if ano not in self.olimpiadas_data[nome_escola]:
                    self.olimpiadas_data[nome_escola][ano] = 0
                self.olimpiadas_data[nome_escola][ano] += 1
            else:
                # Adicionar às paralimpíadas com a categoria (deficiência)
                # Formatar o ano para remover a palavra "ano"
                ano_formatado = self._formatar_ano_paralimpiadas(ano)
                self._add_paralimpiadas(nome_escola, ano_formatado, deficiencia_valor)
    
    def _formatar_ano_paralimpiadas(self, ano: str) -> str:
        """
        Remove a palavra 'ano' do texto, deixando apenas o número e símbolo
        Exemplo: '1° ano' -> '1°'
        """
        # Remove variações de 'ano' (com ou sem acentos, maiúsculas)
        ano_formatado = re.sub(r'\s*anos?\s*', '', ano, flags=re.IGNORECASE)
        return ano_formatado.strip()
    
    def _add_paralimpiadas(self, escola: str, ano: str, categoria: str):
        """Adiciona um registro às paralimpíadas"""
        # Se categoria estiver vazia, usar "Não informado"
        if not categoria or categoria == "":
            categoria = "Não informado"
        
        # Procurar se já existe
        for item in self.paralimpiadas_data:
            if item['escola'] == escola and item['ano'] == ano and item['categoria'] == categoria:
                item['quantidade'] += 1
                return
        
        # Se não existe, criar novo
        self.paralimpiadas_data.append({
            'escola': escola,
            'categoria': categoria,
            'ano': ano,
            'quantidade': 1
        })
    
    def _find_column(self, headers: List, keywords: List[str]) -> str:
        """Encontra uma coluna baseada em palavras-chave"""
        for header in headers:
            if pd.isna(header):
                continue
            header_lower = str(header).lower()
            for keyword in keywords:
                if keyword in header_lower:
                    return header
        return None
    
    def _get_anos_ordenados(self) -> List[str]:
        """
        Retorna lista de anos ordenada numericamente quando possível
        EJA e EJAI vão para o final
        """
        anos_list = list(self.anos_set)
        
        # Separar anos regulares de EJA/EJAI
        anos_regulares = []
        anos_eja = []
        
        for ano in anos_list:
            ano_upper = ano.upper()
            if 'EJA' in ano_upper:
                anos_eja.append(ano)
            else:
                anos_regulares.append(ano)
        
        def sort_key(ano: str):
            # Tenta extrair número do ano para ordenação
            match = re.search(r'\d+', ano)
            if match:
                return (0, int(match.group()))
            return (1, ano)
        
        # Ordenar cada lista separadamente
        anos_regulares_sorted = sorted(anos_regulares, key=sort_key)
        anos_eja_sorted = sorted(anos_eja, key=sort_key)
        
        # Retornar anos regulares primeiro, depois EJA
        return anos_regulares_sorted + anos_eja_sorted
    
    def _create_olimpiadas_pivot(self) -> pd.DataFrame:
        """Cria DataFrame pivotado para olimpíadas"""
        rows = []
        anos_ordenados = self._get_anos_ordenados()
        
        for escola, anos_dict in self.olimpiadas_data.items():
            row = {'Escola': escola}
            for ano in anos_ordenados:
                row[ano] = anos_dict.get(ano, 0)
            rows.append(row)
        
        df = pd.DataFrame(rows)
        
        # Ordenar por nome da escola
        if not df.empty:
            df = df.sort_values('Escola').reset_index(drop=True)
            
            # Reorganizar colunas: Escola primeiro, depois anos em ordem
            cols = ['Escola'] + anos_ordenados
            df = df[cols]
        
        return df
    
    def _create_paralimpiadas_long(self) -> pd.DataFrame:
        """Cria DataFrame normalizado para paralimpíadas"""
        df = pd.DataFrame(self.paralimpiadas_data)
        
        if not df.empty:
            # Renomear colunas conforme padrão
            df = df.rename(columns={
                'escola': 'Escola',
                'categoria': 'Categoria',
                'ano': 'Ano',
                'quantidade': 'Quantidade'
            })
            
            # Criar chave de ordenação numérica para anos
            def extract_number(ano_str):
                match = re.search(r'\d+', str(ano_str))
                if match:
                    return int(match.group())
                return 999  # Para casos especiais como EJA
            
            df['_sort_key'] = df['Ano'].apply(extract_number)
            
            # Ordenar por escola, categoria e ano
            df = df.sort_values(['Escola', 'Categoria', '_sort_key']).reset_index(drop=True)
            df = df.drop('_sort_key', axis=1)
            
            # Reordenar colunas: Escola, Categoria, Ano, Quantidade
            df = df[['Escola', 'Categoria', 'Ano', 'Quantidade']]
        
        return df