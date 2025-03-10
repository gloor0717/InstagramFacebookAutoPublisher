from elevenlabs.client import ElevenLabs
from elevenlabs import save
from config import ELEVENLABS_API_KEY

def generate_voiceover(text, output_audio="audio.mp3"):
    """Generates AI voice-over using ElevenLabs."""
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    save(audio, output_audio)
    print(f"✅ Voice-over generated: {output_audio}")

if __name__ == "__main__":
    sample_text = "Le Caterpillar 910 : la solution idéale pour tous vos besoins de chargement et de manutention !"
    generate_voiceover(sample_text)
