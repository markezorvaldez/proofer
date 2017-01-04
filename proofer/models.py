from django.db import models


class Proof(models.Model):
	premise = models.TextField()
	proof = models.TextField()

	def prove(self):
		self.save()

	def check_proof(self):
		if self.premise == "Long have we waited":
			self.premise += " now we jebaited LUL"