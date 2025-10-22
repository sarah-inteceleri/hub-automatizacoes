"""
Página de Unir Abas - Processamento de Olimpíadas e Paralimpíadas
"""

import streamlit as st
import pandas as pd
from utils.data_processor import OlimpiadasProcessor
from utils.file_handler import FileHandler

def run():
    """Função principal da página de unir abas"""
    
    st.title("📊 Processador de Olimpíadas e Paralimpíadas")
    
    st.markdown("""
    Este sistema processa planilhas de participantes de olimpíadas escolares, 
    separando automaticamente os dados em **Olimpíadas** e **Paralimpíadas**.
    """)
    
    st.markdown("---")
    
    # Sidebar com informações específicas
    with st.sidebar:
        st.markdown("### 🎯 Critério de Classificação")
        st.success(
            "**Olimpíadas:** Alunos com texto exato 'Não possui deficiência/transtorno'\n\n"
            "**Paralimpíadas:** Qualquer outro valor ou vazio"
        )
        
        st.markdown("### 📋 Formatos de Saída")
        st.markdown(
            "🥇 **Olimpíadas:** Formato pivotado (anos nas colunas)\n\n"
            "🥈 **Paralimpíadas:** Formato normalizado (long format)"
        )
    
    # Seção de upload
    render_upload_section()
    
    # Processar arquivo se enviado
    if 'uploaded_file_olimpiadas' in st.session_state and st.session_state['uploaded_file_olimpiadas'] is not None:
        uploaded_file = st.session_state['uploaded_file_olimpiadas']
        
        try:
            with st.spinner("🔄 Processando planilha..."):
                # Processar arquivo
                processor = OlimpiadasProcessor()
                file_handler = FileHandler()
                
                # Ler arquivo Excel
                workbook_data = file_handler.read_excel(uploaded_file)
                
                # Processar dados
                olimpiadas_df, paralimpiadas_df, anos_ordenados = processor.process_workbook(
                    workbook_data
                )
                
                # Salvar no session state
                st.session_state['olimpiadas'] = olimpiadas_df
                st.session_state['paralimpiadas'] = paralimpiadas_df
                st.session_state['anos_ordenados'] = anos_ordenados
                st.session_state['processed'] = True
                
            st.success("✅ Planilha processada com sucesso!")
            
            # Renderizar resultados
            render_results_section(
                olimpiadas_df,
                paralimpiadas_df,
                anos_ordenados,
                file_handler
            )
            
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
            with st.expander("🔍 Ver detalhes do erro"):
                st.exception(e)
    else:
        # Mostrar instruções quando não há arquivo
        render_instructions()


def render_upload_section():
    """Renderiza a seção de upload"""
    st.markdown("### 📤 Upload da Planilha")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Escolha o arquivo Excel",
            type=['xlsx', 'xls'],
            help="Selecione a planilha com múltiplas abas (uma por escola)",
            key='uploaded_file_olimpiadas'
        )


def render_results_section(
    olimpiadas_df: pd.DataFrame,
    paralimpiadas_df: pd.DataFrame,
    anos_ordenados: list,
    file_handler: FileHandler
):
    """Renderiza a seção de resultados"""
    st.markdown("---")
    st.markdown("## 📊 Resultados")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    total_olimpiadas = 0
    if not olimpiadas_df.empty and len(olimpiadas_df.columns) > 1:
        total_olimpiadas = olimpiadas_df.iloc[:, 1:].sum().sum()
    
    total_paralimpiadas = paralimpiadas_df['Quantidade'].sum() if not paralimpiadas_df.empty else 0
    total_escolas = len(olimpiadas_df) if not olimpiadas_df.empty else 0
    
    with col1:
        st.metric("🥇 Total Olimpíadas", int(total_olimpiadas))
    with col2:
        st.metric("🥈 Total Paralimpíadas", int(total_paralimpiadas))
    with col3:
        st.metric("🏫 Total de Escolas", total_escolas)
    
    st.markdown("---")
    
    # Seção Olimpíadas
    st.markdown("### 🥇 Olimpíadas - Formato Pivotado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📊 **{len(olimpiadas_df)}** escolas processadas")
    with col2:
        st.info(f"📅 **{len(anos_ordenados)}** anos escolares encontrados")
    
    with st.expander("👁️ Visualizar dados", expanded=True):
        st.dataframe(olimpiadas_df, use_container_width=True, height=400)
    
    # Botões de download Olimpíadas
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data, mime, ext = file_handler.get_download_button_data(olimpiadas_df, 'excel')
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name=f"olimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    with col2:
        csv_data, mime, ext = file_handler.get_download_button_data(olimpiadas_df, 'csv')
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name=f"olimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Seção Paralimpíadas
    st.markdown("### 🥈 Paralimpíadas - Formato Normalizado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📊 **{len(paralimpiadas_df)}** registros processados")
    with col2:
        if not paralimpiadas_df.empty:
            escolas_para = paralimpiadas_df['Escola'].nunique()
            st.info(f"🏫 **{escolas_para}** escolas com participantes")
    
    with st.expander("👁️ Visualizar dados", expanded=True):
        st.dataframe(paralimpiadas_df, use_container_width=True, height=400)
    
    # Botões de download Paralimpíadas
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data, mime, ext = file_handler.get_download_button_data(paralimpiadas_df, 'excel')
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name=f"paralimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    with col2:
        csv_data, mime, ext = file_handler.get_download_button_data(paralimpiadas_df, 'csv')
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name=f"paralimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )


def render_instructions():
    """Renderiza as instruções de uso"""
    st.markdown("---")
    st.markdown("## 📋 Como Usar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Preparação
        - Certifique-se de que sua planilha tenha múltiplas abas
        - Cada aba representa uma escola diferente
        - A aba "DIVISÃO" será automaticamente ignorada
        
        ### 2️⃣ Estrutura Esperada
        - **Linha 1:** Nome da escola
        - **Linha 2:** Cabeçalhos das colunas
        - **Linha 3+:** Dados dos estudantes
        
        ### 3️⃣ Colunas Necessárias
        - `Ano` - Ano escolar do estudante
        - `Deficiência/Transtorno` - Status do estudante
        """)
    
    with col2:
        st.markdown("""
        ### 4️⃣ Processamento
        O sistema irá:
        - ✅ Ler todas as abas (exceto "DIVISÃO")
        - ✅ Identificar automaticamente as colunas
        - ✅ Separar em Olimpíadas e Paralimpíadas
        - ✅ Gerar dois relatórios diferentes
        
        ### 5️⃣ Formatos de Saída
        **🥇 Olimpíadas:** Formato pivotado
        - Anos regulares primeiro, EJA/EJAI no final
        
        **🥈 Paralimpíadas:** Formato normalizado
        - Ano sem a palavra "ano" (ex: "1°", "2°")
        """)
    
    st.markdown("---")
    
    # Exemplos visuais
    st.markdown("### 📊 Exemplos de Saída")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🥇 Olimpíadas (Pivotado)**")
        exemplo_olimpiadas = pd.DataFrame({
            'Escola': ['ESC. MUNICIPAL PEIXE-BOI', 'ESC. ESTADUAL EXEMPLO'],
            '1° ano': [5, 3],
            '2° ano': [3, 2],
            '5° ano': [10, 7],
            'EJA': [2, 4]
        })
        st.dataframe(exemplo_olimpiadas, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**🥈 Paralimpíadas (Normalizado)**")
        exemplo_paralimpiadas = pd.DataFrame({
            'Escola': ['ESC. MUN. PEIXE-BOI', 'ESC. MUN. PEIXE-BOI'],
            'Categoria': ['TEA', 'TDAH'],
            'Ano': ['5°', '3°'],
            'Quantidade': [10, 5]
        })
        st.dataframe(exemplo_paralimpiadas, use_container_width=True, hide_index=True)