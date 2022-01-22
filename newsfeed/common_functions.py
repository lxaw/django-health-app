##################################################################
#
# Here we store common functions that are not views.
# These are often called when deleting models or creating them
#
##################################################################

# for times
from django.utils import timezone

# newsfeed models
from newsfeed.models import HelpRequest,HelpRequestOffer

from core.models import (NotificationHelpRequest, 
FeedbackHelpRequestOffer, FeedbackHelpRequestOffer,Dm,RoomDm)



class CommonFunctions:
	"""
	Stores common functions needed in newsfeed
	"""
	def voidDeleteHelpRequestOffer(modelHelpRequestOffer):
		"""
		# Inputs:
		# modelHelpRequestOffer
		# Outputs:
		# void
		# Utility:
		# Deletes a help request offer and 
		# all notifications associated
		"""
		# deletes a help request offer

		# remove the help request offer from the help request
		modelHelpRequestOffer.help_request.accepted_user = None

		# delete all the notifications necessary
		# delete all notifs from author of offer to author of help request
		qsNotifsToDelete = NotificationHelpRequest.objects.filter(
			sender=modelHelpRequestOffer.author,
			recipient=modelHelpRequestOffer.help_request.author,
			help_request=modelHelpRequestOffer.help_request
			)
		for modelNotif in qsNotifsToDelete:
			modelNotif.delete()
		
		# make sure no user is accepted anymore
		modelHelpRequestOffer.help_request.accepted_user = None
		modelHelpRequestOffer.help_request.save()

		# remove the help request offer
		modelHelpRequestOffer.delete()
	
	def voidHelpRequestOfferAccept(modelHelpRequestOffer):
		"""
		Inputs:
		Help Request Offer
		Outputs:
		void
		Utility:
		Accepts a help request offer by setting the accepted user of
		the help request to modelUserToBeAccepted

		Also creates a Room to store the DMs for that help request 

		NOTE:
		Should we delete all help request offers / notifications as well?
		"""
		modelHelpRequestOffer.help_request.accepted_user = modelHelpRequestOffer.author
		modelHelpRequestOffer.help_request.save()

		# create a room for chat
		modelRoomDm = RoomDm(author = modelHelpRequestOffer.help_request.author,
		partner=modelHelpRequestOffer.author,name=modelHelpRequestOffer.help_request.title)
		modelRoomDm.save()
	
		# DELETE THE HELP REQUEST OFFER WHEN COMPLETE
		modelHelpRequestOffer.delete()