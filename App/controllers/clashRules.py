from App.models import ClashRule
from App.database import db

def custom_clash_rule(clashRuleID, userID, clashRuleTitle, clashRuleDescription, allowableDays): #create_new_clash_rule? as a possible function name
    rule = ClashRule.query.get(clashRuleID)
    if rule: 
        return rule
    else:
         #Add new rule
        newRule = ClashRule.addNewRule(clashRuleID, userID, clashRuleTitle, clashRuleDescription, allowableDays) #possible name "addNewRule?" for the adding new rules/custome rules that would be in the models section
        db.session.add(newRule)
        db.session.commit()
        return newRule

    #Note the class and function call names and the ordering of the parameter might have to change depending on the models    