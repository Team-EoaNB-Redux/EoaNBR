<style>
	p {
		line-height: 1.4;
	}
	table, th, td {
		border: 1px solid;
		text-align: center;
		padding: 8px;
	}
	.example-header {
		background-color: #f6e985;
	}
	.example-row:nth-child(even) {
		background-color: #fffff1;
	}
	.example-row:hover {
		font-weight: bold;
		background-color: #eeee30dd;
	}
	.define-header {
		background-color: #85dff6;
	}
	.define-row:nth-child(even) {
		background-color: #f1ffff;
	}
	.define-row:hover {
		font-weight: bold;
		background-color: #30eededd;
	}


	div.tablecontainer {
		overflow-x: auto;
	}
</style>

# EoaNBR Internal Politics Documentation
#### Written by Vanadium 
This page contains the documentation for the various effects, triggers and modifiers for the internal politics system.

Attempting to use a scripted effect in the wrong scope may result in weird and unintended effects that can break the system. Please don't do that.

Presume by default that tooltips are done for you. Also, all temp variables used by these scripted effects will be reset to 0 after firing the effect.

## Objects Documentation


### Coalitions

Coalitions are dynamic groups of parties within a country's legislature that *typically* vote in blocks for and against policy. Each coalition represents a different portion of your legislature and 

<div>
	<table >
		<tr class="example-header">
			<th width=140px>Coalition Type</th>
			<th width=140px>Token</th>
			<th width=140px>Rules</th>
			<th>Notes</th>
		</tr>
		<tr class="example-row">
			<td>Ruling Coalition</td>
			<td>ruling_coalition</td>
			<td></td>
			<td><p>Represents the collection of parties that currently control the legislature. With exemption of <i>Executive Orders</i> and <i>Revolutions</i>, all legislation passed for your country must have at least passive approve of the Ruling Coalition.</p><p>Your head of state may or may not be party of your ruling coalition (dependent on your government type)</p></td>
		</tr>
		<tr class="example-row">
			<td>Opposition</td>
			<td>oppositional_parties</td>
			<td></td>
			<td><p>Represents the collection of parties that actively oppose the control of the <i>Ruling Coalition</i>.</p><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Marginalized</td>
			<td>marginalized_parties</td>
			<td></td>
			<td><p>Represents the collection of parties or interest groups that have minimal authority (or popularity) within the national legislature.</p><p></p></td>
		</tr>
	<table>
</div>


### Parties

Parties are dynamic collections of interest groups that have agreed to vote together 

<div>
	<table >
		<tr class="define-header">
			<th width=140px>Value</th>
			<th width=140px>Variable</th>
			<th width=140px>Variable Type</th>
			<th>Notes</th>
		</tr>
		<tr class="define-row">
			<td>Party</td>
			<td><i>&lt;party_object&gt;</i></td>
			<td>&lt;party_token&gt;</td>
			<td><p>Token that represents the party. It is stored in the <i>parties_array</i> of each country and all relevant information of individual parties are stored as targeted variables at their respective party token.</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Party Name</td>
			<td>name_override</td>
			<td>&lt;party_token&gt;</td>
			<td><p><i>(Optional)</i> Token that can override a party's name, if not the same as your party token's default name. This can be used to represent parties that have changed their name throughout the timeline without reassigning the variables.</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Party Color</td>
			<td>color</td>
			<td>&lt;color_token&gt;</td>
			<td><p>Token that represents a party's color identifier within national politics. This will be used in lists, labels and charts. It is not recommended that you have two parties with the same color.</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Party Type</td>
			<td>type</td>
			<td>&lt;pr_token&gt;</td>
			<td><p>Token that represents a party's "type." This is used to determine which interest groups would be willing to align with the party, based on existing interest group membership.</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Party Leader</td>
			<td>leader</td>
			<td>&lt;character_token&gt;</td>
			<td><p>Character that represents the leader of the party. This character will typically be the leader of the party's most strong interest group and will become your head of state, if the party comes to power within the legislature (dependent on government type).</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Marginalized</td>
			<td>marginalized</td>
			<td>&lt;boolean&gt;</td>
			<td><p>Represents whether the party is considered 'marginalized' in national politics. Marginalized Parties cannot join either the ruling coalition, nor the oppositional coalition. They have a downsized influence in legislative voting, regardless their popularity within the national populous.</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Interest Group Members</td>
			<td>interest_groups</td>
			<td>array of &lt;ig_token(s)&gt;</td>
			<td><p>Array that represents the group of Interest Groups that will vote together per Party Interests.</p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Party Treasury</td>
			<td>treasury</td>
			<td>&lt;float&gt;</td>
			<td><p></p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Popularity</td>
			<td>popularity</td>
			<td>&lt;float&gt;</td>
			<td><p></p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Strength</td>
			<td>strength</td>
			<td>&lt;float&gt;</td>
			<td><p></p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Enthusiasm</td>
			<td>enthusiasm</td>
			<td>&lt;percentage&gt;</td>
			<td><p></p><p></p></td>
		</tr>
		<tr class="define-row">
			<td>Unity</td>
			<td>unity</td>
			<td>&lt;percentage&gt;</td>
			<td><p></p><p></p></td>
		</tr>
		<tr class="define-row">
			<td></td>
			<td></td>
			<td></td>
			<td><p></p><p></p></td>
		</tr>
		<tr class="define-row">
			<td></td>
			<td></td>
			<td></td>
			<td><p></p><p></p></td>
		</tr>
	<table>
</div>

### Default Parties

This is the list of parties that may appear in a country's legislature if no custom parties have been defined.

<div>
	<table >
		<tr class="example-header">
			<th width=140px>Party</th>
			<th width=140px>Token</th>
			<th width=140px>Type</th>
			<th width=240px>Interest Groups</th>
			<th>Notes</th>
		</tr>
		<tr class="example-row">
			<td>Communist Party</td>
			<td>party_communist_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Socialist Party</td>
			<td>party_socialist_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Liberal Party</td>
			<td>party_liberal_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Conservative Party</td>
			<td>party_conservative_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Reactionary Party</td>
			<td>party_reactionary_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Chauvinist Party</td>
			<td>party_chauvinist_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Monarchist Party</td>
			<td>party_monarchist_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Fundamentalist Party</td>
			<td>party_fundamentalist_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Military Junta</td>
			<td>party_stratocratic_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Tribal Council</td>
			<td>party_tribal_council</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
		<tr class="example-row">
			<td>Independence Party</td>
			<td>party_independence_party</td>
			<td></td>
			<td></td>
			<td><p></p></td>
		</tr>
	<table>
</div>

### Interest Groups

### Interest Traits

### Laws

### Policies

###

## Actions

### Executive Orders

### Debates

### Revolutions

## Scripted Effects

## Scripted Triggers

## Scripted Localisation


