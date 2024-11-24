from App.models import Admin, ClashRule
from App.database import db

def login_admin(email, password):
    try:
        if not email or not password:
            return {"Error Message": "All fields are required"}
        
        admin = db.session.query(Admin).filter(Admin.email==email).first()
        if admin != None:
            if admin.check_password(password):
                return {"Login Successful": admin.login()}
        return {"Error Message" : "Invalid email or password"}
    
    except Exception as e:
        print(f"Error Login Failed: {e}")
        return None 

def custom_clash_rule(clashRuleID, userID, clashRuleTitle, clashRuleDescription, allowableDays): #create_new_clash_rule? as a possible function name
    try:
        if not clashRuleID or not userID or not clashRuleTitle or not clashRuleDescription or not allowableDays:
            return {"Error Message": "All fields are required"}
        
        rule = ClashRule.query.get(clashRuleID)
        if rule: 
            return {"Rule Already Exists": rule}
        
        #Add new rule
        newRule = ClashRule(clashRuleID = clashRuleID, userID = userID, clashRuleTitle = clashRuleTitle, clashRuleDescription  = clashRuleDescription, allowableDays = allowableDays)
        db.session.add(newRule)
        db.session.commit()
        return {"New Rule Added": newRule}
    
    except Exception as e:
        print(f"Error Adding New Rule: {e}")
        db.session.rollback() 
        return None

def list_clash_rules():
    try:
        return ClashRule.query.all()
    
    except Exception as e:
        print(f"Error While Trying to List Clash Rules: {e}") 
        return None 

