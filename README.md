# ROGUE LIKING ⚔️

**Desenvolvedor:** Rafael Cardoso Ferreira

> Um jogo do gênero **Roguelike** desenvolvido em Python utilizando a biblioteca **PgZero**.

Este projeto foi desenvolvido como parte de um desafio técnico para tutores, com o objetivo de demonstrar domínio da linguagem Python, lógica de programação e arquitetura de software, respeitando restrições rígidas de bibliotecas.

---

## 📋 O Desafio Proposto

O objetivo foi criar um jogo completo "do zero", sem depender de engines robustas, para validar a compreensão dos fundamentos da programação de jogos.

**Requisitos e Restrições Atendidos:**
* **Bibliotecas Permitidas:** Uso exclusivo de `pgzero`, `math`, `random` e a classe `Rect` do `pygame`. Nenhuma outra biblioteca externa foi utilizada.
* **Gênero:** Roguelike (visão top-down com movimentação baseada em células/grid).
* **Mecânicas Obrigatórias:**
    * Movimentação suave entre células da grade.
    * Menu principal funcional (Iniciar, Configurações, Sair).
    * Música de fundo e efeitos sonoros.
    * Inimigos com comportamento autônomo e perigoso.
    * Animação de sprites (idle, walk, attack).

---

## 🚀 O Que Foi Implementado

O código foi estruturado utilizando Programação Orientada a Objetos (POO), separando responsabilidades em classes distintas.

* **Grid-Based Movement:** O jogador se move preso à grade, mas com interpolação visual suave (`smooth movement`) entre os tiles.
* **Geração de Nível:** O mapa possui variações visuais de terreno (grama, terra, grama escura) geradas proceduralmente.
* **Inteligência Artificial (Inimigos):**
    * **SmartEnemy (Esqueleto):** Alterna entre estados de "Patrulha" e "Perseguição" dependendo da distância do jogador.
    * **WitchEnemy (Bruxa):** Variação de inimigo com velocidade e parâmetros de detecção distintos.
* **Sistema de Combate:** Hitboxes dinâmicas para ataque, invencibilidade temporária após dano e feedback visual.
* **Interface (UI):** Menu principal, telas de Vitória e Game Over, com controle de áudio (On/Off).

---

## 📸 Screenshots

*(Espaço reservado para adicionar as imagens do jogo)*

| Menu Principal | Gameplay |
| :---: | :---: |
| ![Menu Screenshot](caminho/para/imagem_menu.png) | ![Gameplay Screenshot](caminho/para/imagem_game.png) |

---

## 🎮 Como Executar

Para jogar, você precisa ter o **Python 3** instalado.

### 1. Instalar Dependências
Certifique-se de estar na pasta raiz do jogo e instale o Pygame Zero executando o comando:

```bash
pip install pgzero
