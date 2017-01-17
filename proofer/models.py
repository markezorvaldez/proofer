from django.db import models
from proofer.parser.parser import parse_premise
#from proofer.parser.proof_parser import parse_proof

class Proof(models.Model):
	premise = models.TextField()
	proof = models.TextField()

	def prove(self):
		self.save()

	def check_proof(self):
		(result) = parse_premise(self.premise)
		self.proof += '\n' + str(result)
		#for line in self.proof.splitlines():