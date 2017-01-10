from django.db import models


class Proof(models.Model):
	premise = models.TextField()
	proof = models.TextField()

	def prove(self):
		self.save()

	def check_proof(self):
		if ((self.premise == "A and B => A") and (self.proof != ("assume A and B" + "\n" + "A"))):
			self.proof += " INCORRECT PROOF"