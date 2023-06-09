import requests  # Biblioteca para fazer requisições HTTP
from bs4 import BeautifulSoup  # Biblioteca para fazer a análise do HTML
from nltk.tokenize import word_tokenize  # Biblioteca para tokenização de palavras
from nltk.sentiment import SentimentIntensityAnalyzer  # Biblioteca para análise de sentimento
from collections import deque  # Biblioteca para criar uma fila
import nltk  # Biblioteca para processamento de linguagem natural
import mysql.connector  # Biblioteca para conectar ao banco de dados MySQL
from mysql.connector import Error  # Classe para tratamento de erros no MySQL

# Definição da classe BTreeNode que representa um nó da árvore B
class BTreeNode:
    def __init__(self, t, is_leaf=False):
        self.t = t  # Ordem da árvore B
        self.is_leaf = is_leaf
        self.keys = []
        self.links = []
        self.children = []

# Definição da classe BTree que representa a árvore B
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    # Função para inserir uma chave e link na árvore B
    def insert(self, key, link):
        if len(self.root.keys) == (2 * self.t) - 1:
            # Se o número de chaves no nó raiz é igual à ordem máxima da árvore (2 * t - 1),
            # então a raiz está cheia e precisa ser dividida

            new_root = BTreeNode(self.t)  # Cria um novo nó raiz
            new_root.children.append(self.root)  # Adiciona o antigo nó raiz como filho do novo nó raiz
            self.root = new_root  # Atualiza o nó raiz da árvore
            self.split_child(self.root, 0)  # Divide o filho do novo nó raiz

        self.insert_non_full(self.root, key, link)  # Insere a chave e o link no nó não cheio


    # Função auxiliar para inserir uma chave e link em um nó não cheio
    def insert_non_full(self, node, key, link):
        i = len(node.keys) - 1  # Índice da última chave do nó
    
        if node.is_leaf:
            # Se o nó é uma folha, insere a chave e o link no lugar correto no nó
    
            while i >= 0 and key < node.keys[i]:
                # Encontra a posição correta para a nova chave no nó
                i -= 1
    
            node.keys.insert(i + 1, key)  # Insere a chave no nó na posição encontrada
            node.links.insert(i + 1, link)  # Insere o link correspondente na posição encontrada
        else:
            # Se o nó não é uma folha, encontra o filho adequado e insere recursivamente nele
    
            while i >= 0 and key < node.keys[i]:
                # Encontra o filho adequado para a nova chave no nó
                i -= 1
    
            i += 1  # Incrementa o índice para apontar para o filho adequado
    
            if len(node.children[i].keys) == (2 * self.t) - 1:
                # Se o filho está cheio, realiza uma divisão
    
                self.split_child(node, i)  # Divide o filho
    
                if key > node.keys[i]:
                    # Verifica se a nova chave deve ser inserida no filho à direita após a divisão
                    i += 1
    
            self.insert_non_full(node.children[i], key, link)  # Insere recursivamente no filho adequado


    # Função para dividir um filho de um nó pai
    def split_child(self, parent, child_index):
        child = parent.children[child_index]  # Obtém o filho a ser dividido
        new_child = BTreeNode(self.t, child.is_leaf)  # Cria um novo filho
    
        parent.keys.insert(child_index, child.keys[self.t - 1])  # Insere uma chave do filho no pai
        parent.links.insert(child_index, child.links[self.t - 1])  # Insere um link do filho no pai
    
        parent.children.insert(child_index + 1, new_child)  # Insere o novo filho no pai
    
        new_child.keys = child.keys[self.t:]  # Copia as chaves da metade superior do filho para o novo filho
        new_child.links = child.links[self.t:]  # Copia os links da metade superior do filho para o novo filho
    
        if not child.is_leaf:
            new_child.children = child.children[self.t:]  # Copia os filhos da metade superior do filho para o novo filho
            child.children = child.children[:self.t]  # Atualiza os filhos do filho original para conter apenas a metade inferior
    
    # Função para imprimir a árvore B
    def print_tree(self):
        self._print_tree(self.root, 0)

    # Função auxiliar para imprimir a árvore B recursivamente
    def _print_tree(self, node, level=0):
        if node:
            prefix = "    " * level
            print(f"{prefix}Node:")

            for i in range(len(node.keys)):
                print(f"{prefix}Key: {node.keys[i]}")
                print(f"{prefix}Link: {node.links[i]}")
                print()

            if not node.is_leaf:
                child_level = level + 1
                for i, child in enumerate(node.children):
                    if i == len(node.children) - 1:
                        self._print_tree(child, child_level)
                    else:
                        print(f"{prefix}Child:")
                        self._print_tree(child, child_level)
                        print()

    

# Função para encontrar as palavras-chave nas páginas fornecidas
def find_keywords(links):
    btree = BTree(4)  # Cria uma árvore B com ordem 4

    # Loop para processar cada link
    for link in links:
        try:
            response = requests.get(link)  # Faz a requisição HTTP para obter o conteúdo da página
            content = response.text  # Obtém o conteúdo da resposta
            soup = BeautifulSoup(content, 'html.parser')  # Faz a análise do HTML usando BeautifulSoup

            title = soup.find('title').text.strip()  # Obtém o título da página

            keywords = get_keywords(title)  # Obtém as palavras-chave do título
            classify_keywords(keywords, link, btree)  # Classifica as palavras-chave e insere na árvore B
        except Exception as e:
            print(f'Error fetching content from {link}: {str(e)}')

    return btree

# Função para obter as palavras-chave a partir do título da página
def get_keywords(title):
    tokenizer = nltk.RegexpTokenizer(r'\w+')  # Cria um tokenizador de palavras
    title_tokens = tokenizer.tokenize(title.lower())  # Tokeniza as palavras do título em minúsculas
    return title_tokens[:4]  # Retorna as 4 primeiras palavras

# Função para classificar as palavras-chave e inserir na árvore B
def classify_keywords(keywords, link, btree):
    for keyword in keywords:
        if keyword not in btree.root.keys:
            btree.insert(keyword, link)  # Insere a palavra-chave e o link na árvore B
            insert_keyword(keyword)  # Insere a palavra-chave no banco de dados
            insert_indexed_link(keyword, link)  # Insere o link indexado no banco de dados
        else:
            index = btree.root.keys.index(keyword)
            existing_links = btree.root.links[index].split(", ")
            if link not in existing_links:
                btree.root.links[index] += ", " + link
                insert_indexed_link(keyword, link)
# Função para inserir uma palavra-chave no banco de dados
def insert_keyword(keyword):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='bingoo',
            user='enrell',
            password='enrellsa10'
        )
        cursor = connection.cursor()
        query = "INSERT INTO keyword (keyword) VALUES (%s)"  # Consulta SQL para inserir a palavra-chave na tabela "keyword"
        values = (keyword,)  # Valores a serem inseridos na consulta (palavra-chave)
        cursor.execute(query, values)  # Executa a consulta com os valores
        connection.commit()  # Confirma a transação no banco de dados
        cursor.close()  # Fecha o cursor
        connection.close()  # Fecha a conexão com o banco de dados
    except Error as e:
        print(f"Error inserting keyword: {str(e)}")  # Exibe uma mensagem de erro em caso de falha na inserção

# Função para inserir um link indexado no banco de dados
def insert_indexed_link(keyword, link):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='bingoo',
            user='enrell',
            password='enrellsa10'
        )
        cursor = connection.cursor()
        keyword_id = get_keyword_id(keyword, cursor)  # Obtém o ID da palavra-chave usando a função "get_keyword_id"
        query = "INSERT INTO indexed_links (keyword_id, link) VALUES (%s, %s)"  # Consulta SQL para inserir o link indexado na tabela "indexed_links"
        values = (keyword_id, link)  # Valores a serem inseridos na consulta (ID da palavra-chave e link)
        cursor.execute(query, values)  # Executa a consulta com os valores
        connection.commit()  # Confirma a transação no banco de dados
        cursor.close()  # Fecha o cursor
        connection.close()  # Fecha a conexão com o banco de dados
    except Error as e:
        print(f"Error inserting indexed link: {str(e)}")  # Exibe uma mensagem de erro em caso de falha na inserção

# Função para obter o ID de uma palavra-chave no banco de dados
def get_keyword_id(keyword, cursor):
    query = "SELECT id FROM keyword WHERE keyword = %s"  # Consulta SQL para selecionar o ID da palavra-chave na tabela "keyword"
    values = (keyword,)  # Valor a ser pesquisado na consulta (palavra-chave)
    cursor.execute(query, values)  # Executa a consulta com o valor
    result = cursor.fetchone()  # Obtém o resultado da consulta
    if result:
        return result[0]  # Retorna o ID da palavra-chave encontrado
    else:
        return None  # Retorna None caso a palavra-chave não seja encontrada


# Função para rastrear os links a partir de uma lista inicial de URLs
def crawl_links(initial_urls):
    btree = BTree(4)  # Cria uma árvore B com ordem 4
    visited_links = set()  # Conjunto de links visitados
    queue = deque(initial_urls)  # Fila de URLs a serem processadas
    page_count = 0  # Contagem de páginas

    while queue and page_count < 1000:  # Verifica se há URLs na fila e se a contagem de páginas é inferior a 1000
        current_url = queue.popleft()  # Remove o próximo URL da fila

        if current_url not in visited_links:  # Verifica se o URL já foi visitado
            try:
                response = requests.get(current_url)  # Faz a requisição HTTP para obter o conteúdo da página
                content = response.text  # Obtém o conteúdo da resposta
                soup = BeautifulSoup(content, 'html.parser')  # Faz a análise do HTML usando BeautifulSoup

                title = soup.find('title').text.strip()  # Obtém o título da página

                keywords = get_keywords(title)  # Obtém as palavras-chave do título
                classify_keywords(keywords, current_url, btree)  # Classifica as palavras-chave e insere na árvore B

                # Extrai e enfileira os links da página
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href.startswith('http'):  # Verifica se o link começa com "http"
                        queue.append(href)  # Adiciona o link na fila
            except Exception as e:
                print(f'Error fetching content from {current_url}: {str(e)}')

            visited_links.add(current_url)  # Adiciona o URL à lista de links visitados
            page_count += 1  # Incrementa a contagem de páginas

    return btree

# Lista de links iniciais
links = [
    'https://www.foodnetwork.com/',
    'https://www.delish.com/cooking/g1956/best-cookies/',
    'https://tasty.co/recipe/the-best-chewy-chocolate-chip-cookies',
    'https://www.tasteofhome.com/collection/the-best-cookie-recipes/',
    'https://vuejs.org/guide/introduction.html',
    'https://vuejs.org/guide/quick-start.html',
    'https://vuejs.org/guide/essentials/application.html'
]

btree = find_keywords(links)

# crawl_links(links)

# Imprime a árvore B
print('B-Tree:')
btree.print_tree()
