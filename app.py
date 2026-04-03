from flask import Flask, render_template_string, request, session, redirect, url_for
import datetime

app = Flask(__name__)
app.secret_key = "l_tigers_2026_secret" # Sécurité pour les sessions

# --- BASE DE DONNÉES DES ÉLÈVES ---

# --- BASE DE DONNÉES DES UTILISATEURS ---
UTILISATEURS = {
    "karl": "lion",           # Ton identifiant est 'karl', ton mot de passe est 'lion'
    "eleve": "reussite",      # Un compte pour tes futurs élèves
    "marie": "maman"          # Un compte pour ta mère avec un mot de passe simple
}


# --- SAVOIR ENCYCLOPÉDIQUE DE NEXA ---
SAVOIR = {
    "maths": "L'Algèbre (x,y) et la Géométrie (formes) sont les piliers de l'école.",
    "physique": "La physique étudie la matière et l'énergie (Newton, Archimède, Einstein).",
    "biologie": "Science de la vie : étude des cellules, de l'ADN et des écosystèmes.",
    "examen": "Tes examens de 9ème année : du 6 au 9 juillet 2026. Prépare-toi !",
    "haiti": "Capitale : Port-au-Prince. Gouvernance : Conseil de Transition (CPT).",
    "kreyòl": "Onè respè ! Mwen kapab pale kreyòl pou ede pèp la avanse.",
    "english": "Hello! I can help you master English for international business."
}

# --- INTERFACE DESIGN (HTML & CSS) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>NEXA - EDUTECH WORLD GE</title>
    <style>
        :root { --gold: #ffcc00; --dark: #121212; --card: #1e1e1e; }
        body { font-family: 'Poppins', sans-serif; background: var(--dark); color: white; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .container { background: var(--card); padding: 40px; border-radius: 20px; border: 1px solid var(--gold); box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 100%; max-width: 400px; text-align: center; }
        h1 { color: var(--gold); margin-bottom: 10px; font-size: 2em; }
        p.subtitle { color: #888; margin-bottom: 30px; font-size: 0.9em; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #333; background: #252525; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: var(--gold); border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255, 204, 0, 0.3); }
        .reponse-box { margin-top: 25px; padding: 15px; background: #252525; border-left: 4px solid var(--gold); text-align: left; border-radius: 5px; }
        .error { color: #ff4444; font-size: 0.8em; margin-top: 10px; }
        .logout { display: block; margin-top: 20px; color: #555; text-decoration: none; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>NEXA v6.0</h1>
        <p class="subtitle">L TIGERS ORGANISATION - EDUTECH WORLD</p>

        {% if not session.get('user') %}
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Identifiant" required>
                <input type="password" name="password" placeholder="Mot de passe" required>
                <button type="submit">ACCÉDER AU SYSTÈME</button>
            </form>
            {% if erreur %}<p class="error">{{ erreur }}</p>{% endif %}
        {% else %}
            <p>Content de vous revoir, <strong>{{ session['user']|capitalize }}</strong></p>
            <form method="POST" action="/ask">
                <input type="text" name="question" placeholder="Quelle est votre question ?" required>
                <button type="submit">INTERROGER L'IA</button>
            </form>

            {% if reponse %}
                <div class="reponse-box">
                    <small style="color: var(--gold);">RÉPONSE NEXA :</small><br>
                    {{ reponse }}
                </div>
            {% endif %}

            <a href="/logout" class="logout">Se déconnecter</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("username").lower().strip()
    pw = request.form.get("password")
    if user in UTILISATEURS and UTILISATEURS[user] == pw:
        session['user'] = user
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE, erreur="Accès refusé. Identifiants invalides.")

@app.route("/ask", methods=["POST"])
def ask():
    if not session.get('user'): return redirect(url_for('index'))
    entree = request.form.get("question").lower().strip()
    
    reponse = "Sujet non répertorié. Nos ingénieurs travaillent sur cette mise à jour."
    
    # Recherche dans le savoir
    for cle, detail in SAVOIR.items():
        if cle in entree:
            reponse = detail
            break
            
    # Moteur de calcul automatique
    try:
        if not any(cle in entree for cle in SAVOIR):
            reponse = f"Résultat du calcul : {eval(entree)}"
    except: pass
    
    return render_template_string(HTML_TEMPLATE, reponse=reponse)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)