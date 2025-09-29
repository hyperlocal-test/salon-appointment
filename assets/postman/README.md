# Postman Collections - Hyperlocal Conversation API

Este diretório contém a collection e o environment do Postman para testar o fluxo conversacional exposto pela API.

## Arquivos Incluídos

### Collection
- Arquivo: `Conversation_Collections.json`
- Descrição: Reúne cenários agrupados por intenção (agendar completo, parcial, cancelamento, preços, localização). Cada grupo contém passos sequenciais representando mensagens do usuário.

### Environment  
- Arquivo: `HYPERLOCA_Environment.json`
- Descrição: Define variáveis utilizadas nas requisições (ex.: `base_url`).

## Como Importar no Postman

### Passo 1: Importar Collection
1. Abra o Postman.
2. Clique em "Import" (atalho: Ctrl+O).
3. Aba "Files" > selecione o arquivo `Conversation_Collections.json` (neste diretório).
4. Confirme em "Import".

### Passo 2: Importar Environment
1. No canto superior direito do Postman, clique em "Environments" (ícone de engrenagem ou dropdown de ambientes).
2. Clique em "Import".
3. Selecione `HYPERLOCA_Environment.json`.
4. Importe e selecione o environment "HYPERLOCAL" como ativo.

### Passo 3: Validar
1. Abra o environment e confirme que `base_url` = `http://localhost:8081` (ajuste se estiver usando outra porta).
2. Certifique-se que a API está rodando localmente antes de enviar as requisições.

## Estrutura da Collection

A collection está organizada por cenários:

### 1. Agendar - Passo a Passo
Fluxo completo de agendamento coletando saudação, intenção, serviço e data/hora em etapas distintas.
	- Limpar Histórico: reinicia a sessão simulando limpeza (`#clear#`).
	- Saudação: exemplo de abertura de conversa.
	- Intent: usuário declara que quer agendar.
	- Service: usuário informa o serviço (ex.: corte de cabelo).
	- Datetime: usuário informa data e/ou horário.

### 2. Agendar - Parcial - Datetime
Cenário onde o usuário já inclui intenção + serviço na saudação e só falta a data/horário.

### 3. Agendar - Parcial - Date - Time
Cenário onde serviço e intenção são dados e data e horário chegam em duas mensagens separadas.

### 4. Agendar - Completo
Usuário já envia tudo em uma única mensagem (intenção + serviço + data + horário).

### 5. Cancelar - Completo
Protótipo inicial para fluxo de cancelamento (a lógica completa pode não estar implementada no backend, mas serve como base de teste).

### 6. Price - Completo
Consulta de preços (similar: classificação de intenção + resposta futura).

### 7. Location - Completo
Consulta de localização/endereço (estrutura para expansão futura).

Cada requisição utiliza `POST /api/v1/conversation` com corpo JSON contendo `session_id` e `message`. O `session_id` permite continuidade de contexto. Mensagens com `#clear#` indicam reset/limpeza de histórico.

## Variáveis de Environment

| Variável | Valor Padrão | Descrição |
|----------|--------------|-----------|
| `base_url` | `http://localhost:8081` | URL base da API local |

Observação: Caso deseje testar em outro host/porta (ex.: container remoto ou túnel), ajuste `base_url` diretamente no environment importado.

## Fluxo de Teste Recomendado

1. Subir a API local (docker compose correspondente).
2. Importar collection e environment (passos acima).
3. Abrir o grupo "Agendar - Passo a Passo".
4. Executar "Limpar Histórico" (opcional quando deseja reiniciar).
5. Executar as requisições subsequentes na ordem para observar enriquecimento incremental.
6. Repetir fluxo usando os cenários parciais e completo para comparar comportamento.

## Exemplo de Sequência (Agendar Completo)

1. Limpar Histórico (`#clear#`).
2. Saudação: "olá, tudo bem?".
3. Intent: "quero fazer um agendamento".
4. Service: "corte de cabelo".
5. Datetime: "na quinta as 16hrs".
6. Resultado esperado: identificador consolidado (serviço + data + horário) e passo concluído.

## Dicas

- O `session_id` mantém o contexto entre mensagens. Sem ele uma nova sessão é iniciada.
- Use `#clear#` para reiniciar a sessão manualmente.
- Teste mensagens completas versus fragmentadas para validar a extração incremental.
- Compare comportamento entre cenários com e sem data/hora definidos.

## Troubleshooting

### API não responde
1. Suba o serviço: `docker compose -f docker-compose-fastapi.yml up --build`.
2. Valide porta/host: `http://localhost:8081`.
3. Verifique logs do container.

### Sessão não continua
1. Confirme se o `session_id` enviado é exatamente o retornado.
2. Verifique se não foi executado `#clear#` antes sem intenção.
3. Garanta que não há truncamento ao copiar o identificador.

### Entidades não extraídas
1. Verifique se o texto inclui termos reconhecíveis (ex.: "corte", "amanhã", "às 15h").
2. Teste versões alternativas ("corte de cabelo", "na sexta as 10").
3. Confirme se a API NER está acessível (variável de ambiente correta).