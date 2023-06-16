import random

TAMANHO_GRID = 10

TIPOS_NAVIOS = {
    "Porta-aviões": 5,
    "Tanque": 4,
    "Contra-torpedeiro": 3,
    "Submarino": 3,
    "Destroyer": 2
}

ESTADO_CELULA = {
    "Vazio": " ",
    "Navio": "O",
    "Ataque_Miss": "-",
    "Ataque_Hit": "X"
}

def criar_grid(tamanho):
    """Cria um grid vazio com o tamanho especificado."""
    grid = []
    for _ in range(tamanho):
        grid.append([ESTADO_CELULA["Vazio"]] * tamanho)
    return grid

def exibir_grid(grid, mostrar_navios=False):
    """Exibe o grid na forma de uma matriz, mostrando os navios se 'mostrar_navios' for True."""
    print("   " + " | ".join(map(str, range(len(grid)))))
    print("  " + "--" * (len(grid) * 2 - 1))
    for i, row in enumerate(grid):
        exibir_row = []
        for cell in row:
            if mostrar_navios and cell == ESTADO_CELULA["Navio"]:
                exibir_row.append(ESTADO_CELULA["Vazio"])
            else:
                exibir_row.append(cell)
        print(f"{i} | {' | '.join(exibir_row)} |")
        if i != len(grid) - 1:
            print("  " + "--" * (len(grid) * 2 - 1))
    print("  " + "--" * (len(grid) * 2 - 1))

def posicao_valida(grid, tipo_navio, x, y, direcao):
    """Verifica se a posição e a direção especificadas são válidas para posicionar um navio."""
    tamanho_navio = TIPOS_NAVIOS[tipo_navio]
    if direcao == "H":
        return y + tamanho_navio <= len(grid) and all(
            grid[x][y + i] == ESTADO_CELULA["Vazio"] for i in range(tamanho_navio)
        )
    elif direcao == "V":
        return x + tamanho_navio <= len(grid) and all(
            grid[x + i][y] == ESTADO_CELULA["Vazio"] for i in range(tamanho_navio)
        )
    return False

def posicionar_navio(grid, tipo_navio, x, y, direcao):
    """Posiciona um navio no grid na posição e direção especificadas."""
    tamanho_navio = TIPOS_NAVIOS[tipo_navio]
    if direcao == "H":
        for i in range(tamanho_navio):
            grid[x][y + i] = ESTADO_CELULA["Navio"]
    elif direcao == "V":
        for i in range(tamanho_navio):
            grid[x + i][y] = ESTADO_CELULA["Navio"]

def posicionar_navios_bot(grid):
    """Posiciona os navios do bot aleatoriamente no grid."""
    for tipo_navio, tamanho_navio in TIPOS_NAVIOS.items():
        while True:
            x = random.randint(0, len(grid) - 1)
            y = random.randint(0, len(grid) - 1)
            direcao = random.choice(["H", "V"])
            if posicao_valida(grid, tipo_navio, x, y, direcao):
                posicionar_navio(grid, tipo_navio, x, y, direcao)
                break

def realizar_ataque(grid, x, y):
    """Realiza um ataque em uma determinada posição do grid e retorna True se acertar um navio."""
    if 0 <= x < len(grid) and 0 <= y < len(grid):
        if grid[x][y] == ESTADO_CELULA["Navio"]:
            grid[x][y] = ESTADO_CELULA["Ataque_Hit"]
            return True
        elif grid[x][y] == ESTADO_CELULA["Vazio"]:
            grid[x][y] = ESTADO_CELULA["Ataque_Miss"]
            return False
    else:
        print("Ataque inválido. As coordenadas estão fora do grid.")
        return False

def verificar_fim_jogo(grid):
    """Verifica se o jogo chegou ao fim, ou seja, se todos os navios foram afundados."""
    return all(cell != ESTADO_CELULA["Navio"] for row in grid for cell in row)

def jogada_bot_dificil(grid):
    """Realiza uma jogada do bot de dificuldade difícil, tentando acertar um navio ou atacar aleatoriamente."""
    navios = []
    for row in grid:
        for cell in row:
            if cell == ESTADO_CELULA["Navio"]:
                navios.append((grid.index(row), row.index(cell)))

    if navios:
        while True:
            x, y = random.choice(navios)
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(grid)
                and 0 <= new_y < len(grid)
                and grid[new_x][new_y] != ESTADO_CELULA["Ataque_Hit"]
            ):
                return new_x, new_y

    while True:
        x = random.randint(0, len(grid) - 1)
        y = random.randint(0, len(grid) - 1)
        if grid[x][y] != ESTADO_CELULA["Ataque_Hit"]:
            return x, y

def jogar_battleship():
    """Função principal para jogar o jogo de Batalha Naval."""
    grid_jogador = criar_grid(TAMANHO_GRID)
    grid_bot = criar_grid(TAMANHO_GRID)
    grid_bot_tiros = criar_grid(TAMANHO_GRID)

    print("Posicione seus navios:")
    for tipo_navio, tamanho_navio in TIPOS_NAVIOS.items():
        exibir_grid(grid_jogador)
        while True:
            try:
                x = int(input(f"Digite a coordenada x para o {tipo_navio}: "))
                y = int(input(f"Digite a coordenada y para o {tipo_navio}: "))
                direcao = input("Digite a direção (H - horizontal, V - vertical): ").upper()
                if posicao_valida(grid_jogador, tipo_navio, x, y, direcao):
                    posicionar_navio(grid_jogador, tipo_navio, x, y, direcao)
                    break
                else:
                    print("Posição inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Tente novamente.")

    print("\nPosicionando os navios do bot...\n")
    posicionar_navios_bot(grid_bot)
    exibir_grid(grid_jogador)

    while True:
    # Jogada do jogador
        while True:
            try:
                x = int(input("Digite a coordenada x para atacar: "))
                y = int(input("Digite a coordenada y para atacar: "))
                if realizar_ataque(grid_bot, x, y):
                    print("Acertou um navio!")
                    if verificar_fim_jogo(grid_bot):
                        print("Parabéns! Você afundou todos os navios do bot. Você venceu!")
                        return
                else:
                    print("Ataque sem sucesso.")
                break
            except ValueError:
                print("Entrada inválida. Tente novamente.")

        # Verificar se o ataque do jogador foi válido
        if x < 0 or x >= len(grid_jogador) or y < 0 or y >= len(grid_jogador):
            print("Ataque inválido. A coordenada está fora do grid.")
            continue

        # Jogada do bot
        x, y = jogada_bot_dificil(grid_jogador)
        if realizar_ataque(grid_jogador, x, y):
            print(f"O bot acertou um navio em ({x}, {y})!")
            if verificar_fim_jogo(grid_jogador):
                print("Todos os seus navios foram afundados. Você perdeu!")
                return

        print("\nSeu grid:")
        exibir_grid(grid_jogador, mostrar_navios=False)

        print("\nGrid do bot:")
        exibir_grid(grid_bot, mostrar_navios=True)

jogar_battleship()
