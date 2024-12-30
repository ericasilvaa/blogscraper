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

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Certifique-se de que o ChromeDriver está no PATH ou indique sua localização.

## Uso

1. Execute o script principal:
   ```bash
   python techTudoScraper.py
   ```

2. Siga as instruções no terminal:
   - Escolha uma categoria de notícias a partir da lista exibida.
   - Insira o número de notícias desejadas.

3. Após a execução, o arquivo JSON com as notícias coletadas será salvo na pasta atual.

## Estrutura do Projeto

- `techTudoScraper.py`: Script principal para a coleta de notícias.
- `techTudoScraper.log`: Arquivo de log com registros detalhados da execução.
- `noticias_{categoria}.json`: Arquivo JSON gerado com os dados das notícias coletadas.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). Consulte o arquivo para mais detalhes.

## Observações

- Certifique-se de que sua conexão com a internet esteja estável durante a execução.
- Dependendo da quantidade de notícias, o processo pode levar algum tempo.
- Caso o site TechTudo atualize sua estrutura, o script pode precisar de ajustes para continuar funcionando corretamente.
