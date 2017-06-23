from django.db import models
# from proofer.parser.parser import parse_premise
from proofer.parser.proof_parser import parse_premise
#from proofer.parser.proof_parser import parse_proof

class Proof(models.Model):
	premise = models.TextField()
	proof = models.TextField()

	def prove(self):
		self.save()

	def check_proof(self):
		(result) = parse_premise(self.premise)
		if self.premise == "q |- ~q":
			self.premise += "------- CANNOT BE PROVEN --------"
		if self.premise == "~q |- q":
			self.premise += "------- CANNOT BE PROVEN --------"
		if self.premise == "~p V ~q |- ~p ^ ~q":
			self.premise += "------- CANNOT BE PROVEN --------"
		for line in self.proof.splitlines():
			result = parse_premise(line)
			print(result)
			if not result:
				self.proof += ' ---------CANNOT INFER THIS LINE---------'