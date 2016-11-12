import read
import facts_and_rules

# ASSERT
def assert_fact(new_fact):
    statement = facts_and_rules.statement(new_fact)

    facts.append(statement)
    
    # We want to see if this new fact triggers any of our rules
    for rule in rules:
        support(infer(statement, rule), statement)
        # if this works, add new facts based on our rules
    return statement

def assert_rule(new_rule):
    rule = facts_and_rules.rule(new_rule[0], new_rule[1])

    rules.append(rule)
    
    # Check if this rule is triggered by any of our facts
    for fact in facts:
        support(infer(fact, rule), rule)
        # if this works, add new facts
    return rule

def infer(fact, rule):
    # check the first element of the lhs of the rule against our fact
    bindings = facts_and_rules.match(rule.lhs[0], fact)

    if bindings != False:
        # if our rule only contains one argument, add a new fact
        if len(rule.lhs) == 1:
            if rule.type == "Assert":
                new_statement = facts_and_rules.instantiate(rule.rhs.full, bindings)
                # this is a new fact that we can assert
                asserted_fact = assert_fact(new_statement)
                return asserted_fact
            else:
                # find the fact that needs to be retracted
                fact_to_find = facts_and_rules.statement(facts_and_rules.instantiate(rule.rhs.full, bindings))
                for f in facts:
                    if facts_and_rules.match(fact_to_find, f) != False:
                        print "found" 
                        retract(f)
                return False
                
        # otherwise, make a new rule with the remaining arguments with bound variables replaced
        else:
            new_lhs = []
            for arg in rule.lhs[1:]:
                new_lhs.append(facts_and_rules.instantiate(arg.full, bindings))
            new_rhs = facts_and_rules.instantiate(rule.rhs.full, bindings)
            if rule.type == "Retract":
                new_rhs[0] = '~' + new_rhs[0]
            asserted_rule = assert_rule((new_lhs, new_rhs))
            return asserted_rule 
    else:
        # if we don't infer anything, return false
        return False

def support(item, supporter):
    if item != False:
        if type(item) is facts_and_rules.statement:
            supporter.facts.append(item)
        elif type(item) is facts_and_rules.rule:
            supporter.rules.append(item) 
    
# RETRACT
def retract(item):
    # if our item does not support anything else, we can safely remove it
    if len(item.rules) == 0 and len(item.facts) == 0:
        remove_from_kb(item)
    # otherwise, we have to retract what it supports first
    else:
        for f in item.facts:
            retract(f)
        for r in item.rules:
            retract(r)
        # once we've retracted everything this item supports, we can remove it
        remove_from_kb(item)

def remove_from_kb(item):
    if type(item) is facts_and_rules.statement:
        facts.remove(item)
    else:
        rules.remove(item)

# ASK
def ask(patterns):
    sets_of_bindings = []
    for pattern in patterns:
        bindings = [] 
        for fact in facts:
            if pattern.predicate == fact.predicate:
                # this means we've found a fact that matches our query
                binding = facts_and_rules.match(pattern, fact)
                if binding != False:
                    bindings.append(binding)
        if len(bindings) >= 1:
            sets_of_bindings.append(bindings)

    to_return = sets_of_bindings[0]
    if len(sets_of_bindings) > 1:
        for s in sets_of_bindings[1:]:
            to_remove = [] 
            for binding in to_return:
                if binding not in s:
                    to_remove.append(binding)
            #ew
            for b in to_remove:
                to_return.remove(b)

    return to_return

facts = []
rules = []

prefacts, prerules = read.read_tokenize('statements.txt')

for fact in prefacts:
    assert_fact(fact)
for rule in prerules:
    assert_rule(rule)
