from django.db import models

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
    archtype = models.CharField(max_length=100, choices=ARCHETYPES)
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
        return self.archtype


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

    name = models.CharField(max_length=100)
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES)
    nickname = models.CharField(max_length=100)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=10)
    agility = models.IntegerField(default=10)
    stamina = models.IntegerField(default=100)
    morale = models.IntegerField(default=100)
    loyalty = models.IntegerField(default=100)
    archtype = models.ForeignKey(Archetype, on_delete=models.SET_NULL, null=True, blank=True)

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

    def __str__(self):
        return f"{self.name} aka {self.nickname}"
    
    def recieve_damage(self):
        healt


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
    damage = models.IntegerField()
    weight = models.FloatField()
    durability = models.IntegerField(default=100)
    is_ranged = models.BooleanField(default=False)
    range = models.IntegerField(default=1)  # 1 = melee, 2+ = ranged

    speed = models.FloatField(default=1.0)  # Attack speed modifier
    crit_chance = models.FloatField(default=0.05)  # Base crit chance

    def __str__(self):
        return f"{self.name} ({self.get_weapon_class_display()})"
