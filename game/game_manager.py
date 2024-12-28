import pygame
from constants import *
from game.game_state import GameState, GamePhase, EndGameException
from ui.game_renderer import GameRenderer


def main(name: str = "Palyer 1"):

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
    game_state.add_player(name)
    game_state.add_player("Player 2")
    game_state.add_player("Player 3")
    game_state.add_player("Player 4")

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Handle button clicks and card interactions
            action = renderer.handle_event(event, game_state)
            if action:
                # item management
                if isinstance(action, tuple):
                    action_type, index = action
                    current_player = game_state.current_player()

                    if game_state.phase == GamePhase.SETUP:
                        if action_type == "equip_item":
                            if index < len(current_player.hand):
                                card = current_player.hand[index]
                                if current_player.equip_item(card):
                                    renderer.set_message(f"Equipped {card.name}!")
                                else:
                                    renderer.set_message("Cannot equip this item!")

                        elif action_type == "unequip_item":
                            if index < len(current_player.equipped_items):
                                item = current_player.equipped_items[index]
                                current_player.unequip_item(item)
                                renderer.set_message(f"Unequipped {item.name}")
                else:
                    print(f"\nButton clicked: {action}")
                    print(f"Current phase: {game_state.phase}")
                    print(f"Current player: {game_state.current_player().name}")

                    if action == "kick_door":
                        game_state.set_game_phase(GamePhase.KICK_DOOR)
                        if game_state.phase == GamePhase.KICK_DOOR:
                            success = game_state.kick_down_door()
                            if success and game_state.current_combat:
                                renderer.set_message(f"Combat started! Fighting {game_state.current_combat.monster.name}!")
                            else:
                                # curse
                                renderer.set_message("You found something else...")
                    elif action == "run_away":
                        if game_state.current_combat:
                            if game_state.current_combat.try_to_run():
                                renderer.set_message("Successfully ran away!")
                                game_state.set_combat(None)
                            else:
                                renderer.set_message(f"Failed to run away! {game_state.current_combat.monster.bad_stuff}")
                                game_state.current_player().level_down()
                            game_state.play_charity_phase()
                            game_state.next_player()
                            curr_turn += 1
                            print("Turno:", curr_turn)

                    elif action == "finish_combat":
                        if game_state.current_combat:
                            try:
                                game_state.resolve_combat()
                            except EndGameException:
                                # mostrar tela de vencedor
                                print("Fim de jogo! Vencedor: ", game_state.current_player().name)
                                raise
                        game_state.next_player()
                        curr_turn += 1
                        print("Turno:", curr_turn)

        # Draw current game state
        try:
            renderer.draw_game_state(game_state)
            pygame.display.flip()
        except Exception as e:
            print(f"Error during rendering: {e}")

        # Cap the frame rate
        clock.tick(60)
