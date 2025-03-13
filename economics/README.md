# Economics ToE Meta-Model
## A Declarative Framework for Agents, Markets, and Economic Dynamics

Covers basic and advanced economic entities—agents, markets, goods, transactions, supply-demand constraints, utility/budget, macro indicators, policies, plus a top-level scenario aggregator. Each entity is designed so it can be executed with no extra sidecar logic: all rules are captured using Schema (S), Data (D), Lookups (L), Aggregations (A), and Calculated Fields (F).

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Economics

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
The Economics extension of the CMCC (Conceptual Model Completeness Conjecture) provides a unified, Snapshot-Consistent structure for modeling economic agents, transactions, markets, and policy rules. By leveraging CMCC’s five fundamental primitives—Schema, Data, Lookups, Aggregations, and Lambda formulas—it captures everything from microeconomic supply-demand dynamics to macroeconomic indicators, bridging them seamlessly with other domains such as mathematics, AI, or even quantum-inspired decision models.

![Economics ToE Meta-Model Entity Diagram](economics.png)
#### Depends On:
- CMCC_ToEMM_Math


### Key Points
- Encodes agents, markets, and transactions as first-class entities with aggregator-based rules (e.g., equilibrium checks, utility maximization).
- Integrates advanced domain logic—like monetary policies or auction mechanisms—purely as declarative data references.
- Facilitates multi-agent simulations via aggregator formulas, bridging micro-level decisions with macro-level outcomes.
- Aligns with the rest of CMCC domains, allowing cross-disciplinary analysis (e.g., game-theoretic approaches using shared mathematics entities).

### Implications
- Simplifies synergy between economics and other fields, enabling direct references to math or AI models for forecasting or agent intelligence.
- Increases reproducibility: economic “theories” are stored as aggregator constraints, ensuring consistent application across data sets.
- Enables Turing-complete scenario analysis without specialized code, providing uniform access to agent-based or equilibrium-based computations.

### Narrative
#### CMCC Economics Extension
Economics is often a balancing act of micro and macro phenomena, traditionally handled by disparate models or software. By placing everything—agents, utility functions, market clearing conditions—in a single Snapshot-Consistent schema, we achieve uniformity and cross-model reusability.
This model treats supply-demand curves, monetary rules, and even advanced scenario simulators (like agent-based modeling) as purely declarative aggregator formulas. Agents can reference AI-based lambda functions for decision logic, while the system tracks equilibrium or stability via aggregator constraints. This integration with the broader CMCC environment permits mathematically rigorous yet flexible modeling of economic phenomena, bridging everything from simple supply-demand charts to large-scale global trade simulations.


---

# Schema Overview

## Entity: FinancialScenarioRecord

**Description**: A top-level container for an economic or financial scenario, linking agents, markets, macro data, and policy instruments at a given time horizon.

### Fields
- **scenario_id**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_description**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_metadata**  
  *Type:* scalar, *Datatype:* json  
  

### Lookups
- **linked_agents**  
  *Target Entity:* EconomicAgent, *Type:* one_to_many  
    
  (Join condition: **EconomicAgent.scenario_id = this.scenario_id**)  
  *Description:* All EconomicAgents associated with this scenario. The agent table references scenario_id.
- **linked_markets**  
  *Target Entity:* Market, *Type:* one_to_many  
    
  (Join condition: **Market.scenario_id = this.scenario_id**)  
  *Description:* Markets that operate within this scenario.
- **linked_indicators**  
  *Target Entity:* MacroIndicator, *Type:* one_to_many  
    
  (Join condition: **MacroIndicator.scenario_id = this.scenario_id**)  
  *Description:* Macro Indicators (e.g. GDP, inflation) that belong to this scenario.
- **linked_policies**  
  *Target Entity:* PolicyInstrument, *Type:* one_to_many  
    
  (Join condition: **PolicyInstrument.scenario_id = this.scenario_id**)  
  *Description:* All policy instruments (taxes, interest rates) active in this scenario.

### Aggregations
- **scenario_total_liquid_assets**  
  *Description:* Sums all agents’ liquid_assets in this scenario, giving a total liquidity measure.  
  *Formula:* `SUM(linked_agents.liquid_assets)`
- **scenario_total_gdp**  
  *Description:* Retrieves the scenario’s current GDP measure (if stored in MacroIndicator).  
  *Formula:* `LOOKUP(linked_indicators WHERE indicator_name='GDP').indicator_value`
- **total_market_supply_vs_demand**  
  *Description:* A scenario-level aggregator that checks if markets collectively have supply-demand imbalances.  
  *Formula:* `Σ over all linked_markets => (total_supply - total_demand). Summed or listed individually.`
- **scenario_gini_coefficient**  
  *Description:* Computes the scenario’s Gini coefficient using each agent’s net_worth_estimate.  
  *Formula:* `ComputeGiniCoefficient( linked_agents.net_worth_estimate )`
- **scenario_total_tax_revenue**  
  *Description:* Totals all taxes/fees collected across transactions in this scenario.  
  *Formula:* `SUM( FOR ALL agent in linked_agents => SUM(agent.transactions.tax_or_fee_amount) )`
- **scenario_money_velocity**  
  *Description:* Approximates money velocity by total transaction value divided by the money supply.  
  *Formula:* `IF( LOOKUP(linked_indicators WHERE indicator_name='MoneySupply') != null ) THEN ( SUM(ALL transactions.net_value_after_tax ) / LOOKUP(linked_indicators WHERE indicator_name='MoneySupply').indicator_value ) ELSE null`
- **scenario_unemployment_rate**  
  *Description:* Retrieves or references the scenario’s unemployment rate from MacroIndicator.  
  *Formula:* `LOOKUP(linked_indicators WHERE indicator_name='UnemploymentRate').indicator_value`
- **scenario_credit_utilization**  
  *Description:* Measures how much of the total available credit is in use across all agents.  
  *Formula:* `SUM(linked_agents.outstanding_debt) / SUM(linked_agents.credit_line)`
- **scenario_inflation_adjusted_gdp**  
  *Description:* Adjusts nominal GDP by the inflation rate in the scenario.  
  *Formula:* `IF(LOOKUP(linked_indicators WHERE indicator_name='InflationRate')!=null, scenario_total_gdp / (1 + (LOOKUP(linked_indicators WHERE indicator_name='InflationRate').indicator_value / 100)), scenario_total_gdp)`
- **scenario_savings_rate**  
  *Description:* Approximate ratio of total agent savings to the scenario GDP.  
  *Formula:* `IF(scenario_total_gdp>0, (SUM(linked_agents.net_worth_estimate) - SUM(linked_agents.liquid_assets) /* or track changes in net worth? */ ) / scenario_total_gdp, null)`
- **average_labor_cost**  
  *Description:* Looks for transactions referencing labor or services to approximate average labor cost.  
  *Formula:* `AVG( FOR ALL tx in ALL linked_markets.transactions => IF(tx.type='demand' AND tx.notes LIKE '%labor%', tx.price_per_unit, null ) )`
- **scenario_inflation_adjusted_money_velocity**  
  *Description:* Adjusts the base money velocity aggregator for inflation in the scenario.  
  *Formula:* `IF( scenario_money_velocity != null AND LOOKUP(linked_indicators WHERE indicator_name='InflationRate')!=null, scenario_money_velocity / (1 + (LOOKUP(linked_indicators WHERE indicator_name='InflationRate').indicator_value / 100)), scenario_money_velocity )`
- **scenario_corporate_tax_revenue**  
  *Description:* Total taxes collected from corporate-type agents across all transactions in this scenario.  
  *Formula:* `SUM( FOR ALL agent in linked_agents WHERE agent.agent_type IN ['firm','corporate'] => SUM( agent.transactions.tax_or_fee_amount ) )`
- **scenario_household_savings_rate**  
  *Description:* Ratio of total net worth of consumer agents to scenario GDP, as a naive measure of household savings.  
  *Formula:* `IF(scenario_total_gdp > 0, (SUM( FOR ALL agent in linked_agents WHERE agent.agent_type='consumer' => agent.net_worth_estimate ) / scenario_total_gdp), null)`
- **scenario_velocity_of_firms**  
  *Description:* Firm-specific velocity of money; sums transaction flows from 'firm' agents over the scenario's money supply.  
  *Formula:* `IF( LOOKUP(linked_indicators WHERE indicator_name='MoneySupply') != null, (SUM( FOR ALL tx in ALL linked_agents.transactions WHERE agent.agent_type IN ['firm','corporate'] => tx.net_value_after_tax ) / LOOKUP(linked_indicators WHERE indicator_name='MoneySupply').indicator_value ), null)`
- **scenario_domestic_vs_foreign_balance**  
  *Description:* Compares total domestic transaction volume vs. foreign-labeled transactions. Positive => domestic surplus.  
  *Formula:* `LET domestic = SUM( transactions WHERE notes LIKE '%domestic%' ), foreign = SUM( transactions WHERE notes LIKE '%foreign%' ); RETURN (domestic - foreign)`
- **scenario_interest_payment_burden**  
  *Description:* Fraction of scenario GDP consumed by total interest payments across all agents.  
  *Formula:* `IF(scenario_total_gdp>0, (SUM( linked_agents.debt_service_cost ) / scenario_total_gdp), null)`
- **scenario_public_debt_ratio**  
  *Description:* Naive public debt to GDP ratio by summing all 'government' agents' debt over scenario GDP.  
  *Formula:* `LET gov_debt = SUM( FOR ALL agent in linked_agents WHERE agent.agent_type='government' => agent.outstanding_debt ); IF(scenario_total_gdp>0, gov_debt / scenario_total_gdp, null)`
- **scenario_household_vs_firm_wealth_gap**  
  *Description:* Difference between total household (consumer) net worth and total firm/producer net worth in this scenario.  
  *Formula:* `SUM(linked_agents, a => IF(a.agent_type='consumer', a.net_worth_estimate, 0)) - SUM(linked_agents, a => IF(a.agent_type='firm' OR a.agent_type='producer', a.net_worth_estimate, 0))`
- **scenario_agent_bankruptcy_count**  
  *Description:* Number of agents whose net worth is negative AND flagged high risk—naively considered 'bankrupt'.  
  *Formula:* `COUNT(linked_agents, a => IF(a.default_risk_flag='HIGH_RISK' AND a.net_worth_estimate < 0, true, false))`
- **scenario_real_disposable_income_total**  
  *Description:* Sums each agent’s disposable income adjusted by the scenario inflation rate, if present.  
  *Formula:* `SUM(linked_agents, a => a.disposable_income_estimate / IF(LOOKUP(linked_indicators, i => i.indicator_name='InflationRate')!=null, (1 + (LOOKUP(linked_indicators, i => i.indicator_name='InflationRate').indicator_value / 100)), 1))`
- **scenario_trade_balance**  
  *Description:* Naive difference between total export-labeled transaction value and total import-labeled value across all agents.  
  *Formula:* `SUM(ALL linked_agents.transactions, t => IF(t.notes LIKE '%export%' OR t.notes LIKE '%domestic_export%', t.net_value_after_tax, 0)) - SUM(ALL linked_agents.transactions, t => IF(t.notes LIKE '%import%' OR t.notes LIKE '%foreign_import%', t.net_value_after_tax, 0))`
- **scenario_average_loan_interest**  
  *Description:* Average interest rate (as a %) across indebted agents: total interest cost / total debt.  
  *Formula:* `IF(COUNT(linked_agents, a => a.outstanding_debt>0)>0, (SUM(linked_agents, a => a.debt_service_cost) / SUM(linked_agents, a => IF(a.outstanding_debt>0, a.outstanding_debt, 0))) * 100, null)`

### Lambdas
- **run_global_economic_update**
    
  *Formula:* `For each linked_policies => apply_instrument(...). Then update linked_indicators via update_indicator.`


---

## Entity: EconomicAgent

**Description**: Represents an individual or organization in the economy. Extended to store scenario links, net worth, and credit lines. All new logic is purely declarative.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **agent_name**  
  *Type:* scalar, *Datatype:* string  
  
- **agent_type**  
  *Type:* scalar, *Datatype:* string  
  
- **liquid_assets**  
  *Type:* scalar, *Datatype:* float  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **credit_line**  
  *Type:* scalar, *Datatype:* float  
  
- **outstanding_debt**  
  *Type:* scalar, *Datatype:* float  
  

### Lookups
- **transactions**  
  *Target Entity:* Transaction, *Type:* one_to_many  
    
  (Join condition: **Transaction.agent_id = this.id**)  
  *Description:* All transactions (supply or demand) performed by this agent.

### Aggregations
- **net_worth_estimate**  
  *Description:* A naive net worth ignoring intangible assets, real estate, or equity.  
  *Formula:* `liquid_assets - outstanding_debt`
- **transaction_count**  
  *Description:* Count how many transaction records reference this agent.  
  *Formula:* `COUNT(transactions)`
- **available_credit**  
  *Description:* How much credit remains for this agent.  
  *Formula:* `credit_line - outstanding_debt`
- **real_net_worth**  
  *Description:* Adjusts the agent’s net worth estimate for inflation, if an inflation rate is present.  
  *Formula:* `IF( LOOKUP(scenario_id.linked_indicators WHERE indicator_name='InflationRate') != null ) THEN ( net_worth_estimate / (1 + (LOOKUP(scenario_id.linked_indicators WHERE indicator_name='InflationRate').indicator_value / 100)) ) ELSE net_worth_estimate`
- **default_risk_flag**  
  *Description:* Simple heuristic that flags high-risk if debt is more than 3x the agent’s liquid assets.  
  *Formula:* `IF( (outstanding_debt / GREATEST(liquid_assets,1)) > 3, 'HIGH_RISK', 'OK' )`
- **debt_service_cost**  
  *Description:* Estimates the agent’s interest cost by multiplying debt by the scenario’s interest rate policy.  
  *Formula:* `IF( scenario_id.linked_policies != null ) THEN ( outstanding_debt * FindInterestRate(scenario_id.linked_policies) ) ELSE 0`
- **consumption_expenditure**  
  *Description:* Total spending on demanded goods by the agent in this scenario.  
  *Formula:* `SUM( transactions WHERE type='demand' => net_value_after_tax )`
- **predicted_spending_next_period**  
  *Description:* A naive consumption function: base=100 plus 60% of net worth.  
  *Formula:* `(100 + 0.6 * net_worth_estimate)`
- **propensity_to_save**  
  *Description:* A simplistic ratio of consumption to current liquid assets, inverted to represent saving.  
  *Formula:* `IF( transaction_count>0, 1 - (consumption_expenditure / (liquid_assets+0.0001)), 0 )`
- **leverage_ratio**  
  *Description:* Indicates how leveraged an agent is, ignoring intangible assets.  
  *Formula:* `outstanding_debt / GREATEST(net_worth_estimate, 1)`
- **average_unit_cost_of_supplies**  
  *Description:* If this agent also buys inputs, calculates average price for those goods demanded.  
  *Formula:* `AVG( FOR ALL t in transactions WHERE t.type='demand' => t.price_per_unit )`
- **disposable_income_estimate**  
  *Description:* Approximates the agent's disposable income ignoring intangible/capital assets.  
  *Formula:* `net_worth_estimate + available_credit - debt_service_cost`
- **labor_income_share**  
  *Description:* Fraction of total inflows derived from labor/wage transactions for this agent.  
  *Formula:* `LET labor_income = SUM( transactions WHERE type='demand' AND (notes LIKE '%labor%' OR notes LIKE '%wage%') => net_value_after_tax ); LET total_inflow = SUM( transactions WHERE type='supply' => net_value_after_tax ) + labor_income; IF(total_inflow>0, labor_income / total_inflow, 0)`
- **consumption_vs_income_ratio**  
  *Description:* How much of the agent's disposable income is spent on consumption.  
  *Formula:* `IF(disposable_income_estimate>0, (consumption_expenditure / disposable_income_estimate), 0)`
- **agent_tax_burden**  
  *Description:* Total tax/fees paid by this agent across all transactions.  
  *Formula:* `SUM( transactions.tax_or_fee_amount )`
- **credit_utilization_ratio**  
  *Description:* Measures how much of the agent's total credit line is still unused.  
  *Formula:* `IF(credit_line>0, available_credit / credit_line, null)`
- **agent_effective_tax_rate**  
  *Description:* Percentage of this agent’s gross transaction value that went to taxes/fees.  
  *Formula:* `IF(SUM(transactions, t => t.total_value)>0, (SUM(transactions, t => t.tax_or_fee_amount) / SUM(transactions, t => t.total_value))*100, 0)`
- **agent_financial_stress_index**  
  *Description:* Simple ratio: debt / (liquid_assets+unused credit). Higher => more financial stress. Arbitrary 9999 if denominator=0.  
  *Formula:* `IF((liquid_assets + available_credit)>0, (outstanding_debt / (liquid_assets + available_credit)), 9999)`
- **agent_investment_propensity**  
  *Description:* Measures fraction of net worth the agent invests (based on demand transactions flagged as 'capital_investment').  
  *Formula:* `IF(net_worth_estimate>0, (SUM(transactions, tx => IF(tx.type='demand' AND tx.notes LIKE '%capital_investment%', tx.net_value_after_tax, 0)) / net_worth_estimate), 0)`
- **agent_average_price_paid**  
  *Description:* Agent-specific average price per unit for all 'demand' transactions they made.  
  *Formula:* `IF(COUNT(transactions, tx => tx.type='demand')>0, (SUM(transactions, tx => IF(tx.type='demand', tx.total_value, 0)) / SUM(transactions, tx => IF(tx.type='demand', tx.quantity, 0))), null)`

### Lambdas
- **apply_interest**
  (Parameters: interest_rate)  
  *Formula:* `IF outstanding_debt>0 => outstanding_debt += outstanding_debt * interest_rate`

### Constraints
- **non_negative_assets**  
  *Formula:* `liquid_assets >= 0`  
  *Error Message:* Agent's liquid_assets cannot be negative
- **credit_line_positive**  
  *Formula:* `credit_line >= 0`  
  *Error Message:* Agent's credit_line must not be negative

---

## Entity: GoodOrService

**Description**: A discrete product or service that can be traded in markets. This remains mostly unchanged, but with more descriptive metadata.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **category**  
  *Type:* scalar, *Datatype:* string  
  
- **unit_of_measure**  
  *Type:* scalar, *Datatype:* string  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: Market

**Description**: A marketplace or exchange for one or more goods, referencing scenario and aggregator fields for clearing, supply, demand.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **market_name**  
  *Type:* scalar, *Datatype:* string  
  
- **good_id**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **opening_time**  
  *Type:* scalar, *Datatype:* datetime  
  
- **closing_time**  
  *Type:* scalar, *Datatype:* datetime  
  
- **clearing_price**  
  *Type:* scalar, *Datatype:* float  
  

### Lookups
- **transactions**  
  *Target Entity:* Transaction, *Type:* one_to_many  
    
  (Join condition: **Transaction.market_id = this.id**)  
  *Description:* All transactions posted in this market.

### Aggregations
- **total_supply**  
  *Description:* Aggregates the total quantity of supply transactions in this market.  
  *Formula:* `SUM(transactions.quantity) WHERE transactions.type='supply'`
- **total_demand**  
  *Description:* Aggregates the total quantity of demand transactions in this market.  
  *Formula:* `SUM(transactions.quantity) WHERE transactions.type='demand'`
- **equilibrium_check**  
  *Description:* If >0 => surplus; if <0 => shortage; if =0 => balanced at current prices.  
  *Formula:* `total_supply - total_demand`
- **median_transaction_price**  
  *Description:* The median posted transaction price in the market so far.  
  *Formula:* `MEDIAN(transactions.price_per_unit)`
- **approx_price_elasticity**  
  *Description:* Naive aggregator that compares changes in clearing_price vs. total_demand to estimate elasticity.  
  *Formula:* `ComputeElasticityOverTime( clearing_price, total_demand )`
- **producer_surplus**  
  *Description:* Naive aggregator for producer surplus, requires a reference_cost or average cost assumption.  
  *Formula:* `SUM( transactions WHERE type='supply' => (price_per_unit - reference_cost) * quantity )`
- **consumer_surplus**  
  *Description:* Naive aggregator for consumer surplus, referencing a 'willingness_to_pay' assumption if available.  
  *Formula:* `SUM( transactions WHERE type='demand' => (willingness_to_pay - price_per_unit) * quantity )`
- **market_tax_collected**  
  *Description:* Totals the taxes or fees collected in this market.  
  *Formula:* `SUM( transactions.tax_or_fee_amount )`
- **price_volatility**  
  *Description:* Standard deviation of transaction prices as a volatility proxy.  
  *Formula:* `STDDEV(transactions.price_per_unit)`
- **turnover_rate**  
  *Description:* Roughly how quickly goods are being traded among distinct agents.  
  *Formula:* `IF( total_supply>0, (total_supply / COUNT(DISTINCT transactions.agent_id)), null )`
- **herfindahl_index**  
  *Description:* Measures market concentration by summing squared supply shares of each agent.  
  *Formula:* `Let supply_by_agent = SUM( quantity ) grouped by agent_id, total = SUM( supply_by_agent ). Return SUM over each agent of ( supply_by_agent/ total )^2.`
- **average_time_between_trades**  
  *Description:* Average time difference between consecutive transactions for this market.  
  *Formula:* `ComputeAverageTimeDelta(transactions.transaction_timestamp) // conceptual function that measures avg delta among consecutive trades`
- **largest_supplier_share**  
  *Description:* Share of total supply from the largest individual supplier.  
  *Formula:* `LET supply_by_agent = GROUP_SUM( transactions WHERE type='supply' => quantity, by agent_id ); LET total = SUM(supply_by_agent); MAX( for each agent => supply_by_agent[agent]/ total )`
- **largest_buyer_share**  
  *Description:* Share of total demand from the largest individual buyer.  
  *Formula:* `LET demand_by_agent = GROUP_SUM( transactions WHERE type='demand' => quantity, by agent_id ); LET total = SUM(demand_by_agent); MAX( for each agent => demand_by_agent[agent]/ total )`
- **daytime_vs_peak_trades_ratio**  
  *Description:* Ratio of transactions occurring in the first 2 hours after opening to all trades in the day.  
  *Formula:* `LET early_window = COUNT( transactions WHERE transaction_timestamp BETWEEN (opening_time) AND (opening_time + 2h) ); LET total_trades = COUNT(transactions); IF(total_trades>0, (early_window / total_trades), null)`
- **excess_inventory_cost**  
  *Description:* Estimates cost of unsold inventory if partial matching logic is stored, referencing a hypothetical 'reference_cost_of_storage'.  
  *Formula:* `IF( partial_matches_tracked, SUM( unmatched_supply.quantity * reference_cost_of_storage ), 0 )`
- **supply_demand_imbalance_ratio**  
  *Description:* Ratio of total_supply to total_demand. If demand=0 but supply>0 => large ratio (9999 as a placeholder).  
  *Formula:* `IF(total_demand>0, total_supply / total_demand, IF(total_supply>0, 9999, 1))`
- **highest_transaction_price**  
  *Description:* Finds the maximum posted price among all transactions in this market.  
  *Formula:* `MAX(transactions, tx => tx.price_per_unit)`
- **consumer_buyer_count**  
  *Description:* Number of unique agent_ids that posted 'demand' transactions in this market.  
  *Formula:* `COUNT( DISTINCT(MAP(FILTER(transactions, tx => tx.type='demand'), x => x.agent_id)) )`
- **total_transaction_value**  
  *Description:* Sum of gross transaction value (quantity * price) for all trades in this market.  
  *Formula:* `SUM(transactions, tx => tx.total_value)`

### Lambdas
- **clear_market**
    
  *Formula:* `Find p* s.t. supply(p*) ~ demand(p*). Then set clearing_price = p*.`
- **update_market_hours**
  (Parameters: new_open_time, new_close_time)  
  *Formula:* `opening_time=new_open_time; closing_time=new_close_time`


---

## Entity: Transaction

**Description**: Represents a supply or demand action in a specific market by a given agent, with optional taxes or fees. Purely declarative aggregator fields handle net value.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **market_id**  
  *Type:* lookup, *Datatype:*   
  
- **agent_id**  
  *Type:* lookup, *Datatype:*   
  
- **type**  
  *Type:* scalar, *Datatype:* string  
  
- **quantity**  
  *Type:* scalar, *Datatype:* float  
  
- **price_per_unit**  
  *Type:* scalar, *Datatype:* float  
  
- **transaction_timestamp**  
  *Type:* scalar, *Datatype:* datetime  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **tax_or_fee_amount**  
  *Type:* scalar, *Datatype:* float  
  
- **instrument_applied**  
  *Type:* lookup, *Datatype:*   
  


### Aggregations
- **total_value**  
  *Description:* Gross transaction value (before taxes or fees).  
  *Formula:* `quantity * price_per_unit`
- **net_value_after_tax**  
  *Description:* Value after subtracting the tax or fee.  
  *Formula:* `total_value - tax_or_fee_amount`
- **loan_repayment_amount**  
  *Description:* Identifies how much of the transaction goes toward repaying debt if type='repayment'.  
  *Formula:* `IF(type='repayment', net_value_after_tax, 0)`
- **effective_tax_rate**  
  *Description:* Percentage tax/fee rate for this transaction.  
  *Formula:* `IF(total_value>0, (tax_or_fee_amount / total_value)*100, null)`
- **subsidy_applied_amount**  
  *Description:* How much subsidy was effectively applied to this transaction (placeholder aggregator).  
  *Formula:* `IF( instrument_applied.applicable_domain='subsidy', some_subsidy_calc, 0 )`
- **real_value**  
  *Description:* Adjusts the nominal transaction value by scenario inflation to get real_value.  
  *Formula:* `IF( market_id.scenario_id != null AND LOOKUP(market_id.scenario_id.linked_indicators WHERE indicator_name='InflationRate')!=null, total_value / (1 + (LOOKUP(market_id.scenario_id.linked_indicators WHERE indicator_name='InflationRate').indicator_value/100)), total_value )`
- **time_since_agent_last_purchase**  
  *Description:* Computes how long since the same agent’s last demand transaction, if any.  
  *Formula:* `TIMEDIFF( transaction_timestamp, MAX(for all t where t.type='demand' and t.agent_id = this.agent_id and t.transaction_timestamp < this.transaction_timestamp) )`
- **marginal_utility_of_income**  
  *Description:* Placeholder aggregator referencing the agent’s utility function to get dU/dIncome at this transaction cost.  
  *Formula:* `EvaluatePartialUtility(agent_id, net_value_after_tax) // conceptual reference to agent's UtilityFunction`
- **cumulative_agent_spending**  
  *Description:* Total historical spending by the same agent up to and including this transaction, demand only.  
  *Formula:* `SUM( FOR ALL t in agent_id.transactions WHERE t.type='demand' AND t.transaction_timestamp <= this.transaction_timestamp => t.net_value_after_tax )`
- **time_in_market_seconds**  
  *Description:* Time between posting and actual fill/closing of the transaction, if tracked.  
  *Formula:* `IF( fill_timestamp != null, TIMEDIFF(fill_timestamp, transaction_timestamp, 'seconds'), null )`
- **suggested_price_based_on_history**  
  *Description:* Uses historical average price for the same agent and the same type of transaction in this market as a naive suggestion.  
  *Formula:* `AVG( FOR ALL t in agent_id.transactions WHERE t.market_id=this.market_id AND t.type=type => t.price_per_unit )`
- **overhead_cost_estimate**  
  *Description:* Placeholder overhead cost for supply transactions: 10% of gross supply value (example formula).  
  *Formula:* `IF(type='supply', (price_per_unit * 0.1 * quantity), 0)`
- **demand_vs_supply_flag**  
  *Description:* Simple textual flag indicating demand vs. supply type.  
  *Formula:* `IF(type='demand', 'BUY_ORDER', 'SELL_ORDER')`
- **inflation_adjusted_revenue**  
  *Description:* Adjusts net revenue by scenario inflation rate if available.  
  *Formula:* `net_value_after_tax / IF( market_id.scenario_id.LOOKUP(linked_indicators, i => i.indicator_name='InflationRate')!=null, (1 + (market_id.scenario_id.LOOKUP(linked_indicators, i => i.indicator_name='InflationRate').indicator_value / 100)), 1)`
- **implied_utility_gain**  
  *Description:* A conceptual aggregator referencing the agent’s utility function, if present, for this transaction’s implied utility.  
  *Formula:* `IF(agent_id != null, EvaluateUtility(agent_id.UtilityFunction, { good: quantity }, 0), null)`

### Lambdas
- **execute_transaction**
    
  *Formula:* `If type='supply' => agent.liquid_assets += net_value_after_tax; If type='demand' => agent.liquid_assets -= net_value_after_tax.`
- **auto_match_transaction**
    
  *Formula:* `If type='demand': find earliest supply with price_per_unit <= this.price_per_unit. Match quantity. etc.`

### Constraints
- **valid_type**  
  *Formula:* `type IN ['supply','demand']`  
  *Error Message:* Transaction type must be 'supply' or 'demand'.
- **positive_quantity**  
  *Formula:* `quantity > 0`  
  *Error Message:* Transaction quantity must be positive.
- **positive_price**  
  *Formula:* `price_per_unit >= 0`  
  *Error Message:* Price per unit cannot be negative.
- **tax_fee_non_negative**  
  *Formula:* `tax_or_fee_amount >= 0`  
  *Error Message:* Tax or fee cannot be negative.

---

## Entity: UtilityFunction

**Description**: Captures an agent’s preference structure over goods, potentially referencing time discounting. This is purely a design-time definition of 'what' a utility is, separate from the 'how' of actual optimization.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **agent_id**  
  *Type:* lookup, *Datatype:*   
  
- **function_repr**  
  *Type:* scalar, *Datatype:* json  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **time_preference_rate**  
  *Type:* scalar, *Datatype:* float  
  
- **multi_good_utility**  
  *Type:* , *Datatype:*   
  
- **intertemporal_utility**  
  *Type:* , *Datatype:*   
  


### Aggregations
- **is_risk_averse**  
  *Description:* Returns true if the function's parameters suggest risk-aversion (concave utility).  
  *Formula:* `CheckRiskAversion(function_repr) // e.g. if CRRA with sigma>1 => risk-averse`

### Lambdas
- **evaluate_utility**
  (Parameters: bundle, time_point)  
  *Formula:* `For example, if type='CobbDouglas': U = x^alpha * y^beta * e^(-time_preference_rate * time_point).`
- **marginal_utility**
  (Parameters: bundle, good_id, time_point)  
  *Formula:* `Compute dU/dx for the relevant good, referencing function_repr.`
- **optimal_consumption_bundle**
  (Parameters: prices_array, budget_amount)  
  *Formula:* `SolveUtilityMax( function_repr, prices_array, budget_amount )`
- **expected_utility_of_lottery**
  (Parameters: outcome_list)  
  *Formula:* `Sum( Probability(o) * EvaluateUtility(o.bundle) ) over outcomes`


---

## Entity: BudgetConstraint

**Description**: Defines each agent’s or household’s budget limit, referencing possible multiple goods. Checking feasibility is purely declarative.

### Fields
- **constraint_id**  
  *Type:* scalar, *Datatype:* string  
  
- **agent_id**  
  *Type:* lookup, *Datatype:*   
  
- **income**  
  *Type:* scalar, *Datatype:* float  
  
- **constraint_equation**  
  *Type:* scalar, *Datatype:* json  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **budget_slack**  
  *Type:* rollup, *Datatype:*   
  
- **overrun_check**  
  *Type:* rollup, *Datatype:*   
  


### Aggregations
- **share_of_income_spent_on_good**  
  *Description:* Ratio of the budget used on a specific good if a consumption bundle is declared.  
  *Formula:* `IF( consumption_bundle != null AND consumption_bundle['some_good']!=null, (price(some_good)*consumption_bundle['some_good'])/income, 0 )`

### Lambdas
- **check_feasibility**
  (Parameters: consumption_bundle)  
  *Formula:* `Sum( price(good) * quantity(good) ) <= income`

### Constraints
- **non_negative_income**  
  *Formula:* `income >= 0`  
  *Error Message:* Budget income must not be negative.
- **overrun_check_enhanced**  
  *Formula:* `budget_slack >= 0`  
  *Error Message:* Consumption plan exceeds the budget!

---

## Entity: MacroIndicator

**Description**: Captures macro-level statistics (GDP, inflation, unemployment, money supply, etc.) aggregated from micro data. Time-based and scenario-based.

### Fields
- **indicator_id**  
  *Type:* scalar, *Datatype:* string  
  
- **indicator_name**  
  *Type:* scalar, *Datatype:* string  
  
- **indicator_value**  
  *Type:* scalar, *Datatype:* float  
  
- **timestamp**  
  *Type:* scalar, *Datatype:* datetime  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **phillips_curve_proxy**  
  *Type:* rollup, *Datatype:*   
  
- **gov_deficit_estimate**  
  *Type:* rollup, *Datatype:*   
  


### Aggregations
- **growth_rate**  
  *Description:* Compares this reading with the previous reading to yield a % growth or change.  
  *Formula:* `ComputeGrowthOverPrevious(indicator_value, timestamp, indicator_name)`
- **rolling_average**  
  *Description:* A smoothed aggregator over the last few data points for this indicator.  
  *Formula:* `AVG( last N indicator_value ) based on indicator_name ordering by timestamp`
- **real_interest_rate**  
  *Description:* Subtracts the inflation rate from nominal interest rate to get real interest.  
  *Formula:* `IF(indicator_name='InflationRate', null, LOOKUP(scenario_id.linked_policies WHERE instrument_name='InterestRate').instrument_value - LOOKUP(scenario_id.linked_indicators WHERE indicator_name='InflationRate').indicator_value )`
- **real_gdp**  
  *Description:* Adjusts nominal GDP by inflation to produce real GDP.  
  *Formula:* `IF(indicator_name='GDP' AND LOOKUP(scenario_id.linked_indicators WHERE indicator_name='InflationRate')!=null, indicator_value / (1 + (LOOKUP(scenario_id.linked_indicators WHERE indicator_name='InflationRate').indicator_value / 100)), indicator_value )`
- **growth_rate_annualized**  
  *Description:* Compares current indicator_value to the previous data point to produce an annualized growth rate.  
  *Formula:* `ComputeAnnualizedGrowth(indicator_name, indicator_value, timestamp)`
- **real_disposable_income_aggregate**  
  *Description:* Aggregate real disposable income for all agents, adjusted by scenario inflation if this record is the inflation indicator.  
  *Formula:* `LET total_disposable = SUM( scenario_id.linked_agents.disposable_income_estimate ); IF( indicator_name='InflationRate' AND indicator_value>0, total_disposable / (1 + (indicator_value/100)), total_disposable )`
- **employed_population_ratio**  
  *Description:* Fraction of total population that is employed, given separate 'Population' indicator in scenario.  
  *Formula:* `IF(indicator_name='EmploymentLevel', (indicator_value / LOOKUP(scenario_id.linked_indicators WHERE indicator_name='Population').indicator_value), null)`
- **policy_effectiveness_score**  
  *Description:* Naive approach to see if, say, an inflation-target policy is reducing inflation or a stimulus policy is boosting GDP.  
  *Formula:* `EvaluatePolicyEffect(indicator_name, indicator_value, scenario_id.linked_policies) // conceptual aggregator that checks if the relevant indicator moves in the intended direction under active policy`
- **real_per_capita_gdp**  
  *Description:* Nominal GDP adjusted by inflation, then divided by scenario population to get real per-capita GDP.  
  *Formula:* `IF(indicator_name='GDP' AND scenario_id!=null AND LOOKUP(scenario_id.linked_indicators, x => x.indicator_name='InflationRate')!=null AND LOOKUP(scenario_id.scenario_metadata, md => md.population_size)!=null, (indicator_value / (1 + (LOOKUP(scenario_id.linked_indicators, i => i.indicator_name='InflationRate').indicator_value / 100))) / scenario_id.scenario_metadata.population_size, null)`
- **monthly_inflation_rate**  
  *Description:* Transforms annual inflation rate to approximate monthly rate if this record is the inflation indicator.  
  *Formula:* `IF(indicator_name='InflationRate', ((POWER((1 + (indicator_value/100)), (1/12))) - 1)*100, null)`
- **gdp_growth_3month_avg**  
  *Description:* Averaged 3-month growth_rate for GDP if this indicator is GDP. References earlier aggregator growth_rate in the same scenario.  
  *Formula:* `IF(indicator_name='GDP', AVG(LASTN(3, LOOKUP_ALL(MacroIndicator, m => m.indicator_name='GDP' AND m.scenario_id=scenario_id), x => x.growth_rate)), null)`
- **public_spending_ratio**  
  *Description:* Ratio of government spending to GDP if this record is the GDP indicator, referencing separate GovernmentSpending indicator.  
  *Formula:* `IF(scenario_id!=null AND LOOKUP(scenario_id.linked_indicators, i => i.indicator_name='GovernmentSpending')!=null AND indicator_name='GDP', (LOOKUP(scenario_id.linked_indicators, i => i.indicator_name='GovernmentSpending').indicator_value / indicator_value), null)`

### Lambdas
- **update_indicator**
  (Parameters: micro_data_array)  
  *Formula:* `Aggregate micro_data_array => new indicator_value. For instance, sum of net_value_after_tax for a quarter => new GDP.`


---

## Entity: PolicyInstrument

**Description**: Represents a government or central bank policy instrument (interest rate, tax rate, subsidy, regulation) that can be applied to relevant agents or markets.

### Fields
- **instrument_id**  
  *Type:* scalar, *Datatype:* string  
  
- **instrument_name**  
  *Type:* scalar, *Datatype:* string  
  
- **instrument_value**  
  *Type:* scalar, *Datatype:* float  
  
- **applicable_domain**  
  *Type:* scalar, *Datatype:* string  
  
- **start_date**  
  *Type:* scalar, *Datatype:* datetime  
  
- **end_date**  
  *Type:* scalar, *Datatype:* datetime  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **time_active_days**  
  *Description:* Rough measure of how many days the policy is in effect (assuming contiguous date range).  
  *Formula:* `DATEDIFF(end_date, start_date, 'days')`
- **binding_price_control_status**  
  *Description:* Determines if a price floor/ceiling is binding by comparing instrument_value to market clearing_price.  
  *Formula:* `IF(applicable_domain='price_control', EvaluateBinding( instrument_value, relevant_market.clearing_price ), null)`
- **estimated_deadweight_loss**  
  *Description:* Approximates the deadweight loss from a tax, referencing supply/demand elasticities in the scenario.  
  *Formula:* `IF(instrument_name='TaxRate', ComputeDeadweightLoss( scenario_id, instrument_value ), null)`
- **active_status**  
  *Description:* Checks if the current date is within the policy’s start/end window.  
  *Formula:* `IF( NOW()>=start_date AND NOW()<=end_date, 'ACTIVE','INACTIVE')`
- **effective_tax_revenue**  
  *Description:* Sums all relevant tax/fee amounts under this policy’s domain in the scenario.  
  *Formula:* `IF(applicable_domain IN ['income_tax','VAT'], SUM( scenario_id.linked_agents.transactions.tax_or_fee_amount ), null)`
- **laffer_curve_estimate**  
  *Description:* Naive aggregator to see if total tax revenue might drop if tax rate is raised further.  
  *Formula:* `ComputeLafferCurve(scenario_id, instrument_value) // conceptual aggregator referencing supply/demand changes`
- **policy_adoption_rate**  
  *Description:* Fraction of total agents that have actually used or benefited from this policy, e.g. a subsidy.  
  *Formula:* `IF(applicable_domain='subsidy', COUNT( FOR ALL agent in scenario_id.linked_agents WHERE agent.transactions.instrument_applied=this.instrument_id ) / COUNT(scenario_id.linked_agents), null)`
- **fiscal_stimulus_multiplier**  
  *Description:* Approximates the ratio ΔGDP / ΔGovernmentSpending to see if there's a multiplier effect from a stimulus policy.  
  *Formula:* `ComputeStimulusMultiplier( scenario_id, instrument_value ) // conceptual aggregator referencing changes in GDP vs. changes in gov spending`
- **inflation_target_deviation**  
  *Description:* How far the actual inflation is from the policy's target, if instrument_name='InflationTarget'.  
  *Formula:* `IF(instrument_name='InflationTarget', ABS( scenario_id.LOOKUP(linked_indicators WHERE indicator_name='InflationRate').indicator_value - instrument_value ), null)`
- **policy_enforcement_gap**  
  *Description:* Naive difference between declared tax rate vs. the effective rate actually observed from scenario transaction data.  
  *Formula:* `IF(applicable_domain='income_tax', (instrument_value - (100 * (SUM(scenario_id.linked_agents, a => SUM(a.transactions, t => t.tax_or_fee_amount)) / SUM(scenario_id.linked_agents, a => SUM(a.transactions, t => t.total_value))))) , null)`
- **scenario_wide_effective_rate**  
  *Description:* Scenario-wide effective interest rate from actual agent debt costs—only relevant if domain=monetary_policy.  
  *Formula:* `IF(applicable_domain='monetary_policy', (SUM(scenario_id.linked_agents, a => a.debt_service_cost) / SUM(scenario_id.linked_agents, a => IF(a.outstanding_debt>0, a.outstanding_debt, 0))) * 100, null)`
- **policy_stability_score**  
  *Description:* Arbitrary measure: If the same policy instrument's rate/level changes frequently, stability is lower. Higher stdev => lower score.  
  *Formula:* `100 - (STDDEV( FILTER(LOOKUP_ALL(PolicyInstrument, p => p.instrument_name=instrument_name AND p.scenario_id=scenario_id), x => x.instrument_value)) * 10)`
- **policy_uptake_ratio**  
  *Description:* Fraction of agents who have at least one transaction referencing this subsidy policy. Null if not a subsidy instrument.  
  *Formula:* `IF(applicable_domain='subsidy', COUNT(scenario_id.linked_agents, a => COUNT(a.transactions, t => IF(t.instrument_applied=this.instrument_id, 1, 0))>0 ) / COUNT(scenario_id.linked_agents), null)`

### Lambdas
- **apply_instrument**
  (Parameters: agent_or_market_id)  
  *Formula:* `If instrument_name='InterestRate' => agent.apply_interest(instrument_value). If tax => transaction tax rate, etc.`
- **sunset_policy_lambda**
    
  *Formula:* `IF( scenario_id.LOOKUP(linked_indicators WHERE indicator_name='InflationRate').indicator_value > 5, end_date=NOW() )`


---


