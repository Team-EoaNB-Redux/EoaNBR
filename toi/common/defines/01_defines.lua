NDefines = {
	NGame = {
		START_DATE = "1857.5.10.24",
		END_DATE = "2100.1.1.1",
		MAX_SCRIPTED_LOC_RECURSION = 100,				-- max recursion for scripted localizations
		HANDS_OFF_START_TAG = "UCT",					-- tag for player country for -hands_off runs. use an existing tag that is less likely to affect the game
	}
	NDiplomacy = {
		MAX_TRUST_VALUE = 80,							-- Max trust value cap.
		MIN_TRUST_VALUE = -80,							-- Min trust value cap.
		MAX_OPINION_VALUE = 200,						-- Max opinion value cap.
		MIN_OPINION_VALUE = -200,						-- Min opinion value cap.
		BASE_TRUCE_PERIOD = 30,						-- Base truce period in days.
		PEACE_INCREASE_COST_FACTOR_PER_MISSING_PERCENT_FOR_CAPITULATION = 0.01, 	-- increase factor if loser has not capitulated, for every percent between surrender level and BASE_SURRENDER_LEVEL
		INFLUENCE_RATIO_CAPITAL = 0.3,                  -- Ratio of influence based on distance to capital
		INFLUENCE_RATIO_CONTROLLED = 0.4,               -- Ratio of influence based on distance to neared controlled territory (including uncontested peace conference bids)
			INFLUENCE_REDUCTION_PER_CAPITAL_DIST = 0.05,    -- Reduce influence with this much per distance_to_capital
			INFLUENCE_REDUCTION_PER_CORE_DIST = 0.05,       -- Reduce influence with this much per distance_to_core
			INFLUENCE_REDUCTION_PER_CONTROLLED_DIST = 0.10, -- Reduce influence with this much per distance_to_controlled
			INFLUENCE_MAX_DISCOUNT = 0.25,                  -- At 100 % influence, reduce the cost this much
		INFLUENCE_DISTANCE_DIVISOR = 30.0,              -- Divide pixel distance with this when determining distance to capital / core / controlled states. Resulting "distance" metric is rounded to nearest integer.
		BASE_IMPROVE_RELATION_COST = 20,                -- Political power cost to initiate relation improvement
		BASE_IMPROVE_RELATION_SAME_IDEOLOGY_GROUP_MAINTAIN_COST = 0.15, -- Political power cost each update when boosting relations with nation of same ideology
		BASE_IMPROVE_RELATION_DIFFERENT_IDEOLOGY_GROUP_MAINTAIN_COST = 0.3,    -- Political power cost each update when boosting relations with nation of different ideology
		TENSION_TIME_SCALE_START_DATE = "1936.1.1.12",	-- Starting at this date, the tension values will be scaled down (will be equal to 1 before that)
		PEACE_SCORE_SCALE_FACTOR = 1.25,                -- Losers' total value times this factor becomes the default total peace conference score that is distributed to the winners.
	}
	NCountry = {
		MAJOR_MIN_FACTORIES = 2000,						-- need at least these many factories to become a major
		STATE_VALUE_MANPOWER_FACTOR = 0.15,              -- State cost increases with this for every 10k population (so 3.1M becomes 310 and then multiplied by this)
		AIR_SUPPLY_CONVERSION_SCALE = 0.0005,				-- Conversion scale for planes to air supply
		STARTING_FUEL_RATIO = 0.1,						-- starting fuel ratio compared to max fuel for countries
		BASE_FUEL_GAIN_PER_OIL = 0.25,						-- base amount of fuel gained hourly per excess oil
		BASE_FUEL_GAIN = 1.0,							-- base amount of fuel gained hourly, independent of excess oil
		BASE_FUEL_CAPACITY = 500,						-- base amount of fuel capacity
	}
	NResistance = {
		COMPLIANCE_FACTOR_ON_STATE_CONTROLLER_CHANGE = -0.1,	-- compliance factor that applies when the state controller changes (in between allies, compliance is zeroed if it is taken by original country)
		COMPLIANCE_DECAY_AT_MAX_COMPLIANCE = -0.1, -- as compliance increases, it gets a decay rate depending on its value. compliance should stabilize at some value until its growth changes
	}
	NProduction = {
		MAX_EQUIPMENT_RESOURCES_NEED = 6, 	-- Max number of different strategic resources an equipment can be dependent on.
		BASE_FACTORY_SPEED_MIL = 5, 				-- Base factory speed multiplier (how much hoi3 style IC each factory gives).
		ANNEX_FUEL_RATIO = 0.5,	-- How much fuel will be transferred on annexation
		MIN_POSSIBLE_TRAINING_MANPOWER = 5000,	-- How many deployment lines minimum can be training
		CAPITULATE_FUEL_RATIO = 0.25, -- How much fuel will be transferred on capitulation
		PRODUCTION_RESOURCE_LACK_PENALTY = -0.5,			-- Penalty decrease while lack of resource per factory
		CONVERSION_SPEED_BONUS = 2.0,							-- Modifier to the production speed when converting equipment
	}
	NTechnology = {
		BASE_TECH_COST = 1000,					-- Base cost for a tech. multiplied with tech cost and ahead of time penalties
	}
	NBuildings = {
		MAX_SHARED_SLOTS = 81,				-- Max slots shared by factories
	}
	NMilitary = {
		HOURLY_ORG_MOVEMENT_IMPACT = -0.1,		-- how much org is lost every hour while moving an army.
		ENGAGEMENT_WIDTH_PER_WIDTH = 5.0,	-- how much enemy combat width we are allowed to engage per width of our own
		INFRASTRUCTURE_MOVEMENT_SPEED_IMPACT = -0.025,	-- speed penalty per infrastucture below maximum.
		WAR_SCORE_PROVINCE_FACTOR = 0.3,							-- war score gained when capturing a province for the first time, multiplied by province's worth
		WAR_SCORE_LEND_LEASE_GIVEN_IC_FACTOR = 0.1,  				-- war score gained for every IC of lend lease sent to allies
		WAR_SCORE_LEND_LEASE_GIVEN_FUEL_FACTOR = 0.01,  				-- war score gained for every unit of fuel lend lease sent to allies
		WAR_SCORE_LEND_LEASE_RECEIVED_IC_FACTOR = 0.1,  			-- war score deducted for every IC of lend lease received from allies
		WAR_SCORE_LEND_LEASE_RECEIVED_FUEL_FACTOR = 0.01, 			-- war score deducted for every unit of fuel lend lease received from allies
		DIVISION_SIZE_FOR_XP = 4,                   -- how many battalions should a division have to count as a full divisions when calculating XP stuff
		MAX_ARMY_EXPERIENCE = 2500,			--Max army experience a country can store
		MAX_NAVY_EXPERIENCE = 2500,			--Max navy experience a country can store
		MAX_AIR_EXPERIENCE = 2500,				--Max air experience a country can store
		LAND_COMBAT_STR_DAMAGE_MODIFIER = 0.03,       -- global damage modifier... but some equipment is returned at end of battles see : EQUIPMENT_COMBAT_LOSS_FACTOR
		LAND_COMBAT_ORG_DAMAGE_MODIFIER = 0.04,       -- global damage modifier
		LAND_AIR_COMBAT_STR_DAMAGE_MODIFIER = 0.04,    -- air global damage modifier
		LAND_AIR_COMBAT_ORG_DAMAGE_MODIFIER = 0.04,    -- global damage modifier
		TACTIC_SWAP_FREQUENCEY = 24,                   -- hours between tactic swaps
		TRAINING_MAX_LEVEL = 10,
		DEPLOY_TRAINING_MAX_LEVEL = 5,
		ARMY_EXP_BASE_LEVEL = 5,
		UNIT_EXP_LEVELS = { 0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.425, 0.55, 0.675, 0.75, 0.775, 0.8, 0.825, 0.85, 0.9, 0.95, 0.99 },		-- Experience needed to progress to the next level
		FIELD_EXPERIENCE_SCALE = 0.002,
		FIELD_EXPERIENCE_MAX_PER_DAY = 3,				-- Most xp you can gain per day
		EXPEDITIONARY_FIELD_EXPERIENCE_SCALE = 0.5,		-- reduction factor in Xp from expeditionary forces
		LEND_LEASE_FIELD_EXPERIENCE_SCALE = 0.005,		-- Experience scale for lend leased equipment used in combat.
		EXPERIENCE_COMBAT_FACTOR = 0.05,
		PARACHUTE_COMPLETE_ORG = 0.1,				   -- Organisation value (in %) after unit being dropped, regardless if failed, disrupted, or successful.
		BORDER_WAR_ATTRITION_FACTOR = 0.01,			   -- How much of borderwar balance of power makes it into attrition
		REINFORCE_CHANCE = 0.03,                 	   -- base chance to join combat from back line when empty
		LOW_ORG_FOR_ATTACK = 0.5,                      -- at what org % we start affecting speed when doign hostile moves. scales down ZERO_ORG_MOVEMENT_MODIFIER
		PLAN_COHESION_DISTANCE_MAX_WHEN_LEFT_BEHIND = 38,	--If not on the frontline and not moving, we can still be relocated if we exceed cohesion distance, but only to locations less than THIS distance. (Note: this is -actual- distance, not weighted distance)
		MIN_DIVISION_DEPLOYMENT_TRAINING = 0.05,			-- Min level of division training
		BORDER_WAR_WIN_DAYS_AGAINST_EMPTY_OPPONENTS = 30,		-- border wars will be automatically won if no opponent shows up for this duration
	}
	NAir = {
		TOP_SPEED_DAMAGE_BONUS_FACTOR = 0.02,				-- A factor for scaling the top speed of a plane into damage buff
		COMBAT_BETTER_SPEED_DAMAGE_INCREASE = 0.45, 		-- How much the better Speed (than opponent's) can reduce increase our damage to them.
		COMBAT_DAMAGE_SCALE = 0.25,							-- Higher value = more shot down planes
		COMBAT_DAMAGE_SCALE_CARRIER = 1,					-- same as above but used inside naval combat for carrier battles
		NAVAL_STRIKE_DAMAGE_TO_STR = 2.0,					-- Balancing value to convert damage ( naval_strike_attack * hits ) to Strength reduction.
		NAVAL_STRIKE_DAMAGE_TO_ORG = 2.5,					-- Balancing value to convert damage ( naval_strike_attack * hits ) to Organisation reduction.
		THRUST_WEIGHT_SPEED_FACTOR = 10,								-- For plane designs, additive Km/h max speed bonus per point of thrust exceeding weight
	}
	NNavy = {
		WAR_SCORE_GAIN_FOR_SUNK_SHIP_MANPOWER_FACTOR = 0.02,			-- war score gained for every manpower killed when sinking a ship
		WAR_SCORE_GAIN_FOR_SUNK_SHIP_PRODUCTION_COST_FACTOR = 0.04,		-- war score gained for every IC of the sunk ship
		WAR_SCORE_GAIN_FOR_SUNK_CONVOY = 10.0,							-- war score gained for every sunk convoy
		WAR_SCORE_DECAY_FOR_BUILT_CONVOY = 5.0,  						-- war score deducted when convoy-raided enemy produces one new convoy
		SHORE_BOMBARDMENT_CAP = 0.5,
		0.75, -- NAVAL_INVASION_SUPPORT (does not cost fuel at base, only costs while doing bombardment and escorting units)
		OUT_OF_FUEL_SPEED_FACTOR = -0.9,
		OUT_OF_FUEL_RANGE_FACTOR = -0.9,
		MISSION_FUEL_COSTS = {  -- fuel cost for each mission
			0.0, -- HOLD (consumes fuel HOLD_MISSION_MOVEMENT_COST fuel while moving)
			1.0, -- PATROL
			1.0, -- STRIKE FORCE (does not cost fuel at base, and uses IN_COMBAT_FUEL_COST in combat. this is just for the movement in between)
			1.0, -- CONVOY RAIDING
			1.0, -- CONVOY ESCORT
			1.0, -- MINES PLANTING
			1.0, -- MINES SWEEPING
			0.6, -- TRAIN
			0.0, -- RESERVE_FLEET (consumes fuel HOLD_MISSION_MOVEMENT_COST fuel while moving)
			1.0, -- NAVAL_INVASION_SUPPORT (does not cost fuel at base, only costs while doing bombardment and escorting units)
		},
		SUPREMACY_PER_SHIP_PER_MANPOWER = 0.5,							-- supremacy of a ship is calculated using its IC, manpower and a base define
		SUPREMACY_PER_SHIP_PER_IC = 0.1,
		SUPREMACY_PER_SHIP_BASE = 500.0,
		BASE_SPOTTING_EFFECT_FOR_INITIAL_UNIT_TRANSFER_SPOTTING = 10.0,	-- same as BASE_SPOTTING_EFFECT_FOR_INITIAL_CONVOY_SPOTTING, but for naval transfer convoys
		SPOTTING_SPEED_EFFECT_FOR_INITIAL_UNIT_TRANSFER_SPOTTING = 20.0, -- same as SPOTTING_SPEED_EFFECT_FOR_INITIAL_CONVOY_SPOTTING, but for naval transfer convoys
		SHIP_TO_FLEET_ANTI_AIR_RATIO									= 0.2,	-- total sum of fleet's anti air will be multiplied with this ratio and added to calculations anti-air of individual ships while air damage reduction
		ANTI_AIR_POW_ON_INCOMING_AIR_DAMAGE								= 0.2,	-- received air damage is calculated using following: 1 - ( (ship_anti_air + fleet_anti_air * SHIP_TO_FLEET_ANTI_AIR_RATIO )^ANTI_AIR_POW_ON_INCOMING_AIR_DAMAGE ) * ANTI_AIR_MULT_ON_INCOMING_AIR_DAMAGE
		ANTI_AIR_MULT_ON_INCOMING_AIR_DAMAGE							= 0.15,
		HIT_PROFILE_MULT 												= 50.0,  	-- multiplies hit profile of every ship
		HIT_PROFILE_SPEED_FACTOR										= 0.5,		-- factors speed value when determining it profile (Vis * HIT_PROFILE_MULT * Ship Hit Profile Mult)
		CONVOY_DEFENSE_MAX_CONVOY_TO_SHIP_RATIO							= 2.0,		-- each ship in convoy defense mission can at most cover this many convoys without losing efficiency
		DEFAULT_LEGACY_VARIANT_CREATION_XP_CUTOFF_LAND = 10,	-- Army XP needed before attempting to create a variant of a type that uses the legacy upgrades system. ai_strategy supports land_xp_spend_priority upgrade_xp_cutoff. If none is set, this define is used instead.
		NAVY_PREFERED_MAX_SIZE = 20,						-- AI will generally attempt to merge fleets into this size, but as a soft limit.
		AREA_DEFENSE_BASE_IMPORTANCE = 3,                  -- Area defense order base importance value (used for determining order of troop selections)
		TRANSPORTS_PER_PARATROOPER = 20,					-- Air transports only duty is to drop paratroopers.
		DOCKYARDS_PER_NAVAL_DESIRE_EFFECT = 0.0,			-- Effects how much AI wants to build dockyards based on how navally focused they are in general. Recommended range -100.0 to 100.0.
		MAX_SCREEN_FORCES_FOR_INVASION_SUPPORT = 0.99, -- max ratio of screens forces to be used in naval invasion missions
		MAX_CAPITAL_FORCES_FOR_INVASION_SUPPORT = 0.99, -- max ratio of capital forces to be used in naval invasion missions
		MIN_UNIT_RATIO_FOR_INVASIONS = 0.2,                         -- don't allocate more divisions than this for naval invasions
		MAX_INVASION_FRONT_SCORE = 2000,                            -- max score for naval invasion front scores
	}
	NFocus = {
		FOCUS_POINT_DAYS = 1,						-- Each point takes a day
	}
}