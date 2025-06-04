from django.db import models
from django.contrib.auth.models import User
from random import randint

# Create your models here.


class Archetype(models.Model):

    ARCHETYPES = [
        ('hoplite', 'Hoplite'),
        ('peltast', 'Peltast'),
        ('toxotes', 'Toxotes'),
        ('hippikon', 'Hippikon'),
        ('psilos', 'Psilos'),
        ('strategos', 'Strategos'),
    ]
    archetype = models.CharField(max_length=100, choices=ARCHETYPES)
    description = models.TextField(blank=True)

    # Optional: Bonus stats
    strength_bonus = models.IntegerField(default=0)
    agility_bonus = models.IntegerField(default=0)
    stamina_bonus = models.IntegerField(default=0)
    morale_bonus = models.IntegerField(default=0)
    intimidation_bonus = models.FloatField(default=0.0)

    # Optional: Starting gear tag or style
    culture = models.CharField(max_length=100, blank=True)  # e.g., "Spartan", "Athenian", "Macedonian"

    def __str__(self):
        return self.archetype


class Character(models.Model):
    RELIGION_CHOICES = [
        # Ancient polytheistic
        ('olympian', 'Olympian Pantheon'),
        ('orphic', 'Orphic Mysteries'),
        ('dionysian', 'Dionysian Cult'),
        ('heroic', 'Hero Cults'),

        # Foreign ancient cults
        ('isis', 'Cult of Isis'),
        ('mithraic', 'Mithraic Mysteries'),
        ('zoroastrian', 'Zoroastrianism'),

        # Major world religions (later or alternate timeline)
        ('christianity', 'Christianity'),
        ('islam', 'Islam'),
        ('judaism', 'Judaism'),]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters', null=True)
    name = models.CharField(max_length=100)
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES)
    nickname = models.CharField(max_length=100)
    skin_tone = models.CharField(max_length=100, choices=[('White', 'White'), ('Tan', 'Tan'), ('Black', 'Black')], default=1)
    hairstyle = models.CharField(max_length=100, choices=[('Bald', 'Bald'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')], default=1)
    facial_hair = models.CharField(max_length=100, choices=[('Bald', 'Bald'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long')], default=1)
    max_health = models.IntegerField(default=100)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    agility = models.IntegerField(default=10)
    stamina = models.IntegerField(default=100)
    max_stamina = models.IntegerField(default=100)
    morale = models.IntegerField(default=100)
    loyalty = models.IntegerField(default=100)
    archetype = models.ForeignKey(Archetype, on_delete=models.SET_NULL, null=True, blank=True)
    money = models.IntegerField(default=34)
    level = models.IntegerField(default=1)
    xp_points = models.FloatField(default=0)
    vitality = models.IntegerField(default=1)
    focus = models.IntegerField(default=1)

    # 🗡 Equipped weapon
    equipped_weapon = models.ForeignKey('Weapon', on_delete=models.SET_NULL, null=True, blank=True)

    # 🛡 Equipped armor slots
    head = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_armor')
    chest = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='chest_armor')
    shoulders = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='shoulders_armor')
    arms = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='arms_armor')
    hands = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='hands_armor')
    waist = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='waist_armor')
    legs = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='legs_armor')
    feet = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='feet_armor')
    shield = models.ForeignKey('Armour', on_delete=models.SET_NULL, null=True, blank=True, related_name='shield_armor')

    def __str__(self) -> str:
        return f"{self.name} aka {self.nickname}"

    def attack(self, target: object, attack_input: str) -> int:
        """
        Attack Target Function
        Targets health reduced accordingly

        Args:
            target (object): Target to inflcit attack upon
            attack_input (str): Type of attack. i.e light, heavy etc

        Returns:
            int: final damage inflicted
        """
        # attack type, damage multiplier, stamina stamina_cost
        attack_types = {
            "light": {"modifier": 0.8, "stamina_cost": 10},
            "normal": {"modifier": 1.0, "stamina_cost": 20},
            "heavy": {"modifier": 1.5, "stamina_cost": 35},
        }

        attack = attack_types[attack_input]
        if self.stamina < attack['stamina_cost']:
            return f'{self.name} does not have enough stamina for {attack_input} attack'

        self.stamina -= attack['stamina_cost']

        if not self.equipped_weapon:
            damage = self.strength * attack["modifier"]

        else:
            damage = self.strength + self.equipped_weapon.calculate_damage() * attack["modifier"]

        final_damage = target.receive_damage(damage)

        return final_damage

    def receive_damage(self, damage: int) -> int:
        """
        Generates the damaged recieved from the attack. Minusing the attack from the overall defence of the target.

        Args:
            damage (int): final damage taken
        """
        defense = self.total_defence_stats()
        actual_damage = max(0, damage - defense)

        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        self.save()

        return actual_damage

    def rest(self, focus) -> int:
        """
        Rest Action in Battle

        Recovers stamina mulitplied by the character's focus attribute.

        Returns:
            int: the amount of stamina gained
        """
        stamina_recovery_amount = 25 * focus
        self.stamina += stamina_recovery_amount
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina
        self.save()
        return stamina_recovery_amount

    def heal(self, vitality) -> int:
        """
        Heal Action in Battle.
        Recovers health using the character's vitality attirbute as a multiplier.

        Args:
            vitaity (int): mulitiplier used to calculate health regained.

        Returns:
            int: the amount of health gained
        """
        health_recovery_amount = 25 * vitality
        self.health += health_recovery_amount
        if self.health > self.max_health:
            self.health = self.max_health
        self.save()
        return health_recovery_amount

    @property
    def health_percent(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if self.max_health == 0:
            return 0
        return int((self.health / self.max_health) * 100)

    def total_defence_stats(self) -> int:
        """
        calculate the total defence of the character, depending on their armour and defence skills.

        Returns:
            int: total defence/armour points
        """
        total_defence = 0
        for armour in [self.head, self.chest, self.shoulders, self.arms, self.hands, self.waist, self.legs, self.feet, self.shield]:
            if armour:
                total_defence += armour.defence
        return total_defence

    def adjust_money(self, amount: int) -> int:
        """
        Adjust money of character from buying or selling items

        Args:
            amount (int): the amount spent/earnt
        """
        self.money += amount
        if self.money < 0:
            self.money = 0

        self.save()
        return self.money

    def battle_winnings(self, level: int):
        """
        Generate winnings from victorious battles
        higher rewards based on higher levels

        Args:
            level (int): the level of opponent fought
        """
        if level == 1:
            winnings = randint(50, 200)
        elif level == 2:
            winnings = randint(200, 450)
        elif level == 3:
            winnings = randint(450, 700)
        else:
            raise ValueError()

        self.money += winnings
        self.save()

        return winnings

    def gain_xp(self, opponent_level: int) -> int:
        """
        The amount of xp gained from battles

        Args:
            opponent_level (int): the level of opponent, determines the 
            amount of xp gained. 

            if xp surpasses the limit for the current level of the user
            it will trigger a level up for the character

        Returns:
            int: amount of xp gained
        """

        gained_xp = randint(10, 20) * opponent_level
        self.xp_points += gained_xp

        while self.xp_points >= self.xp_to_next_level:
            self.xp_points -= self.xp_to_next_level
            self.level += 1

        self.save()

        return gained_xp

    @property
    def xp_to_next_level(self) -> int:
        """
        Increases the xp amount needed to level up as the character
        progreses and levels up.

        Returns:
            int: the amount of xp required to level up
        """
        return 100 + (self.level - 1) * 50


class Armour(models.Model):
    BODY_PART_CHOICES = [
        ('head', 'Head'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('hands', 'Hands'),
        ('chest', 'Chest'),
        ('waist', 'Waist'),
        ('legs', 'Legs'),
        ('feet', 'Feet'),
        ('shield', 'Shield'),
    ]
    name = models.CharField(max_length=100)
    defence = models.IntegerField()
    weight = models.FloatField()
    durability = models.IntegerField(default=100)
    body_part = models.CharField(max_length=50, choices=BODY_PART_CHOICES)


class Weapon(models.Model):
    WEAPON_CLASS_CHOICES = [
        ('sword', 'Sword'),
        ('spear', 'Spear'),
        ('axe', 'Axe'),
        ('bow', 'Bow'),
        ('javelin', 'Javelin'),
        ('sling', 'Sling'),
        ('dagger', 'Dagger'),
        ('mace', 'Mace'),
        ('staff', 'Staff'),
        ('polearm', 'Polearm'),
    ]
    name = models.CharField(max_length=100)
    weapon_class = models.CharField(max_length=20, choices=WEAPON_CLASS_CHOICES)
    min_damage = models.IntegerField()
    max_damage = models.IntegerField()
    weight = models.FloatField()
    durability = models.IntegerField(default=100)
    is_ranged = models.BooleanField(default=False)
    range = models.IntegerField(default=1)  # 1 = melee, 2+ = ranged

    speed = models.FloatField(default=1.0)  # Attack speed modifier
    crit_chance = models.FloatField(default=0.05)  # Base crit chance

    def __str__(self):
        return f"{self.name} ({self.get_weapon_class_display()})"

    def calculate_damage(self):
        """calculate damage from the weapon damage range available

        Returns:
            int: damage points
        """
        damage = randint(self.min_damage, self.max_damage)
        return damage

