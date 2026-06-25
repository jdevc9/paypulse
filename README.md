# Paypulse

## Sistema de transferências e pagamentos digitais inspirado em plataformas como PayPal,
desenvolvido em Python com foco em segurança, escalabilidade e arquitetura modular.

<img width="2752" height="1536" alt="gere_uma_thumbnail_para_meu_202606250822" src="https://github.com/user-attachments/assets/70db5290-1af3-47ab-9235-7b0266fe5d1e" />

---

## Aviso importante

Este projeto é educacional e não deve ser usado em produção real sem auditoria de segurança, criptografia robusta e conformidade legal (PCI-DSS, LGPD).

Pagamentos não são um problema de “código funcionando” — são um problema de confiança matemática + segurança + idempotência + rastreabilidade total .

---

## O Paypulse simula uma plataforma de pagamentos digitais onde os usuários podem:

* Criar contas digitais

<img width="1366" height="637" alt="screencapture-127-0-0-1-5000-login-2026-06-25-05_44_27" src="https://github.com/user-attachments/assets/d9593d80-7f4a-49de-b928-ceb827a83108" />


* Realizar transferências entre usuários

<img width="1366" height="745" alt="screencapture-127-0-0-1-5000-send-2026-06-25-05_45_44" src="https://github.com/user-attachments/assets/5bad1ecd-e783-4ba3-bb20-bf11cef37bea" />


* Consultar saldo e extratos

<img width="1366" height="1189" alt="screencapture-127-0-0-1-5000-dashboard-2026-06-25-05_51_16" src="https://github.com/user-attachments/assets/84870c83-58a7-42f3-b1e0-503076c0a1a4" />


  
* Registrador histórico transacional

<img width="1366" height="1419" alt="screencapture-127-0-0-1-5000-transactions-2026-06-25-05_45_58" src="https://github.com/user-attachments/assets/ad7d909b-885d-475f-bdec-b4c984f8c05f" />





---

## Objetivo do projeto

### Construir uma base sólida para entender:

* Arquitetura de sistemas financeiros
* cabeça de concorrência
* Integridade de transações
* Boas práticas de segurança em back-end
* Modelagem de dados para sistemas críticos

---

## Arquitetura

### O sistema é estruturado em camadas:

Paypulse/
│<br>
├── app.py           App Principal<br> 
├── models/            Entidades (User, Transaction, Contact)<br>
├── routes/            Lógica de aplicação (payment service)<br>
├── database.py        Acesso a dados (DB layer)<br>
├── static/            Estilo e funções do sistema<br>
├── templates/         Páginas do app<br>

---

## Conceitos de segurança aplicados

Mesmo em ambiente simulado, o projeto considera:

* Validação de transações antes da execução
* Proteção contra duplicidade (idempotência conceitual)
* Registro imutável de transações (trilha de auditoria)
* Separação entre lógica de negócio e acesso a dados

---

## Tecnologias

* Python 3.x
* Flask / FastAPI (dependendo da versão)
* SQLite/PostgreSQL (simulado ou real)
* SQLAlchemy (ORM)
* PyTest (testes)
* JWT (autenticação simulada, aplicável)

---

## Fluxo de uma transação

* Usuário envia solicitação de transferência
* Sistema de validação de saldo e destino
* A transação é registrada como “pendente”
* Execução da transferência
* Atualização de saldo
* Registro final no histórico

---

## Como executar o projeto  

### clonar repositório
git clone https://github.com/seuusuario/paypulse

### entrar no diretório
cd paypulse

### criar ambiente virtual
python -m venv venv

### ativar ambiente
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

### instalar dependências
pip install -r requirements.txt

### rodar aplicação
python app.py

---

## Complexidade real do problema

Um erro comum é pensar que “transferir dinheiro” é uma simples atualização no banco.

Na prática, você precisa lidar com:

* Concorrência (duas transferências ao mesmo tempo)
* Falhas no meio da operação
* Consistência eventual vs forte
* Risco de inconsistência de saldo
* Auditório

### Esse tipo de sistema não é programado – é engenharia de confiança.
