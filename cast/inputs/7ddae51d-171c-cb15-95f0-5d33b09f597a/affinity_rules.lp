% Chemistry
attribute_affinity(chemistry, high, chemistry, high, 2).
attribute_affinity(chemistry, low, chemistry, low, 1).
attribute_affinity(chemistry, low, chemistry, high, -1).
attribute_affinity(chemistry, high, chemistry, low, -1).

% Methamphetamine Production
attribute_affinity(methamphetamine_production, high, methamphetamine_production, high, 3).
attribute_affinity(methamphetamine_production, low, methamphetamine_production, low, 1).
attribute_affinity(methamphetamine_production, low, methamphetamine_production, high, -2).
attribute_affinity(methamphetamine_production, high, methamphetamine_production, low, -2).

% Drug Dealing
attribute_affinity(drug_dealing, high, drug_dealing, high, 2).
attribute_affinity(drug_dealing, low, drug_dealing, low, 1).
attribute_affinity(drug_dealing, low, drug_dealing, high, -1).
attribute_affinity(drug_dealing, high, drug_dealing, low, -1).

% Money Laundering
attribute_affinity(money_laundering, high, money_laundering, high, 1).
attribute_affinity(money_laundering, low, money_laundering, low, 1).
attribute_affinity(money_laundering, low, money_laundering, high, -1).
attribute_affinity(money_laundering, high, money_laundering, low, -1).

% Law Enforcement
attribute_affinity(law_enforcement, high, law_enforcement, high, 3).
attribute_affinity(law_enforcement, low, law_enforcement, low, 1).
attribute_affinity(law_enforcement, low, law_enforcement, high, -2).
attribute_affinity(law_enforcement, high, law_enforcement, low, -2).
attribute_affinity(cancer_struggle, high, cancer_struggle, high, -2).
attribute_affinity(cancer_struggle, low, cancer_struggle, low, 2).
attribute_affinity(cancer_struggle, low, cancer_struggle, high, -1).
attribute_affinity(cancer_struggle, high, cancer_struggle, low, -1).

attribute_affinity(criminal_involvement, high, criminal_involvement, high, 3).
attribute_affinity(criminal_involvement, low, criminal_involvement, low, -1).
attribute_affinity(criminal_involvement, low, criminal_involvement, high, -2).
attribute_affinity(criminal_involvement, high, criminal_involvement, low, -2).

attribute_affinity(family_dynamics, high, family_dynamics, high, 2).
attribute_affinity(family_dynamics, low, family_dynamics, low, 0).
attribute_affinity(family_dynamics, low, family_dynamics, high, -2).
attribute_affinity(family_dynamics, high, family_dynamics, low, -2).

attribute_affinity(morality_conflict, high, morality_conflict, high, -3).
attribute_affinity(morality_conflict, low, morality_conflict, low, 1).
attribute_affinity(morality_conflict, low, morality_conflict, high, 1).
attribute_affinity(morality_conflict, high, morality_conflict, low, 1).

attribute_affinity(power_struggle, high, power_struggle, high, -4).
attribute_affinity(power_struggle, low, power_struggle, low, 2).
attribute_affinity(power_struggle, low, power_struggle, high, -1).
attribute_affinity(power_struggle, high, power_struggle, low, -1).