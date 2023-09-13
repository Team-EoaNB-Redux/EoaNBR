# Economy Documenation
### Written by Strat
This file contains the documenation for the various effects, triggers, and modifiers.

Presume by default that tooltips are done for you.

```
Effects
(Country Scope)
- Add Months of Income
- Add Treasury
- Adjust Budget
- Add Loan
- Remove Loan
- Borrow Money
- Repay Debt
- Adjust Trade

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
</table>

## Modifiers

## Triggers