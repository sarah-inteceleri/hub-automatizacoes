# 🛠️ Hub de Automatizações

Sistema unificado de automatizações para processar planilhas e gerar documentos.

## 🎯 Funcionalidades

### 🏷️ Criação de Etiquetas
- Gera etiquetas em PDF para provas escolares
- Suporta provas adaptadas e não adaptadas
- Detecção automática de colunas
- Limpeza inteligente de nomes de escolas
- Exportação em PDF pronto para impressão

### 📊 Unir Abas (Olimpíadas)
- Processa planilhas de olimpíadas escolares
- Separa automaticamente Olimpíadas e Paralimpíadas
- Formato pivotado para Olimpíadas
- Formato normalizado para Paralimpíadas
- Exportação em Excel ou CSV

## 🚀 Como Usar

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/hub-automatizacoes.git
cd hub-automatizacoes
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run app.py
```

### Deploy no Streamlit Cloud

1. Faça fork deste repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Configure o arquivo principal como `app.py`
5. Deploy! 🎉

## 📁 Estrutura do Projeto
```
hub-automatizacoes/
├── app.py                          # Hub principal
├── pages/
│   ├── etiquetas.py               # Página de etiquetas
│   └── unir_abas.py               # Página de unir abas
├── modules/
│   ├── criacao_adaptadas.py       # Geração de PDF adaptadas
│   ├── criacao_nao_adaptadas.py   # Geração de PDF não adaptadas
│   ├── etiquetas_adaptadas_logic.py
│   └── etiquetas_nao_adaptadas_logic.py
├── utils/
│   ├── data_processor.py          # Processamento de dados
│   ├── file_handler.py            # Manipulação de arquivos
│   └── ui_components.py           # Componentes de UI
├── .streamlit/
│   └── config.toml                # Configurações do Streamlit
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologias

- **Streamlit** - Interface web
- **Pandas** - Manipulação de dados
- **ReportLab** - Geração de PDFs
- **OpenPyXL** - Leitura/escrita de Excel

## 📋 Requisitos

- Python 3.8+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- ReportLab 4.0.0+
- OpenPyXL 3.0.0+

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido com ❤️ para automatizar processos educacionais.