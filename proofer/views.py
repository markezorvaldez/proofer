from django.shortcuts import render
from .models import Proof
from .forms import ProofForm

def post_list(request):
	if request.method == "POST":
		proofs = ProofForm(request.POST)
		if proofs.is_valid():
			proof = proofs.save(commit=False)
			if proof.premise == "Long have we waited":
				proof.premise += " now we jebaited"
			proof.save()
			proofs = ProofForm(instance=proof)
	else:
		proofs = ProofForm()
	return render(request, 'proofer/post_list.html', {'proofs': proofs})