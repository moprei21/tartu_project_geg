from dotenv import load_dotenv
import openai
import os
import argparse

GERMAN_SYSTEM_PROMPT = "Du bist ein hilfreicher Assistent, der sich auf die Korrektion von Grammatik spezialisiert hat. "
GERMAN_PROMPT = "Hier ist ein Text mit Fehlern: #erroneous_text.  Bitte korrigiere die Grammatik des Textes"


class GPTConversationalClient:
    def __init__(self, model_name="gpt-4.1", temperature=2.0):
        load_dotenv(override=True)
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model_name = model_name
        self.top_p = 0.9
        self.temperature = temperature
        self.max_tokens = 300
        self.conversation = []

    def set_conversation(self, conversation):
        """Initialize the conversation history"""
        self.conversation = conversation

    def query(self, response_format=None):
        """Send the conversation to the API and return the assistant's response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=self.temperature,
                top_p=self.top_p,
                messages=self.conversation,
                max_tokens=self.max_tokens,
                **({"response_format": response_format} if response_format else {}),
            )
            finish_reason = response.choices[0].finish_reason
            message_content = response.choices[0].message.content

            if finish_reason == "stop":
                return message_content
            elif finish_reason == "length":
                print("Warning: Response was truncated due to length limits.")
                return message_content
            elif finish_reason == "content_filter":
                raise ValueError("Response was filtered due to content restrictions.")
            else:
                raise ValueError(f"Unexpected finish reason: {finish_reason}")
        except Exception as e:
            raise RuntimeError(f"API query failed: {e}")


def main():
    text_incorrect = "Sie sind überzeugt , dass die Theorie ist wichtiger . "
    text_correct = "Sie sind überzeugt, dass die Theorie wichtiger ist."
    annotation = " A 7 9|||R:WO|||wichtiger ist|||REQUIRED|||-NONE-|||0 "
    # init client
    setting = 0
    client = GPTConversationalClient(model_name="gpt-4.1", temperature=0)

    system_prompt = "Du bist ein hilfreicher Assistent, der sich auf die Korrektur von Grammatik spezialisiert hat. Du bist speziell gut in der Eklärung vom grammatikalischen Fehlern."
    if setting == 0:
        prompt = f"""Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect}\n 
        Gib mir eine Erklärung der/des grammatikalischen Fehler(s)."""
    elif setting == 1:
        prompt = f"""Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect}\n
        Hier ist der korrigierte Text: \n {text_correct}\n 
        Bitte erkläre, warum die Korrektur(en) nötig ist/sind."""
    elif setting == 2:
        prompt = f"""Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect}\n
        Hier ist der korrigierte Text: \n {text_correct}\n 
        und dazu die Fehlerannotation im M2 Stil: \n {annotation}
        Bitte erkläre, warum die Korrektur(en) nötig ist/sind. Nutze dafür auch die Annotation"""

    conversation = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    print(prompt)

    client.set_conversation(conversation)

    response = client.query()
    print(f"Response: {response}")


if __name__ == "__main__":
    main()
