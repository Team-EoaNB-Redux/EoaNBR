# Economy Documenation
### Written by Strat
This file contains the documenation for the various effects, triggers, and modifiers.

Presume by default that tooltips are done for you.

```
Effects
(Country Scope)
- Copy over Economy Stuff for new tags
- Subsume Economic Stuff

- Add Months of Income
- Add Treasury
- Adjust Budget
- Add Loans
- Remove Loans
- Borrow Money
- Repay Debt
- Adjust Trade

- Set Budget Slider Maximum
- Set Budget Slider Minimum

- Improve Economic Situation
- Worsen Economic Situation
- Set Economic Situation
- Generate Investment Opportunity
- Generate All Investment Opportunities

- Create Project
- Cancel Project
- Clear Projects
- Complete Project

(State Scope)
- Add Population
- Migrate Population
- Construct Buildings
- Remove Buildings
- Cancel Construction
- Upgrade Production Method
- Set Production Method

Triggers
(Country Scope)
- has_x_gdp
- has_x_gdp_per_c
- has_x_average_sol
- has_x_debt
- has_x_treasury
- has_x_months_of_income
- has_x_tax_revenue
- has_x_spending
- has_x_net_budget

- has_x_workforce
- has_x_capitalists
- has_x_aristocrats
- has_x_investment_income
- has_x_investment_spending
- has_attractive_opportunity

- has_x_supply
- has_x_demand
- has_x_production
- has_x_trade
- has_x_offers
- has_x_balance
- has_x_relative_price
- has_x_relative_balance

- has_x_consumer_confidence
- has_x_investment_confidence
- has_x_banking_confidence

(State Scope)
- has_buildings (Include specific buildings/pms/size)
- has_construction
- has_arable_land
- has_deposits
- has_free_deposits
- has_spare_industrial_capacity
- has_gdp_growth
- is_profitable
- has_production

- has_x_building_count
- has_x_productivity
- has_x_wage
- has_x_gdp
- has_x_gdp_per_c
- has_x_workforce
- has_x_available_workforce
- has_x_peasants
- has_x_unemployed
- has_x_unemployed_percent
- has_x_employed
- has_x_average_sol

- has_x_supply
- has_x_demand
- has_x_production
- has_x_balance
- has_x_relative_price
- has_x_relative_balance

Modifiers
(Country Scope)
- banking_confidence_modifier
- consumer_confidence_modifier
- investment_confidence_modifier
- tax_efficiency_factor
- corruption_factor
- bureaucratic_efficiency_factor
- aristocrats_investment_contribution_factor
- capitalists_investment_contribution_factor
- government_investment_efficiency_factor

- building_construction_speed_factor
- building_construction_cost_factor
- building_upgrade_speed_factor
- building_upgrade_cost_factor
- building_input_factor
- building_output_factor
- building_throughput_factor
- building_attractiveness_modifier
- building_attractiveness_factor
- building_industrial_capacity_use_factor

- building_subsistence_agriculture_input_factor
- building_subsistence_agriculture_output_factor
- building_subsistence_farm_input_factor
- building_subsistence_farm_output_factor
- building_rice_paddy_input_factor
- building_rice_paddy_output_factor

- building_factory_input_factor
- building_factory_output_factor
- building_factory_throughput_factor
- building_factory_attractiveness_modifier
- building_factory_attractiveness_factor
- building_factory_industrial_capacity_use_factor

- building_agriculture_input_factor
- building_agriculture_output_factor
- building_agriculture_throughput_factor
- building_agriculture_attractiveness_modifier
- building_agriculture_attractiveness_factor
- building_agriculture_industrial_capacity_use_factor

- building_plantation_input_factor
- building_plantation_output_factor
- building_plantation_throughput_factor
- building_plantation_attractiveness_modifier
- building_plantation_attractiveness_factor
- building_plantation_industrial_capacity_use_factor

- building_resource_input_factor
- building_resource_output_factor
- building_resource_throughput_factor
- building_resource_attractiveness_modifier
- building_resource_attractiveness_factor
- building_resource_industrial_capacity_use_factor

- building_transport_input_factor
- building_transport_output_factor
- building_transport_throughput_factor
- building_transport_industrial_capacity_factor
- building_transport_shipping_capacity_factor
- building_transport_attractiveness_modifier
- building_transport_attractiveness_factor

- building_[type]_input_factor
- building_[type]_output_factor
- building_[type]_throughput_factor
- building_[type]_attractiveness_modifier
- building_[type]_attractiveness_factor
- building_[type]_industrial_capacity_use_factor

(State Scope)
- local_building_construction_speed_factor
- local_building_construction_cost_factor
- local_building_upgrade_speed_factor
- local_building_upgrade_cost_factor
- local_building_input_factor
- local_building_output_factor
- local_building_throughput_factor
- local_building_attractiveness_modifier
- local_building_attractiveness_factor
- local_building_industrial_capacity_use_factor

- local_building_subsistence_agriculture_input_factor
- local_building_subsistence_agriculture_output_factor
- local_building_subsistence_farm_input_factor
- local_building_subsistence_farm_output_factor
- local_building_rice_paddy_input_factor
- local_building_rice_paddy_output_factor

- local_building_factory_input_factor
- local_building_factory_output_factor
- local_building_factory_throughput_factor
- local_building_factory_attractiveness_modifier
- local_building_factory_attractiveness_factor
- local_building_factory_industrial_capacity_use_factor

- local_building_agriculture_input_factor
- local_building_agriculture_output_factor
- local_building_agriculture_throughput_factor
- local_building_agriculture_attractiveness_modifier
- local_building_agriculture_attractiveness_factor
- local_building_agriculture_industrial_capacity_use_factor

- local_building_plantation_input_factor
- local_building_plantation_output_factor
- local_building_plantation_throughput_factor
- local_building_plantation_attractiveness_modifier
- local_building_plantation_attractiveness_factor
- local_building_plantation_industrial_capacity_use_factor

- local_building_resource_input_factor
- local_building_resource_output_factor
- local_building_resource_throughput_factor
- local_building_resource_attractiveness_modifier
- local_building_resource_attractiveness_factor
- local_building_resource_industrial_capacity_use_factor

- local_building_transport_input_factor
- local_building_transport_output_factor
- local_building_transport_throughput_factor
- local_building_transport_industrial_capacity_factor
- local_building_transport_shipping_capacity_factor
- local_building_transport_attractiveness_modifier
- local_building_transport_attractiveness_factor

- local_building_[type]_input_factor
- local_building_[type]_output_factor
- local_building_[type]_throughput_factor
- local_building_[type]_attractiveness_modifier
- local_building_[type]_attractiveness_factor
- local_building_[type]_industrial_capacity_use_factor

Variables (Read-Only)
``````

## Effects
<table>
    <tr>
        <th>Name</th>
        <th>Parameters</th>
        <th>Examples</th>
        <th>Description</th>
        <th>Notes</th>
        <th>Scope</th>
    </tr>
    <tr>
        <td> add_months_of_income </td>
        <td> <code> x_temp = float </code> <br> Months of revenue to add/subtract to treasury. </td>
        <td> <code> set_temp_variable = { x_temp = 5 } <br> add_months_of_income = yes </code> </td>
        <td> Adds or subtracts money to your treasury. Subtracting treasury beyond negatives will add debt. Amount is relative to your government revenue. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> add_treasury </td>
        <td> <code> x_temp = float </code> <br> Amount to add/subtract to treasury. </td>
        <td> <code> set_temp_variable = { x_temp = 500 } <br> add_treasury = yes </code> </td>
        <td> Adds or subtracts money to your treasury. Subtracting treasury beyond negatives will add debt. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> set_treasury </td>
        <td> <code> x_temp = float </code> <br> Amount to set treasury to. </td>
        <td> <code> set_temp_variable = { x_temp = 500 } <br> set_treasury = yes </code> </td>
        <td> Sets your treasury to this amount. Setting treasury to a negative value will add debt and reset treasury to 0. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> set_budget </td>
        <td> <code> upper_tax_temp = integer <br> middle_tax_temp = integer <br> lower_tax_temp = integer <br> sales_tax_temp = integer <br> corporate_tax_temp = integer <br> import_tariff_temp = integer <br> export_tariff_temp = integer <br> <br> military_spending_temp = integer <br> construction_spending_temp = integer <br> import_subsidies_temp = integer <br> export_subsidies_temp = integer <br> research_subsidies_temp = integer </code> <br> What to set each slider. Sliders go from 0 to 100. Set the value to a negative value to set it to 0. Zero values are ignored. </td>
        <td> <code> set_temp_variable = { upper_tax_temp = -1 } <br> set_temp_variable = { construction_spending_temp = 100 } <br> set_budget = yes </code> </td>
        <td> Sets the sliders in your budget. Does not cost political power. Setting values beyond the minimum/maximum will get them auto-corrected to the minimum/maximum. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> adjust_budget </td>
        <td> <code> upper_tax_temp = integer <br> middle_tax_temp = integer <br> lower_tax_temp = integer <br> sales_tax_temp = integer <br> corporate_tax_temp = integer <br> import_tariff_temp = integer <br> export_tariff_temp = integer <br> <br> military_spending_temp = integer <br> construction_spending_temp = integer <br> import_subsidies_temp = integer <br> export_subsidies_temp = integer <br> research_subsidies_temp = integer </code> <br> How much to adjust each slider. Sliders go from 0 to 100. Negative values will decrease the slider. </td>
        <td> <code> set_temp_variable = { upper_tax_temp = 50 } <br> set_temp_variable = { middle_tax_temp = 25 } <br> adjust_budget = yes </code> </td>
        <td> Adjusts the sliders in your budget. Does not cost political power. Adjusting values beyond the minimum/maximum will get them auto-corrected to the minimum/maximum. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> set_budget_maximum </td>
        <td> <code> upper_tax_temp = integer <br> middle_tax_temp = integer <br> lower_tax_temp = integer <br> sales_tax_temp = integer <br> corporate_tax_temp = integer <br> import_tariff_temp = integer <br> export_tariff_temp = integer <br> <br> military_spending_temp = integer <br> construction_spending_temp = integer <br> import_subsidies_temp = integer <br> export_subsidies_temp = integer <br> research_subsidies_temp = integer </code> <br> What to cap each slider at. Sliders go from 0 to 100. To cap at 0, set integer to any negative value. Values of 0 will be ignored. </td>
        <td> <code> set_temp_variable = { upper_tax_temp = 50 } <br> set_temp_variable = { middle_tax_temp = 75 } <br> set_budget_maximum = yes </code> </td>
        <td> Caps the sliders in your budget. Auto adjusts sliders if sliders are over the new maximum. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> set_budget_minimum </td>
        <td> <code> upper_tax_temp = integer <br> middle_tax_temp = integer <br> lower_tax_temp = integer <br> sales_tax_temp = integer <br> corporate_tax_temp = integer <br> import_tariff_temp = integer <br> export_tariff_temp = integer <br> <br> military_spending_temp = integer <br> construction_spending_temp = integer <br> import_subsidies_temp = integer <br> export_subsidies_temp = integer <br> research_subsidies_temp = integer </code> <br> What to cap each slider at. Sliders go from 0 to 100. To cap at 0, set integer to any negative value. Values of 0 will be ignored. </td>
        <td> <code> set_temp_variable = { upper_tax_temp = -1 } <br> set_temp_variable = { middle_tax_temp = 25 } <br> set_budget_minimum = yes </code> </td>
        <td> Caps the sliders in your budget. Auto adjusts sliders if sliders are under the new minimum. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> add_debt </td>
        <td> <code> x_temp = float </code> <br> Amount of debt to add/remove. <br> <code> debt_level_temp = float </code> <br> Amount of debt levels to add/remove. </td>
        <td> <code> set_temp_variable = { x_temp = 500 } <br> add_debt = yes <br> // OR <br> set_temp_variable = { debt_level_temp = 2 } add_debt = yes </code> </td>
        <td> Adds or removes debt. Does not affect treasury. Automatically converts into debt level. Checks for bankruptcy on addition.</td>
        <td> Using both x_temp and debt_level_temp on the same effect will apply both. They are applied first before bankruptcy condition is checked. </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> borrow_money </td>
        <td> <code> x_temp = float </code> <br> Amount of money to borrow. Only positive float values accepted. </td>
        <td> <code> set_temp_variable = { x_temp = 500 } <br> borrow_money = yes </code> </td>
        <td> Adds this amount of debt to the country. Also adds to your treasury. Automatically converts into debt level. </td>
        <td> Bankruptcy clears your treasury. </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> repay_debt </td>
        <td> <code> x_temp = float </code> <br> Amount of money to repay. Only positive float values accepted. </td>
        <td> <code> set_temp_variable = { x_temp = 500 } <br> add_treasury = yes </code> </td>
        <td> Adds or subtracts money to your treasury. Subtracting treasury beyond negatives will add debt. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> adjust_trade </td>
        <td> <code> resource_temp = token:resource </code> <br> Resource to adjust. To set, use token:resource_token. <br> <code> x_temp = float </code> <br> Amount to add/subtract to treasury. </td>
        <td> <code> set_temp_variable = { resource_temp = token:resource_consumer_goods } <br> set_temp_variable = { x_temp = 20 } <br> adjust_trade = yes </code> </td>
        <td> Adjusts trade offers. Positive values increase imports/decrease exports while negative values increase exports/decrease imports. </td>
        <td> Resource tokens are found both under common/resources/00_resources.txt and common/ideas/_economy_tokens.txt</td>
        <td> Country </td>
    </tr>
    <tr>
        <td> improve_economic_situation </td>
        <td> </td>
        <td> <code> improve_economic_situation = yes </code> </td>
        <td> Improves the economic situation by one level. </td>
        <td> Economic situation is found under common/ideas/0_eoanb_state_country.txt </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> worsen_economic_situation </td>
        <td> </td>
        <td> <code> worsen_economic_situation = yes </code> </td>
        <td> Worsens the economic situation by one level. </td>
        <td> Economic situations are found under common/ideas/0_eoanb_state_country.txt </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> set_economic_situation </td>
        <td> <code> situation_temp = token:economic_situation </code> <br> Economic situation to set </td>
        <td> <code> set_temp_variable = { situation_temp = token:depression } <br> set_economic_situation = yes </code> </td>
        <td> Sets the economic situation to the given level. </td>
        <td> Economic situations are found under common/ideas/0_eoanb_state_country.txt </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> generate_investment_opportunity </td>
        <td> </td>
        <td> <code> generate_investment_opportunity = yes </code> </td>
        <td> Generates a new investment opportunity. Does not generate a new investment opportunity if already at IO cap. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> generate_all_investment_opportunities </td>
        <td> </td>
        <td> <code> generate_all_investment_opportunities = yes </code> </td>
        <td> Generates investment opportunities until cap is reached. Does not generate a new investment opportunity if already at IO cap. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> proj_create </td>
        <td> <code> project_token_temp = token:project_token </code> <br> Project to create <br> <code> project_state_temp = STATE </code> <br> (Potentially Required) If project is a state-project, then provide a state <br> <code> relative_temp = float </code> <br> (Potentially Required) If project has relative cost, then provide a scaling for its completion requirements </td>
        <td> <code> set_temp_variable = { project_token_temp = token:work_programs } <br> proj_create = yes </code> </td>
        <td> Creates a project. </td>
        <td> List of projects can be found under common/ideas/_economy_projects_tokens.txt </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> proj_cancel </td>
        <td> <code> project_token_temp = token:project_token </code> <br> Project to create <br> <code> project_state_temp = STATE </code> <br> (Potentially Required) If project is a state-project, then provide a state. </td>
        <td> <code> set_temp_variable = { project_token_temp = token:work_programs } <br> proj_cancel = yes </code> </td>
        <td> Cancels a project currently in progress. If project doesn't exist, then the effect does nothing. </td>
        <td> List of projects can be found under common/ideas/_economy_projects_tokens.txt </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> proj_complete </td>
        <td> <code> project_token_temp = token:project_token </code> <br> Project to create <br> <code> project_state_temp = STATE </code> <br> (Potentially Required) If project is a state-project, then provide a state. </td>
        <td> <code> set_temp_variable = { project_token_temp = token:work_programs } <br> proj_complete = yes </code> </td>
        <td> Completes a project currently in progress. Its effects fire immediately. Does not fire the effects if the project didn't exist. </td>
        <td> List of projects can be found under common/ideas/_economy_projects_tokens.txt </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> proj_clear </td>
        <td> </td>
        <td> <code> proj_clear = yes </code> </td>
        <td> Cancels all projects currently in-progress. </td>
        <td> </td>
        <td> Country </td>
    </tr>
    <tr>
        <td> add_population </td>
        <td> <code> x_temp = float </code> <br> Population (in thousands) to add </td>
        <td> <code> set_temp_variable = { x_temp = 12.3 } <br> add_population = yes </code> </td>
        <td> Adds population to the state whilst updating various population-related values. </td>
        <td> </td>
        <td> State </td>
    </tr>
    <tr>
        <td> migrate_population </td>
        <td> <code> x_temp = float </code> <br> Population (in thousands) to leave from this state <br> <code> state_temp = STATE </code> <br> State for pops to migrate to <br> <code> culture_temp = token:culture_token </code> <br> (Optional) Which culture to migrate <br> <code> religion_temp = token:religion_token </code> <br> (Optional) Which religion to migrate <br> <code> ignore_demographics = 0 or 1 </code> <br> (Optional) If non-zero, will only migrate population and ignore moving culture/religion </td>
        <td> <code> set_temp_variable = { x_temp = 12.3 } <br> set_temp_variable = { state_temp = 12 } <br> migrate_population = yes </code> </td>
        <td> Migrates pops from the currently scoped state to another state. Carries over culture & religion by default. <br> If amount is greater than population present, will migrate all. <br> Migrating with culture & religion set will cap migration amount to min(culture, religion) </td>
        <td> Culture and Religion tokens are under common/ideas/_eoanbr_demographic_tokens.txt </td>
        <td> State </td>
    </tr>
    <tr>
        <td> construct_x_buildings </td>
        <td> <code> x_temp = integer </code> <br> (Optional) Amount of buildings of the given type to build. Default is 1. <br> <code> financier_temp = SCOPE </code> (Optional) The entity that is financing this construction. Default, 0, is local, a state scope is a corporation (if present), country scope is government. <br> <code> building_token = token:building </code> <br> Building type to be built. <br> <code> production_method_temp = integer </code> <br> (Optional) Production method for the building to be set to. Default is latest available. Use -1 for basic production method. </td>
        <td> <code> set_temp_variable = { x_temp = 1 } <br> set_temp_variable = { financer_temp = ROOT } <br> set_temp_variable = { building_token = token:building_consumer_goods_factory } <br> set_temp_variable = { production_method_temp = -1 } <br> construct_x_buildings = yes </code> </td>
        <td> Starts construction of the given building type in the state. Does NOT allow Rice Paddies/Subsistence Farms. If provided a production method that is too advanced (that you don't have tech for  or the building doesn't support) or simple (that the building doesn't support), then it will auto adjust. However, if there is not a valid PM available, then the building will not start construction. Negative values do NOT work.. </td>
        <td> Building tokens can be found under common/ideas/_economy_tokens.txt </td>
        <td> State </td>
    </tr>
    <tr>
        <td> remove_x_buildings </td>
        <td> <code> x_temp = integer </code> <br> (Optional) Amount of buildings of the given type to remove. Default is 1. <br> <code> building_token = token:building </code> <br> Building type to be removed. </td>
        <td> <code> set_temp_variable = { x_temp = 1 } <br> set_temp_variable = { building_token = token:building_consumer_goods_factory } <br> remove_x_buildings = yes </code> </td>
        <td> Removes X buildings from the state. Does NOT allow removal of Rice Paddies/Subsistence Farms. Negative values do NOT work. Any building which reaches size 0 will be removed from the state. </td>
        <td> Building tokens can be found under common/ideas/_economy_tokens.txt </td>
        <td> State </td>
    </tr>
    <tr>
        <td> cancel_building_construction </td>
        <td> <code> building_token = token:building </code> <br> (Optional) Which building to stop construction of. Default is to stop all construction in a state. </td>
        <td> set_temp_variable = { building_token = token:building_consumer_goods_factory } <br> cancel_building_construction = yes </code> </td>
        <td> Cancels the construction of one or all buildings in a state. Does not refund construction.. </td>
        <td> Building tokens can be found under common/ideas/_economy_tokens.txt </td>
        <td> State </td>
    </tr>
    <tr>
        <td> upgrade_production_method </td>
        <td> <code> building_token = token:building </code> <br> Building type to be upgraded. <br> <code> financier_temp = SCOPE </code> (Optional) The entity that is financing this upgrade. Default, 0, is local, a state scope is a corporation (if present), country scope is government. </td>
        <td> <code> set_temp_variable = { financier_temp = ROOT } <br> set_temp_variable = { building_token = token:building_consumer_goods_factory } <br> upgrade_production_method = yes </code> </td>
        <td> Starts the upgrade of a building's production method. Does not start upgrading if the financier doesn't have the tech. </td>
        <td> Building tokens can be found under common/ideas/_economy_tokens.txt. Do not worry about the financier just yet. Production Method upgrades haven't been implemented yet, so this effect currently just increases a building's production method by 1. </td>
        <td> State </td>
    </tr>
    <tr>
        <td> set_production_method </td>
        <td> <code> building_token = token:building </code> <br> Which building's production method is to be changed. <br> <code> production_method_temp = integer </code> <br> (Optional) Production method for the building to be set to. Default is latest available. Use -1 for basic production method. </td>
        <td> <code> set_temp_variable = { building_token = token:building_consumer_goods_factory } <br> set_production_method = yes </code> </td>
        <td> Changes the production method of a building. There is no upgrade process nor cost. </td>
        <td> Building tokens can be found under common/ideas/_economy_tokens.txt </td>
        <td> State </td>
    </tr>
</table>

## Modifiers

## Triggers