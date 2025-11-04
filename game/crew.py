"""
Star Trek Game - Crew Officer System
Manages crew officers, stations, skills, and recruitment
"""

import random

# Station definitions and their effects on ship systems
STATIONS = {
    'conn': {
        'name': 'Conn Officer',
        'description': 'Controls navigation and helm',
        'effects': {
            'evasion': 'Increases chance to evade enemy fire in combat',
            'navigation_speed': 'Reduces travel time between systems',
            'initiative': 'Improves turn order in combat'
        },
        'primary_skill': 'tactical'
    },
    'tactical': {
        'name': 'Tactical Officer',
        'description': 'Manages weapons and shields',
        'effects': {
            'weapons_accuracy': 'Increases weapon hit chance and damage',
            'shield_efficiency': 'Improves shield damage absorption',
            'targeting': 'Better targeting of enemy subsystems'
        },
        'primary_skill': 'tactical'
    },
    'engineering': {
        'name': 'Chief Engineer',
        'description': 'Maintains ship systems and power',
        'effects': {
            'repair_rate': 'Faster repair of damaged systems',
            'power_efficiency': 'Better power distribution to systems',
            'warp_speed': 'Increases maximum warp speed',
            'system_reliability': 'Reduces chance of system failures'
        },
        'primary_skill': 'engineering'
    },
    'science': {
        'name': 'Science Officer',
        'description': 'Operates sensors and research',
        'effects': {
            'scanning_range': 'Detects objects at greater distances',
            'anomaly_detection': 'Better chance to find anomalies',
            'analysis_speed': 'Faster analysis of scan data'
        },
        'primary_skill': 'science'
    },
    'medical': {
        'name': 'Chief Medical Officer',
        'description': 'Handles crew health and injuries',
        'effects': {
            'crew_recovery': 'Faster recovery from injuries',
            'medical_efficiency': 'Better treatment outcomes',
            'combat_casualty_reduction': 'Reduces crew casualties in combat'
        },
        'primary_skill': 'science'
    },
    'communications': {
        'name': 'Communications Officer',
        'description': 'Manages subspace communications',
        'effects': {
            'diplomacy_bonus': 'Improves diplomatic interactions',
            'hailing_range': 'Can hail ships from greater distance',
            'translation_accuracy': 'Better first contact translations'
        },
        'primary_skill': 'diplomacy'
    }
}

# Officer ranks (must be below player's rank to recruit)
OFFICER_RANKS = [
    'Ensign',           # 0
    'Lieutenant JG',    # 1
    'Lieutenant',       # 2
    'Lt. Commander',    # 3
    'Commander',        # 4
    'Captain',          # 5
    'Commodore',        # 6
    'Rear Admiral',     # 7
    'Vice Admiral',     # 8
    'Admiral'           # 9
]

# Extensive name lists for each race
NAMES = {
    'Human': {
        'first': [
            # Male names
            'James', 'William', 'Benjamin', 'Christopher', 'Thomas', 'Robert', 'John', 
            'Michael', 'David', 'Richard', 'Joseph', 'Charles', 'Daniel', 'Matthew',
            'Andrew', 'Joshua', 'Kevin', 'Brian', 'George', 'Edward', 'Ronald', 'Anthony',
            'Paul', 'Mark', 'Steven', 'Kenneth', 'Samuel', 'Alexander', 'Patrick', 'Jack',
            'Dennis', 'Jerry', 'Tyler', 'Aaron', 'Henry', 'Douglas', 'Peter', 'Walter',
            'Nathan', 'Zachary', 'Kyle', 'Harold', 'Carl', 'Arthur', 'Lawrence', 'Dylan',
            'Ryan', 'Justin', 'Frank', 'Raymond', 'Gregory', 'Marcus', 'Vincent', 'Eric',
            'Louis', 'Philip', 'Scott', 'Adam', 'Ian', 'Noah', 'Ethan', 'Oliver', 'Lucas',
            'Mason', 'Logan', 'Jacob', 'Isaac', 'Sean', 'Timothy', 'Victor', 'Albert',
            'Leonard', 'Miles', 'Julian', 'Wesley', 'Harry', 'Malcolm', 'Travis', 'Pavel',
            # Female names
            'Kathryn', 'Beverly', 'Christine', 'Nyota', 'Jennifer', 'Elizabeth', 'Sarah', 
            'Jessica', 'Emily', 'Amanda', 'Melissa', 'Michelle', 'Laura', 'Rebecca', 'Sharon',
            'Cynthia', 'Kathleen', 'Amy', 'Angela', 'Rachel', 'Anna', 'Stephanie', 'Nicole',
            'Emma', 'Samantha', 'Lisa', 'Karen', 'Helen', 'Sandra', 'Ashley', 'Kimberly',
            'Donna', 'Carol', 'Ruth', 'Maria', 'Nancy', 'Betty', 'Dorothy', 'Margaret',
            'Linda', 'Barbara', 'Patricia', 'Susan', 'Mary', 'Deborah', 'Grace', 'Victoria',
            'Hannah', 'Sophia', 'Isabella', 'Mia', 'Charlotte', 'Abigail', 'Madison', 'Lily',
            'Natalie', 'Claire', 'Zoe', 'Hoshi', 'Keiko', 'Kasidy', 'Leah', 'Alyssa'
        ],
        'last': [
            'Kirk', 'Picard', 'Sisko', 'Janeway', 'Archer', 'Pike', 'Riker', 'Data',
            'LaForge', 'Crusher', 'Paris', 'Kim', 'Torres', 'Chakotay', 'Tucker', 'Reed',
            'Mayweather', 'Anderson', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
            'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Taylor', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Robinson', 'Walker', 'Young', 'Allen',
            'King', 'Wright', 'Scott', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams',
            'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
            'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins',
            'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Morgan',
            'Peterson', 'Cooper', 'Reed', 'Bailey', 'Bell', 'Coleman', 'Jenkins', 'Perry',
            'Powell', 'Long', 'Patterson', 'Hughes', 'Flores', 'Washington', 'Butler', 'Simmons',
            'Foster', 'Bryant', 'Alexander', 'Russell', 'Griffin', 'Hayes', 'Myers', 'Ford'
        ]
    },
    'Vulcan': {
        'first': [
            # Male names (typically start with S, V, T, or K)
            'Spock', 'Sarek', 'Tuvok', 'Soval', 'Vorik', 'Sybok', 'Solkar', 'Surak',
            'Selek', 'Skon', 'Stron', 'Syrran', 'Mestral', 'Sopek', 'Taurik', 'Tavek',
            'Sevek', 'Velek', 'Tolek', 'Soral', 'Vanik', 'Satok', 'Venok', 'Stark',
            'Talak', 'Suvan', 'Toran', 'Stonn', 'Syrrek', 'Sonak', 'Soval', 'Sevrin',
            'Stasek', 'Suvok', 'Tarek', 'Torak', 'Varen', 'Velar', 'Vektan', 'Voris',
            'Kolos', 'Kovan', 'Sorel', 'Sevel', 'Tekav', 'Tobin', 'Vekh', 'Saren',
            'Solok', 'Stelok', 'Sutok', 'Teval', 'Tolek', 'Volis', 'Koss', 'Sopak',
            # Female names (typically T', some S)
            'T\'Pol', 'T\'Pau', 'Saavik', 'T\'Pring', 'Valeris', 'T\'Pel', 'T\'Lar',
            'T\'Plana', 'T\'Les', 'T\'Mir', 'T\'Vran', 'T\'Paal', 'T\'Kara', 'T\'Lani',
            'T\'Sara', 'T\'Rell', 'T\'Vora', 'T\'Meni', 'T\'Pran', 'T\'Pren', 'T\'Pel',
            'T\'Ria', 'T\'Sai', 'T\'Sora', 'T\'Vral', 'T\'Rea', 'T\'Nara', 'T\'Lara',
            'T\'Kala', 'T\'Shanik', 'T\'Pana', 'T\'Pela', 'T\'Seva', 'Sakonna', 'Sarda',
            'Selok', 'Simona', 'Soval', 'T\'Ara', 'T\'Elas', 'T\'Jana', 'T\'Rama'
        ],
        'last': [
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            'of Vulcan', 'of ShiKahr', 'of Gol', 'of T\'Paal', 'of Vulcana Regar',
            'of Kir', 'of Raal', 'of T\'Khasi', 'of Shi\'al', 'of Vulcan', 'of ShiKahr'
        ]
    },
    'Andorian': {
        'first': [
            # Thaan (male) names - often start with Th, Sh, Kh
            'Shran', 'Thy\'lek', 'Shras', 'Keval', 'Thelin', 'Thoris', 'Shantherin',
            'Thelev', 'Thelin', 'Shravek', 'Tharvik', 'Thy\'ren', 'Thorak', 'Shavok',
            'Theren', 'Shrale', 'Thy\'kir', 'Thoris', 'Shavan', 'Thalos', 'Thrix',
            'Shralek', 'Thy\'lan', 'Thorin', 'Shalen', 'Thy\'rok', 'Shenik', 'Thy\'var',
            'Shoran', 'Thalak', 'Shreva', 'Theras', 'Shavey', 'Keth', 'Kelev', 'Kheras',
            'Thralen', 'Shevek', 'Thy\'kor', 'Thalys', 'Shrev', 'Khavek', 'Theran',
            # Shen (female) names - often start with T, Sh, Th
            'Talas', 'Talla', 'Tarah', 'Thelara', 'Talath', 'Talesh', 'Tareen', 'Talvir',
            'Thara', 'Thessa', 'Sheva', 'Shreva', 'Tavin', 'Telas', 'Thrass', 'Tarial',
            'Shara', 'Thira', 'Teval', 'Sharal', 'Thelys', 'Tavanna', 'Shiral', 'Thelis',
            'Talera', 'Shavra', 'Thyra', 'Tarella', 'Shelana', 'Thessa', 'Tavris', 'Shalen',
            # Chaan and Zhen names (mixed)
            'Charivretha', 'Chiara', 'Vretha', 'Zhavey', 'Zharath', 'Zhera', 'Cherev',
            'Charal', 'Vrax', 'Zhenara', 'Chevek', 'Chreva', 'Zhiren', 'Velar', 'Zhenka'
        ],
        'last': [
            # th- prefix = thaan (male), ch- = chaan (male), sh- = shen (female), zh- = zhen (female)
            'th\'Thane', 'ch\'Thane', 'sh\'Thane', 'zh\'Thane', 'th\'Raan', 'ch\'Raan',
            'sh\'Raan', 'zh\'Raan', 'th\'Kren', 'ch\'Kren', 'sh\'Kren', 'zh\'Kren',
            'th\'Velik', 'ch\'Velik', 'sh\'Velik', 'zh\'Velik', 'th\'Kor', 'ch\'Kor',
            'sh\'Kor', 'zh\'Kor', 'th\'Raav', 'ch\'Raav', 'sh\'Raav', 'zh\'Raav',
            'th\'Eneg', 'ch\'Eneg', 'sh\'Eneg', 'zh\'Eneg', 'th\'Lesinas', 'ch\'Lesinas',
            'sh\'Lesinas', 'zh\'Lesinas', 'th\'Vrenek', 'ch\'Vrenek', 'sh\'Vrenek', 'zh\'Vrenek',
            'th\'Talak', 'ch\'Talak', 'sh\'Talak', 'zh\'Talak', 'th\'Shraan', 'ch\'Shraan',
            'sh\'Shraan', 'zh\'Shraan', 'th\'Garev', 'ch\'Garev', 'sh\'Garev', 'zh\'Garev',
            'th\'Dhael', 'ch\'Dhael', 'sh\'Dhael', 'zh\'Dhael', 'th\'Yash', 'ch\'Yash'
        ]
    },
    'Tellarite': {
        'first': [
            # Male names - gruff, consonant-heavy (Gr, Br, Kr, Dr, Sk sounds)
            'Gral', 'Gav', 'Brag', 'Naarg', 'Skalaar', 'Terev', 'Grek', 'Brok',
            'Krog', 'Doran', 'Bralek', 'Navik', 'Skal', 'Terav', 'Grenn', 'Brolak',
            'Krogan', 'Dornak', 'Gorak', 'Brakk', 'Navok', 'Terix', 'Brogar', 'Krovek',
            'Dorax', 'Gorath', 'Braxus', 'Navrek', 'Skallix', 'Terok', 'Grelak', 'Brovek',
            'Krodak', 'Dorvan', 'Gorvik', 'Bravik', 'Navix', 'Grath', 'Braxan', 'Krevok',
            'Dronak', 'Skorvik', 'Trevok', 'Grenvik', 'Bralak', 'Krovik', 'Gravik', 'Brevan',
            'Skoral', 'Drevak', 'Grovak', 'Brogal', 'Kravok', 'Skeltar', 'Trevik', 'Gorvek',
            # Female names - slightly softer but still gruff
            'Gora', 'Brava', 'Krana', 'Drala', 'Skalla', 'Grenna', 'Breva', 'Krevna',
            'Dorla', 'Gorva', 'Brana', 'Krava', 'Skora', 'Greva', 'Bralla', 'Krella',
            'Drova', 'Gorna', 'Briska', 'Krovla', 'Skorna', 'Grelda', 'Brelka', 'Krenka',
            'Drovka', 'Gorina', 'Braska', 'Krovara', 'Skelna', 'Grevla', 'Bronka', 'Kravis'
        ],
        'last': [
            'Thag', 'Grek', 'Brok', 'Kron', 'Drev', 'Skon', 'Vran', 'Thok', 'Grav',
            'Brax', 'Krov', 'Drok', 'Sval', 'Vrek', 'Thal', 'Gron', 'Bral', 'Kral',
            'Dral', 'Skal', 'Vral', 'Thex', 'Grax', 'Brex', 'Krax', 'Drax', 'Svax',
            'Vrax', 'Thol', 'Grol', 'Brol', 'Krol', 'Drol', 'Svol', 'Vrol', 'Thrak',
            'Grak', 'Brek', 'Krek', 'Drek', 'Skol', 'Vrok', 'Threv', 'Grev', 'Brev',
            'Krev', 'Skar', 'Trog', 'Gror', 'Bror', 'Kror', 'Dror', 'Skor', 'Vrag'
        ]
    },
    'Betazoid': {
        'first': [
            # Male names - elegant, flowing (often ending in -n, -s, -l)
            'Lon', 'Tam', 'Ves', 'Maques', 'Reginod', 'Varel', 'Wyatt', 'Xelo',
            'Zan', 'Aras', 'Belar', 'Danan', 'Faras', 'Jarel', 'Laren', 'Nexar',
            'Rexan', 'Toran', 'Vexor', 'Xylon', 'Ardan', 'Coran', 'Delan', 'Eran',
            'Felan', 'Goran', 'Ixar', 'Keral', 'Lexan', 'Moran', 'Nelan', 'Paron',
            'Quoran', 'Reval', 'Sevan', 'Telan', 'Uvar', 'Velan', 'Xoran', 'Yeran',
            'Zaran', 'Axel', 'Beryn', 'Calen', 'Daren', 'Evran', 'Faron', 'Galen',
            # Female names - graceful, elegant (often -a, -na, -ra endings)
            'Deanna', 'Lwaxana', 'Kestra', 'Nerys', 'Sarna', 'Tarella', 'Cyra',
            'Elara', 'Gella', 'Hana', 'Iara', 'Kara', 'Mira', 'Nara', 'Orah',
            'Pella', 'Rena', 'Sela', 'Tara', 'Ula', 'Vara', 'Wella', 'Xara',
            'Yara', 'Zena', 'Alana', 'Berina', 'Calara', 'Denna', 'Elina', 'Farana',
            'Galena', 'Ilana', 'Jelara', 'Kalara', 'Liana', 'Mirana', 'Nalara', 'Orala',
            'Pelara', 'Reyana', 'Selena', 'Talana', 'Ulara', 'Velara', 'Xelara', 'Yvanna',
            'Zarena', 'Ariana', 'Belana', 'Celara', 'Delana', 'Evanna', 'Falara', 'Girana'
        ],
        'last': [
            'Troi', 'Xavier', 'Dumont', 'Kell', 'Elbrun', 'Grax', 'Enaren', 'Hagan',
            'Inzar', 'Jaren', 'Kolm', 'Laxon', 'Moran', 'Nexar', 'Olan', 'Prax',
            'Quinor', 'Rexan', 'Stron', 'Toran', 'Ulran', 'Vexor', 'Wexar', 'Xylon',
            'Yoran', 'Zelak', 'Ardan', 'Bexon', 'Coran', 'Delan', 'Eran', 'Felan',
            'Goran', 'Ixan', 'Jelan', 'Keran', 'Lexon', 'Meran', 'Nevan', 'Oxar',
            'Pelan', 'Rexar', 'Selan', 'Tevan', 'Uxar', 'Veran', 'Xelan', 'Yevan',
            'Zoran', 'Axar', 'Bevan', 'Celan', 'Devar', 'Exor', 'Fevar', 'Gelan'
        ]
    },
    'Trill': {
        'first': [
            # Male names - varied, often two syllables
            'Curzon', 'Torias', 'Tobin', 'Joran', 'Verad', 'Timor', 'Yedrin', 'Selin',
            'Arjin', 'Bejal', 'Hanor', 'Keren', 'Paron', 'Varel', 'Zharys', 'Coris',
            'Emon', 'Gorus', 'Novar', 'Talur', 'Vered', 'Zaren', 'Belar', 'Daran',
            'Felen', 'Goran', 'Jonan', 'Koral', 'Liran', 'Moran', 'Neral', 'Odan',
            'Reval', 'Soran', 'Toran', 'Varen', 'Zeral', 'Aldren', 'Beren', 'Coran',
            'Dorin', 'Eran', 'Faren', 'Galen', 'Horin', 'Jalen', 'Kalan', 'Lorin',
            # Female names - elegant, often ending in -a or -i
            'Jadzia', 'Ezri', 'Audrid', 'Emony', 'Lela', 'Lenara', 'Renhol', 'Nilani',
            'Neema', 'Reeza', 'Azlyn', 'Ilona', 'Kareel', 'Liryn', 'Rionoj', 'Alara',
            'Brina', 'Cera', 'Delia', 'Erela', 'Falia', 'Gina', 'Ilani', 'Jessa',
            'Kera', 'Liora', 'Melia', 'Nora', 'Orela', 'Pelia', 'Rina', 'Sela',
            'Tela', 'Urela', 'Vina', 'Wila', 'Xara', 'Yela', 'Zara', 'Alina',
            'Belina', 'Celara', 'Delora', 'Elina', 'Felara', 'Galia', 'Irela', 'Jolara'
        ],
        'last': [
            'Dax', 'Tigan', 'Kahn', 'Otner', 'Ral', 'Pahl', 'Belar', 'Soran', 'Vok',
            'Lon', 'Tem', 'Gan', 'Ryx', 'Tor', 'Vel', 'Wen', 'Xan', 'Yor', 'Zek',
            'Arax', 'Bren', 'Cyl', 'Dren', 'Elos', 'Fax', 'Gren', 'Hox', 'Ilon',
            'Jex', 'Kyl', 'Lex', 'Myx', 'Nox', 'Pex', 'Rex', 'Syx', 'Tox', 'Vex',
            'Wex', 'Yex', 'Zex', 'Alar', 'Bex', 'Cax', 'Dor', 'Elax', 'Fren',
            'Gax', 'Hax', 'Ivar', 'Jor', 'Kax', 'Lan', 'Max', 'Nar', 'Ox'
        ]
    },
    'Bajoran': {
        'first': [
            # Male names - varied, spiritual feel
            'Bareil', 'Antos', 'Shakaar', 'Edon', 'Jaro', 'Essa', 'Lenaris', 'Holem',
            'Furel', 'Tahna', 'Los', 'Vedek', 'Yarka', 'Taluno', 'Falor', 'Bek',
            'Mora', 'Pol', 'Mullibok', 'Vaatrik', 'Ishan', 'Anjar', 'Biran', 'Yevir',
            'Akorem', 'Kelar', 'Menos', 'Prylar', 'Reon', 'Telna', 'Varis', 'Yarim',
            'Asarem', 'Belar', 'Darrah', 'Elias', 'Fransu', 'Ghemor', 'Hotek', 'Jakin',
            'Kelan', 'Lonar', 'Makar', 'Neela', 'Ornak', 'Proka', 'Rakal', 'Solis',
            # Female names - spiritual, elegant
            'Nerys', 'Laren', 'Adami', 'Sulan', 'Nalas', 'Lupaza', 'Ziyal', 'Leeta',
            'Onara', 'Keeve', 'Tora', 'Opaka', 'Winn', 'Kira', 'Lenara', 'Sito',
            'Jaxa', 'Portal', 'Yevala', 'Asarem', 'Bellis', 'Charna', 'Deela', 'Erlin',
            'Fasil', 'Gantt', 'Hava', 'Iliana', 'Jillur', 'Kalisi', 'Latha', 'Meral',
            'Natima', 'Opel', 'Pallra', 'Rinara', 'Sarish', 'Talis', 'Ulani', 'Vana',
            'Weld', 'Yanas', 'Zayra', 'Aluura', 'Belar', 'Cerin', 'Desta', 'Elendra'
        ],
        'last': [
            # Family names (used first in Bajoran naming: "Kira Nerys" = family Kira, given name Nerys)
            'Kira', 'Ro', 'Bareil', 'Winn', 'Opaka', 'Li', 'Shakaar', 'Jaro', 'Lenaris',
            'Furel', 'Tahna', 'Keeve', 'Falor', 'Tora', 'Prylar', 'Mora', 'Vaatrik',
            'Ishan', 'Anjar', 'Biran', 'Yevir', 'Lupaza', 'Onara', 'Taluno', 'Ghemor',
            'Lenara', 'Prenor', 'Rusot', 'Sito', 'Jaxa', 'Menos', 'Portal', 'Reon',
            'Akorem', 'Asarem', 'Belar', 'Darrah', 'Elias', 'Fransu', 'Hotek', 'Jakin',
            'Kelan', 'Lonar', 'Makar', 'Neela', 'Ornak', 'Proka', 'Rakal', 'Solis',
            'Telna', 'Varis', 'Yarim', 'Bellis', 'Charna', 'Deela', 'Erlin', 'Fasil'
        ]
    },
    'Caitian': {
        'first': [
            # Male names - strong, with apostrophes (M', R', S', T', K')
            'M\'Raaw', 'M\'Rell', 'R\'Mor', 'S\'Byrl', 'M\'Rahn', 'R\'Vann', 'S\'Tarr',
            'M\'Kora', 'R\'Leth', 'S\'Varl', 'R\'Vek', 'S\'Keth', 'R\'Pax', 'M\'Vexa',
            'R\'Kan', 'S\'Mara', 'R\'Tesh', 'M\'Reth', 'R\'Nex', 'S\'Kor', 'M\'Keth',
            'R\'Sek', 'S\'Vek', 'M\'Varr', 'R\'Kess', 'S\'Rax', 'T\'Kar', 'T\'Rell',
            'K\'Rar', 'K\'Vex', 'M\'Torr', 'R\'Ghan', 'S\'Kral', 'T\'Shar', 'K\'Rath',
            'M\'Jarr', 'R\'Thak', 'S\'Varn', 'T\'Lok', 'K\'Shar', 'M\'Rakar', 'R\'Shaav',
            # Female names - graceful, feline (M', R', S', T', K', L')
            'M\'Ress', 'S\'Ressa', 'T\'Mara', 'M\'Erah', 'M\'Tara', 'S\'Lara', 'M\'Vexa',
            'R\'Sora', 'S\'Nara', 'M\'Tess', 'S\'Vera', 'M\'Sora', 'R\'Lara', 'S\'Kira',
            'M\'Pera', 'S\'Tora', 'M\'Rexa', 'R\'Essa', 'S\'Lyra', 'M\'Lessa', 'R\'Mira',
            'S\'Kessa', 'T\'Lara', 'T\'Resa', 'K\'Lara', 'L\'Ress', 'L\'Mara', 'M\'Yara',
            'R\'Vala', 'S\'Tera', 'T\'Nara', 'K\'Sera', 'L\'Vara', 'M\'Lira', 'R\'Kira',
            'S\'Mera', 'T\'Vara', 'K\'Lessa', 'L\'Tara', 'M\'Shara', 'R\'Thera', 'S\'Lyssa'
        ],
        'last': [
            'R\'Mora', 'S\'Taal', 'M\'Kora', 'R\'Vek', 'S\'Leth', 'M\'Raan', 'R\'Kess',
            'S\'Vara', 'M\'Tess', 'R\'Pax', 'S\'Kor', 'M\'Vara', 'R\'Sek', 'S\'Rax',
            'M\'Keth', 'R\'Tora', 'S\'Vek', 'M\'Reth', 'R\'Vara', 'S\'Kora', 'M\'Sek',
            'R\'Leth', 'S\'Mek', 'M\'Tora', 'R\'Kora', 'S\'Reth', 'M\'Vek', 'R\'Sora',
            'T\'Kal', 'T\'Rek', 'K\'Ral', 'K\'Shor', 'L\'Rek', 'L\'Mor', 'M\'Shar',
            'R\'Thak', 'S\'Kral', 'T\'Vex', 'K\'Ress', 'L\'Tess', 'M\'Jarr', 'R\'Shaav',
            'S\'Varr', 'T\'Lok', 'K\'Thera', 'L\'Mara', 'M\'Lyra', 'R\'Shara', 'S\'Lira'
        ]
    },
    'Klingon': {
        'first': [
            # Male names - harsh, warrior-like (K, G, M, Q sounds)
            'Worf', 'Kurn', 'Martok', 'Gowron', 'Duras', 'Klag', 'Kol', 'Kor',
            'Koloth', 'Kang', 'Kruge', 'Chang', 'Gorkon', 'Kahless', 'Mogh', 'Ja\'rod',
            'Toral', 'Alexander', 'K\'mpec', 'Qua\'lon', 'Drex', 'Kaga', 'Kargan',
            'Nu\'Daq', 'Kopek', 'Korax', 'Maltz', 'Koth', 'Rodek', 'Klaa', 'Vagh',
            'Koral', 'Korath', 'Kohlar', 'Krell', 'Krugar', 'Kromag', 'Kurn', 'Kras',
            'Koltar', 'Kurn', 'Kornan', 'Krevek', 'Grelak', 'Garak', 'Goroth', 'Grevak',
            'Magh', 'Morak', 'Mokar', 'Morglar', 'Qagh', 'Quvak', 'Qolka', 'Qargh',
            'Torak', 'Torghn', 'Targak', 'Tavek', 'Valkris', 'Vorok', 'Valkris', 'Vekh',
            # Female names - strong but slightly softer
            'K\'Ehleyr', 'B\'Elanna', 'Lursa', 'B\'Etor', 'Grilka', 'Sirella', 'Mara',
            'Valkris', 'Kurak', 'Azetbur', 'Kora', 'Korva', 'Krana', 'Kevara', 'Kathra',
            'Grava', 'Grella', 'Gorana', 'Miral', 'Morina', 'Mevara', 'Qarna', 'Qelara',
            'Toral', 'Tovara', 'Tarkana', 'Vala', 'Vorna', 'Vrella', 'Lessa', 'Lorna'
        ],
        'last': [
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            'of House Mogh', 'of House Martok', 'of House Duras', 'of House Kor',
            'of House K\'mpec', 'of House Grilka', 'of House Noggra', 'of House Konjah',
            'of House D\'Ghor', 'of House Kozak', 'of House Quark', 'of House Palkar',
            'of House Grilka', 'of House Gorkon', 'of House Kang', 'of House Koloth',
            'of House Kruge', 'of House Chang', 'of House Kahless', 'of House Kor',
            'of House Torg', 'of House Kresh', 'of House Magh', 'of House Varnak'
        ]
    },
    'Bolian': {
        'first': [
            # Male names - melodic, often B, M, R, L sounds
            'Mot', 'Boq\'ta', 'Rixx', 'Brex', 'Bril', 'Borus', 'Borath', 'Belak',
            'Bokar', 'Bravik', 'Belar', 'Bralak', 'Morax', 'Movar', 'Mevek', 'Miral',
            'Marex', 'Morek', 'Belak', 'Rivik', 'Rovar', 'Ravik', 'Relak', 'Reval',
            'Lovik', 'Lavik', 'Levik', 'Lorak', 'Bevan', 'Borak', 'Breval', 'Mevak',
            'Rovik', 'Ralak', 'Lekan', 'Borin', 'Mavik', 'Revar', 'Lorin', 'Berak',
            # Female names - flowing, elegant
            'Lysia', 'Bolka', 'Mitra', 'Riala', 'Brila', 'Belara', 'Morina', 'Larana',
            'Rivka', 'Belina', 'Mirala', 'Borana', 'Levara', 'Ralina', 'Bevala', 'Mevara',
            'Rolara', 'Liara', 'Berina', 'Morvala', 'Rivala', 'Belara', 'Lorana', 'Mirana',
            'Bevina', 'Ralara', 'Levina', 'Borina', 'Mirela', 'Rolina', 'Livara', 'Belira'
        ],
        'last': [
            'Mot', 'Brex', 'Rixx', 'Borath', 'Belak', 'Movar', 'Rivik', 'Lovik',
            'Bevan', 'Mavik', 'Rovik', 'Lekan', 'Borin', 'Lysia', 'Bolka', 'Mitra',
            'Riala', 'Brila', 'Belara', 'Morina', 'Larana', 'Rivka', 'Belina', 'Mirala',
            'Borana', 'Levara', 'Ralina', 'Bevala', 'Mevara', 'Rolara', 'Liara', 'Berina',
            'Morvala', 'Rivala', 'Lorana', 'Mirana', 'Bevina', 'Ralara', 'Levina', 'Borina'
        ]
    }
}



class Officer:
    """Represents a crew officer"""
    
    def __init__(self, species, rank_level, station=None):
        self.species = species
        self.rank_level = rank_level
        self.rank = OFFICER_RANKS[rank_level]
        self.station = station
        
        # Generate name
        self.name = self._generate_name()
        
        # Generate skills (based on rank and species bonuses)
        self.skills = self._generate_skills()
        
        # Calculate reputation cost (based on rank and total skills)
        self.reputation_cost = self._calculate_cost()
        
    def _generate_name(self):
        """Generate a random name for the officer"""
        first = random.choice(NAMES[self.species]['first'])
        last = random.choice(NAMES[self.species]['last'])
        
        if last:
            return f"{first} {last}"
        return first
    
    def _generate_skills(self):
        """Generate skills based on rank level"""
        # Base skill range increases with rank
        base = 30 + (self.rank_level * 7)  # Ensign: 30-40, Admiral: 93-103
        variance = 10
        
        skills = {
            'command': random.randint(base, base + variance),
            'tactical': random.randint(base, base + variance),
            'science': random.randint(base, base + variance),
            'engineering': random.randint(base, base + variance),
            'diplomacy': random.randint(base, base + variance)
        }
        
        # Apply species bonuses from character.py
        species_bonuses = {
            'Human': {'command': 5, 'diplomacy': 5},
            'Vulcan': {'science': 10, 'diplomacy': 5},
            'Andorian': {'tactical': 10, 'command': 5},
            'Tellarite': {'engineering': 10, 'diplomacy': -5},
            'Betazoid': {'diplomacy': 15, 'science': 5},
            'Trill': {'science': 5, 'command': 5, 'diplomacy': 5},
            'Bajoran': {'diplomacy': 5, 'science': 5},
            'Caitian': {'tactical': 10, 'science': 5},
            'Klingon': {'tactical': 15, 'command': 5, 'diplomacy': -10}
        }
        
        if self.species in species_bonuses:
            for skill, bonus in species_bonuses[self.species].items():
                skills[skill] = max(0, skills[skill] + bonus)
        
        return skills
    
    def _calculate_cost(self):
        """Calculate reputation cost to recruit this officer"""
        # Base cost by rank
        base_costs = [50, 100, 200, 350, 550, 800, 1100, 1450, 1850, 2300]
        base = base_costs[self.rank_level]
        
        # Add bonus for high total skills
        total_skills = sum(self.skills.values())
        avg_skill = total_skills / len(self.skills)
        skill_bonus = int((avg_skill - 30) * 5)  # Each point above 30 adds 5 rep
        
        return base + skill_bonus
    
    def get_station_bonus(self):
        """Calculate the bonus this officer provides to their station"""
        if not self.station:
            return 0
        
        # Use primary skill for the station
        primary_skill = STATIONS[self.station]['primary_skill']
        skill_value = self.skills.get(primary_skill, 0)
        
        # Convert skill to percentage bonus (skill 50 = 10% bonus, skill 100 = 20% bonus)
        bonus = (skill_value - 30) / 5
        return max(0, bonus)
    
    def get_info(self):
        """Get formatted information about this officer"""
        info = {
            'name': self.name,
            'species': self.species,
            'rank': self.rank,
            'rank_level': self.rank_level,
            'station': self.station,
            'skills': self.skills.copy(),
            'reputation_cost': self.reputation_cost,
            'station_bonus': self.get_station_bonus() if self.station else 0
        }
        return info
    
    def to_dict(self):
        """Convert officer to dictionary for saving"""
        return {
            'name': self.name,
            'species': self.species,
            'rank_level': self.rank_level,
            'station': self.station,
            'skills': self.skills,
            'reputation_cost': self.reputation_cost
        }
    
    @staticmethod
    def from_dict(data):
        """Create officer from dictionary"""
        officer = Officer.__new__(Officer)
        officer.name = data['name']
        officer.species = data['species']
        officer.rank_level = data['rank_level']
        officer.rank = OFFICER_RANKS[data['rank_level']]
        officer.station = data.get('station')
        officer.skills = data['skills']
        officer.reputation_cost = data['reputation_cost']
        return officer


def get_available_species():
    """Get list of species available for crew recruitment"""
    return list(NAMES.keys())


def get_station_list():
    """Get list of available stations"""
    return list(STATIONS.keys())


def get_station_info(station):
    """Get information about a specific station"""
    return STATIONS.get(station, {})

