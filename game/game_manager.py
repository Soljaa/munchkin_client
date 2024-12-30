import pygame
from constants import *
from game.game_state import GameState, GamePhase, EndGameException
from ui.game_renderer import GameRenderer
from game.cards.monsters import (Monster, CompositeEffect, PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect, NotPursueLevelEffect,
                       LoseLevelBadStuff)


def main(name: str = "Player", avatar_img_dir="assets/selecao_player/avatares/avatar1.png"):

    """
    MAIN GAME LOOP: GERENCIA O GAMESTATE E POSSIBILITA FUTURA IMPLEMENTAÇÃO DE MULTIPLAYER
    TODO: class game_manager
    """

    try:
        pygame.init()
    except pygame.error as e:
        print(f"Failed to initialize pygame: {e}")
        return

    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SWSURFACE)
        pygame.display.set_caption("Munchkin")
    except pygame.error as e:
        print(f"Failed to set display mode: {e}")
        pygame.quit()
        return

    clock = pygame.time.Clock()

    curr_turn = 1

    # TODO: entry point for multiplayer
    # Initialize game state, default 1P Vs Com
    game_state = GameState()
    game_state.add_player(name, avatar_img_dir)
    game_state.add_player("Player 2", "assets/selecao_player/avatares/avatar2.png")
    game_state.add_player("Player 3", "assets/selecao_player/avatares/avatar3.png")
    game_state.add_player("Player 4", "assets/selecao_player/avatares/avatar4.png")

    # Initialize renderer
    renderer = GameRenderer(screen)

    # Main game loop
    while True:
        # Clear the screen
        screen.fill(WHITE)
        # Render the dungeon_backgorund (play area)
        renderer.draw_dungeon_background()
        # Render the gameboard
        renderer.draw_gameboard()

        # Revive jogador morto
        if game_state.current_player().level==0: # Se o jogador morreu
            game_state.current_player().level_up() # Revive (dando +1 de nível, ficando com nível 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Handle button clicks and card interactions
            action = renderer.handle_event(event, game_state)
            if action:
                current_player = game_state.current_player()

                # item management
                if isinstance(action, tuple): # Se o clique for em um item
                    action_type, index = action

                    if game_state.phase == GamePhase.SETUP:                      
                        if action_type == "equip_item":
                            if index < len(current_player.hand): # "Possívelmente" redundante (o index obrigatoriamente já vai ser menor que o tamanho da mão, haja vista que é gerado a partir de uma seleção dessa propria mão)
                                card = current_player.hand[index]
                                if current_player.equip_item(card):
                                    renderer.set_message(f"Equipped {card.name}!")
                                else:
                                    renderer.set_message("Cannot equip this item!")

                        elif action_type == "unequip_item":
                            if index < len(current_player.equipped_items): # "Possívelmente" redundante (pelo mesmo motivo acima)
                                item = current_player.equipped_items[index]
                                current_player.unequip_item(item)
                                renderer.set_message(f"Unequipped {item.name}")
                else: # Se o clique não for em um item (for em um botão)
                    print(f"\nButton clicked: {action}")
                    print(f"Current phase: {game_state.phase}")
                    print(f"Current player: {current_player.name}")
                    current_combat = game_state.current_combat

                    if action == "kick_door": # Se aperto para chutar porta
                        game_state.set_game_phase(GamePhase.KICK_DOOR)
                        if game_state.phase == GamePhase.KICK_DOOR: # "Possívelmente" redundante (pois essa fase acaba de ser setada acima)
                            success = game_state.kick_down_door() # True ou False para se retirou uma carta com sucesso
                            if success and current_combat: # Se tirou carta com sucesso e estamos na fase de combate (fase de combate é setada em "game_state.kick_down_door()" caso tenha retirado um monstro)
                                renderer.set_message(f"Combat started! Fighting {current_combat.monster.name}!")
                            else:
                                # curse
                                renderer.set_message("You found something else... You are Cursed")
                                # show look for trouble ou loot
                    elif action == "run_away": # Se aperto para fugir...
                        player_died = False
                        if current_combat: # ... e estou em combate
                            game_state.dice.roll() # Então rolo o dado 
                            renderer.draw_dice_animation(game_state.dice) # Faço a animação da rolagem
                            value = game_state.dice.last_roll # E salvo o valor do dado após a rolagem
                            if current_combat.try_to_run(value): # Se consigo fugir com sucesso (value>=5)
                                renderer.set_message("Successfully ran away!")
                                game_state.set_combat(None)
                            else: # Se não consigo fugir (value<5)
                                renderer.set_message(f"Failed to run away! {current_combat.monster.bad_stuff}")
                                current_combat.monster.apply_bad_stuff(current_player)

                                if current_player.level <= 0: # Se o jogador estiver morto
                                    renderer.draw_alert_player_die(current_player) # Desenha imagem do aviso da death do jogador
                                    # refazer toda essa parte de morte, ta dando respawn mas ta feio
                                    #dead_player = (current_player().name,
                                                   #current_player().avatar_img_dir)
                                    #game_state.players.remove(current_player())
                                    #game_state.add_player(dead_player[0], dead_player[1])
                                    player_died = True
                            renderer.set_message("Doing charity... Redistributing cards")
                            game_state.play_charity_phase(player_died)
                            game_state.next_player()
                            curr_turn += 1
                            print("Turno:", curr_turn)

                    elif action == "loot": # Se aperto por saquear
                        if game_state.phase == GamePhase.KICK_DOOR: # Acho que deve ser uma fase intermediária entre KICK_DOOR e LOOT_ROOM, caso sim, dps trocar
                            game_state.set_game_phase(GamePhase.LOOT_ROOM)
                            if game_state.phase == GamePhase.LOOT_ROOM: # "Possivelmente" redundante, pois já foi setado acima"
                                game_state.loot()
                                renderer.set_message("Doing charity... Redistributing cards")
                                game_state.play_charity_phase()
                                game_state.next_player()
                                curr_turn += 1
                                print("Turno:", curr_turn)

                    elif action == "finish_combat": # Se aperto para finalizar o combate...
                        if current_combat: #... e estou na fase de combate
                            try:
                                game_state.resolve_combat() # Resolve o combate, aplicando as devidas bonificações ou penalizações
                                renderer.set_message("Doing charity... Redistributing cards")
                                game_state.play_charity_phase()
                                game_state.next_player()
                                curr_turn += 1
                                print("Turno:", curr_turn)
                            except EndGameException:
                                # mostrar tela de vencedor
                                print("Fim de jogo! Vencedor:", game_state.current_player().name)
                                raise
                        #game_state.next_player()

                    elif action == "look_for_trouble":
                        # abre modal pro player escolher um monstro da mão, vou mocar com um monstro aleatorio mas
                        # tem q fazer a lógica para ver se o cara tem monstro na mão e escolher o monstro mas precisa
                        # melhorar o display de cartas primeiro, se nao tiver monstro, mostrar aviso e nao fazer
                        # nada, so restando pra ele saquear
                        game_state.set_game_phase(GamePhase.LOOK_FOR_TROUBLE)
                        if game_state.phase == GamePhase.LOOK_FOR_TROUBLE:
                            monster_selected = Monster(
                                name="Wight Brothers",
                                image="assets/door_cards/WightBrothers.png",
                                level=16,
                                treasure=4,
                                effect=CompositeEffect(
                                    PlayerLoseLevelsIfLevelIsBiggerThanMonsterEffect(2),
                                    NotPursueLevelEffect(3)
                                ),
                                bad_stuff=LoseLevelBadStuff(1),
                            )
                            success = game_state.look_for_trouble(monster_selected)
                            if success and current_combat:
                                renderer.set_message(
                                    f"Combat started! Fighting {current_combat.monster.name}!")



        # Draw current game state
        try:
            renderer.draw_game_state(game_state)
            pygame.display.flip()
        except Exception as e:
            raise e
            print(f"Error during rendering: {e}")

        # Cap the frame rate
        clock.tick(60)
