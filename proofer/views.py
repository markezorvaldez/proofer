from django.shortcuts import render
from .models import Proof

def post_list(request):
	proofs = Proof.objects.all()
	return render(request, 'proofer/post_list.html', {'proofs': proofs})