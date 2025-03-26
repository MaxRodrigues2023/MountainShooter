
from code.EnemyShot import EnemyShot
from code.PlayerShot import PlayerShot
from code.const import WIN_WIDTH, ENTITY_SCORE
from code.enemy import Enemy
from code.entity import Entity
from code.player import Player


class EntityMediator:



    @staticmethod
    def verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __give_score(enemy: Entity, entity_list: list[Entity]):
        if enemy.last_dmg and enemy.last_dmg.endswith('Shot'):
            shooter_name = enemy.last_dmg.replace('Shot', '')
            for ent in entity_list:
                if ent.name == shooter_name:
                    ent.score += ENTITY_SCORE[enemy.name]
                    print(f"{shooter_name} scored {ENTITY_SCORE[enemy.name]} points for killing {enemy.name}")
                    break

    @staticmethod
    def verify_collision_entity(ent1: Entity, ent2: Entity, entity_list: list[Entity]):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.verify_collision_entity(entity1, entity2, entity_list)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        # First award points for defeated enemies
        for ent in entity_list[:]:
            if isinstance(ent, Enemy) and ent.health <= 0:
                EntityMediator.__give_score(ent, entity_list)

        # Then remove dead entities
        entity_list[:] = [ent for ent in entity_list if ent.health > 0]
