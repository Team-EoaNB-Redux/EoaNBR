NDefines.NGame.START_DATE = "1857.5.10.24" -- "1936.1.1.12"
NDefines.NGame.END_DATE = "2100.1.1.1" -- "1949.1.1.1"
NDefines.NGame.MAX_SCRIPTED_LOC_RECURSION = 60 -- 30
NDefines.NGame.HANDS_OFF_START_TAG = "UCT" --URG

NDefines.NDiplomacy.MAX_TRUST_VALUE = 80 -- 100
NDefines.NDiplomacy.MIN_TRUST_VALUE = -80 -- -100
NDefines.NDiplomacy.MAX_OPINION_VALUE = 200 -- 100
NDefines.NDiplomacy.MIN_OPINION_VALUE = -200 -- -100
NDefines.NDiplomacy.BASE_TRUCE_PERIOD = 30 -- 180
NDefines.NDiplomacy.PEACE_INCREASE_COST_FACTOR_PER_MISSING_PERCENT_FOR_CAPITULATION = 0.01 -- 0.002
NDefines.NDiplomacy.INFLUENCE_RATIO_CAPITAL = 0.3 -- 0.2
NDefines.NDiplomacy.INFLUENCE_RATIO_CONTROLLED = 0.4 -- 0.5
NDefines.NDiplomacy.TENSION_TIME_SCALE_START_DATE = "1857.5.10.24" -- "1936.1.1.12"
-- NDefines.NDiplomacy.INFLUENCE_REDUCTION_PER_CAPITAL_DIST = 0.05 -- depreciated 1.12.5
-- NDefines.NDiplomacy.INFLUENCE_REDUCTION_PER_CORE_DIST = 0.05 -- depreciated 1.12.5
-- NDefines.NDiplomacy.INFLUENCE_REDUCTION_PER_CONTROLLED_DIST = 0.10 -- depreciated 1.12.5
-- NDefines.NDiplomacy.INFLUENCE_MAX_DISCOUNT = 0.25  -- depreciated 1.12.5
NDefines.NDiplomacy.BASE_IMPROVE_RELATION_COST = 20 -- 10
NDefines.NDiplomacy.BASE_IMPROVE_RELATION_SAME_IDEOLOGY_GROUP_MAINTAIN_COST = 0.15 -- 0.20
NDefines.NDiplomacy.BASE_IMPROVE_RELATION_DIFFERENT_IDEOLOGY_GROUP_MAINTAIN_COST = 0.3 --0.4
NDefines.NDiplomacy.PEACE_SCORE_SCALE_FACTOR = 1.25 -- 1.35

NDefines.NCountry.BASE_RESEARCH_SLOTS = 1
NDefines.NCountry.POPULATION_YEARLY_GROWTH_BASE = 0.010
NDefines.NCountry.STATE_VALUE_MANPOWER_FACTOR = 0.15 --0.1
NDefines.NCountry.AIR_SUPPLY_CONVERSION_SCALE = 0.001 -- 0.002

NDefines.NCountry.MAJOR_MIN_FACTORIES = 100000						-- need at least these many factories to become a major --35

NDefines.NCountry.STARTING_FUEL_RATIO = 0.1						-- starting fuel ratio compared to max fuel for countries --.5
NDefines.NCountry.BASE_FUEL_GAIN_PER_OIL = 0.25						-- base amount of fuel gained hourly per excess oil --2
NDefines.NCountry.BASE_FUEL_GAIN = 1.0						-- base amount of fuel gained hourly, independent of excess oil --2
NDefines.NCountry.BASE_FUEL_CAPACITY = 500						-- base amount of fuel capacity --50k

NDefines.NProduction.MAX_EQUIPMENT_RESOURCES_NEED = 6 	-- Max number of different strategic resources an equipment can be dependent on. --3
NDefines.NProduction.BASE_FACTORY_SPEED_MIL = 2				-- vanilla 5 Base factory speed multiplier (how much hoi3 style IC each factory gives). --4.5
NDefines.NProduction.BASE_FACTORY_SPEED_MIL = 4       -- vanilla 4.5
NDefines.NProduction.BASE_FACTORY_SPEED_NAV = 3      -- vanilla 2.5
NDefines.NProduction.ANNEX_FUEL_RATIO = 0.5	-- How much fuel will be transferred on annexation
NDefines.NProduction.MIN_POSSIBLE_TRAINING_MANPOWER = 5000	-- How many deployment lines minimum can be training --100k
NDefines.NProduction.CAPITULATE_FUEL_RATIO = 0.25 -- How much fuel will be transferred on capitulation --.5
NDefines.NProduction.PRODUCTION_RESOURCE_LACK_PENALTY = -0.4			-- Penalty decrease while lack of resource per factory --0.05

NDefines.NTechnology.BASE_TECH_COST = 2000 -- 100
NDefines.NTechnology.MIN_RESEARCH_SPEED = 0.2						-- research speed can't go below this value

NDefines.NPolitics.BASE_POLITICAL_POWER_INCREASE = 1.0

NDefines.NBuildings.MAX_SHARED_SLOTS = 81 -- 25

NDefines.NMilitary.WAR_SCORE_PROVINCE_FACTOR = 0.3 -- 2.0
NDefines.NMilitary.WAR_SCORE_LEND_LEASE_GIVEN_IC_FACTOR = 0.1 -- 0.001
NDefines.NMilitary.WAR_SCORE_LEND_LEASE_GIVEN_FUEL_FACTOR = 0.01 -- 0.001
NDefines.NMilitary.WAR_SCORE_LEND_LEASE_RECEIVED_IC_FACTOR = 0.1 -- 0.001
NDefines.NMilitary.WAR_SCORE_LEND_LEASE_RECEIVED_FUEL_FACTOR = 0.01 -- 0.001
NDefines.NMilitary.PARACHUTE_COMPLETE_ORG = 0.1 -- 0.4

NDefines.NMilitary.HOURLY_ORG_MOVEMENT_IMPACT = -0.1		-- how much org is lost every hour while moving an army. --.2
NDefines.NMilitary.ENGAGEMENT_WIDTH_PER_WIDTH = 5.0	-- how much enemy combat width we are allowed to engage per width of our own --2
NDefines.NMilitary.INFRASTRUCTURE_MOVEMENT_SPEED_IMPACT = -0.025	-- speed penalty per infrastucture below maximum. ---0.05
NDefines.NMilitary.DIVISION_SIZE_FOR_XP = 4                 -- how many battalions should a division have to count as a full divisions when calculating XP stuff
NDefines.NMilitary.MAX_ARMY_EXPERIENCE = 2500			--Max army experience a country can store
NDefines.NMilitary.MAX_NAVY_EXPERIENCE = 2500			--Max navy experience a country can store
NDefines.NMilitary.MAX_AIR_EXPERIENCE = 2500				--Max air experience a country can store
NDefines.NMilitary.TRAINING_MAX_LEVEL = 10
NDefines.NMilitary.DEPLOY_TRAINING_MAX_LEVEL = 5
NDefines.NMilitary.TRAINING_EXPERIENCE_SCALE = 62.0
NDefines.NMilitary.TRAINING_ORG = 0.2
NDefines.NMilitary.ARMY_EXP_BASE_LEVEL = 5
NDefines.NMilitary.UNIT_EXP_LEVELS = { 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.425, 0.55, 0.675, 0.75, 0.775, 0.8, 0.825, 0.85, 0.9, 0.95, 0.99 }		-- Experience needed to progress to the next level
NDefines.NMilitary.FIELD_EXPERIENCE_SCALE = 0.002
NDefines.NMilitary.FIELD_EXPERIENCE_MAX_PER_DAY = 3				-- Most xp you can gain per day
NDefines.NMilitary.EXPEDITIONARY_FIELD_EXPERIENCE_SCALE = 0.5		-- reduction factor in Xp from expeditionary forces
NDefines.NMilitary.LEND_LEASE_FIELD_EXPERIENCE_SCALE = 0.005		-- Experience scale for lend leased equipment used in combat.
NDefines.NMilitary.EXPERIENCE_COMBAT_FACTOR = 0.05
NDefines.NMilitary.LOW_ORG_FOR_ATTACK = 0.5                    -- at what org % we start affecting speed when doign hostile moves. scales down ZERO_ORG_MOVEMENT_MODIFIER
NDefines.NMilitary.MIN_DIVISION_DEPLOYMENT_TRAINING = 0.05			-- Min level of division training
NDefines.NMilitary.BORDER_WAR_WIN_DAYS_AGAINST_EMPTY_OPPONENTS = 30		-- border wars will be automatically won if no opponent shows up for this duration

NDefines.NAir.TOP_SPEED_DAMAGE_BONUS_FACTOR = 0.02 -- 0.025
NDefines.NAir.COMBAT_BETTER_SPEED_DAMAGE_INCREASE = 0.45 -- 0.60
NDefines.NAir.COMBAT_DAMAGE_SCALE = 0.25 -- 1.0
NDefines.NAir.COMBAT_DAMAGE_SCALE_CARRIER = 1 -- 5.0
NDefines.NAir.NAVAL_STRIKE_DAMAGE_TO_STR = 2.0 -- 1.0
NDefines.NAir.NAVAL_STRIKE_DAMAGE_TO_ORG = 2.5 -- 1.5
NDefines.NAir.THRUST_WEIGHT_SPEED_FACTOR = 6 -- 3

NDefines.NNavy.WAR_SCORE_GAIN_FOR_SUNK_SHIP_MANPOWER_FACTOR = 0.02 -- 0.001
NDefines.NNavy.WAR_SCORE_GAIN_FOR_SUNK_SHIP_PRODUCTION_COST_FACTOR = 0.04 -- 0.004
NDefines.NNavy.WAR_SCORE_GAIN_FOR_SUNK_CONVOY = 10.0 -- 0.05
NDefines.NNavy.WAR_SCORE_DECAY_FOR_BUILT_CONVOY = 5.0 -- 0.03
NDefines.NNavy.SHIP_TO_FLEET_ANTI_AIR_RATIO = 0.2 -- 0.25
NDefines.NNavy.ANTI_AIR_POW_ON_INCOMING_AIR_DAMAGE = 0.2 -- 0.25
NDefines.NNavy.ANTI_AIR_MULT_ON_INCOMING_AIR_DAMAGE = 0.15 -- 0.2
NDefines.NNavy.HIT_PROFILE_MULT = 50.0 -- 100
NDefines.NNavy.HIT_PROFILE_SPEED_FACTOR = 0.5 -- 2
NDefines.NNavy.OUT_OF_FUEL_SPEED_FACTOR = -0.95
NDefines.NNavy.OUT_OF_FUEL_RANGE_FACTOR = -0.95
NDefines.NNavy.SUPREMACY_PER_SHIP_PER_MANPOWER = 0.5							-- supremacy of a ship is calculated using its IC, manpower and a base define
NDefines.NNavy.SUPREMACY_PER_SHIP_PER_IC = 0.1
NDefines.NNavy.SUPREMACY_PER_SHIP_BASE = 500.0
NDefines.NNavy.CONVOY_DEFENSE_MAX_CONVOY_TO_SHIP_RATIO	= 2.0		-- each ship in convoy defense mission can at most cover this many convoys without losing efficiency

NDefines.NAI.DEFAULT_LEGACY_VARIANT_CREATION_XP_CUTOFF_LAND = 10 -- 50
NDefines.NAI.NAVY_PREFERED_MAX_SIZE = 25 -- 25
NDefines.NAI.AREA_DEFENSE_BASE_IMPORTANCE = 3                  -- Area defense order base importance value (used for determining order of troop selections)
NDefines.NAI.DOCKYARDS_PER_NAVAL_DESIRE_EFFECT = 10.0			-- Effects how much AI wants to build dockyards based on how navally focused they are in general. Recommended range -100.0 to 100.0.
NDefines.NAI.MAX_SCREEN_FORCES_FOR_INVASION_SUPPORT = 0.99 -- max ratio of screens forces to be used in naval invasion missions
NDefines.NAI.MAX_CAPITAL_FORCES_FOR_INVASION_SUPPORT = 0.99 -- max ratio of capital forces to be used in naval invasion missions
NDefines.NAI.MIN_UNIT_RATIO_FOR_INVASIONS = 0.2                         -- don't allocate more divisions than this for naval invasions
NDefines.NAI.MAX_INVASION_FRONT_SCORE = 2000                            -- max score for naval invasion front scores
NDefines.NAI.MAX_INVASION_FRONT_SCORE = 2000                            -- max score for naval invasion front scores
NDefines.NAI.DIVISION_DESIGN_COMBAT_WIDTH_TARGET_WEIGHT = -500.0	-- This score is reduced the farther the width is from the target width (if set)
NDefines.NAI.DIVISION_MATCH_ROLE_BOOST_FACTOR = 1.2                -- When finding closest matching existing template to a target template, boost the score by this much if the template also has the correct role
NDefines.NAI.AREA_DEFENSE_IMPORTANCE_FACTOR = 0.5               -- used to balance defensive area importance vs other fronts
NDefines.NAI.AREA_DEFENSE_BASE_IMPORTANCE = 10                  -- Area defense order base importance value (used for determining order of troop selections)
NDefines.NAI.EQUIPMENT_MARKET_UPDATE_FREQUENCY_DAYS = 30    -- 11 AI will not ask to purchase equipment more often than this (TODO Market: may want to change how this works)

NDefines.NFocus.FOCUS_POINT_DAYS = 1 -- 7
NDefines.NMapMode.UI_CONFIGURABLE_SLOT_TO = 12
NDefines.NGraphics.GRADIENT_BORDERS_THICKNESS_STATE = 11.0
NDefines.NGraphics.GRADIENT_BORDERS_THICKNESS_RESISTANCE = 11.0
NDefines.NGraphics.COUNTRY_FLAG_SMALL_TEX_MAX_SIZE = 256
NDefines.NGraphics.MINIMUM_PROVINCE_SIZE_IN_PIXELS = 1
NDefines.NGraphics.POLITICAL_GRID_SMALL_BOX_LIMIT = 100