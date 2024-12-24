import pygame
import sys
from constants import *
from game.game_state import GameState, GamePhase
from ui.game_renderer import GameRenderer

def main():
    # Set pygame to use software rendering
    import os
    os.environ['SDL_VIDEODRIVER'] = 'windows'
    
    # Initialize Pygame with error handling
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

    # Initialize game state
    game_state = GameState()
    game_state.add_player("Player 1")
    game_state.add_player("Player 2")

    # Initialize renderer
    renderer = GameRenderer(screen)

    # Main game loop
    running = True
    while running:
        # Clear the screen
        screen.fill(WHITE)
        # Render the dungeon_backgorund (play area)
        renderer.draw_dungeon_background()
        # Render the gameboard
        renderer.draw_gameboard()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle button clicks and card interactions
            action = renderer.handle_event(event, game_state)
            if action:
                if isinstance(action, tuple):
                    action_type, index = action
                    current_player = game_state.current_player()
                    
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
                        if game_state.phase == GamePhase.KICK_DOOR:
                            success = game_state.kick_down_door()
                            if success and game_state.current_combat:
                                renderer.set_message(f"Combat started! Fighting {game_state.current_combat.monster.name}!")
                            else:
                                renderer.set_message("You found something else...")
                    elif action == "run_away":
                        if game_state.current_combat:
                            if game_state.current_combat.try_to_run():
                                renderer.set_message("Successfully ran away!")
                                game_state.current_combat = None
                            else:
                                renderer.set_message(f"Failed to run away! {game_state.current_combat.monster.bad_stuff}")
                                game_state.current_player().level_down()
                            game_state.phase = GamePhase.CHARITY
                    elif action == "end_turn":
                        if game_state.current_combat:
                            success, result = game_state.resolve_combat()
                            if success:
                                renderer.set_message(f"Victory! Gained {result['treasure']} treasure(s)!")
                            else:
                                renderer.set_message(f"Defeat! {result['bad_stuff']}")
                        else:
                            next_player = game_state.players[(game_state.current_player_index + 1) % len(game_state.players)]
                            renderer.set_message(f"Turn ended. {next_player.name}'s turn!")
                        game_state.next_player()

        # Draw current game state
        try:
            renderer.draw_game_state(game_state)
            pygame.display.flip()
        except Exception as e:
            print(f"Error during rendering: {e}")
            
        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
