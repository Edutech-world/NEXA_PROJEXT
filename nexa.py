import datetime

# --- BASE DE CONNAISSANCES DÉTAILLÉE ---
savoir = {
    "maths": "L'Algèbre (équations x,y) et la Géométrie (formes 2D/3D) sont les bases des mathématiques.",
    "physique": "La physique étudie la matière et l'énergie (Mécanique, Optique, Électricité).",
    "biologie": "C'est l'étude du vivant : les cellules, l'ADN et les écosystèmes.",
    "examen": "Tes examens de 9ème année sont prévus du 6 au 9 juillet 2026. Courage !",
    "haiti": "Capitale : Port-au-Prince. Gouvernance : Conseil Présidentiel de Transition (CPT).",
    "usa": "Capitale : Washington D.C. Président : Joe Biden.",
    "france": "Capitale : Paris. Président : Emmanuel Macron.",
    "kreyòl": "Onè respè ! Mwen kapab pale kreyòl pou ede w travay.",
    "salut": "Bonjour ! Je suis NEXA, ton assistant pour EDUTECH WORLD GE. Comment puis-je t'aider ?",
    "bonjour": "Salut ! Prêt pour une session de révisions ou des calculs ?",
    "aide": "Demande-moi : 'maths', 'physique', 'heure', 'haiti' ou tape un calcul."
}

def demarrer_nexa():
    print("="*50)
    print("       SYSTEME NEXA v4.0 - EDUTECH WORLD GE")
    print("="*50)
    print("Statut : Prêt | Tape 'quitter' pour fermer.")
    print("="*50)

    # Le programme reste allumé grâce à cette boucle
    while True:
        entree = input("\n[NEXA] Pose ta question : ").lower().strip()

        # 1. QUITTER LE PROGRAMME
        if entree in ["quitter", "exit", "stop"]:
            print("[IA] Fermeture... Bon repos et bon jeûne !")
            break

        # 2. L'HEURE DANS LE MONDE
        if "heure" in entree:
            maintenant = datetime.datetime.now()
            print(f"[IA] Il est exactement {maintenant.strftime('%H:%M:%S')}.")
            continue

        # 3. RECHERCHE DANS LE SAVOIR (Maths, Géo, Langues, Saluts)
        trouve = False
        for cle, detail in savoir.items():
            if cle in entree:
                print(f"\n[IA - {cle.upper()}] : {detail}")
                trouve = True
                break

        # 4. MOTEUR DE CALCUL (ALGEBRE)
        if not trouve:
            try:
                # Si tu tapes 15*15 ou 100/2, il calcule direct
                resultat = eval(entree)
                print(f"[IA - CALCUL] Résultat : {resultat}")
            except:
                print("[IA] Je ne connais pas encore ce sujet. Essaie 'aide' ou un calcul !")

if __name__ == "__main__":
    demarrer_nexa()