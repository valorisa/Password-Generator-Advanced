# Angle i — coherence des versions (le "triangle")

Decision (humain + LLM_A + LLM_B) : option "Verifier", on garde __version__.

A appliquer au PROCHAIN bump (pas maintenant) : dans le job release,
avant `poetry build`, verifier que tag == pyproject.toml == __init__.py,
et ECHOUER (exit 1) si desaccord — une alarme, pas un controle qui se tait.

Pourquoi plus tard : aucune faille active aujourd'hui (le job release
ne tourne que sur tag), donc on evite de toucher la prod sans
declencheur reel ; le prochain bump fournira de toute facon un vrai
run tagge pour tester la correction en conditions reelles.

Marqueur operationnel : commentaire TODO dans
.github/workflows/ci.yml (juste au-dessus du job release).
