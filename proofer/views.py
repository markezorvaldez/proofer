from django.shortcuts import render
from .models import Proof
from .forms import ProofForm

def post_list(request):
	if request.method == "POST":
		proofs = ProofForm(request.POST)
		if proofs.is_valid():
			proof = proofs.save(commit=False)
			proof.check_proof()
			proof.prove()
			proofs = ProofForm(instance=proof)
	else:
		proofs = ProofForm()
	return render(request, 'proofer/post_list.html', {'proofs': proofs})