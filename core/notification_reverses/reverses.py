#############################
# This file contains all the reverses for notifications.
# Be sure to update it when you change a reverse.
#############################

strNewsfeed = "newsfeed"
strCommunities = "communities"

dictNotificationReverses = {
	strNewsfeed:{
		"help-request":{
			"detail":"{}:help-request-detail".format(strNewsfeed),
		},
		"help-request-offer":{
			"detail":"{}:help-request-offer-detail".format(strNewsfeed),
		}
	},
	strCommunities:{
		"post":{
			"detail":"{}:post-detail".format(strCommunities),
		}
	}
}