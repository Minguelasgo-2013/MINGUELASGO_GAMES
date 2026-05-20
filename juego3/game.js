class Player {
    constructor(name, characterClass) {
        this.name = name;
        this.characterClass = characterClass;
        this.level = 1;
        this.experience = 0;
        this.maxExperience = 100;
        this.gold = 0;
        this.health = 100;
        this.maxHealth = 100;
        this.mana = 50;
        this.maxMana = 50;
        
        // Estadísticas base según la clase
        this.stats = this.getClassStats(characterClass);
        
        this.inventory = [];
        this.equipment = {
            weapon: null,
            armor: null,
            accessory: null
        };
        this.abilities = this.getClassAbilities(characterClass);
        this.achievements = [];
        this.questsCompleted = [];
        this.totalDamageDealt = 0;
        this.enemiesDefeated = 0;
    }

    getClassStats(characterClass) {
        const baseStats = {
            strength: 10,
            defense: 10,
            speed: 10,
            intelligence: 10,
            criticalChance: 5
        };

        switch(characterClass) {
            case 'warrior':
                return {
                    ...baseStats,
                    strength: 15,
                    defense: 13,
                    criticalChance: 3
                };
            case 'mage':
                return {
                    ...baseStats,
                    intelligence: 16,
                    strength: 7,
                    criticalChance: 8
                };
            case 'rogue':
                return {
                    ...baseStats,
                    speed: 16,
                    criticalChance: 15,
                    defense: 8
                };
            default:
                return baseStats;
        }
    }

    getClassAbilities(characterClass) {
        const abilities = {
            warrior: [
                {
                    name: 'Ataque Potente',
                    description: 'Ataque con 150% de daño',
                    damage: 1.5,
                    manaCost: 10,
                    cooldown: 0,
                    icon: '⚔️'
                },
                {
                    name: 'Escudo Defensivo',
                    description: 'Aumenta defensa un 50% durante 2 turnos',
                    defense: 1.5,
                    manaCost: 15,
                    cooldown: 0,
                    icon: '🛡️'
                },
                {
                    name: 'Golpe Devastador',
                    description: 'Ataque crítico garantizado',
                    damage: 2.5,
                    manaCost: 25,
                    cooldown: 0,
                    icon: '💥'
                }
            ],
            mage: [
                {
                    name: 'Bola de Fuego',
                    description: 'Ataque mágico de 120% de daño',
                    damage: 1.2,
                    manaCost: 15,
                    cooldown: 0,
                    icon: '🔥'
                },
                {
                    name: 'Escudo Mágico',
                    description: 'Reduce daño recibido un 40%',
                    defense: 0.6,
                    manaCost: 20,
                    cooldown: 0,
                    icon: '✨'
                },
                {
                    name: 'Tormenta Arcana',
                    description: 'Ataque masivo de 200% de daño',
                    damage: 2.0,
                    manaCost: 40,
                    cooldown: 0,
                    icon: '⚡'
                }
            ],
            rogue: [
                {
                    name: 'Puñalada Rápida',
                    description: 'Ataque rápido de 110% de daño',
                    damage: 1.1,
                    manaCost: 8,
                    cooldown: 0,
                    icon: '🗡️'
                },
                {
                    name: 'Sombras',
                    description: 'Evasión de 60% de daño durante 1 turno',
                    evasion: 0.6,
                    manaCost: 12,
                    cooldown: 0,
                    icon: '🌑'
                },
                {
                    name: 'Asesino Mortal',
                    description: 'Ataque crítico con 300% de daño',
                    damage: 3.0,
                    manaCost: 30,
                    cooldown: 0,
                    icon: '💀'
                }
            ]
        };

        return abilities[characterClass] || abilities.warrior;
    }

    gainExperience(amount) {
        this.experience += amount;
        let leveledUp = false;

        while (this.experience >= this.maxExperience) {
            this.experience -= this.maxExperience;
            this.levelUp();
            leveledUp = true;
        }

        return leveledUp;
    }

    levelUp() {
        this.level++;
        this.maxHealth += 20;
        this.health = this.maxHealth;
        this.maxMana += 10;
        this.mana = this.maxMana;
        this.maxExperience = Math.floor(this.maxExperience * 1.1);
        
        // Aumentar estadísticas
        this.stats.strength += 2;
        this.stats.defense += 1;
        this.stats.intelligence += 2;
        this.stats.speed += 1;
        
        addCombatLog(`¡${this.name} subió al nivel ${this.level}!`, 'levelup');
    }

    takeDamage(damage) {
        const finalDamage = Math.max(1, damage - this.stats.defense);
        this.health = Math.max(0, this.health - finalDamage);
        return finalDamage;
    }

    heal(amount) {
        this.health = Math.min(this.maxHealth, this.health + amount);
    }

    useMana(amount) {
        if (this.mana >= amount) {
            this.mana -= amount;
            return true;
        }
        return false;
    }

    restoreMana(amount) {
        this.mana = Math.min(this.maxMana, this.mana + amount);
    }

    getAttackDamage() {
        const baseDamage = 5 + this.stats.strength;
        const isCritical = Math.random() * 100 < this.stats.criticalChance;
        const weaponBonus = this.equipment.weapon ? this.equipment.weapon.damage : 0;
        
        let finalDamage = (baseDamage + weaponBonus) * (isCritical ? 1.5 : 1);
        finalDamage += Math.random() * 5 - 2; // Variación ±2
        
        return {
            damage: Math.floor(finalDamage),
            isCritical
        };
    }

    addItem(item) {
        this.inventory.push(item);
    }

    removeItem(itemName) {
        this.inventory = this.inventory.filter(item => item.name !== itemName);
    }

    equip(item) {
        if (item.type === 'weapon') {
            if (this.equipment.weapon) {
                this.addItem(this.equipment.weapon);
            }
            this.equipment.weapon = item;
            this.removeItem(item.name);
        } else if (item.type === 'armor') {
            if (this.equipment.armor) {
                this.addItem(this.equipment.armor);
            }
            this.equipment.armor = item;
            this.removeItem(item.name);
        }
    }

    getInventoryByType(type) {
        return this.inventory.filter(item => item.type === type);
    }

    addGold(amount) {
        this.gold += amount;
    }

    completeQuest(questId) {
        if (!this.questsCompleted.includes(questId)) {
            this.questsCompleted.push(questId);
        }
    }

    addAchievement(achievement) {
        if (!this.achievements.includes(achievement)) {
            this.achievements.push(achievement);
        }
    }

    getStats() {
        return {
            nombre: this.name,
            clase: this.characterClass,
            nivel: this.level,
            experiencia: `${this.experience}/${this.maxExperience}`,
            oro: this.gold,
            salud: `${this.health}/${this.maxHealth}`,
            mana: `${this.mana}/${this.maxMana}`,
            fuerza: this.stats.strength,
            defensa: this.stats.defense,
            velocidad: this.stats.speed,
            inteligencia: this.stats.intelligence,
            critico: `${this.stats.criticalChance}%`,
            enemigosDefeados: this.enemiesDefeated,
            danoTotal: this.totalDamageDealt
        };
    }

    isAlive() {
        return this.health > 0;
    }
}
