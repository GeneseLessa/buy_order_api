### API para transação básica e ordem de pedidos

Pequeno projeto em que uma API REST (não RESTFull) simula um processo de compras por carrinho e ao final permite finalizar a compra e gera uma ordem de pedido.

Esta API foi desenvolvida usando python 3 (3.9.6), Django (3.2.7), Django Rest Framework (3.12.4), bem como o sistema de testes padrão do Django, bem como Django Rest Framework e outros acessórios, visíveis no arquivo requirements.txt na raiz do projeto.

Demais versões dos pacotes podem ser observadas no arquivo requirements.txt na raiz do projeto.

### Instruções para execução

Sugerido ambiente virtual para instalação dedicada dos pacotes usados (via pip).

* Clone este repositório
* Crie um ambiente virtual com: $ python -m venv venv_name
* Ative-o: $ source venv_name/bin/activate
* Instale as dependências do projeto: $ pip install -r requirements.txt
* Crie e execute as migrações do projeto (vide documentação do django)
* O ambiente encontra-se sem dados, mas suporta django-admin e permite realizar o acompanhamento dos models de forma intuitiva
* O ambiente de testes pode ser executado com $ python manage.py test

### Endpoints disponíveis

Por padrão o ambiente é executado em http://localhost:8000 (vou considerar esta URL como base)


* GET /products/search/[string] = busca um produto por nome conforme requisitado
* GET /shopping/start = inicia um carrinho de compras vazio para uso no processo
* GET /shopping/cart/[id do carrinho]/clean = extra para esvaziar o carrinho
* POST /shopping/cart/add_product = insere um produto cadastrado no carrinho, obedecendo as regras dispostas no cadastro do produto relacionadas  ao cadastro e uso. Necessário passar (via JSON) os dados no formato: { "cart": id_do_carrinho, "product": id_do_produto, "quantity": quantidade }
* POST /shopping/cart/change_product = endpoint criado para efetuar a quantidade de itens em um determinado produto no carrinho. Necessário informar vie JSON os seguintes campos: { "cart": id_do_carrinho, "product": id_do_produto, "quantity": quantidade }
* POST /shopping/cart/remove_product = permite remover um item do carrinho. Necessário informar o id do item (JSON): { "product": id_do_produto_a_ser_removido }
* GET /shopping/cart/[id do carrinho]/details = permite visualizar o detalhamento do carrinho conforme requisitado.
* POST /shopping/close = finaliza o processo gerando o pedido e limpando o conteúdo do carrinho. Passar (via JSON) o carrinho no processo { "cart": id_do_carrinho }

