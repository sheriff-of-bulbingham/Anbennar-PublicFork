#This file is VERY important, DO NOT edit it without reading the guide

races = ["centaur", "dwarven", "elven", "gnollish", "gnomish", "goblin", "halfling", "half_elven", "half_orcish", "harimari", "harpy", "hobgoblin", "human", "kobold", "ogre", "orcish", "ruinborn", "troll"]

monster_races = ["centuar", "kobold","orcish","gnollish","goblin","harpy","troll","hobgoblin","centaur","ogre"]

greentide_races = ["orcish","goblin"]

# Note Gnomish one is treated special as it goes away in the age of artificers, else this shows which races are HATED by other races e.g "dwarven" : "orcish", "goblin" means orcs and goblins get a 10* factor for expelling dwarves
racial_hatred = {
	"orcish" : ["dwarven"],
	"goblin" : ["dwarven"],
	"dwarven" : ["orcish", "goblin"],
	"kobold" : ["gnomish"],
}

def getRacialHatred(race, racial_hatred_races):
    racial_hatred = """
"""
    if race == "kobold":
        racial_hatred += """			#+Special - gnomish hatred until age of artificers
			modifier = {{
				factor = 3
				has_country_modifier = gnomish_administration
				NOT = {{ current_age = age_of_revolutions }}
			}}""".format(race)
    elif (race in racial_hatred_races):
        racial_hatred += """			#+Special - racial hatred
			modifier = {{
				factor = 10
				OR = {{
""".format(race)
        for hater_race in racial_hatred_races[race]:
            racial_hatred += """            		has_country_modifier = {0}_administration
""".format(hater_race)
        racial_hatred += """				}}
			}}""".format(hater_race)
    return racial_hatred

#Special getter for expel factors
def getExpelFactors(race, racial_hatred):
	expel_factors = """
"""
	if not(race in monster_races):
		expel_factors += """			#+Is not a Monstrous Race
			modifier = {{
				factor = 0.6 #Makes base factor 3 for removing non-monstrous races
				always = yes
			}}
			#+Special - Slave States of The Command encouraged to displace
			modifier = {{
				factor = 2
				is_subject_of_type = slave_state 
			}}
""".format(race)
	if race == "orcish":
		expel_factors += """			#-Special: if you have orcish slaves enabled then you dont want to do it
			modifier = {{ 
				factor = 0.1
				has_country_modifier = orcish_slaves_in_colonies
			}}""".format(race)
		expel_factors += """			#-Special - Silverforge wont expel it's slaves
			modifier = {{
				factor = 0
				tag = A73
			}}""".format(race)
	if not(race in greentide_races):
		expel_factors += """			#-Humanists dont do it
			modifier = {{
				factor = 0
                OR = {{
                    has_idea_group = humanist_ideas
                    personality = ai_diplomat
                }}
			}}""".format(race)
	else:
		expel_factors += """			#-Humanists dont do it
			modifier = {{
				factor = 0
                OR = {{
                    has_idea_group = humanist_ideas
                    personality = ai_diplomat
                }}
                NOT = {{ has_country_modifier = dwarven_administration }}
			}}""".format(race)
	expel_factors += getRacialHatred(race, racial_hatred)
	return(expel_factors)
    
#Special getter for end expel factors
def getEndExpelFactors(race):
    end_expel_factors = """
"""
    if race in greentide_races:
        
        end_expel_factors +="""#+Special - don't stop expel during greentide
			modifier = {{
				factor = 0
				has_reform = adventurer_reform
				current_age = age_of_discovery
			}}""".format(race)
            
    return(end_expel_factors)

#Special getter for purge factors
def getPurgeFactors(race, racial_hatred):
	purge_factors = """
"""
	if race in greentide_races:
		purge_factors +="""#+Special - adventurers purge during greentide
			modifier = {{
				factor = 3
				has_reform = adventurer_reform
				current_age = age_of_discovery
			}}""".format(race)
	if race == "orcish":
		purge_factors += """#-Special: if you have orcish slaves enabled then you dont want to do it
			modifier = {{ 
				factor = 0.1
				has_country_modifier = orcish_slaves_in_colonies
			}}""".format(race)
	purge_factors += getRacialHatred(race, racial_hatred)
	return(purge_factors)

#Special getter for end purge factors
def getEndPurgeFactors(race):
    end_purge_factors = """
"""
    if race in greentide_races:
        end_purge_factors +="""#+Special - don't stop purge during greentide
			modifier = {{
				factor = 0
				has_reform = adventurer_reform
				current_age = age_of_discovery
			}}""".format(race)
            
    return(end_purge_factors)

def getRaceText(race, racial_hatred):
    #These events are common between all racial pop events
    start = """#This file was made using a script, if you wish to edit the file make sure to update the script: 
namespace = racial_pop_events_{0}

#Demand Representation
country_event = {{
	id = racial_pop_events_{0}.1
	title = racial_pop_events_{0}.1.t
	desc = racial_pop_events_{0}.1.d
	picture = DEBATE_REPUBLICAN_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
		NOT = {{ has_country_modifier = {0}_administration }}
		any_owned_province = {{
			NOT = {{ local_autonomy = 50 }}
			is_capital = no
			has_{0}_minority_trigger = yes
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	immediate = {{
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					is_capital = no
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ local_autonomy = 50 }}
					is_capital = no
					has_{0}_minority_trigger = yes
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ local_autonomy = 50 }}
					is_capital = no
					has_{0}_minority_trigger = yes
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
		}}
	}}
	
	option = {{		#Granted!
		name = racial_pop_events_{0}.1.a
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_increase_tolerance_{0} = yes
			}}
		}}
		
		add_adm_power = -40
		
		medium_increase_of_{0}_tolerance_effect = yes
		
		event_target:racial_pop_province_target = {{
			add_local_autonomy = 25
		}}
	}}
	
	option = {{		#Make some concessions
		name = racial_pop_events_{0}.1.b
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_maintain_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 0.5
				average_autonomy = 10
			}}
		}}
		
		add_adm_power = -20
		
		event_target:racial_pop_province_target = {{
			add_local_autonomy = 10
		}}

	}}
	
	option = {{		#No. Haven't we given them enough?!
		name = racial_pop_events_{0}.1.c
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
	option = {{		#Special: Make empty promises
		name = racial_pop_events_{0}.1.e
		trigger = {{ ruler_has_personality = charismatic_negotiator_personality }}
		highlight = yes
		ai_chance = {{
			factor = 100
			modifier = {{
				factor = 0.25
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 1.5
				average_autonomy = 10
			}}
		}}
		
		add_dip_power = -10
		
		small_increase_of_{0}_tolerance_effect = yes
		
		event_target:racial_pop_province_target = {{
			add_local_autonomy = 1
		}}
		
	}}
}}


#Tolerance Increase
country_event = {{
	id = racial_pop_events_{0}.2
	title = racial_pop_events_{0}.2.t
	desc = racial_pop_events_{0}.2.d
	picture = GOOD_WITH_MONARCH_eventPicture
	
	trigger = {{
		NOT = {{ has_country_modifier = {0}_administration }}
		OR = {{
			stability = 1
			in_golden_age = yes
			ruler_has_personality = tolerant_personality
			ruler_has_personality = kind_hearted_personality
			ruler_has_personality = benevolent_personality
			has_idea_group = humanist_ideas
			
			any_ally = {{
				has_country_modifier = {0}_administration
			}}
		}}
		any_owned_province = {{
			has_{0}_minority_trigger = yes
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	immediate = {{
		hidden_effect = {{
		
			random_list = {{
				75 = {{
					set_country_flag = racial_pop_small_increase
				}}
				25 = {{
					set_country_flag = racial_pop_medium_increase
				}}
			}}
		}}
	}}
	
	option = {{		#Good for them
		name = racial_pop_events_{0}.2.a
		ai_chance = {{
			factor = 50
		}}
		
		trigger_switch = {{
			on_trigger = has_country_flag
			racial_pop_small_increase = {{ small_increase_of_{0}_tolerance_effect = yes }}
			racial_pop_medium_increase = {{ medium_increase_of_{0}_tolerance_effect = yes }}
		}}
		
		clear_racial_pop_tolerance_chance_flags = yes
		
	}}
	
}}


#Tolerance Decrease
country_event = {{
	id = racial_pop_events_{0}.3
	title = racial_pop_events_{0}.3.t
	desc = racial_pop_events_{0}.3.d
	picture = BAD_WITH_MONARCH_eventPicture
	
	trigger = {{
		NOT = {{ has_country_modifier = {0}_administration }}
		
		OR = {{
			NOT = {{ stability = 0 }}
			is_bankrupt = yes
			inflation = 25
			AND = {{
				is_at_war = yes
				NOT = {{ war_score = 20 }}
			}}
			war_exhaustion = 10
			ruler_has_personality = cruel_personality
			ruler_has_personality = malevolent_personality
			ruler_has_personality = conqueror_personality
			
			any_rival_country = {{
				has_country_modifier = {0}_administration
			}}
		}}
		any_owned_province = {{
			has_{0}_minority_trigger = yes
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	immediate = {{
		hidden_effect = {{
		
			random_list = {{
				75 = {{
					set_country_flag = racial_pop_small_decrease
				}}
				25 = {{
					set_country_flag = racial_pop_medium_decrease
				}}
			}}
		}}
	}}
	
	option = {{		#That's unfortunate
		name = racial_pop_events_{0}.3.a
		ai_chance = {{
			factor = 50
		}}
		
		trigger_switch = {{
			on_trigger = has_country_flag
			racial_pop_small_decrease = {{ small_decrease_of_{0}_tolerance_effect = yes }}
			racial_pop_medium_decrease = {{ medium_decrease_of_{0}_tolerance_effect = yes }}
		}}
		
		clear_racial_pop_tolerance_chance_flags = yes
		
	}}
	
}}


#Independent Pop Grow - small to large
country_event = {{
	id = racial_pop_events_{0}.4
	title = racial_pop_events_{0}.4.t
	desc = racial_pop_events_{0}.4.d
	picture = STREET_SPEECH_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
		any_owned_province = {{
			has_small_{0}_minority_trigger = yes
			OR = {{
				is_prosperous = yes
				development = 20
			}}
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_small_{0}_minority_trigger = yes
					is_prosperous = yes
				}}
				save_event_target_as = racial_pop_province_target
			}}
			#random_owned_province = {{
			#	limit = {{
			#		has_small_{0}_minority_trigger = yes
			#		is_capital = yes
			#	}}
			#	save_event_target_as = racial_pop_province_target
			#}}
			random_owned_province = {{
				limit = {{
					has_small_{0}_minority_trigger = yes
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
		}}
	}}
	
	option = {{		#The more the merrier?
		name = racial_pop_events_{0}.4.a
		ai_chance = {{
			factor = 50
		}}
	
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
		}}
	}}
	
}}


#Independent Pop Decrease - large/small decrease
country_event = {{
	id = racial_pop_events_{0}.5
	title = racial_pop_events_{0}.5.t
	desc = racial_pop_events_{0}.5.d
	picture = WOUNDED_SOLDIERS_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
		any_owned_province = {{
			has_{0}_minority_trigger = yes
			OR = {{
				unrest = 15
				devastation = 50
				has_oppressed_{0}_minority_trigger = yes
			}}
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
				}}
				save_event_target_as = racial_pop_province_target
			}}
		}}
	}}
	
	option = {{		#Large minority decreases to small
		name = racial_pop_events_{0}.5.a
		trigger = {{
			event_target:racial_pop_province_target = {{
				has_large_{0}_minority_trigger = yes
			}}
		}}
		ai_chance = {{
			factor = 50
		}}
	
		event_target:racial_pop_province_target = {{
			remove_{0}_minority_size_effect = yes
		}}
	}}
	
	option = {{		#Small minority is removed (becomes insignificant)
		name = racial_pop_events_{0}.5.b
		trigger = {{
			event_target:racial_pop_province_target = {{
				has_small_{0}_minority_trigger = yes
			}}
		}}
		ai_chance = {{
			factor = 50
		}}
	
		event_target:racial_pop_province_target = {{
			remove_{0}_minority_size_effect = yes
		}}
	}}
}}



#Pop Migrates - Within Country
country_event = {{
	id = racial_pop_events_{0}.6
	title = racial_pop_events_{0}.6.t
	desc = racial_pop_events_{0}.6.d
	picture = COLONIZATION_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
		num_of_cities = 2	#you have something to migrate to
		any_owned_province = {{
			has_{0}_minority_trigger = yes
			OR = {{
				devastation = 33
				unrest = 10
				NOT = {{ development = 10 }}
			}}
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
		hidden_effect = {{
			#Origin Province Setter
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					NOT = {{ development = 10 }}
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					unrest = 10 
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					devastation = 33
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			
			#Target Province Setter
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					NOT = {{ has_large_{0}_minority_trigger = yes }}
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					OR = {{
						NOT = {{ devastation = 33 }}
						NOT = {{ unrest = 10 }}
					}}
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					NOT = {{ has_large_{0}_minority_trigger = yes }}
					OR = {{
						NOT = {{ devastation = 33 }}
						NOT = {{ unrest = 10 }}
					}}
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					OR = {{
						NOT = {{ devastation = 33 }}
						NOT = {{ unrest = 10 }}
					}}
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					NOT = {{ has_large_{0}_minority_trigger = yes }}
					OR = {{
						NOT = {{ devastation = 33 }}
						NOT = {{ unrest = 10 }}
					}}
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					OR = {{
						NOT = {{ devastation = 33 }}
						NOT = {{ unrest = 10 }}
					}}
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
			random_owned_province = {{
				limit = {{
					NOT = {{ province_id = event_target:racial_pop_province_origin }}
					NOT = {{ has_large_{0}_minority_trigger = yes }}
					OR = {{
						NOT = {{ devastation = 33 }}
						NOT = {{ unrest = 10 }}
					}}
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
		}}
	}}
	
	#Welcome to [new province]!
	option = {{		
		name = racial_pop_events_{0}.6.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_increase_tolerance_{0} = yes
			}}
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
		}}
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
	}}
	
	#Prevent migration
	option = {{		
		name = racial_pop_events_{0}.6.b
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			
			#If Persecuting
			modifier = {{
				factor = 3
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
		}}
		
		add_adm_power = -10
		
		small_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
}}



#Pop Migrates - Outside Country
country_event = {{
	id = racial_pop_events_{0}.7
	title = racial_pop_events_{0}.7.t
	desc = racial_pop_events_{0}.7.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		num_of_cities = 2	#you have something to migrate to
		#Country that tolerates race
		any_neighbor_country = {{ 
			NOT = {{ low_tolerance_{0}_race_trigger = yes }}
		}}
		any_owned_province = {{
			has_{0}_minority_trigger = yes
			OR = {{
				devastation = 33
				unrest = 10
				NOT = {{ development = 10 }}
				has_oppressed_{0}_minority_trigger = yes
			}}
		}}
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
	
		#Origin Province Setter
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_oppressed_{0}_minority_trigger = yes 
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					NOT = {{ development = 10 }}
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					unrest = 10 
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					devastation = 33
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
			
		#Which country to migrate to
		hidden_effect = {{
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					high_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					OR = {{
						medium_tolerance_{0}_race_trigger = yes
						high_tolerance_{0}_race_trigger = yes
					}}
					any_owned_province = {{
						development = 20
						NOT = {{ has_{0}_minority_trigger = yes }}
						NOT = {{ has_{0}_majority_trigger = yes }}
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#Good luck in [new country]!
	option = {{		
		name = racial_pop_events_{0}.7.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_increase_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				NOT = {{ stability = 1 }}
			}}
			modifier = {{	#this is to push refugees essentially
				factor = 1.5
				is_at_war = yes
			}}
			
			#This is the same as expelling them but voluntarily so they're good with it
			modifier = {{
				factor = 3
				has_country_modifier = racial_pop_{0}_expulsion
			}}
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
		}}
	
		#Calls Migrants Arrive to Migration Country
		event_target:racial_pop_migration_country  = {{
			country_event = {{
				id = racial_pop_events_{0}.9
				days = 14
				random = 31
			}}
		}}
	}}
	
	#Prevent migration
	option = {{		
		name = racial_pop_events_{0}.7.b
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				stability = 2
			}}
			modifier = {{	#they're integrated so they technically want them to stay
				factor = 1.5
				high_tolerance_{0}_race_trigger = yes
			}}
			
			#Purgers dont want them to get away
			modifier = {{
				factor = 3
				has_country_modifier = racial_pop_{0}_purge
			}}
		}}
		
		add_dip_power = -10
		
		small_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
}}


#Pop Migrates - To Colony
country_event = {{
	id = racial_pop_events_{0}.8
	title = racial_pop_events_{0}.8.t
	desc = racial_pop_events_{0}.8.d
	picture = CARIBBEAN_PIRATE_FORT_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		num_of_cities = 2	#you have something to migrate to
		
		#Country that tolerates race
		any_subject_country = {{ 
			is_colonial_nation = yes
		}}
		any_owned_province = {{
			has_{0}_minority_trigger = yes
			OR = {{
				devastation = 33
				unrest = 10
				NOT = {{ development = 10 }}
				has_oppressed_{0}_minority_trigger = yes
			}}
		}}
		
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
	
		#Origin Province Setter
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_oppressed_{0}_minority_trigger = yes 
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					NOT = {{ development = 10 }}
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					unrest = 10 
				}}
				save_event_target_as = racial_pop_province_origin
			}}
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
					devastation = 33
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
			
		#Which country to migrate to
		hidden_effect = {{
			random_subject_country = {{
				limit = {{
					is_colonial_nation = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_subject_country = {{
				limit = {{
					any_owned_province = {{
						development = 20
					}}
					is_colonial_nation = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#[colonyname] could use the help!
	option = {{		
		name = racial_pop_events_{0}.8.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 2
				personality = ai_colonialist 
			}}
			modifier = {{
				factor = 2
				has_idea_group = expansion_ideas
			}}
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
		}}
	
		#Calls Migrants Arrive to Migration Country
		event_target:racial_pop_migration_country  = {{
			country_event = {{
				id = racial_pop_events_{0}.9
				days = 14
				random = 31
			}}
		}}
	}}
	
	#Prevent them from leaving, they belong at home
	option = {{		
		name = racial_pop_events_{0}.8.b
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 30
			modifier = {{
				factor = 2
				ruler_has_personality = careful_personality
			}}
			
			#If Persecuting
			modifier = {{
				factor = 3
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
		}}
		
		add_dip_power = -10
		
		small_decrease_of_{0}_tolerance_effect = yes
	}}
	
}}


#Migrants Arrive
country_event = {{
	id = racial_pop_events_{0}.9
	title = racial_pop_events_{0}.9.t
	desc = racial_pop_events_{0}.9.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
		hidden_effect = {{
			
			#Target Province Setter
			random_owned_province = {{
				limit = {{
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
		}}
	}}
	
	#Welcome to [new province]!
	option = {{		
		name = racial_pop_events_{0}.9.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_increase_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				high_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 2
				OR = {{
					is_colonial_nation = yes
					is_subject_of = ROOT
				}}
			}}
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
				}}
			}}
			modifier = {{
				factor = 3
				has_idea_group = humanist_ideas
			}}
		}}
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
	}}
	
	#They can settle, for a price
	option = {{		
		name = racial_pop_events_{0}.9.b
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 1.5
				is_bankrupt = yes
			}}
			modifier = {{
				factor = 2
				ruler_has_personality = greedy_personality
			}}
			modifier = {{
				factor = 1.5
				has_personal_deity = ara
			}}
		}}
		
		add_years_of_income = 0.1
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
		
		small_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
	#Reject migrants
	option = {{		
		name = racial_pop_events_{0}.9.c
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				low_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = malevolent_personality
					ruler_has_personality = cruel_personality
				}}
			}}
			modifier = {{
				factor = 1.5
				OR = {{
					ruler_has_personality = careful_personality
				}}
			}}
			
			#If Persecuting
			modifier = {{
				factor = 3
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
		}}
		
		add_mil_power = -10
		
		small_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
}}


#Refugees Arrive - First Try
country_event = {{
	id = racial_pop_events_{0}.10
	title = racial_pop_events_{0}.10.t
	desc = racial_pop_events_{0}.10.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
		hidden_effect = {{
			
			#Target Province Setter
			random_owned_province = {{
				limit = {{
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
		}}
		
		#Which country to migrate to
		hidden_effect = {{
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					high_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					OR = {{
						medium_tolerance_{0}_race_trigger = yes
						high_tolerance_{0}_race_trigger = yes
					}}
					any_owned_province = {{
						development = 20
						NOT = {{ has_{0}_minority_trigger = yes }}
						NOT = {{ has_{0}_majority_trigger = yes }}
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#Let them in
	option = {{		
		name = racial_pop_events_{0}.10.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_increase_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				high_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 2
				OR = {{
					is_colonial_nation = yes
					is_subject_of = ROOT
				}}
			}}
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
				}}
			}}
			modifier = {{
				factor = 3
				has_idea_group = humanist_ideas
			}}
		}}
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
			add_local_autonomy = 10
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
		
		small_increase_of_{0}_tolerance_effect = yes
	}}
	
	#Confiscate their valuables in return
	option = {{		
		name = racial_pop_events_{0}.10.b
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 1.5
				is_bankrupt = yes
			}}
			modifier = {{
				factor = 2
				ruler_has_personality = greedy_personality
			}}
			modifier = {{
				factor = 1.5
				has_personal_deity = ara
			}}
		}}
		
		add_years_of_income = 0.2
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
			add_local_autonomy = 10
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
	#There's no room for you here!
	option = {{		
		name = racial_pop_events_{0}.10.c
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				low_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = malevolent_personality
					ruler_has_personality = cruel_personality
				}}
			}}
			modifier = {{
				factor = 1.5
				OR = {{
					ruler_has_personality = careful_personality
				}}
			}}
			
			#If Persecuting
			modifier = {{
				factor = 3
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
		}}
		
		if = {{
			limit = {{
				any_neighbor_country = {{ 
					OR = {{
						NOT = {{ has_country_modifier = racial_pop_{0}_purge  }}
						NOT = {{ has_country_modifier = racial_pop_{0}_expulsion  }}
					}}
				}}
			}}
			#Calls Migrants Arrive to Migration Country
			event_target:racial_pop_migration_country  = {{
				country_event = {{
					id = racial_pop_events_{0}.11
					days = 31
					random = 31
				}}
			}}
		}}
		
		add_mil_power = -20
		
		medium_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
}}


#Refugees Arrive - Second Try (forcefully settle)
country_event = {{
	id = racial_pop_events_{0}.11
	title = racial_pop_events_{0}.11.t
	desc = racial_pop_events_{0}.11.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_target
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{
		hidden_effect = {{
			
			#Target Province Setter
			random_owned_province = {{
				limit = {{
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 10
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 15
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					NOT = {{ has_{0}_minority_trigger = yes }}
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			random_owned_province = {{
				limit = {{
					development = 20
				}}
				save_event_target_as = racial_pop_province_target
			}}
			
		}}
	}}
	
	#Let those poor souls in
	option = {{		
		name = racial_pop_events_{0}.11.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_increase_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				high_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 2
				OR = {{
					is_colonial_nation = yes
					is_subject_of = ROOT
				}}
			}}
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
				}}
			}}
			modifier = {{
				factor = 3
				has_idea_group = humanist_ideas
			}}
		}}
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
			add_local_autonomy = 10
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
		
		small_increase_of_{0}_tolerance_effect = yes
	}}
	
	#Confiscate what they have in return
	option = {{		
		name = racial_pop_events_{0}.11.b
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 1.5
				is_bankrupt = yes
			}}
			modifier = {{
				factor = 2
				ruler_has_personality = greedy_personality
			}}
			modifier = {{
				factor = 1.5
				has_personal_deity = ara
			}}
		}}
		
		add_years_of_income = 0.15
	
		#Add Minority to New Province
		event_target:racial_pop_province_target = {{
			add_{0}_minority_size_effect = yes
			add_local_autonomy = 10
		}}
		
		#Boost Dev if Large already
		if = {{
			limit = {{
				event_target:racial_pop_province_target = {{
					OR = {{
						has_large_{0}_minority_trigger = yes
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			event_target:racial_pop_province_target = {{
				random = {{
					chance = 50
					add_base_production = 1
				}}
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
		
	}}
	
	#Prevent them with force, if necessary
	option = {{		
		name = racial_pop_events_{0}.11.c
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
			modifier = {{
				factor = 1.5
				wants_to_decrease_tolerance_{0} = yes
			}}
			modifier = {{
				factor = 2
				low_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = malevolent_personality
					ruler_has_personality = cruel_personality
				}}
			}}
			modifier = {{
				factor = 1.5
				OR = {{
					ruler_has_personality = careful_personality
				}}
			}}
			
			#If Persecuting
			modifier = {{
				factor = 3
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
		}}
		
		random = {{
		chance = 50
		
			event_target:racial_pop_province_target = {{
				add_{0}_minority_size_effect = yes
				add_local_autonomy = 10
			}}
			
			#Boost Dev if Large already
			if = {{
				limit = {{
					event_target:racial_pop_province_target = {{
						OR = {{
							has_large_{0}_minority_trigger = yes
							has_{0}_majority_trigger = yes
						}}
					}}
				}}
				event_target:racial_pop_province_target = {{
					random = {{
						chance = 50
						add_base_production = 1
					}}
				}}
			}}
		}}
		
		
		add_mil_power = -30
		
		large_decrease_of_{0}_tolerance_effect = yes
		
		
	}}
	
}}""".format(race)
    popmenu_start = """
#Pop Menu
country_event = {{
	id = racial_pop_events_{0}.12
	title = racial_pop_events_{0}.12.t
	desc = racial_pop_events_{0}.12.d
	picture = REFUGEES_ESCAPING_eventPicture
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	#Go back
	option = {{		
		name = racial_pop_events_{0}.12.c
		highlight = yes
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 100

		}}
		
		if = {{
			limit = {{
				ai = yes
			}}
			add_country_modifier = {{ 
				name = racial_pop_menu_cooldown
				duration = 3650
				hidden = yes
			}}
			hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
		}}
		else = {{
			country_event = {{ 
				id = racial_pop_misc.1
			}}
		}}
	
	}}""".format(race)
	
    expulsion = """
    #Expulsion
	option = {{		
		name = racial_pop_events_{0}.12.a
		trigger = {{
			NOT = {{
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
			NOT = {{ has_country_modifier = {0}_administration }}
			NOT = {{ has_country_modifier = {0}_military }}
			NOT = {{ ruler_is_{0} = yes }}
			if = {{
				limit = {{
					ai = yes
				}}
				OR = {{
					any_owned_province = {{
						has_{0}_minority_trigger = yes
					}}
					any_owned_province = {{
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
		}}
		ai_chance = {{
			factor = 10
			
			#+Oppressing Race
			modifier = {{
				factor = 1.25
				wants_to_decrease_tolerance_{0} = yes
			}}
			
			#+Want to oppress
			modifier = {{
				factor = 1.25
				wants_to_decrease_tolerance_{0} = yes
			}}
			
			#+Lots of oppressed 
			modifier = {{
				factor = 1.5
				AND = {{
					low_tolerance_{0}_race_trigger = yes
					calc_true_if = {{
						all_owned_province = {{
							has_oppressed_{0}_pop_trigger = yes	
						}}
						amount = 20
					}}
				}}
			}}
			
			#+Negative stability blames issues on other races
			modifier = {{
				factor = 1.25
				stability = -3
				NOT = {{ stability = 0 }}
			}}
			
			#+Unrest in province (as minorities give unrest)
			modifier = {{
				factor = 1.5
				average_unrest = 10
			}}
			
			#+Douche ruler
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = malevolent_personality
					ruler_has_personality = cruel_personality
				}}
			}}
			
			#+If you're a loyal subject you're more inclined to follow overlord's policies
			modifier = {{
				factor = 2
				ROOT = {{
					is_subject = yes
					NOT = {{ liberty_desire = 50 }}
				}}
				overlord = {{ 
					has_country_modifier = racial_pop_{0}_purge
				}}
			}}
			
			
			#+Evil country stuff
			modifier = {{
				factor = 1.25
				OR = {{
					has_country_modifier = evil_nation
					has_country_modifier = lich_ruler
				}}
			}}
			
			#+If you have a enemy or rival
			modifier = {{
				factor = 1.25
				OR = {{
					any_enemy_country = {{
						has_country_modifier = {0}_administration
					}}
					any_rival_country = {{
						has_country_modifier = {0}_administration
					}}

				}}
			}}
			
			#+Monstrous countries more likely to purge
			modifier = {{
				factor = 2
				has_country_modifier = monstrous_nation
			}}
			
			#+If theres a monstrous country and you're NOT monstrous (opposite of above)
			modifier = {{
				factor = 1.5
				AND = {{
					ROOT = {{ NOT = {{ has_country_modifier = {0}_administration }} }}
					any_known_country = {{
						has_country_modifier = {0}_administration
						has_country_modifier = monstrous_nation
					}}
					NOT = {{ is_year = 1700 }} #just a generic time to stop purging I guess?
				}}
			}}
			
			#-Wont do it if theres rebels (as province gives unrest)
			modifier = {{ 
				factor = 0.1
				OR = {{
					num_of_rebel_armies = 3
					num_of_rebel_controlled_provinces = 5
				}}
			}}
			
			#-Anbennar countries more tolerant overall
			modifier = {{ 
				factor = 0.25
				is_part_of_hre = yes
			}}
			
			#-Any loyal subject you wont do it to em
			modifier = {{
				factor = 0.25
				any_subject_country = {{
					NOT = {{ liberty_desire = 50 }}
				}}
			}}
			
			#-If theres a country thats NOT monstrous
			modifier = {{
				factor = 0.75
				any_known_country = {{
					has_country_modifier = {0}_administration
					NOT = {{ has_country_modifier = monstrous_nation }}
				}}
			}}
			
			#-If I have an ally thats this race
			modifier = {{
				factor = 0.1
				any_ally = {{
					has_country_modifier = {0}_administration
				}}
			}}
			
			#-Cant enact if not enough income
			#modifier = {{
			#	factor = 0.5
			#	NOT = {{ monthly_income = 0.5 }}
			#}}
			#No longer costs income
			
			#-Not good adm surplus
			modifier = {{
				factor = 0.75
				NOT = {{ adm_power = 100 }}
			}}
			
			#-Cant do if you have race as country administration or military
			modifier = {{
				factor = 0
				OR = {{
					has_country_modifier = {0}_administration
					has_country_modifier = {0}_military
				}}
			}}
			
			#-Lower chance if good personality
			modifier = {{
				factor = 0.1
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
					ruler_has_personality = careful_personality
					ruler_has_personality = just_personality
				}}
			}}
			
			#-Higher tolerances wont do it
			modifier = {{
				factor = 0.25
				medium_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 0
				high_tolerance_{0}_race_trigger = yes
			}}
			#- Won't do it to overlords race
			modifier = {{
				factor = 0
				ROOT = {{
					is_subject = yes
					NOT = {{ liberty_desire = 50 }}
				}}
				overlord = {{ 
					has_country_modifier = {0}_administration
				}}
			}}
			#Special Stuff""".format(race)
			
    #TODO - Special expel code
    special_expel = getExpelFactors(race, racial_hatred)
	
    purge = """
        }}
		
		hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
		
		country_event = {{ 
			id = racial_pop_events_{0}.13
		}}
		
		add_adm_power = -50
		
		large_decrease_of_{0}_tolerance_effect = yes
		
		add_country_modifier = {{ 
			name = racial_pop_{0}_expulsion
			duration = -1  
		}}
		
		custom_tooltip = racial_pop_events_debug.2.tooltip
		
		custom_tooltip = racial_pop_events_debug.4.tooltip
		
		hidden_effect = {{
			every_owned_province = {{
				limit = {{
					has_small_{0}_minority_trigger = yes
				}}
				add_unrest = 2
			}}
			every_owned_province = {{
				limit = {{
					has_large_{0}_minority_trigger = yes
				}}
				add_unrest = 5
			}}
			every_owned_province = {{
				limit = {{
					has_{0}_majority_trigger = yes
				}}
				add_unrest = 10
			}}
		}}
		
	}}
	
	#Purge
	option = {{		
		name = racial_pop_events_{0}.12.b
		trigger = {{
			NOT = {{
				OR = {{
					has_country_modifier = racial_pop_{0}_purge
					has_country_modifier = racial_pop_{0}_expulsion
				}}
			}}
			NOT = {{ has_country_modifier = {0}_administration }}
			NOT = {{ has_country_modifier = {0}_military }}
			NOT = {{ ruler_is_{0} = yes }}
			if = {{
				limit = {{
					ai = yes
				}}
				OR = {{
					any_owned_province = {{
						has_{0}_minority_trigger = yes
					}}
					any_owned_province = {{
						has_{0}_majority_trigger = yes
					}}
				}}
			}}
			NOT = {{ has_country_modifier = forced_to_end_{0}_purge }}
		}}
		ai_chance = {{
			factor = 5
			
			#+Want to oppress
			modifier = {{
				factor = 1.25
				wants_to_decrease_tolerance_{0} = yes
			}}
			
			#+Lots of oppressed 
			modifier = {{
				factor = 1.5
				AND = {{
					low_tolerance_{0}_race_trigger = yes
					calc_true_if = {{
						all_owned_province = {{
							has_oppressed_{0}_pop_trigger = yes	
						}}
						amount = 20
					}}
				}}
			}}
			
			#+Negative stability blames issues on other races
			modifier = {{
				factor = 1.25
				stability = -3
				NOT = {{ stability = 0 }}
			}}
			
			#+Unrest in province (as minorities give unrest)
			modifier = {{
				factor = 1.5
				average_unrest = 10
			}}
			
			#+Douche ruler
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = malevolent_personality
					ruler_has_personality = cruel_personality
				}}
			}}
			
			#+If you're a loyal subject you're more inclined to follow overlord's policies
			modifier = {{
				factor = 2
				ROOT = {{
					is_subject = yes
					NOT = {{ liberty_desire = 50 }}
				}}
				overlord = {{ 
					has_country_modifier = racial_pop_{0}_purge
				}}
			}}
			
			#+Corrupt countries purge
			modifier = {{
				factor = 1.25
				corruption = 3
			}}
			
			#+Evil country stuff
			modifier = {{
				factor = 1.5
				OR = {{
					has_country_modifier = evil_nation
					has_country_modifier = lich_ruler
				}}
			}}
			
			#+If you have a enemy or rival
			modifier = {{
				factor = 1.25
				OR = {{
					any_enemy_country = {{
						has_country_modifier = {0}_administration
					}}
					any_rival_country = {{
						has_country_modifier = {0}_administration
					}}

				}}
			}}
			
			#+Monstrous countries more likely to purge
			modifier = {{
				factor = 3
				has_country_modifier = monstrous_nation
			}}
			
			#+If theres a monstrous country and you're NOT monstrous (opposite of above)
			modifier = {{
				factor = 2
				AND = {{
					ROOT = {{ NOT = {{ has_country_modifier = {0}_administration }} }}
					any_known_country = {{
						has_country_modifier = {0}_administration
						has_country_modifier = monstrous_nation
					}}
					NOT = {{ is_year = 1700 }} #just a generic time to stop purging I guess?
				}}
			}}
			
			#-Wont do it if theres rebels (as province gives unrest)
			modifier = {{ 
				factor = 0.1
				OR = {{
					num_of_rebel_armies = 3
					num_of_rebel_controlled_provinces = 5
				}}
			}}
			
			#-Anbennar countries more tolerant overall
			modifier = {{ 
				factor = 0.25
				is_part_of_hre = yes
			}}
			
			#-Any loyal subject you wont do it to em
			modifier = {{
				factor = 0.25
				NOT = {{ diplomatic_reputation = 1 }}
			}}
			
			#-Any loyal subject you wont do it to em
			modifier = {{
				factor = 0.25
				any_subject_country = {{
					NOT = {{ liberty_desire = 50 }}
				}}
			}}
			
			#-Less likely if not great power
			modifier = {{
				factor = 0.8
				NOT = {{ is_great_power = yes }}
			}}
			
			#-If theres a country thats NOT monstrous - WAY LOWER CHANCE to purge because of this, as you're more likely to purge monstrous in general
			modifier = {{
				factor = 0.1
				any_known_country = {{
					has_country_modifier = {0}_administration
					NOT = {{ has_country_modifier = monstrous_nation }}
				}}
			}}
			
			#-If I have an ally thats this race
			modifier = {{
				factor = 0.1
				any_ally = {{
					has_country_modifier = {0}_administration
				}}
			}}
			
			#-Cant enact if not enough income
			#modifier = {{
			#	factor = 0.5
			#	NOT = {{ monthly_income = 0.5 }}
			#}}
			#No longer costs income
			
			#-Not good adm surplus
			modifier = {{
				factor = 0.75
				NOT = {{ adm_power = 150 }}
			}}
			
			#-Cant do if you have race as country administration or military
			modifier = {{
				factor = 0
				OR = {{
					has_country_modifier = {0}_administration
					has_country_modifier = {0}_military
				}}
			}}
			
			#-Lower chance if good personality
			modifier = {{
				factor = 0.1
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
					ruler_has_personality = careful_personality
					ruler_has_personality = just_personality
				}}
			}}
			
			#-Humanists dont do it
			modifier = {{
				factor = 0
				has_idea_group = humanist_ideas
			}}
			
			#-Diplomats dont do it
			modifier = {{
				factor = 0
				personality = ai_diplomat
			}}
			
			#-Higher tolerances wont do it
			modifier = {{
				factor = 0.25
				medium_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 0
				high_tolerance_{0}_race_trigger = yes
			}}
			#- Won't do it to overlords race
			modifier = {{
				factor = 0
				ROOT = {{
					is_subject = yes
					NOT = {{ liberty_desire = 50 }}
				}}
				overlord = {{ 
					has_country_modifier = {0}_administration
				}}
			}}
			
			#Race Specific""".format(race)
			
#TODO - Special purge stuff here
    special_purge = getPurgeFactors(race, racial_hatred)

    end_expel = """
                }}
		
		hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
		
		country_event = {{ 
			id = racial_pop_events_{0}.14
		}}
		
		add_adm_power = -100
		
		largest_decrease_of_{0}_tolerance_effect = yes
		
		add_country_modifier = {{ 
			name = racial_pop_{0}_purge
			duration = -1  
		}}
		
		custom_tooltip = racial_pop_events_debug.3.tooltip
		
		custom_tooltip = racial_pop_events_debug.4.tooltip
		
		hidden_effect = {{
			every_owned_province = {{
				limit = {{
					has_small_{0}_minority_trigger = yes
				}}
				add_unrest = 5
			}}
			every_owned_province = {{
				limit = {{
					has_large_{0}_minority_trigger = yes
				}}
				add_unrest = 7
			}}
			every_owned_province = {{
				limit = {{
					has_{0}_majority_trigger = yes
				}}
				add_unrest = 15
			}}
		}}
	
	}}
	
	#Cannot Expel as you're Purging
	option = {{		
		name = racial_pop_events_{0}.12.f
		trigger = {{
			has_country_modifier = racial_pop_{0}_expulsion
		}}
		ai_chance = {{
			factor = 0
		}}
		country_event = {{ 
			id = racial_pop_misc.1
		}}
	}}
	
	#Cannot Purge as you're Purging
	option = {{		
		name = racial_pop_events_{0}.12.g
		trigger = {{
			has_country_modifier = racial_pop_{0}_purge
		}}
		ai_chance = {{
			factor = 0
		}}
		
		country_event = {{ 
			id = racial_pop_misc.1
		}}
		
	}}
	
	#Cannot Purge as you're forced to stop
	option = {{		
		name = racial_pop_events_{0}.12.h
		highlight = yes
		trigger = {{
			has_country_modifier = forced_to_end_{0}_purge
		}}
		ai_chance = {{
			factor = 0
		}}
		
		country_event = {{ 
			id = racial_pop_misc.1
		}}
	}}
	
	#End Expulsion
	option = {{		
		name = racial_pop_events_{0}.12.dd
		trigger = {{
			has_country_modifier = racial_pop_{0}_expulsion
			NOT = {{ has_country_modifier = racial_pop_menu_cooldown }}
		}}
		ai_chance = {{
			factor = 20
			
			#+low diplo reputation
			modifier = {{
				factor = 1.5
				NOT = {{ diplomatic_reputation = -3 }}
			}}
			
			#+Should remove asap if country administration or military
			modifier = {{
				factor = 10
				OR = {{
					has_country_modifier = {0}_administration
					has_country_modifier = {0}_military
				}}
			}}
			
			#+If want to like race
			modifier = {{
				factor = 2
				wants_to_increase_tolerance_{0} = yes
			}}
			
			#+If race is in good standing
			modifier = {{
				factor = 10
				medium_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 20
				high_tolerance_{0}_race_trigger = yes
			}}
			
			#+Any loyal subject you wont do it to em
			modifier = {{
				factor = 2
				any_subject_country = {{
					NOT = {{ liberty_desire = 50 }}
				}}
			}}
			
			#+If I have an ally thats this race
			modifier = {{
				factor = 5
				any_ally = {{
					has_country_modifier = {0}_administration
				}}
			}}
			
			#+If good personality
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
					ruler_has_personality = careful_personality
					ruler_has_personality = just_personality
				}}
			}}
			
			#+Humanists want to stop it
			modifier = {{
				factor = 10
				has_idea_group = humanist_ideas
			}}
			
			#+Bankrupt countries cannot expel
			modifier = {{
				factor = 5
				is_bankrupt = yes
			}}
			
			#+If you're a loyal subject you're more inclined to follow overlord's policies
			modifier = {{
				factor = 10
				ROOT = {{
					is_subject = yes
					NOT = {{ liberty_desire = 50 }}
				}}
				overlord = {{ 
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
			}}
			
		}}
		
		add_adm_power = -50
		hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
		
		country_event = {{ 
			id = racial_pop_events_{0}.15
		}}
	
	}}""".format(race)
    
    special_end_expel = getEndExpelFactors(race)
	
    end_purge = """
    #End Purge
	option = {{		
		name = racial_pop_events_{0}.12.e
		trigger = {{
			has_country_modifier = racial_pop_{0}_purge
			NOT = {{ has_country_modifier = racial_pop_menu_cooldown }}
		}}
		ai_chance = {{
			factor = 20
			
			#+low diplo reputation
			modifier = {{
				factor = 1.5
				NOT = {{ diplomatic_reputation = -3 }}
			}}
			
			#+Should remove asap if country administration or military
			modifier = {{
				factor = 10
				OR = {{
					has_country_modifier = {0}_administration
					has_country_modifier = {0}_military
				}}
			}}
			
			#+If want to like race
			modifier = {{
				factor = 2
				wants_to_increase_tolerance_{0} = yes
			}}
			
			#+If race is in good standing
			modifier = {{
				factor = 10
				medium_tolerance_{0}_race_trigger = yes
			}}
			modifier = {{
				factor = 20
				high_tolerance_{0}_race_trigger = yes 
			}}
			
			#+Any loyal subject you wont do it to em
			modifier = {{
				factor = 2
				any_subject_country = {{
					NOT = {{ liberty_desire = 50 }}
				}}
			}}
			
			#+If I have an ally thats this race
			modifier = {{
				factor = 5
				any_ally = {{
					has_country_modifier = {0}_administration
				}}
			}}
			
			#+If good personality
			modifier = {{
				factor = 2
				OR = {{
					ruler_has_personality = tolerant_personality
					ruler_has_personality = kind_hearted_personality
					ruler_has_personality = benevolent_personality
					ruler_has_personality = careful_personality
					ruler_has_personality = just_personality
				}}
			}}
			
			#+Humanists want to stop it
			modifier = {{
				factor = 10
				has_idea_group = humanist_ideas
			}}
			
			#+Bankrupt countries cannot expel
			modifier = {{
				factor = 5
				is_bankrupt = yes
			}}
			
			#+If you're a loyal subject you're more inclined to follow overlord's policies
			modifier = {{
				factor = 10
				ROOT = {{
					is_subject = yes
					NOT = {{ liberty_desire = 50 }}
				}}
				overlord = {{ 
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
			}}""".format(race)
            
    special_end_purge = getEndPurgeFactors(race)
        
    end = """}}
		
		add_adm_power = -100
		
		hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
		
		country_event = {{ 
			id = racial_pop_events_{0}.16
		}}
	
	}}
	
	#You cannot purge a race that administers your country or contains the bulk of your army
	option = {{		
		name = racial_pop_events_debug.1.a
		trigger = {{
			OR = {{
				has_country_modifier = {0}_administration
				has_country_modifier = {0}_military
				ruler_is_{0} = yes
			}}
		}}
		ai_chance = {{
			factor = 1

		}}
		custom_tooltip = racial_pop_events_debug.1.tooltip
		country_event = {{ 
			id = racial_pop_misc.1
		}}
	
	}}
	
	# Set Focus
	option = {{		
		name = racial_pop_events_debug.1.d
		ai_chance = {{
			factor = 0
		}}
		trigger = {{
			NOT = {{ has_racial_focus = yes }}
		}}
		add_dip_power = -50
		add_country_modifier = {{
			name = racial_focus_{0}
			duration = -1
		}}
		custom_tooltip = racial_event_increase_tt
		hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
	}}

	# Remove Focus
	option = {{		
		name = racial_pop_events_debug.1.e
		ai_chance = {{
			factor = 0
		}}
		trigger = {{
			has_country_modifier = racial_focus_{0}
		}}
		remove_country_modifier = racial_focus_{0}
		hidden_effect = {{ clr_country_flag = racial_pop_menu_opened }}
	}}
	
	# Already set focus
	option = {{		
		name = racial_pop_events_debug.1.c
        highlight = yes
		trigger = {{
			has_racial_focus = yes
			NOT = {{ has_country_modifier = racial_focus_{0} }}
		}}
		ai_chance = {{
			factor = 0
		}}
		country_event = {{ 
			id = racial_pop_misc.1
		}}
	
	}}
}}	


#Expulsion Reveal
country_event = {{
	id = racial_pop_events_{0}.13
	title = racial_pop_events_{0}.13.t
	desc = racial_pop_events_{0}.13.d
	picture = REFUGEES_ESCAPING_eventPicture
	
	major = yes
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{

	}}
	
	#Begin Expulsion of [race]
	option = {{		
		name = racial_pop_events_{0}.13.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 10
		}}
		
		custom_tooltip = racial_pop_events_debug.5.tooltip
		
		hidden_effect = {{
			country_event = {{
				id = race_setup_events.9
				days = 1
			}}
			
		}}
	
		
		#Trigger one of them events
	}}
	
	# #Take backsies for player only so they can see what the modifier does (they still lose the adm for doing this tho)
	# option = {{		
		# name = racial_pop_events_debug.1.b
		# trigger = {{
			# ai = no
		# }}
		# ai_chance = {{
			# factor = 1

		# }}
		
		# country_event = {{ 
			# id = racial_pop_misc.1
		# }}
	
	# }}

}}


#Purge Reveal
country_event = {{
	id = racial_pop_events_{0}.14
	title = racial_pop_events_{0}.14.t
	desc = racial_pop_events_{0}.14.d
	picture = PLAGUE_eventPicture
	
	major = yes
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{

	}}
	
	#Begin Expulsion of [race]
	option = {{		
		name = racial_pop_events_{0}.14.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 10
		}}
		
		hidden_effect = {{
			country_event = {{
				id = race_setup_events.9
				days = 1
			}}
		}}
		
		custom_tooltip = racial_pop_events_debug.6.tooltip
		
		#Trigger one of them events
	}}

}}


#Expulsion End
country_event = {{
	id = racial_pop_events_{0}.15
	title = racial_pop_events_{0}.15.t
	desc = racial_pop_events_{0}.15.d
	picture = REFUGEES_ESCAPING_eventPicture
	
	major = yes
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{

	}}
	
	#End Expulsion of [race]
	option = {{		
		name = racial_pop_events_{0}.15.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 10
		}}
		
		remove_country_modifier = racial_pop_{0}_expulsion
		
		hidden_effect = {{
			country_event = {{
				id = race_setup_events.9
				days = 1
			}}
		}}
		
		custom_tooltip = racial_pop_events_debug.7.tooltip
		
	}}

}}


#Purge End
country_event = {{
	id = racial_pop_events_{0}.16
	title = racial_pop_events_{0}.16.t
	desc = racial_pop_events_{0}.16.d
	picture = PLAGUE_eventPicture
	
	major = yes
	
	trigger = {{
	
	}}
	
	is_triggered_only = yes
	
	mean_time_to_happen = {{
		days = 1
	}}
	
	immediate = {{

	}}
	
	#End Purge of [race]
	option = {{		
		name = racial_pop_events_{0}.16.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 10
		}}
		
		remove_country_modifier = racial_pop_{0}_purge
		
		hidden_effect = {{
			country_event = {{
				id = race_setup_events.9
				days = 1
			}}
		}}
		
		custom_tooltip = racial_pop_events_debug.8.tooltip
		
	}}

}}


#Expulsion - Minority Expelled
country_event = {{
	id = racial_pop_events_{0}.17
	title = racial_pop_events_{0}.17.t
	desc = racial_pop_events_{0}.17.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		has_country_modifier = racial_pop_{0}_expulsion
		
		any_owned_province = {{
			has_{0}_minority_trigger = yes
		}}
	}}
	
	mean_time_to_happen = {{
		days = 1825
		modifier = {{
			factor = 0.1
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 100
			}}
		}}
		modifier = {{
			factor = 0.5
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 50
			}}
		}}
		modifier = {{
			factor = 0.75
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 25
			}}
		}}
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 0.4
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.55
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.75
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.25
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_minority_trigger = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
	
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
			
		#Which country to migrate to
		hidden_effect = {{
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					high_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					OR = {{
						medium_tolerance_{0}_race_trigger = yes
						high_tolerance_{0}_race_trigger = yes
					}}
					any_owned_province = {{
						development = 20
						NOT = {{ has_{0}_minority_trigger = yes }}
						NOT = {{ has_{0}_majority_trigger = yes }}
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.17.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
			add_devastation = 10
		}}
	
		#Calls Migrants Arrive to Migration Country
		if = {{	#only does this if they have an adjacent country
			limit = {{
				any_neighbor_country = {{ 
					NOT = {{ low_tolerance_{0}_race_trigger = yes }}
				}}
			}}
			event_target:racial_pop_migration_country  = {{
				country_event = {{
					id = racial_pop_events_{0}.10
					days = 14
					random = 31
				}}
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
	}}
	
	option = {{		#Special: Greedy confiscate
		name = racial_pop_events_{0}.17.b
		trigger = {{ ruler_has_personality = greedy_personality }}
		highlight = yes
		ai_chance = {{
			factor = 100
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
			add_devastation = 10
		}}
	
		#Calls Migrants Arrive to Migration Country
		if = {{	#only does this if they have an adjacent country
			limit = {{
				any_neighbor_country = {{ 
					NOT = {{ low_tolerance_{0}_race_trigger = yes }}
				}}
			}}
			event_target:racial_pop_migration_country  = {{
				country_event = {{
					id = racial_pop_events_{0}.10
					days = 14
					random = 31
				}}
			}}
		}}
		
		if = {{
			limit = {{
				event_target:racial_pop_province_origin = {{
					development = 20
				}}
			}}
			add_treasury = 50
		}}
		else = {{
			add_treasury = 10
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
	}}
	
}}


#Expulsion - Majority Expelled
country_event = {{
	id = racial_pop_events_{0}.18
	title = racial_pop_events_{0}.18.t
	desc = racial_pop_events_{0}.18.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		has_country_modifier = racial_pop_{0}_expulsion
		
		any_owned_province = {{
			has_{0}_majority_trigger = yes
			culture_is_{0} = yes
		}}
	}}
	
	mean_time_to_happen = {{
		days = 2737
		modifier = {{
			factor = 0.1
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 100
			}}
		}}
		modifier = {{
			factor = 0.5
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 50
			}}
		}}
		modifier = {{
			factor = 0.75
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 25
			}}
		}}
		
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 0.4
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.55
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.75
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.25
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_majority_trigger = yes
					# culture_is_{0} = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
	
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
			
		#Which country to migrate to
		hidden_effect = {{
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					high_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					OR = {{
						medium_tolerance_{0}_race_trigger = yes
						high_tolerance_{0}_race_trigger = yes
					}}
					any_owned_province = {{
						development = 20
						NOT = {{ has_{0}_minority_trigger = yes }}
						NOT = {{ has_{0}_majority_trigger = yes }}
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.18.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			change_culture = ROOT
			change_religion = ROOT
			add_devastation = 30
		}}
	
		#Calls Migrants Arrive to Migration Country
		if = {{	#only does this if they have an adjacent country
			limit = {{
				any_neighbor_country = {{ 
					NOT = {{ low_tolerance_{0}_race_trigger = yes }}
				}}
			}}
			event_target:racial_pop_migration_country  = {{
				country_event = {{
					id = racial_pop_events_{0}.10
					days = 14
					random = 31
				}}
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
	}}
	
}}


#Purge - Minority Purged
country_event = {{
	id = racial_pop_events_{0}.19
	title = racial_pop_events_{0}.19.t
	desc = racial_pop_events_{0}.19.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		has_country_modifier = racial_pop_{0}_purge
		
		any_owned_province = {{
			has_{0}_minority_trigger = yes
		}}
	}}
	
	mean_time_to_happen = {{
		days = 3650
		modifier = {{
			factor = 0.1
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 100
			}}
		}}
		modifier = {{
			factor = 0.5
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 50
			}}
		}}
		modifier = {{
			factor = 0.75
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 25
			}}
		}}
		
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 0.4
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.55
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.75
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.25
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_minority_trigger = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
	
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.19.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
			add_devastation = 20
		}}
		
		large_decrease_of_{0}_tolerance_effect = yes
	}}
	
	option = {{		#Special: Evil Purge them entirely
		name = racial_pop_events_{0}.19.b
		trigger = {{ 
			ruler_has_personality = cruel_personality 
			event_target:racial_pop_province_origin = {{
				has_large_{0}_minority_trigger = yes
			}}
		}}
		highlight = yes
		ai_chance = {{
			factor = 100
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
			remove_{0}_minority_size_effect = yes
			add_devastation = 20
		}}
		
		large_decrease_of_{0}_tolerance_effect = yes
	}}
	
}}


#Purge - Majority Purged
country_event = {{
	id = racial_pop_events_{0}.20
	title = racial_pop_events_{0}.20.t
	desc = racial_pop_events_{0}.20.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		has_country_modifier = racial_pop_{0}_purge
		
		any_owned_province = {{
			has_{0}_majority_trigger = yes
			culture_is_{0} = yes
		}}
	}}
	
	mean_time_to_happen = {{
		days = 5475
		modifier = {{
			factor = 0.1
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 100
			}}
		}}
		modifier = {{
			factor = 0.5
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 50
			}}
		}}
		modifier = {{
			factor = 0.75
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 25
			}}
		}}
		
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 0.4
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.55
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.75
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.25
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_majority_trigger = yes
					# culture_is_{0} = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
	
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.20.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			add_devastation = 30
			change_culture = ROOT
			change_religion = ROOT
			random_list = {{
				1 = {{
					add_base_tax = -1
				}}
				1 = {{
					add_base_production = -1
				}}
				1 = {{
					add_base_manpower = -1
				}}
			}}
			
			hidden_effect = {{
				remove_province_modifier = {0}_majority_oppressed
				remove_province_modifier = {0}_majority_coexisting
				remove_province_modifier = {0}_majority_integrated
			}}
		}}
		
		large_decrease_of_{0}_tolerance_effect = yes
	}}
	
	
}}



#Purge - Minority Flees
country_event = {{
	id = racial_pop_events_{0}.21
	title = racial_pop_events_{0}.21.t
	desc = racial_pop_events_{0}.21.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		has_country_modifier = racial_pop_{0}_purge
		
		any_owned_province = {{
			has_{0}_minority_trigger = yes
		}}
	}}
	
	mean_time_to_happen = {{
		days = 1825
		modifier = {{
			factor = 0.1
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 100
			}}
		}}
		modifier = {{
			factor = 0.5
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 50
			}}
		}}
		modifier = {{
			factor = 0.75
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_minority_trigger = yes
				}}
				amount = 25
			}}
		}}
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 0.4
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.55
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.75
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.25
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
						# has_{0}_minority_trigger = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
					# has_{0}_minority_trigger = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_minority_trigger = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
	
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_minority_trigger = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
			
		#Which country to migrate to
		hidden_effect = {{
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					high_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					OR = {{
						medium_tolerance_{0}_race_trigger = yes
						high_tolerance_{0}_race_trigger = yes
					}}
					any_owned_province = {{
						development = 20
						NOT = {{ has_{0}_minority_trigger = yes }}
						NOT = {{ has_{0}_majority_trigger = yes }}
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.17.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		#Remove Minority from Origin Province
		event_target:racial_pop_province_origin = {{
			remove_{0}_minority_size_effect = yes
			add_devastation = 10
		}}
	
		#Calls Migrants Arrive to Migration Country
		if = {{	#only does this if they have an adjacent country
			limit = {{
				any_neighbor_country = {{ 
					NOT = {{ low_tolerance_{0}_race_trigger = yes }}
				}}
			}}
			event_target:racial_pop_migration_country  = {{
				country_event = {{
					id = racial_pop_events_{0}.10
					days = 14
					random = 31
				}}
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
	}}
	
	
}}


#Purge - Majority Flees
country_event = {{
	id = racial_pop_events_{0}.22
	title = racial_pop_events_{0}.22.t
	desc = racial_pop_events_{0}.22.d
	picture = REFUGEES_ESCAPING_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		has_country_modifier = racial_pop_{0}_purge
		
		any_owned_province = {{
			has_{0}_majority_trigger = yes
			culture_is_{0} = yes
		}}
	}}
	
	mean_time_to_happen = {{
		days = 2555
		modifier = {{
			factor = 0.1
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 100
			}}
		}}
		modifier = {{
			factor = 0.5
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 50
			}}
		}}
		modifier = {{
			factor = 0.75
			calc_true_if = {{
				all_owned_province = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				amount = 25
			}}
		}}
		
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 0.4
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.55
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.75
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.25
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_majority_trigger = yes
					# culture_is_{0} = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
	
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
			
			
		#Which country to migrate to
		hidden_effect = {{
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					medium_tolerance_{0}_race_trigger = yes
					any_owned_province = {{
						development = 20
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					high_tolerance_{0}_race_trigger = yes
				}}
				save_event_target_as = racial_pop_migration_country
			}}
			random_neighbor_country = {{
				limit = {{
					NOT = {{ has_country_modifier = racial_pop_{0}_purge }}
					NOT = {{ has_country_modifier = racial_pop_{0}_expulsion }}
					OR = {{
						medium_tolerance_{0}_race_trigger = yes
						high_tolerance_{0}_race_trigger = yes
					}}
					any_owned_province = {{
						development = 20
						NOT = {{ has_{0}_minority_trigger = yes }}
						NOT = {{ has_{0}_majority_trigger = yes }}
					}}
				}}
				save_event_target_as = racial_pop_migration_country
			}}
		}}
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.17.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		#Remove majority from Origin Province
		event_target:racial_pop_province_origin = {{
			add_devastation = 30
			change_culture = ROOT
			change_religion = ROOT
			random_list = {{
				1 = {{
					add_base_tax = -1
				}}
				1 = {{
					add_base_production = -1
				}}
				1 = {{
					add_base_manpower = -1
				}}
			}}
			
			hidden_effect = {{
				remove_province_modifier = {0}_majority_oppressed
				remove_province_modifier = {0}_majority_coexisting
				remove_province_modifier = {0}_majority_integrated
			}}
		}}
	
		#Calls Migrants Arrive to Migration Country
		if = {{	#only does this if they have an adjacent country
			limit = {{
				any_neighbor_country = {{ 
					NOT = {{ low_tolerance_{0}_race_trigger = yes }}
				}}
			}}
			event_target:racial_pop_migration_country  = {{
				country_event = {{
					id = racial_pop_events_{0}.10
					days = 14
					random = 31
				}}
			}}
		}}
		
		medium_decrease_of_{0}_tolerance_effect = yes
	}}
	
	
}}



#Purge/Expel - Majority Unrest
country_event = {{
	id = racial_pop_events_{0}.23
	title = racial_pop_events_{0}.23.t
	desc = racial_pop_events_{0}.23.d
	picture = ANGRY_MOB_eventPicture
	goto = racial_pop_province_origin
	
	trigger = {{
		OR = {{
			has_country_modifier = racial_pop_{0}_purge
			has_country_modifier = racial_pop_{0}_expulsion
		}}
		
		any_owned_province = {{
			has_{0}_majority_trigger = yes
			culture_is_{0} = yes
			NOT = {{ unrest = 20 }}
		}}
	}}
	
	mean_time_to_happen = {{
		days = 1850
		
		modifier = {{
			factor = 0.75
			
			has_country_modifier = racial_pop_{0}_purge
		}}
		
		#Distances
		# Removing these has caused a vast increase in purging MTTH.
		# Until (something similar?) is re-implemented, sharply cutting purge times.
		modifier = {{ factor = 0.5 always = yes }}

		# modifier = {{
			# factor = 1.5
			
			# NOT = {{
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.3
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 50
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 25
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 1.1
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 75
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 50
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.8
			
			# AND = {{
				# NOT = {{
					# capital_scope = {{
						# any_owned_province = {{
							# has_{0}_majority_trigger = yes
							# culture_is_{0} = yes
							
							# province_distance = {{
								# who = PREV
								# distance = 125
							# }}
						# }}
					# }}
				# }}
				# capital_scope = {{
					# any_owned_province = {{
						# has_{0}_majority_trigger = yes
						# culture_is_{0} = yes
						
						# province_distance = {{
							# who = PREV
							# distance = 100
						# }}
					# }}
				# }}
			# }}
		# }}
		
		# modifier = {{
			# factor = 0.5
			
			# capital_scope = {{
				# any_owned_province = {{
					# has_{0}_majority_trigger = yes
					# culture_is_{0} = yes
					
					# province_distance = {{
						# who = PREV
						# distance = 125
					# }}
				# }}
			# }}
		# }}
	}}
	
	immediate = {{
		#Origin Province Setter
		
		#Make this the monstrous purge thing
		hidden_effect = {{
			random_owned_province = {{
				limit = {{
					has_{0}_majority_trigger = yes
					culture_is_{0} = yes
				}}
				save_event_target_as = racial_pop_province_origin
			}}
		}}
		
	}}
	
	#Good Riddance!
	option = {{		
		name = racial_pop_events_{0}.23.a
		trigger = {{
			
		}}
		ai_chance = {{
			factor = 50
		}}
		
		if = {{
			limit = {{
				has_country_modifier = racial_pop_{0}_expulsion
			}}
			#Remove majority from Origin Province
			event_target:racial_pop_province_origin = {{
				add_devastation = 5
				add_unrest = 5
			}}
		}}
		
		if = {{
			limit = {{
				has_country_modifier = racial_pop_{0}_purge
			}}
			#Remove majority from Origin Province
			event_target:racial_pop_province_origin = {{
				add_devastation = 10
				add_unrest = 10
			}}
		}}
		
		
		small_decrease_of_{0}_tolerance_effect = yes
	}}
}}""".format(race)

    all = start + popmenu_start + expulsion + special_expel + purge + special_purge + end_expel + special_end_expel + end_purge + special_end_purge + end
    return(all)


def create_race_file(race):
	filename = "anb_racial_pop_events_{0}.txt".format(race)
	print("Creating File:" + filename)
	with open(filename, 'w') as f:
		f.write(getRaceText(race, racial_hatred))

for race in races:
    create_race_file(race)
input()