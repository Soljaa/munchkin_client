import pygame
from constants import *
from game.combat import CombatStates
from game.game_phases.charity_phase import CharityPhase
from game.game_phases.kick_door_phase import KickDoorFase
from game.game_phases.look_for_trouble_phase import LookForTroublePhase
from game.game_phases.loot_room_phase import LootRoomPhase
from game.game_phases.setup_phase import SetupPhase
from game.game_state import GameState, GamePhase, EndGameException
from ui.game_renderer import GameRenderer
from game.card import RaceTypes, Item


class GameManager:
    def __init__(self, players: [dict]):
        try:
            pygame.init()
        except pygame.error as e:
            print(f"Failed to initialize pygame: {e}")
            return

        self._display = pygame.display
        self.screen = self._display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SWSURFACE)
        self.clock = pygame.time.Clock()
        self.curr_turn = 1
        self.game_state = GameState()
        self.renderer = GameRenderer(self.screen)
        self.players = players
        self.waiting_timer = 120


    def run(self):
        try:
            self._display.set_caption("Munchkin")
        except pygame.error as err:
            print(f"Failed to set display mode: {err}")
            pygame.quit()
            return

        # add players
        for player in self.players:
            self.game_state.add_player(player['name'], player['avatar'], player['gender'], player['is_ai'])

        while True:
            self.screen.fill(WHITE)
            self.renderer.draw_dungeon_background()
            self.renderer.draw_gameboard()

            if pygame.key.get_pressed()[pygame.K_F11]:
                self._display.toggle_fullscreen()

            # revive player and draw hand again
            if self.game_state.current_player().level == 0:
                self.game_state.current_player().level_up()
                if not self.game_state.current_player().hand:
                    for _ in range(4):
                        self.game_state.current_player().draw_card(self.game_state.door_deck)
                        self.game_state.current_player().draw_card(self.game_state.treasure_deck)

            # AI turn ir player is ai
            if self.game_state.current_player().is_ai:
                self.play_automatic_turn()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  # Verifica se a tecla foi pressionada
                    if event.key == pygame.K_p:   # Verifica se a tecla pressionada foi 'P'
                        self.renderer.draw_selection_player(self.game_state.players, self.game_state.current_player(), "Jogadores", background="assets/game/sell_modal.jpeg")

                if event.type == pygame.QUIT:
                    return

                # Handle button clicks and card interactions
                action = self.renderer.handle_event(event, self.game_state)
                self.handle_action(action)


            # Draw current game state
            try:
                self.renderer.draw_game_state(self.game_state)
                self._display.flip()
            except Exception as err:
                print(f"Error during rendering: {err}")

            # Cap the frame rate
            self.clock.tick(60)


    def increase_global_turns(self):
        print(f"Turno concluído. Próximo jogador: {self.game_state.current_player().name}")
        return self.curr_turn + 1

    def play_automatic_turn(self):
        action = None
        self.renderer.set_message(f"Turno de IA ({self.game_state.current_player().name})")
        if self.waiting_timer > 0:
            self.waiting_timer -= 1
        else:
            if self.game_state.phase == GamePhase.SETUP:
                for item in self.game_state.current_player().hand:
                    if isinstance(item, Item):
                        setup_phase = SetupPhase(self.game_state, ('equip_item', item), self.renderer)
                        setup_phase.run()
                action = "kick_door"
            if self.game_state.phase == GamePhase.KICK_DOOR:
                action = "loot"
            if self.game_state.phase == GamePhase.COMBAT and self.game_state.current_combat:
                if self.game_state.current_combat.get_combat_state() == CombatStates.WINNING:
                    action = "finish_combat"
                else:
                    action = "run_away"
            if self.game_state.phase == GamePhase.FINAL_SETUP:
                action = "end_turn"
            if self.game_state.phase == GamePhase.CHARITY:
                print("ia na caridade")
                action = None
                self.game_state.next_player()
            self.waiting_timer = 60
            if action:
                self.handle_action(action, ai_turn=True)

    def handle_action(self, action=None, ai_turn: bool=False):
        if action:
            # item management É COMO SE FOSSE A FASE DE **PREPARAÇÃO**
            if isinstance(action, tuple):  # Se o clique for em um item
                if self.game_state.phase == GamePhase.SETUP or self.game_state.phase == GamePhase.FINAL_SETUP:
                    setup_phase = SetupPhase(self.game_state, action, self.renderer)
                    setup_phase.run()
            else:  # Se o clique não for em um item (for em um botão)
                print(f"\nButton clicked: {action}")
                print(f"Current phase: {self.game_state.phase}")
                print(f"Current player: {self.game_state.current_player().name}")
                current_combat = self.game_state.current_combat

                if action == "kick_door":  # Se aperto para chutar porta # KICK DOOR
                    if self.game_state.phase == GamePhase.SETUP:
                        self.renderer.draw_kick_door_transition()
                        kick_door_phase = KickDoorFase(self.game_state, self.renderer)
                        kick_door_phase.run()

                elif action == "run_away":  # Se aperto para fugir... # RUN AWAY
                    player_died = False
                    current_combat.monster.apply_effect(self.game_state.current_player())
                    if current_combat.monster.pursue is not True:
                        self.renderer.draw_run_away_success_transition()
                        self.renderer.set_message("Level muito baixo, o monstro decidiu não te perseguir!")
                        self.game_state.set_combat(None)
                        self.renderer.set_message("Prepare-se antes de fazer caridade!")
                        self.game_state.set_game_phase(GamePhase.FINAL_SETUP)
                    elif self.game_state.phase == GamePhase.COMBAT and self.game_state.current_combat:  # ... e estou em combate
                        self.game_state.dice.roll()  # Então rolo o dado
                        self.renderer.draw_dice_animation(self.game_state.dice)  # Faço a animação da rolagem
                        value = self.game_state.dice.last_roll  # E salvo o valor do dado após a rolagem
                        if self.game_state.current_player().get_player_race() == RaceTypes.ELF:  # Se for Elf, dá +1 no Run Away
                            value += 1
                        self.game_state.door_deck.discard(current_combat.monster)
                        print("VALOR DO DADO: ", value)
                        if current_combat.try_to_run(value):  # Se consigo fugir com sucesso (value>=5)
                            self.renderer.draw_run_away_success_transition()  # Imagem referente ao sucesso na fuga
                            self.renderer.set_message("Fugiu com sucesso!")
                            self.game_state.set_combat(None)
                            self.renderer.set_message("Prepare-se antes de fazer caridade!")
                            self.game_state.set_game_phase(GamePhase.FINAL_SETUP)
                        else:  # Se não consigo fugir (value<5)
                            self.renderer.draw_run_away_failed_transition()  # Imagem referente a falha na fuga
                            self.renderer.set_message(
                                f"Fuga falhou! {self.game_state.current_combat.monster.bad_stuff}")
                            current_combat.monster.apply_bad_stuff(self.game_state.current_player())

                            if self.game_state.current_player().level <= 0:  # Se o jogador estiver morto por causa do bad stuff do monstro (class Death())
                                self.renderer.draw_transition("assets/death_background.jpg", duration=2,
                                                              extra_element=lambda: self.renderer.alert_player_die(
                                                                  self.game_state.current_player()))
                                player_died = True

                            if player_died:
                                charity_phase = CharityPhase(self.game_state, self.renderer, ai_turn=ai_turn)
                                charity_phase.run(player_died)
                                self.game_state.next_player()
                                self.increase_global_turns()
                            else:
                                self.game_state.set_combat(None)
                                self.renderer.set_message("Prepare-se antes de fazer caridade!")
                                self.game_state.set_game_phase(GamePhase.FINAL_SETUP)

                elif action == "loot":  # Se aperto por saquear # LOOT
                    if self.game_state.phase == GamePhase.KICK_DOOR:
                        self.game_state.current_curse = None
                        loot_room_phase = LootRoomPhase(self.game_state)
                        loot_room_phase.run()
                        loot_card = loot_room_phase.show_loot_card()
                        self.renderer.draw_loot_the_room_transition(loot_card)
                        self.renderer.set_message("Prepare-se antes de fazer caridade!")
                        self.game_state.set_game_phase(GamePhase.FINAL_SETUP)

                elif action == "finish_combat":  # Se aperto para finalizar o combate...
                    if self.game_state.phase == GamePhase.COMBAT and self.game_state.current_combat:  # ... e estou na fase de combate
                        try:
                            monster_card = self.game_state.current_combat.monster
                            self.game_state.resolve_combat()  # Resolve o combate, aplicando as devidas bonificações ou penalizações
                            self.game_state.door_deck.discard(monster_card)
                            self.renderer.set_message("Prepare-se antes de fazer caridade!")
                            self.game_state.set_game_phase(GamePhase.FINAL_SETUP)

                        except EndGameException:
                            # mostrar tela de vencedor
                            self.renderer.draw_transition("assets/game/bg_winner.jpg", duration=2,
                                                          extra_element=lambda: self.renderer.draw_winner(
                                                              self.game_state.current_player()))
                            print("Fim de jogo! Vencedor:", self.game_state.current_player().name)
                            raise

                elif action == "look_for_trouble":
                    if self.game_state.phase == GamePhase.KICK_DOOR:
                        self.game_state.current_curse = None
                        look_for_trouble_phase = LookForTroublePhase(self.game_state,
                                                                     self.renderer)  # Adicionando renderer
                        if not look_for_trouble_phase.run():
                            self.renderer.set_message("Sem monstros ou fase cancelada!")
                            self.game_state.set_game_phase(GamePhase.KICK_DOOR)

                elif action == "end_turn":
                    charity_phase = CharityPhase(self.game_state, self.renderer, ai_turn=ai_turn)
                    charity_phase.run()
                    self.game_state.next_player()
                    self.increase_global_turns()

                elif action == "sell_items":
                    if self.game_state.phase == GamePhase.SETUP or self.game_state.phase == GamePhase.FINAL_SETUP:
                        setup_phase = SetupPhase(self.game_state, ("sell_items", None), self.renderer)
                        setup_phase.run()
