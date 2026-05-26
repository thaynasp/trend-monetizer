import os
import json
import markdown
import glob

# Carregar configuração
with open('../config.json', 'r') as f:
    config = json.load(f)

# Carregar template
with open('../assets/template.html', 'r') as f:
    template = f.read()

# Criar pasta docs se não existir
if not os.path.exists('../docs'):
    os.makedirs('../docs')
if not os.path.exists('../docs/blog'):
    os.makedirs('../docs/blog')

def generate_page(md_path):
    with open(md_path, 'r') as f:
        md_content = f.read()
    
    # Extrair título (primeira linha #)
    lines = md_content.split('\n')
    title = "Artigo"
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Converter para HTML
    html_content = markdown.markdown(md_content)
    
    # Substituir placeholders
    page_html = template.replace('{{title}}', title)
    page_html = page_html.replace('{{site_name}}', config['site_name'])
    page_html = page_html.replace('{{site_tagline}}', config['site_tagline'])
    page_html = page_html.replace('{{contact_email}}', config['contact_email'])
    page_html = page_html.replace('{{content}}', html_content)
    page_html = page_html.replace('{{description}}', f"Saiba tudo sobre {title} no Portal Vitalidade Feminina.")
    
    # Lógica simples para link de afiliado (poderia ser mais complexo)
    affiliate_link = config['affiliate_links']['magnesium'] # Default
    if 'creatina' in md_content.lower():
        affiliate_link = config['affiliate_links']['creatine']
    elif 'maca' in md_content.lower():
        affiliate_link = config['affiliate_links']['maca']
        
    page_html = page_html.replace('{{affiliate_link}}', affiliate_link)
    
    # Salvar
    filename = os.path.basename(md_path).replace('.md', '.html')
    output_path = os.path.join('../docs/blog', filename)
    with open(output_path, 'w') as f:
        f.write(page_html)
    
    return {
        'title': title,
        'url': f'blog/{filename}'
    }

# Gerar todos os artigos
articles = []
for md_file in glob.glob('../content/*.md'):
    article_info = generate_page(md_file)
    articles.append(article_info)

# Gerar Index.html
index_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{site_name}} | {{site_tagline}}</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <h1>{{site_name}}</h1>
        <nav>
            <a href="index.html">Início</a>
            <a href="#artigos">Artigos</a>
        </nav>
    </header>

    <div class="hero">
        <h2>{{site_tagline}}</h2>
        <p>Informação baseada em ciência para mulheres que buscam o melhor da maturidade.</p>
    </div>

    <div class="container" id="artigos">
        <h2>Últimas Postagens</h2>
        {{article_list}}
    </div>

    <footer>
        <p>&copy; 2026 {{site_name}}</p>
    </footer>
</body>
</html>
"""

article_list_html = ""
for art in articles:
    article_list_html += f"""
    <div class="article-card">
        <h3><a href="{art['url']}">{art['title']}</a></h3>
        <p>Saiba mais sobre este tema fundamental para sua saúde...</p>
        <a href="{art['url']}" class="cta-button">Ler Artigo Completo</a>
    </div>
    """

index_html = index_template.replace('{{site_name}}', config['site_name'])
index_html = index_html.replace('{{site_tagline}}', config['site_tagline'])
index_html = index_html.replace('{{article_list}}', article_list_html)

with open('../docs/index.html', 'w') as f:
    f.write(index_html)

print(f"Sucesso! {len(articles)} artigos gerados.")
