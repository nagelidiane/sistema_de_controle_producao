
import sys
import pandas as pd

class Peca:
    def __init__(self, id_peca, peso, cor, comprimento):
        self.id = id_peca
        self.peso = peso
        self.cor = cor.lower()
        self.comprimento = comprimento

class SistemaControleProducao:
    def __init__(self, capacidade_caixa=10):
        self.capacidade_caixa = capacidade_caixa
        self.todas_pecas = [] 
        self.pecas_aprovadas = []
        self.pecas_reprovadas = []
        self.caixas = []
        self.caixa_atual = []

    def avaliar_peca(self, peca):
        motivos_reprovacao = []

        if not (95 <= peca.peso <= 105):
            motivos_reprovacao.append(f"Peso fora do padrão ({peca.peso}g)")
        
        cores_permitidas = ["azul", "verde"]
        if peca.cor not in cores_permitidas:
            motivos_reprovacao.append(f"Cor não permitida ({peca.cor})")
            
        if not (10 <= peca.comprimento <= 20):
            motivos_reprovacao.append(f"Comprimento fora do padrão ({peca.comprimento}cm)")

        if not motivos_reprovacao:
            self._armazenar_peca(peca)
            return True, "Aprovada"
        else:
            motivo_final = " | ".join(motivos_reprovacao)
            self.pecas_reprovadas.append({"peca": peca, "motivo": motivo_final})
            return False, motivo_final

    def _armazenar_peca(self, peca):
        self.pecas_aprovadas.append(peca)
        self.caixa_atual.append(peca)
        
        if len(self.caixa_atual) == self.capacidade_caixa:
            self.caixas.append(list(self.caixa_atual))
            self.caixa_atual = []

    def remover_peca(self, id_peca):
        peca_encontrada = None
        for p in self.todas_pecas:
            if str(p.id) == str(id_peca):
                peca_encontrada = p
                break
        
        if not peca_encontrada:
            return False, "Peça não encontrada."

        self.todas_pecas.remove(peca_encontrada)
        self._resetar_estado()
        for p in self.todas_pecas:
            self.avaliar_peca(p)
            
        return True, f"Peça {id_peca} removida e sistema atualizado."

    def _resetar_estado(self):
        self.pecas_aprovadas = []
        self.pecas_reprovadas = []
        self.caixas = []
        self.caixa_atual = []

    def exportar_para_excel(self, nome_arquivo="relatorio_producao.xlsx"):
        if not self.todas_pecas:
            return False, "Não há dados para exportar."
        
        dados = []
        reprovadas_ids = {item['peca'].id: item['motivo'] for item in self.pecas_reprovadas}
        
        for p in self.todas_pecas:
            status = "Aprovada"
            motivo = "-"
            if p.id in reprovadas_ids:
                status = "Reprovada"
                motivo = reprovadas_ids[p.id]
            
            dados.append({
                "ID": p.id,
                "Peso (g)": p.peso,
                "Cor": p.cor,
                "Comprimento (cm)": p.comprimento,
                "Status": status,
                "Motivo Reprovação": motivo
            })
        
        df = pd.DataFrame(dados)
        try:
            df.to_excel(nome_arquivo, index=False)
            return True, f"Arquivo '{nome_arquivo}' gerado com sucesso!"
        except Exception as e:
            return False, f"Erro ao gerar Excel: {str(e)}"

    def gerar_relatorio(self):
        print("\n" + "="*50)
        print("      RELATÓRIO CONSOLIDADO DE PRODUÇÃO")
        print("="*50)
        print(f"Total de peças processadas: {len(self.todas_pecas)}")
        print(f"Total de peças aprovadas:   {len(self.pecas_aprovadas)}")
        print(f"Total de peças reprovadas:  {len(self.pecas_reprovadas)}")
        print(f"Quantidade de caixas cheias: {len(self.caixas)}")
        print("="*50 + "\n")

def exibir_menu():
    print("\n--- SISTEMA DE AUTOMAÇÃO INDUSTRIAL v3 ---")
    print("1. Cadastrar nova peça")
    print("2. Listar peças aprovadas/reprovadas")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório no terminal")
    print("6. EXPORTAR PARA EXCEL")
    print("0. Sair")
    return input("Escolha uma opção: ")

def main():
    sistema = SistemaControleProducao(capacidade_caixa=10)
    
    while True:
        opcao = exibir_menu()
        
        if opcao == '1':
            try:
                id_p = input("ID da peça: ")
                peso = float(input("Peso (g): "))
                cor = input("Cor (azul/verde/outra): ")
                comp = float(input("Comprimento (cm): "))
                
                nova_peca = Peca(id_p, peso, cor, comp)
                sistema.todas_pecas.append(nova_peca)
                aprovada, msg = sistema.avaliar_peca(nova_peca)
                
                if aprovada:
                    print(f"\n[OK] Peça {id_p} aprovada.")
                else:
                    print(f"\n[!] Peça {id_p} REPROVADA. Motivo: {msg}")
            except ValueError:
                print("\n[Erro] Entrada inválida.")

        elif opcao == '2':
            print("\n--- LISTAGEM ---")
            for p in sistema.todas_pecas:
                status = "Aprovada"
                for r in sistema.pecas_reprovadas:
                    if r['peca'].id == p.id:
                        status = f"Reprovada ({r['motivo']})"
                print(f"ID: {p.id} | Status: {status}")

        elif opcao == '3':
            id_rem = input("ID para remover: ")
            sucesso, msg = sistema.remover_peca(id_rem)
            print(f"\n{msg}")

        elif opcao == '4':
            print(f"\n--- CAIXAS ({len(sistema.caixas)}) ---")
            for i, caixa in enumerate(sistema.caixas, 1):
                print(f"Caixa {i}: {[p.id for p in caixa]}")

        elif opcao == '5':
            sistema.gerar_relatorio()

        elif opcao == '6':
            sucesso, msg = sistema.exportar_para_excel()
            print(f"\n{msg}")

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
