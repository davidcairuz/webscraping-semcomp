# Web Scraping

Bem-vindos ao curso de Web Scraping oferecido pela Semcomp!

Este repositório foi criado para ser um ponto de referência e suporte durante o nosso curso. Vale ressaltar que nem todos os códigos disponibilizados aqui serão abordados durante a aula.

## 1. Entendendo HTML

Nesta seção, começaremos com um arquivo HTML simples para compreender os fundamentos da linguagem de marcação e entender como funcionam as principais bibliotecas usadas para extrair dados de páginas estáticas da web.

Dentro da pasta `understanding_html`, você encontrará:
1. `simple_page.html`: Esta é uma página básica que abordará os conceitos iniciais de extração de dados.
2. `scraper.py`: Este script é designado para extrair informações da página mencionada anteriormente e contém linhas e comentários adicionais que detalham as funcionalidades da biblioteca beautifulsoup4.

Para desenvolver esta seção, me inspirei no vídeo [Python Tutorial: Web Scraping with BeautifulSoup and Requests](https://www.youtube.com/watch?v=ng2o98k983k) de Corey Shafer, que considero ser um dos melhores instrutores de Python no YouTube.

## 2. Extraindo informações de produtos de e-commerce

Com base no que aprendemos anteriormente, agora nos aprofundaremos na extração de dados de uma página real da web. Dado que o arquivo HTML não estará localmente em nosso dispositivo, usaremos a biblioteca `requests` para acessar o conteúdo da página de interesse.

Em seguida, discutiremos como usar as ferramentas de Inspeção e Visualização de código fonte presentes na maioria dos navegadores. Com a combinação dessas ferramentas e o conhecimento adquirido anteriormente, aprenderemos a selecionar as informações desejadas de quase qualquer página da web.

No diretório `kabum`, você encontrará:
1. `single_product.py`: Script que extrai informações de uma única página de produto.
2. `category_single_page.py`: Este código recolhe informações de todos os produtos em uma única página de categoria.
3. `category_single_page_async.py`: Um script que realiza a mesma função que o anterior, mas de maneira assíncrona, tornando-o mais eficiente.
4. `category_all_pages_async.py`: Este código foi projetado para extrair informações de todos os produtos de uma categoria específica de forma assíncrona.

## 3. Extraindo informações de sites dinâmicos

Sites dinâmicos apresentam um desafio adicional para web scraping, pois o conteúdo é gerado e modificado em tempo real. Aqui, aprenderemos técnicas e ferramentas para contornar esses obstáculos.

O site que utilizaremos como exemplo é o Instagram - nosso objetivo é obter todos os posts de uma conta.

O passo a passo que seguiremos será:
1. Visitar a página em um browser
2. Utilizando a aba **Network** do Inspect, vamos identificar a requisição que está sendo feita pelo site para obtenção do conteúdo
3. Vamos copiar essa requisição e visitar o site [cURL Converter](https://curlconverter.com) para obter código em Python
4. Entender e modificar esse código para obtermos o dado que queremos

No diretório `instagram`, você encontrará alguns código. Para essa seção, o mais relevante é:
1. `get_user_posts.py`: Este código é capaz de obter todos os posts de uma página do Instagram - mas pode ser facilmente limitado pela falta de utilização de proxies.

## 4. Obtendo dados de forma assíncrona

Agora vamos dar um passo pra trás na complexidade para entender como podemos deixar nossos códigos mais rápidos. Para isso, vamos explorar a PokeAPI e criar três códigos distintos - um sequencial, um multithread e um assíncrono.

No diretório `pokeapi` você encontrará os três códigos abaixo, capazes de coletar informações sobre 100 pokemons:
`sequential.py`: realiza a tarefa em 30 segundos.
`multithread.py`: realiza a mesma tarefa em 3 segundos.
`async.py`: faz o mesmo que os dois códigos acima em apenas 0.9 segundos.

Todo o cálculo do tempo foi realizado em meu computador pessoal e vai variar de máquina para máquina.

## 5. Utilizando proxies

A utilização de proxies pode ser essencial para contornar restrições geográficas ou para evitar ser bloqueado por realizar muitas requisições. Nesta seção, discutiremos como integrar proxies às nossas ferramentas de scraping.

Um simples código mostrando como fazer isso pode ser encontrado em `proxies/get_current_ip.py`

## 6. Autenticação

Em algumas situações, pode ser necessário autenticar-se em um site para acessar as informações desejadas. Neste módulo, exploraremos o que são e como criar `Sessions` com `requests` - e como podemos utilizá-las para fazer login.

Vamos explorar como podemos fazer login no Instagram, mostrando medidas comuns que podem acabar nos atrapalhando.

Você pode encontrar o código para isso em `instagram/instagram_login.py`


## 7. Google Cloud Functions

Agora vamos explorar as Google Cloud Functions e entender como podemos coletar dados rapidamente em escala.

Para esse exemplo vamos utilizar o IMDB - e nosso objetivo é coletar sinopses e sumários dos filmes.

Você encontrará dois códigos na pasta `imdb`:
1. `get_summaries_async.py`: para obter dados de 1000 filmes, esse código levou 22 segundos assincronamente. Portanto, faz sentido esperar que, para coletar dados de 100k filmes esse código levaria em torno de 35 minutos.
2. `publish_movie_urls_to_topic.py`: envia as urls para que uma Cloud Function realize o trabalho - coletamos dados de 100k filmes em 1-2 minutos utilizando 10k instâncias.

## Upwork

Vamos utilizar nosso tempo aqui para que todos aqueles interessados saiam com uma conta criada no Upwork!

Aqui estão também alguns recursos que nos serão úteis:
1. [Escrevendo uma boa Cover Letter](https://www.upwork.com/resources/how-to-write-a-cover-letter)

2. [Criando uma boa biografia](https://www.upwork.com/resources/upwork-profile-examples)

3. Grammarly

4. DeepL

5. ChatGPT