from mage2gen import Snippet

def add_snippets(request):
	snippets = []
	for snippet in Snippet.snippets():
		snippets.append(snippet.name())
	return {
		'mage2gen_snippets': sorted(snippets)
	}