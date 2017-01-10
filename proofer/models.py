from django.db import models
from proofer.parser.parser import parse_proof

class Proof(models.Model):
	premise = models.TextField()
	proof = models.TextField()

	def prove(self):
		self.save()

	def check_proof(self):
		if ((self.premise == "A and B => A") and (self.proof != ("assume A and B" + "\n" + "A"))):
			self.proof += " INCORRECT PROOF"
		result = parse_proof(self.premise)
		self.proof += str(result)