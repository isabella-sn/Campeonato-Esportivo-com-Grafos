# 🏟️ Knowledge Graph Esportivo em Python

Este projeto implementa um **Knowledge Graph (Grafo de Conhecimento)** voltado para o domínio esportivo, permitindo o cadastro, consulta e visualização de **torneios, times, jogadores e jogos**, além de seus relacionamentos.

O sistema funciona de forma **interativa via terminal**, com geração opcional de uma **visualização gráfica do grafo** utilizando o **Graphviz**.

---

## 📌 Objetivo do Projeto

O objetivo é demonstrar, de forma prática, conceitos de:
- Grafos
- Modelagem de conhecimento
- Relacionamentos entre entidades
- Consultas estruturadas
- Visualização de dados em grafos

O projeto pode ser aplicado em contextos acadêmicos, estudos de grafos, sistemas inteligentes ou bases de conhecimento.

---

## 🧠 Estrutura do Knowledge Graph

### 🟩 Nós (Entidades)
- **Torneio**: nome, ano, formato
- **Time**: nome, cidade
- **Jogador**: nome, posição
- **Jogo**: data, placar

### 🔗 Relacionamentos
- `PARTICIPA_DE` → Time participa de um Torneio  
- `JOGA_PELO` → Jogador joga por um Time  
- `TIME_CASA` / `TIME_VISITANTE` → Times em um Jogo  
- `VENCEU` / `PERDEU_PARA` → Resultado de Jogos  

---

## ⚙️ Funcionalidades Principais

✅ Criação interativa de torneios  
✅ Cadastro de times, jogadores e jogos  
✅ Consulta por propriedades (ex: jogadores por posição)  
✅ Consulta por relacionamentos (ex: jogadores de um time)  
✅ Busca de jogos vencidos por um time  
✅ Visualização resumida e detalhada dos nós  
✅ Geração de grafo visual com **Graphviz**  

---

## 🖼️ Visualização do Grafo

O sistema gera automaticamente uma imagem `.png` do grafo com:
- Cores diferentes por tipo de entidade
- Relações nomeadas
- Layout horizontal (Left → Right)

Exemplo de saída:
``
