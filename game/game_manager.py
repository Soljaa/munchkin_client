import pygame
from constants import *
from game.game_phases.charity_phase import CharityPhase
from game.game_phases.kick_door_phase import KickDoorFase
from game.game_phases.look_for_trouble_phase import LookForTroublePhase
from game.game_phases.loot_room_phase import LootRoomPhase
from game.game_phases.setup_phase import SetupPhase
from game.game_state import GameState, GamePhase, EndGameException
from ui.game_renderer import GameRenderer
from game.card import Gender


def main(name: str = "Player", avatar_img_dir="assets/selecao_player/avatares/avatar1.png", gender=Gender.MALE):

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
    game_state.add_player(name, avatar_img_dir, gender)
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
                # item management É COMO SE FOSSE A FASE DE **PREPARAÇÃO**
                if isinstance(action, tuple): # Se o clique for em um item
                    if game_state.phase == GamePhase.SETUP:
                        setup_phase = SetupPhase(game_state, action, renderer)
                        setup_phase.run()
                else: # Se o clique não for em um item (for em um botão)
                    print(f"\nButton clicked: {action}")
                    print(f"Current phase: {game_state.phase}")
                    print(f"Current player: {game_state.current_player().name}")
                    current_combat = game_state.current_combat

                    if action == "kick_door": # Se aperto para chutar porta # KICK DOOR
                        if game_state.phase == GamePhase.SETUP:
                            renderer.draw_kick_door_transition()
                            kick_door_phase = KickDoorFase(game_state, renderer)
                            kick_door_phase.run()

                    elif action == "run_away": # Se aperto para fugir... # RUN AWAY
                        player_died = False
                        if game_state.phase == GamePhase.COMBAT and game_state.current_combat: # ... e estou em combate
                            game_state.dice.roll() # Então rolo o dado 
                            renderer.draw_dice_animation(game_state.dice) # Faço a animação da rolagem
                            value = game_state.dice.last_roll # E salvo o valor do dado após a rolagem
                            if current_combat.try_to_run(value): # Se consigo fugir com sucesso (value>=5)
                                renderer.draw_run_away_success_transition() #Imagem referente ao sucesso na fuga
                                renderer.set_message("Fugiu com sucesso!")
                                game_state.set_combat(None)
                            else: # Se não consigo fugir (value<5)
                                renderer.draw_run_away_failed_transition() # Imagem referente a falha na fuga
                                renderer.set_message(f"Fuga falhou! {game_state.current_combat.monster.bad_stuff}")
                                current_combat.monster.apply_bad_stuff(game_state.current_player())

                                if game_state.current_player().level <= 0: # Se o jogador estiver morto (logo após a perda do nível)
                                    renderer.draw_alert_player_die(game_state.current_player()) # Desenha imagem do aviso da death do jogador
                                    player_died = True
                            game_state.door_deck.discard(current_combat.monster)
                            charity_phase = CharityPhase(game_state, renderer)
                            charity_phase.run(player_died)
                            game_state.next_player()
                            curr_turn = increase_global_turns(curr_turn, game_state)
                            print("Turno:", curr_turn)

                    elif action == "loot": # Se aperto por saquear # LOOT
                        if game_state.phase == GamePhase.KICK_DOOR:
                            #renderer.draw_loot_the_room_transition()
                            loot_room_phase = LootRoomPhase(game_state)
                            loot_room_phase.run()
                            loot_card = loot_room_phase.show_loot_card()
                            renderer.draw_loot_the_room_transition(loot_card)
                            charity_phase = CharityPhase(game_state, renderer)
                            charity_phase.run()
                            game_state.next_player()
                            curr_turn = increase_global_turns(curr_turn, game_state)
                            print("Turno:", curr_turn)

                    elif action == "finish_combat": # Se aperto para finalizar o combate...
                        if game_state.phase == GamePhase.COMBAT and game_state.current_combat: #... e estou na fase de combate
                            try:
                                monster_card = game_state.current_combat.monster
                                game_state.resolve_combat() # Resolve o combate, aplicando as devidas bonificações ou penalizações
                                game_state.door_deck.discard(monster_card)
                                charity_phase = CharityPhase(game_state, renderer)
                                charity_phase.run()
                                game_state.next_player()
                                curr_turn = increase_global_turns(curr_turn, game_state)
                                print("Turno:", curr_turn)
                            except EndGameException:
                                # mostrar tela de vencedor
                                print("Fim de jogo! Vencedor:", game_state.current_player().name)
                                raise


                    elif action == "look_for_trouble":
                        if game_state.phase == GamePhase.KICK_DOOR:
                            look_for_trouble_phase = LookForTroublePhase(game_state, renderer)  # Adicionando renderer
                            if not look_for_trouble_phase.run():
                                renderer.set_message("Sem monstros ou fase cancelada!")
                                game_state.set_game_phase(GamePhase.KICK_DOOR)

        # Draw current game state
        try:
            renderer.draw_game_state(game_state)
            pygame.display.flip()
        except Exception as e:
            print(f"Error during rendering: {e}")
            raise e

        # Cap the frame rate
        clock.tick(60)


def increase_global_turns(turn, game_state):
    print(f"Turno concluído. Próximo jogador: {game_state.current_player().name}")
    return turn + 1
