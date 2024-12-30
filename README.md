# techTudoScraper

techTudoScraper é uma aplicação em Python para coletar e organizar notícias do site TechTudo. Ela é útil para pesquisadores, analistas de dados e entusiastas de tecnologia que desejam analisar conteúdo específico de forma automatizada.

## Funcionalidades

- **Listagem de Categorias**: Identifica e lista todas as categorias de notícias disponíveis no TechTudo.
- **Coleta de Notícias**: Permite coletar uma quantidade específica de notícias de uma categoria escolhida.
- **Exportação para JSON**: Salva os dados coletados em arquivos JSON organizados.
- **Automação Completa**: Utiliza Selenium para navegação e BeautifulSoup para análise de conteúdo.

## Requisitos

- Python 3.8 ou superior
- Dependências Python (instaláveis via `pip`):
  - selenium
  - beautifulsoup4
  - requests
- Google Chrome instalado
- ChromeDriver compatível com a versão do Google Chrome

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/odoricoveloso/techTudoScraper.git
   cd techTudoScraper
