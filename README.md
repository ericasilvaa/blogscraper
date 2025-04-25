# blogscraper


## Funcionalidades 

 **Listagem de Categorias**: Identifica e exibe todas as categorias ou seções disponíveis no blog alvo.
- **Coleta de Artigos**: Permite definir a quantidade de artigos a serem coletados em uma categoria.
- **Exportação para JSON**: Salva os dados extraídos (título, autor, data, conteúdo, link) em arquivos `.json`.
- **Automação Completa**: Utiliza Selenium para automação da navegação e BeautifulSoup para extração dos dados.

## 📦 Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome
- Bibliotecas Python:
  - `selenium`
  - `beautifulsoup4`
  - `requests`

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seudominio/blogScraper.git
   cd blogScraper

2. Crie um ambiente virtual:
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate


3. Instale as dependências:
pip install -r requirements.txt


4. Certifique-se de que o chromedriver está disponível no seu PATH ou informe o caminho no script.

    Execute o script principal:

    python blogScraper.py / python3 blogScraper.py


5. Siga as instruções no terminal:

Escolha uma categoria de artigos.

Informe o número de posts que deseja coletar.

6. Os dados serão salvos como:

artigos_{categoria}.json
