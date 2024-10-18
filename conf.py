author = 'Kayce Basques'
copyright = '2024, Kayce Basques'
exclude_patterns = [
    '.github',
    '.gitignore',
    '_build',
    'Makefile',
    'README.md',
    'boostrap.sh',
    'data/anchors.rst',
    # 'data/embeddings.rst',
    'mdx',
    'requirements.txt',
    'venv'
]
extensions = [
    'matplotlib.sphinxext.plot_directive',
    'sphinx_reredirects'
]
html_extra_path = [
    'rss.xml'
]
html_permalinks_icon = '#'
html_static_path = ['_static']
project = 'technicalwriting.dev'
pygments_style = 'sphinx'
redirects = {
    'www/pdf': '../ux/pdf.html'
}
release = '0.0.0'
templates_path = ['_templates']
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html#configuration-options
plot_html_show_formats = False
