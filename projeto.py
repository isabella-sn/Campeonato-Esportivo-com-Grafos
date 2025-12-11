import sys 
import graphviz 

# =====================================================================
# CLASSE KnowledgeGraph (KG) - O NÚCLEO DO GRAFO
# =====================================================================

class KnowledgeGraph:
    """
    Implementação básica de um Knowledge Graph.
    """

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.node_id_counter = 1

    # --- Métodos de Manipulação (Omitidos para brevidade, mas o mesmo do código anterior) ---
    def adicionar_no(self, label: str, propriedades: dict) -> str:
        new_id = f"N{self.node_id_counter}"
        self.nodes[new_id] = {
            "label": label, 
            "propriedades": propriedades
        }
        self.node_id_counter += 1
        return new_id

    def adicionar_relacionamento(self, sujeito_id: str, predicado: str, objeto_id: str) -> bool:
        if sujeito_id not in self.nodes or objeto_id not in self.nodes:
            return False
        self.edges.append({
            "sujeito_id": sujeito_id,
            "predicado": predicado,
            "objeto_id": objeto_id
        })
        return True

    def consultar_por_propriedade(self, label: str, propriedade: str, valor: any) -> list:
        resultados = []
        for node_id, node_data in self.nodes.items():
            if node_data["label"] == label:
                if node_data["propriedades"].get(propriedade) == valor:
                    resultados.append((node_id, node_data))
        return resultados
    
    # --- Métodos de Apoio (Omitidos para brevidade) ---
    # Remova os 'pass' e cole os métodos 'remover_no', 'imprimir_grafo_resumo', etc.
    def remover_no(self, node_id: str) -> bool:
        if node_id not in self.nodes:
            return False
        del self.nodes[node_id]
        self.edges = [
            edge for edge in self.edges 
            if edge["sujeito_id"] != node_id and edge["objeto_id"] != node_id
        ]
        print(f"Sucesso: Nó {node_id} e suas arestas relacionadas removidos.")
        return True

    def imprimir_grafo_resumo(self):
        print("\n--- Resumo do Knowledge Graph ---")
        print(f"Total de Nós: {len(self.nodes)}")
        print(f"Total de Relacionamentos (Arestas): {len(self.edges)}")
        labels = [data["label"] for data in self.nodes.values()]
        print(f"Distribuição de Labels: {dict((l, labels.count(l)) for l in set(labels))}")

    def imprimir_no_detalhado(self, node_id: str):
        if node_id not in self.nodes:
             print(f"Nó {node_id} não encontrado.")
             return
        node_data = self.nodes[node_id]
        print(f"\n--- Detalhes do Nó: {node_id} ({node_data['label']}) ---")
        print(f"Propriedades: {node_data['propriedades']}")
        print("Relacionamentos de Saída:")
        found_relationships = False
        for edge in self.edges:
            if edge["sujeito_id"] == node_id:
                objeto_data = self.nodes.get(edge["objeto_id"], {"label": "N/A", "propriedades": {"nome": "Nó Removido"}})
                nome_objeto = objeto_data['propriedades'].get('nome', 'N/A')
                print(f"  -> {edge['predicado']} -> {edge['objeto_id']} ({objeto_data['label']}: {nome_objeto})")
                found_relationships = True
        if not found_relationships:
             print("  Nenhum relacionamento de saída encontrado.")


    # -----------------------------------------------------------------
    # NOVO MÉTODO: Geração de Visualização (COM PALETA DE CORES ATUALIZADA)
    # -----------------------------------------------------------------
    
    def gerar_visualizacao_graphviz(self, filename="knowledge_graph_esportivo", view=True):
        """
        Gera uma representação visual do Grafo de Conhecimento e salva como arquivo de imagem.
        Atenção: Requer a instalação da ferramenta Graphviz no sistema.
        """
        try:
            dot = graphviz.Digraph(
                comment='Knowledge Graph Esportivo', 
                graph_attr={'rankdir': 'LR', 'splines': 'true', 'overlap': 'false'},
                node_attr={'shape': 'box', 'style': 'filled', 'fontname': 'Arial'} # Adiciona fonte
            )

            # --- NOVA PALETA DE CORES ---
            color_map = {
                "Time": '#FFD700',      # Amarelo Ouro (Ex: Time)
                "Jogador": '#3CB371',   # Verde Meio (Ex: Jogador)
                "Torneio": '#00BFFF',   # Azul Céu Profundo (Ex: Evento Principal)
                "Jogo": '#FF6347'       # Vermelho Tomate (Ex: Resultado/Evento)
            }
            # -----------------------------

            # 1. Adicionar Nós
            for node_id, data in self.nodes.items():
                label_text = f"<{data['label']}> \n--- ID: {node_id} ---\n" # Usando tags HTML para formatação
                
                # Adiciona as propriedades principais ao rótulo (label) do nó
                for key, value in data['propriedades'].items():
                    if key not in ['id', 'cidade', 'ano'] or len(str(value)) < 20: 
                        label_text += f"{key}: {value}\n"
                
                color = color_map.get(data['label'], '#E0E0E0') # Cinza Claro para o padrão
                
                # Configurações de cor do texto (opcional, para garantir contraste)
                fontcolor = 'black' 
                
                dot.node(node_id, label=label_text, fillcolor=color, fontcolor=fontcolor)

            # 2. Adicionar Arestas (Relacionamentos)
            for edge in self.edges:
                dot.edge(
                    edge["sujeito_id"], 
                    edge["objeto_id"], 
                    label=edge["predicado"],
                    fontcolor='#696969', # Cor do texto do relacionamento (cinza escuro)
                    color='#A9A9A9'      # Cor da linha do relacionamento (cinza médio)
                )

            # Salva o arquivo no formato PNG (o view=True tenta abrir o arquivo após gerar)
            dot.render(filename, view=view, format='png', cleanup=True) 
            print(f"\n[SUCESSO] Visualização do Grafo gerada com nova paleta de cores!")
            print(f"Arquivo salvo como: '{filename}.png' (Pode ser inserido no seu relatório/docs).")

        except ImportError:
            print("\n[ERRO FATAL] A biblioteca 'graphviz' não está instalada. Execute: pip install graphviz")
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um erro ao gerar o gráfico. Certifique-se de que a ferramenta Graphviz está instalada e no PATH do sistema. Erro: {e}")

# ... (Resto das Funções Interativas permanecem as mesmas, incluindo main e menus) ...
# O código completo seria idêntico ao anterior, com esta única modificação no método.

def registrar_jogo(kg, times_ids):
    # Função para registrar jogo (mantida para completar o código)
    print("\n--- NOVO JOGO ---")
    print(f"Times disponíveis: {list(times_ids.keys())}")
    
    time1_nome = input("Nome do Time da Casa: ")
    time2_nome = input("Nome do Time Visitante: ")
    
    id1 = times_ids.get(time1_nome)
    id2 = times_ids.get(time2_nome)
    
    if not id1 or not id2:
        print("Um ou ambos os times não foram encontrados. Voltando.")
        return False, None

    data_jogo = input("Data do Jogo (AAAA-MM-DD): ")
    placar = input("Placar (ex: 2x1): ")
    vencedor_nome = input("Vencedor (Digite o nome do time vencedor ou 'EMPATE'): ")
    
    jogo_id = kg.adicionar_no("Jogo", {"data": data_jogo, "placar": placar})

    kg.adicionar_relacionamento(jogo_id, "TIME_CASA", id1)
    kg.adicionar_relacionamento(jogo_id, "TIME_VISITANTE", id2)
    
    if vencedor_nome.upper() == time1_nome.upper():
        kg.adicionar_relacionamento(id1, "VENCEU", jogo_id)
        kg.adicionar_relacionamento(id2, "PERDEU_PARA", jogo_id)
    elif vencedor_nome.upper() == time2_nome.upper():
        kg.adicionar_relacionamento(id2, "VENCEU", jogo_id)
        kg.adicionar_relacionamento(id1, "PERDEU_PARA", jogo_id)
        
    print(f"[SUCESSO] Jogo adicionado. Resultado: {placar}. ID: {jogo_id}")
    return True, jogo_id

def adicionar_entidades_e_relacionamentos(kg, times_ids):
    while True:
        print("\n--- ✏️ ADICIONAR AO GRAFO ---")
        print("1. Adicionar Jogador a um Time")
        print("2. Adicionar Resultado de Jogo")
        print("3. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            adicionar_jogador(kg, times_ids)
        elif escolha == '2':
            registrar_jogo(kg, times_ids) 
        elif escolha == '3':
            break
        else:
            print("Opção inválida.")
            
def adicionar_jogador(kg, times_ids):
    print("\n--- NOVO JOGADOR ---")
    print(f"Times disponíveis: {list(times_ids.keys())}")
    nome_time = input("Nome do Time onde o jogador joga: ")
    time_id = times_ids.get(nome_time)
    
    if not time_id:
        print("Time não encontrado. Voltando.")
        return

    nome_jogador = input("Nome do Jogador: ")
    posicao = input("Posição (ex: Atacante): ")
    
    jogador_id = kg.adicionar_no("Jogador", {"nome": nome_jogador, "posicao": posicao})
    kg.adicionar_relacionamento(jogador_id, "JOGA_PELO", time_id)
    print(f"[SUCESSO] Jogador '{nome_jogador}' adicionado ao {nome_time}.")

def criar_campeonato_interativo(kg):
    print("\n--- 🏟️ INÍCIO DA CRIAÇÃO DO CAMPEONATO ---")
    nome_torneio = input("1. Digite o NOME do campeonato: ")
    ano_torneio = input("2. Digite o ANO do campeonato: ")
    
    formato_choice = input("3. Digite o FORMATO:\n   [1] Pontos Corridos\n   [2] Mata-Mata\n   Escolha (1 ou 2): ")
    
    if formato_choice == '1':
        formato = "Pontos Corridos"
    elif formato_choice == '2':
        formato = "Mata-Mata"
    else:
        print("Opção de formato inválida. Definindo como 'Não Especificado'.")
        formato = "Não Especificado"
        
    id_torneio = kg.adicionar_no("Torneio", {"nome": nome_torneio, "ano": ano_torneio, "formato": formato})
    print(f"\n[SUCESSO] Torneio '{nome_torneio}' criado com ID: {id_torneio}.")
    
    times_ids = {}
    print("\n--- ⚽ REGISTRO DE TIMES (Mínimo de 4) ---")
    num_times = 0
    while num_times < 4 or input("Deseja adicionar mais um time? (s/n): ").lower() == 's':
        
        print(f"\nTime #{num_times + 1}")
        nome_time = input("Nome do Time: ")
        cidade = input("Cidade do Time: ")
        
        time_id = kg.adicionar_no("Time", {"nome": nome_time, "cidade": cidade})
        times_ids[nome_time] = time_id
        
        kg.adicionar_relacionamento(time_id, "PARTICIPA_DE", id_torneio)
        print(f"[SUCESSO] Time '{nome_time}' adicionado. ID: {time_id}.")
        num_times += 1

    print("\n--- 🥅 ADIÇÃO DE JOGADORES INICIAIS ---")
    for i in range(len(times_ids) * 3 + 3):
        time_nomes = list(times_ids.keys())
        time_para_add = time_nomes[i % len(time_nomes)]
        
        if input(f"Adicionar Jogador ao {time_para_add}? (s/n, se 's' será criado o nó): ").lower() == 's':
            nome_jogador = input(f"Nome do Jogador para {time_para_add}: ")
            posicao = input("Posição (ex: Atacante): ")
            
            jogador_id = kg.adicionar_no("Jogador", {"nome": nome_jogador, "posicao": posicao})
            kg.adicionar_relacionamento(jogador_id, "JOGA_PELO", times_ids[time_para_add])
            print(f"  [SUCESSO] Jogador '{nome_jogador}' adicionado.")
            
    print("\n--- 🏟️ REGISTRO DE JOGOS INICIAIS (Mínimo de 2) ---")
    num_jogos = 0
    while num_jogos < 2 or input("Deseja registrar mais um Jogo? (s/n): ").lower() == 's':
        
        print(f"\nRegistro de Jogo #{num_jogos + 1}")
        success, _ = registrar_jogo(kg, times_ids)
        if success:
            num_jogos += 1
            
    print(f"\n[INFO] Configuração inicial concluída. Total de Nós no Grafo: {len(kg.nodes)}.")
    return id_torneio, times_ids

def menu_consultas(kg, times_ids):
    while True:
        print("\n--- 🔍 CONSULTAS AO GRAFO ---")
        print("1. Buscar jogadores por Posição (Consulta por Propriedade)")
        print("2. Buscar jogadores por Time (Consulta Inversa por Relacionamento)")
        print("3. Buscar jogos Vencidos por um Time")
        print("4. Voltar ao Menu Principal")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            posicao = input("Qual Posição buscar (ex: Atacante): ")
            resultados = kg.consultar_por_propriedade("Jogador", "posicao", posicao)
            print(f"\nResultados para Posição '{posicao}':")
            if resultados:
                for _, data in resultados:
                    print(f"  - {data['propriedades']['nome']}")
            else:
                print("Nenhum jogador encontrado para essa posição.")

        elif escolha == '2':
            print(f"Times disponíveis: {list(times_ids.keys())}")
            nome_time = input("Nome do Time para buscar jogadores: ")
            time_id = times_ids.get(nome_time)
            
            if time_id:
                jogadores = []
                for edge in kg.edges:
                    if edge['objeto_id'] == time_id and edge['predicado'] == 'JOGA_PELO':
                        jogador_id = edge['sujeito_id']
                        if jogador_id in kg.nodes:
                             jogadores.append(kg.nodes[jogador_id]['propriedades']['nome'])
                
                print(f"\nJogadores que JOGAM_PELO {nome_time}:")
                if jogadores:
                    for nome in jogadores:
                        print(f"  - {nome}")
                else:
                    print("Nenhum jogador encontrado para este time.")
            else:
                print("Time não encontrado.")
                
        elif escolha == '3':
            print(f"Times disponíveis: {list(times_ids.keys())}")
            nome_time = input("Nome do Time para buscar jogos vencidos: ")
            time_id = times_ids.get(nome_time)
            
            if time_id:
                jogos_vencidos = []
                for edge in kg.edges:
                    if edge['sujeito_id'] == time_id and edge['predicado'] == 'VENCEU':
                        jogo_id = edge['objeto_id']
                        if jogo_id in kg.nodes:
                             placar = kg.nodes[jogo_id]['propriedades']['placar']
                             data = kg.nodes[jogo_id]['propriedades']['data']
                             jogos_vencidos.append(f"Jogo {data} (Placar: {placar})")
                
                print(f"\nJogos Vencidos pelo {nome_time}:")
                if jogos_vencidos:
                    for jogo in jogos_vencidos:
                        print(f"  - {jogo}")
                else:
                    print(f"{nome_time} não venceu nenhum jogo registrado.")
            else:
                print("Time não encontrado.")

        elif escolha == '4':
            break
        else:
            print("Opção inválida.")


def main():
    """Função principal que gerencia o fluxo de execução interativo."""
    kg = KnowledgeGraph()
    times_ids = {}
    
    print("\n=============================================")
    print("      Sistema de Knowledge Graph Esportivo     ")
    print("=============================================")
    print("INSTRUÇÃO: Crie o campeonato para iniciar. O mínimo de 20 nós será atingido.")

    id_torneio, times_ids = criar_campeonato_interativo(kg)
    
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print(f"1. Adicionar/Detalhar Entidades (Jogadores, Jogos)")
        print("2. Consultar o Knowledge Graph (Buscar dados)")
        print("3. Visualizar resumo e detalhes de um Nó (DEBUG)")
        print("4. GERAR GRÁFICO (Salvar em 'knowledge_graph_esportivo.png')")
        print("5. Sair e Gerar Relatório (Encerrar)")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_entidades_e_relacionamentos(kg, times_ids)
        elif escolha == '2':
            menu_consultas(kg, times_ids)
        elif escolha == '3':
            kg.imprimir_grafo_resumo()
            if kg.nodes:
                node_id_to_view = input("Digite o ID de um Nó para ver detalhes (ex: N1): ")
                if hasattr(kg, 'imprimir_no_detalhado'):
                    kg.imprimir_no_detalhado(node_id_to_view)
        
        elif escolha == '4':
            kg.gerar_visualizacao_graphviz()
            
        elif escolha == '5':
            print("\nEncerrando o sistema. Não se esqueça de gerar o seu relatório!")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.")

# --- INÍCIO DA EXECUÇÃO INTERATIVA ---
if __name__ == "__main__":
    main()