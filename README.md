# Mini-SIEM: Sistema de Gerenciamento de Eventos de Segurança Simplificado

Este projeto é uma ferramenta de **Mini-SIEM (Security Information and Event Management)** desenvolvida em **Python** e **Uvicorn**, projetada para analisar e classificar eventos de segurança de arquivos de log de forma rápida e eficiente. Ele automatiza a triagem inicial de logs, transformando dados brutos em informações de segurança acionáveis.

O sistema recebe arquivos de log de entrada e os processa, gerando um novo arquivo de saída com os eventos categorizados por nível de risco, justificativas técnicas detalhadas e sugestões de ações mitigadoras.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Uvicorn](https://img.shields.io/badge/Uvicorn-gray.svg)
![GitHub contributors](https://img.shields.io/github/contributors/oFelipeee/SIEM.svg)

### ⚙️ Funcionalidades

  * **Análise e Ingestão de Logs:** Processa arquivos de log brutos, preparando os dados para a análise de segurança.
  * **Categorização de Riscos:** Classifica automaticamente os eventos de acordo com o seu nível de risco (alto, médio, baixo), ajudando a priorizar a resposta a incidentes.
  * **Justificativas Técnicas:** Para cada evento classificado, o sistema fornece uma justificativa técnica clara, explicando o motivo da categorização.
  * **Ações Mitigadoras:** Oferece sugestões práticas e acionáveis para mitigar a ameaça ou vulnerabilidade identificada.
  * **Geração de Relatório:** Cria um novo arquivo de log de saída, organizado e filtrado, que serve como um relatório de segurança simplificado.

-----

### 🛠️ Tecnologias Utilizadas

  * **Python:** A linguagem de programação principal, utilizada para a lógica de análise e processamento de logs.
  * **Uvicorn:** Um servidor web assíncrono para Python, usado para executar a aplicação de forma leve e rápida.

-----

### 🚀 Como Usar

#### Pré-requisitos

Certifique-se de ter o **Python** (versão 3.6 ou superior) instalado em sua máquina.

#### 1\. Instalação

Clone o repositório do projeto para o seu diretório local.

```bash
git clone https://github.com/oFelipeee/SIEM.git
```

Navegue até o diretório do projeto e instale as dependências necessárias.

```bash
cd SIEM
pip install uvicorn
```

#### 2\. Adicione seus Arquivos de Log

Coloque os arquivos de log que você deseja analisar no diretório do projeto. Por exemplo, você pode criar uma pasta `logs_in` para organizar seus arquivos.

```bash
/SIEM
├── app.py
├── logs_in/
│   ├── log_file_1.log
│   └── another_log.log
└── ...
```

#### 3\. Execução

Execute a aplicação com o Uvicorn. O servidor iniciará e processará os arquivos de log na pasta designada.

```bash
uvicorn main:app --reload
```

A aplicação processará os arquivos de log e gerará os arquivos de saída na pasta `logs_out`.

-----

### 📊 Estrutura da Saída

O sistema irá gerar um novo arquivo de log com o nome `filtered_logs.log` (ou similar) no diretório de saída. Cada entrada neste arquivo será estruturada da seguinte forma:

  * **Categorização do Risco:** A indicação de risco (`[ALTO]`, `[MÉDIO]`, `[BAIXO]`).
  * **Justificativa Técnica:** Uma breve explicação do porquê o evento foi classificado com esse nível de risco.
  * **Ações Mitigadoras:** Sugestões práticas para resolver ou mitigar o problema.

**Exemplo de linha de saída:**

```
[ALTO] - Tentativa de login falha repetida. Justificativa: Múltiplas tentativas de login em um curto período indicam um possível ataque de força bruta. Ações Sugeridas: Bloquear o endereço IP de origem, notificar o usuário da conta, e revisar políticas de senha.
```

-----

### 🤝 Contribuição

Contribuições são sempre bem-vindas\! Se você tiver sugestões, encontrar bugs ou quiser adicionar novas funcionalidades, por favor, abra uma *issue* ou envie um *pull request*.

-----

### 📝 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.
