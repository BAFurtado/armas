#### Análise crimininalidade com modelos baseados em agentes -- ABMs  

We developed the model on top of [https://github.com/projectmesa/mesa] mesa wolf_sheep example
We thank David Massa e all the contributors of the mesa project. 

**Alan Rafael Dill**

**Lígia Mori Madeira**

**Bernardo Alves Furtado**

We are considering two models (see github.com/bafurtado/home_violence) for the other one: 

### 2. Gun-reaction model

See folder `guns_model`

1. A partir do modelo simples, descrito em Proposta.docx, construímos três classes de agentes.
2. Vítimas, Agressores e Policiais
3. Todos movem-se aleatoriamente pelo grid
4. 1. Quando Agressor se encontra com vítima(s), escolhe uma para confrontar
   2. Se há policial na vizinhança imediata (uma célula, Moore), há confronto, determinado pela letalidade policial (parâmetro do modelo)
        1. Ou agressor ou policial morrem.
   3. Quando não há policial, agressor confronta vítima
        1. Se vítima possui arma
            1. Se há reação da vítima, 
                1. Morre vítima ou agressor  

## To run the models:
#### Para rodar os modelos, desde a instalação inicial

1. Preferencialmente, download e instale Python, via [https://www.anaconda.com/distribution] conda. No mínimo, tenha Pyton3 instalado
2. Preferencialmente, download e instale uma IDE. Sugiro [https://www.jetbrains.com/pycharm/download/] PyCharm Community. Universitários tem acesso à versão profissional, basta cadastro com e-mail institucional. 
3. Donwload e instale [https://git-scm.com/downloads] [GIT].
4. Com todos funcionando, vá até o Terminal do PyCharm (ou command line com acesso a Python) e usando o Git, clone esse repositório:
    1. `git clone https://github.com/BAFurtado/armas.git`  
    2. `pip install mesa`
    
#### To actually run
5. Utilize o comando `cd` para que o Terminal esteja no diretorio correto: 
    1. `cd ~/mesa_guns/guns_model` directory OU `cd ~/mesa_guns/home_violence`
    2. Type `mesa runserver` e pronto. Se tudo foi instalado, o browser se abriu automaticamente. 
    3. Altere os parâmetros como quiser.
    4. Clique em `Reset` no último botão à direita, na barra preta ao alto.
    5. Clique em `Start`, à esquerda do `Reset'
    
Enjoy modeling!
