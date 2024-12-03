from flask import Flask, render_template, request, jsonify
import openai
import config

app = Flask(__name__)

# Configure OpenAI API Key
openai.api_key = config.api_gpt

@app.route("/")
def index():
    """Page d'accueil avec la fonctionnalité principale."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Génération de réponse basée sur les champs de l'index."""
    try:
        # Récupération des données depuis le frontend
        data = request.json
        user_request = data.get("user_request", "").strip()
        user_response = data.get("user_response", "").strip()

        if not user_request or not user_response:
            return jsonify({"error": "Les champs ne doivent pas être vides."}), 400

        # Prompt pour GPT-3.5 Turbo
        prompt = (
            f"Je veux que tu agisses comme un rédacteur assistant expérimenté dans la rédaction d'emails. "
            f"Voici une demande d'un utilisateur de notre plateforme Supertripper : {user_request}\n"
            f"Voici les éléments de réponses proposés : {user_response}\n\n"
            f"Répond à la demande sur un ton professionnel, formel, empathique, clair, cohérent, fluide et facilement compréhensible. "
            f"Utilise les codes rédactionnels d'un email rédigé par un service client avec les formules de politesse."
        )

        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional helpdesk assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        # Récupération de la réponse générée
        gpt_response = response['choices'][0]['message']['content']
        return jsonify({"response": gpt_response})

    except openai.error.OpenAIError as e:
        # Capture les erreurs spécifiques de l'API OpenAI
        print("Erreur OpenAI : ", e)
        return jsonify({"error": f"Erreur de l'API OpenAI : {str(e)}"}), 500

    except Exception as e:
        # Capture toutes les autres erreurs
        print("Erreur serveur : ", e)
        return jsonify({"error": "Erreur interne du serveur."}), 500

@app.route("/correct", methods=["POST"])
def correct():
    try:
        # Récupération des données depuis le frontend
        data = request.json
        input_text = data.get("input_text", "").strip()

        if not input_text:
            return jsonify({"error": "Le texte fourni est vide."}), 400

        # Prompt pour GPT-3.5 Turbo
        prompt = (
            f"Corriger ce texte, et appliquer un ton professionnel, formel, empathique, clair, cohérent, fluide et facilement compréhensible. "
            f"Utilisez les codes rédactionnels d'un email rédigé par un service client avec les formules de politesse. "
            f"Voici le texte : {input_text}"
        )

        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional writing assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        gpt_response = response['choices'][0]['message']['content']
        return jsonify({"response": gpt_response})

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"Erreur de l'API OpenAI : {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur."}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Gestion globale des erreurs Flask."""
    print("Erreur capturée : ", e)
    return jsonify({"error": "Une erreur est survenue, veuillez réessayer."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
