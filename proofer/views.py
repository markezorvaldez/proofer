from django.shortcuts import render
from .models import Proof
from .forms import ProofForm

def post_list(request):

	proofs = ProofForm()
	return render(request, 'proofer/post_list.html', {'proofs': proofs})