import speech_recognition as sr
from google.cloud import texttospeech
from playsound import playsound
import os

# Inicializa cliente Google Cloud TTS
client = texttospeech.TextToSpeechClient()

def falar(frase_texto):
    # Converte frase simples em SSML com pausas para soar mais natural
    # Você pode melhorar pausas aqui adicionando tags <break> onde preferir
    ssml = f"""
    <speak>
      {frase_texto}
      <break time="500ms"/>
    </speak>
    """

    print("🤖:", frase_texto)

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code="pt-BR",
        name="pt-BR-Wavenet-A",  # voz feminina neural natural e suportada
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    filename = "resposta.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    playsound(filename)
    os.remove(filename)

def ouvir():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Ouvindo o cliente...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("🗣️ Cliente disse:", texto)
        return texto.lower()
    except Exception as e:
        print("❌ Não entendi.", e)
        return ""

# Preços fictícios
tamanhos_valores = {"pequena": 30, "média": 40, "grande": 50}
adicionais_valor = 5
taxa_entrega = 8
tempo_entrega = "40 minutos"

# Início do atendimento
falar("Pizzaria do momento, Olá, Boa noite!")
falar("Quantas pizzas você gostaria de pedir?")
qtd = ouvir()
try:
    qtd_pizzas = int([s for s in qtd.split() if s.isdigit()][0])
except:
    qtd_pizzas = 1

pedidos = []

for i in range(qtd_pizzas):
    falar(f"Qual o tamanho da pizza número {i+1}? Pequena, média ou grande?")
    tamanho = ouvir()
    while not any(t in tamanho for t in tamanhos_valores.keys()):
        falar("Desculpe, não entendi o tamanho. Pode repetir?")
        tamanho = ouvir()

    falar(f"Qual o sabor da pizza número {i+1}?")
    sabor = ouvir()

    falar("Deseja algum adicional? Exemplo: borda recheada, extra queijo.")
    adicional = ouvir()

    pedidos.append({
        "tamanho": tamanho,
        "sabor": sabor,
        "adicional": adicional
    })

falar("Gostaria de alguma bebida?")
bebida = ouvir()

falar("Qual o endereço de entrega, por favor?")
endereco = ouvir()

# Calcular total
total = sum([tamanhos_valores.get(p["tamanho"].split()[0], 40) + (adicionais_valor if p["adicional"] != "" else 0) for p in pedidos])
if bebida != "":
    total += 7  # valor fixo fictício
total += taxa_entrega

def resumo_pedido():
    falar("Perfeito! Aqui está o resumo do seu pedido:")
    for i, p in enumerate(pedidos):
        falar(f"Pizza {i+1}: {p['tamanho']}, sabor {p['sabor']}, adicional: {p['adicional'] or 'nenhum'}.")
    if bebida != "":
        falar(f"Bebida: {bebida}.")
    falar(f"Endereço de entrega: {endereco}.")
    falar(f"O total do pedido, incluindo a taxa de entrega, é R$ {total:.2f}.")
    falar(f"O prazo estimado de entrega é de {tempo_entrega}.")

resumo_pedido()

while True:
    falar("Gostaria de incluir ou alterar alguma coisa no seu pedido? Por favor, responda sim ou não.")
    resposta = ouvir()
    if "sim" in resposta:
        falar("Quantas pizzas adicionais você gostaria de pedir?")
        qtd_extra = ouvir()
        try:
            qtd_extra_pizzas = int([s for s in qtd_extra.split() if s.isdigit()][0])
        except:
            qtd_extra_pizzas = 0

        for i in range(qtd_extra_pizzas):
            falar(f"Qual o tamanho da pizza número {len(pedidos)+1}? Pequena, média ou grande?")
            tamanho = ouvir()
            while not any(t in tamanho for t in tamanhos_valores.keys()):
                falar("Desculpe, não entendi o tamanho. Pode repetir?")
                tamanho = ouvir()

            falar(f"Qual o sabor da pizza número {len(pedidos)+1}?")
            sabor = ouvir()

            falar("Deseja algum adicional? Exemplo: borda recheada, extra queijo.")
            adicional = ouvir()

            pedidos.append({
                "tamanho": tamanho,
                "sabor": sabor,
                "adicional": adicional
            })
        total = sum([tamanhos_valores.get(p["tamanho"].split()[0], 40) + (adicionais_valor if p["adicional"] != "" else 0) for p in pedidos])
        if bebida != "":
            total += 7
        total += taxa_entrega

        resumo_pedido()

    elif "não" in resposta or "nao" in resposta:
        falar("Ótimo! Seu pedido foi finalizado.")
        falar("Obrigado por pedir com a gente! 🍕")
        break
    else:
        falar("Desculpe, não entendi. Por favor, responda apenas sim ou não.")
