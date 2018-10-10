#G01076852
#nojibe
#PROJECT_________________________________________________________________________
class Invitation:
#INITIALIZATION OF INSTANCE VARIABLES	
	def __init__(self, name, num_invited):
		self.name = name
		self.num_invited = num_invited
	def __str__(self):
#REPRESENTATIONS OF CLASS
		return "Invitation('{}', {})"\
		.format(self.name, self.num_invited)
	def __repr__(self):
		return Invitation.__str__(self)
#IS SELF == OTHER (IN EVERY ASPECT)?
	def __eq__(self, other):
		return self.name == other.name and self.num_invited == other.num_invited
	def __lt__(self, other):
#If the names aren't the same, then alpahabetically sort.
		if self.name != other.name:
			return self.name < other.name
#If the names are the same, then organize by ascending order of number invited
		else:
			return self.num_invited < other.num_invited
class Response:
#INITIALIZATION OF INSTANCE VARIABLES
	def __init__(self, name, ans, num_attending):
		self.name = name
		self.ans = ans
		self.num_attending = num_attending
#REPRESENTATIONS OF CLASS
	def __str__(self):
		return "Response('{}', {}, {})"\
		.format(self.name, self.ans, self.num_attending)
	def __repr__(self):
		return "Response('{}', {}, {})"\
		.format(self.name, self.ans, self.num_attending)
#IS SELF == OTHER (IN EVERY ASPECT)?
	def __eq__(self, other):
		return self.name == other.name \
		and self.ans == self.ans and self.num_attending == other.num_attending
	def __lt__(self, other):
#if the names aren't the same, then alphabetically organize them
		if self.name != other.name:
			return self.name < other.name
#if the names are the same, then organize by the boolean statements 
#(True = False < True)																	
#(False = False > True)
		elif self.ans != self.ans:
			return self.ans < other.ans
#if the boolean statements are the same, 
#then organize by ascending order of number of people attending
		else:
			return self.num_attending < other.num_attending
class InviteNotFoundError(LookupError):
#INITIALIZATION OF INSTANCE VARIABLES
	def __init__(self, name):
		self.name = name
#REPRESENTATIONS OF CLASS
	def	__str__(self):
		return "no invite for '{}' found.".format(self.name)
	def	__repr__(self):
		return "InviteNotFoundError('{}')".format(self.name)
#IS SELF == OTHER (IN EVERY ASPECT)?
	def	__eq__(self, other):
		return self.name == other.name

class TooManyError(ValueError):
#INITIALIZATION OF INSTANCE VARIABLES
	def __init__(self, num_requested, num_allowed):
		self.num_requested = num_requested
		self.num_allowed = num_allowed
#REPRESENTATIONS OF CLASS
	def __str__(self):
		return "too many: {} requested, {} allowed."\
		.format(self.num_requested, self.num_allowed)
	def __repr__(self):
		return "TooManyError({}, {})".format(self.num_requested, self.num_allowed)
#IS SELF == OTHER (IN EVERY ASPECT)?
	def __eq__(self, other):
		return self.num_requested==\
		other.num_requested and self.num_allowed == other.num_allowed

class Event:
#INITIALIZATION OF INSTANCE VARIABLES
	def __init__(self, title, invites=None, responses=None):
		self.title = title
#If there are no invites and/or responses, then initialize at an empty list
#otherwise, initialize both with a sorted list
		if invites == None:
			self.invites = []
		else:
			self.invites = sorted(invites)
		if responses == None:
			self.responses = []
		else:
			self.responses = sorted(responses)
#REPRESENTATIONS OF CLASS
	def __str__(self):
		return "Event('{}', {}, {})"\
		.format(self.title, self.invites, self.responses)
	def __repr__(self):
		return Event.__str__(self)
#IS SELF == OTHER (IN EVERY ASPECT)?
	def __eq__(self, other):
		return self.title == other.title and self.invites == other.invites and\
		self.responses == other.responses
	def find_invite(self, name):
#Search through list of invitation objects
		for invite in self.invites:
#if the name of an invitation object is the same as 'name'
			if invite.name == name:
				return invite
#if invite is never found, raise error
		raise InviteNotFoundError(name)
	def pop_invite(self,name):
#form a list with only invitation objects that have the same name as 'name'
		popped_invites = \
		[invite for invite in self.invites if invite.name == name]
#form a list with only invitation objects that have different names from 'name'
		self.invites = [invite for invite in self.invites if invite.name != name]
#if the popped_invites list found values, 
#then remove the respone object(s) of the same name
#and return the first item in the list of popped_invites
		if len(popped_invites) > 0:
			self.responses = \
			[response for response in self.responses if response.name != name]
			return popped_invites[0]
#Otherwise, raise an error
		else:
			raise InviteNotFoundError(name)
	def add_invite(self, inv):
#try to pop the invite object with name, and then append the invitation obejct
		try:
			Event.pop_invite(self, inv.name)
			self.invites.append(inv)
#if pop returns an error, then just append the invitation object
		except:
			self.invites.append(inv)
#self.invites is sorted 
		self.invites = sorted(self.invites)
#return the newly sorted and appended-to list
		return self.invites
	def find_response(self, name):
#search through list of response objects
		for response in self.responses:
			if response.name == name:
				return response
#if not found, then raise error
		raise LookupError("no Response found with name='{}'.".format(name))
	def pop_response(self, name):
#form a list with only response objects that have the same name as 'name'
		popped_responses = \
		[response for response in self.responses if response.name == name]
#form a list with only response objects that have different names from 'name'
		self.responses = \
		[response for response in self.responses if response.name != name]
#if popped_responses didn't pick up any values with the same name, then raise the error
		if len(popped_responses) == 0:
			raise LookupError("no Response found with name='{}'.".format(name))
#Otherwise, return the first item in popped_responses
		else:
			return popped_responses[0]

	def read_response(self, response):
#find the invite corresponding to the name 
		invite = Event.find_invite(self, response.name)
#if the number invited in the invite object 
#is less than the number attending in the response object
#then raise a TooManyError
		if invite.num_invited < response.num_attending:
			raise TooManyError(invite.num_invited, response.num_attending)
#the list of responses will be remade and reassigned
#without any objects that have the same name as 'name'
		self.responses = [r for r in self.responses if r.name != response.name]
#append the response to list of responses
		self.responses.append(response)
#go through all of the responses in reponses list
#if anyone has said they aren't coming (ans==False)
#then change the number of attending to 0
		for r in self.responses:
			if r.ans == False:
				r.num_attending = 0
#sort the responses
		self.responses = sorted(self.responses)

	def count_attendees(self):
		total = 0
#add to 'total' the number of attendees from each response
		for response in self.responses:
			total += response.num_attending
#return 'total'
		return total

	def count_pending(self):
		total = 0

		for invite in self.invites:
#find the response with the corresponding invite
			try:
				Event.find_response(self, invite.name)
#if the response isn't found, then add the number invited to 'total'
			except:
				total += invite.num_invited
#return 'total'
		return total

	def max_attendance(self):
		total = 0
#add the number of pending people and attendees to 'total'
		total = Event.count_attendees(self) + Event.count_pending(self)
#return total
		return total

	def count_rejections(self):
		total = 0
#go through responses
		for response in self.responses:
#find the corresponding invite
			invite = Event.find_invite(self, response.name)
#if they're attending 
#then subtract the number of people attending from the invited
#and add that to total
			if response.ans == True:
				total += invite.num_invited - response.num_attending
#if the entire party isn't attending then add that number to the total
			if response.ans == False:
				total += invite.num_invited
#return 'total'
		return total

	def rescind_invitation(self, name):
#try to pop the reponse and invite with the corresponding name
		try:
			Event.pop_invite(self, name)
			Event.pop_response(self,name)
#if an error comes up, then pass
		except:
			pass
			






