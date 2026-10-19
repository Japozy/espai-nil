from flask import Flask, jsonify, render_template, request
from google import genai
app = Flask(name)
Inicializamos el cliente de Gemini (recoge la clave GEMINI_API_KEY de las variables de entorno de Render)
client = genai.Client()

@app.route("/")
def home():
return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
data = request.get_json()
user_message = data.get("message", "")
subject_title = data.get("subject", "Materia SMX")
pdf_context = data.get("context", "")
if not user_message:
return jsonify({"error": "Mensaje vacío"}), 400
prompt = f"""
Eres una IA asistente y estricta para el estudiante Nil en su ciclo SMX 1A.
Estás ayudando con la asignatura: '{subject_title}'.
    A continuación tienes los apuntes y archivos PDF de esta materia proporcionados por Nil:
    ----------------
    {pdf_context if pdf_context.strip() else "No hay archivos PDF ni apuntes detallados adjuntos todavía."}
    ----------------
    
    INSTRUCCIÓN ESTRICTA: Responde a la siguiente pregunta de Nil basándote EXCLUSIVAMENTE en el texto de los apuntes o archivos PDF anteriores. Si la respuesta no está en el contenido proporcionado, indícale amablemente que debe adjuntar o escribir más apuntes sobre ello.
    
    Pregunta de Nil: {user_message}
    """

try:
interaction = client.interactions.create(
model="gemini-4-argon", input=prompt
)
return jsonify({"response": interaction.output_text})
except Exception as e:
return jsonify({"error": str(e)}), 500

if name == "main":
app.run(host="0.0.0.0", port=5000)