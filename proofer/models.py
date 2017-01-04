from django.db import models


class Proof(models.Model):
	premise = models.TextField()
	proof = models.TextField()

	def prove(self):
		self.save()