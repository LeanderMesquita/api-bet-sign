# Projeto de Automação

Este projeto segue o padrão de factory para gerenciar a instância de tasks (classes) e utiliza Flask para executar a aplicação. Abaixo estão os detalhes sobre a estrutura do projeto, tasks e instruções para configuração e execução.

## Estrutura do Projeto

- **Padrão de Factory:** 
  - A classe `Factory` é responsável pela instância das tasks (classes).
  
- **Função Principal:**
  - A função principal `start_injection` está localizada em `/api/index.py` e é responsável por instanciar uma task a ser cumprida.

## Tasks

- **Descrição:**
  - As tasks são classes que representam as "tarefas", ou seja, os scripts de automação que devem ser cumpridos.

## Instruções

### 1. Criar o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```sh
python -m venv nomedavenv
```

### 2. Ativar o Ambiente Virtual

Ative o ambiente virtual criado:

- **Windows:**

```sh
nomedavenv\Scripts\activate
```

- **Mac/Linux:**

```sh
source nomedavenv/bin/activate
```

### 3. Instalar Dependências

Navegue até o diretório `/api` e instale as dependências necessárias:

```sh
cd /api
pip install -r requirements.txt
```

### 4. Executar o Projeto

Certifique-se que está dentro de /api, caso não:

```sh
cd /api
```

Para executar o projeto, use o comando:

```sh
flask run
```

Isso iniciará o servidor Flask e você poderá testar a aplicação.

---

Siga estas instruções para configurar e executar corretamente o projeto de automação. Se houver alguma dúvida ou problema, consulte a documentação ou entre em contato.