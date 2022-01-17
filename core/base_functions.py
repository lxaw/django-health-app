#######################
# Basic functions
#######################

def boolModelOwnershipCheck(model,field,user):
	if getattr(model, field) == user:
		return True
	else:
		return False