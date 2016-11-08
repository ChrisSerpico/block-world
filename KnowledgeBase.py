# Assert statements and rules
# Retract statements and rules
# Ask our knowledge base what is true

# Knowledge base is a list of facts 
facts = []
# facts have two parts, the predicate and the argument
# to see if a statment is true, just check if the predicate is true, and the argument is true
# The only tweak is that we want to be able to check facts against statements with variables
# eg We want to be able to check on(?x, ?y), and if on(21, 22) is a fact, then we know that on(?x, ?y) is true for ?x = 21, ?y = 22

#
rules = [] 


# Want classes/objects for
# Statements
    # predicates
    # arguments
    # methods for matching
    # supports
        # other statements that this fact supports (both facts and rules, so a retracted fact can retract rules and facts, which recursively retract rules and facts etc.) 
        # in other words, what else to remove if we retract this statement 
# Variables
    # name
    # methods for matching
# Constants
    # name
    # methods for matching
# Bindings List
# Rules
    # LHS
        # Left hand side
        # A list of statements
    # RHS
        # Right hand side
        # A single statement
    # If the left hand side statements are all true for some set of bindings, then we know
    # that the right hand side is true (is a fact) for the bindings provided. We can then add this fact to our knowledge base 

# A binding is a tuple connecting a variable with a constant
# eg (?x, A); this means that x is bound to A
    # Useful for asking questions like is A on top of B?
    # On(?x, B) is true when (?x, A)
    # In other words, ?x is on top of B when ?x is bound to (=) A 

# When we get a new fact, we want to run inferences
    # want to see if the new fact triggers any of our rules
# Whenever we get a new rule, we also want to run inferences
    # want to see if the new rule is triggered by any of our facts

# When we assert, we want to draw inferences from the new fact
# When we retract, we want to remove inferences that were supported by the removed fact

# When we have a new fact or a new rule, we ask ourselves "Is the first element/conjuct of a rule true?"
# Because it needs to be in order to draw an inference. If it's not, we don't bother checking the other parts 
    # This way we can short circuit and avoid looping over everything all the time
# Can also make partial conclusions
    # If Bigger(A, B) is true, then we know that On(A, B) => Covered(B)
    # This is a very narrow rule
# When we match all parts of a rule, we add a new fact
# When we match only part of a rule, we make a new rule (it will be very narrow)
# Thus when we get a new fact, we either get a new fact or a new rule 

