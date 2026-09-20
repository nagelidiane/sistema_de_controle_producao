# Sistema de Controle de Produção

Projeto em Python para simular o controle de qualidade de peças em uma linha de produção.

O sistema permite cadastrar peças, verificar se elas estão dentro dos padrões definidos e separar automaticamente as peças aprovadas das reprovadas.

## O que o sistema faz

* Cadastra peças
* Verifica peso, cor e comprimento
* Mostra o motivo quando uma peça é reprovada
* Organiza as peças aprovadas em caixas de até 10 unidades
* Permite remover uma peça já cadastrada
* Mostra um resumo da produção
* Exporta os dados para Excel

## Regras

Para ser aprovada, a peça precisa estar dentro destes valores:

* **Peso:** entre 95g e 105g
* **Cor:** azul ou verde
* **Comprimento:** entre 10cm e 20cm

Se algum desses critérios não for atendido, a peça é reprovada.

Por exemplo:

```text
Peso: 100g
Cor: azul
Comprimento: 15cm
```

Nesse caso, a peça é aprovada.

Já uma peça com:

```text
Peso: 110g
Cor: vermelho
Comprimento: 25cm
```

será reprovada e o sistema informa todos os motivos.

## Como rodar

É necessário ter o Python instalado.

Depois, instale as bibliotecas usadas no projeto:

```bash
pip install pandas openpyxl
```

Execute o programa:

```bash
python sistema_producao.py
```

## Menu

O programa funciona pelo terminal e apresenta estas opções:

```text
1. Cadastrar nova peça
2. Listar peças aprovadas/reprovadas
3. Remover peça cadastrada
4. Listar caixas fechadas
5. Gerar relatório no terminal
6. Exportar para Excel
0. Sair
```

### Cadastro de peça

Ao escolher a opção `1`, o sistema pede:

```text
ID da peça:
Peso (g):
Cor:
Comprimento (cm):
```

Depois da avaliação, o resultado aparece no terminal.

Exemplo:

```text
[OK] Peça P001 aprovada.
```

ou:

```text
[!] Peça P002 REPROVADA.
Motivo: Peso fora do padrão (110g)
```

## Controle das caixas

As peças aprovadas são colocadas em uma caixa.

Cada caixa comporta 10 peças. Quando chega nesse limite, ela é fechada e o sistema começa a preencher a próxima.

A capacidade pode ser alterada no código:

```python
SistemaControleProducao(capacidade_caixa=10)
```

## Exportação para Excel

Na opção `6`, o programa gera um arquivo chamado:

```text
relatorio_producao.xlsx
```

O arquivo contém os dados das peças e informa se cada uma foi aprovada ou reprovada.

Para peças reprovadas, também aparece o motivo.

## Estrutura do projeto

Por enquanto, o projeto possui um arquivo principal:

```text
sistema_producao.py
```

Dentro dele existem duas classes principais:

* `Peca` — representa os dados de uma peça.
* `SistemaControleProducao` — responsável pelas avaliações, caixas, remoções e relatórios.

Também existe o `main()`, que controla o menu e a interação com o usuário.

## Tecnologias utilizadas

* Python
* Pandas
* OpenPyXL

## Observação

Os dados ficam apenas enquanto o programa está rodando. Se o programa for fechado, os dados cadastrados são perdidos.

O relatório em Excel pode ser usado para guardar os resultados da execução.
