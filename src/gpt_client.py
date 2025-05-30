from dotenv import load_dotenv
import openai
import os
import argparse
import json
import detokenization

GERMAN_SYSTEM_PROMPT = "Du bist ein hilfreicher Assistent, der sich auf die Korrektion von Grammatik spezialisiert hat. "
GERMAN_PROMPT = "Hier ist ein Text mit Fehlern: #erroneous_text.  Bitte korrigiere die Grammatik des Textes"


class GPTConversationalClient:
    def __init__(self, model_name="gpt-4.1", temperature=2.0, azure_client=False):
        load_dotenv(override=True)
        self.api_key = os.environ["OPENAI_API_KEY"]
        if azure_client:
            self.api_key = os.environ["AZURE_OPENAI_API_KEY"]
            self.client = openai.AzureOpenAI(
                azure_endpoint="https://tu-openai-api-management.azure-api.net/ltat-tartunlp",
                api_key=self.api_key,
                api_version="2024-08-01-preview"
            )
        else:
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
    language = 'est'
    setting = 0
    client = GPTConversationalClient(model_name="gpt-4.1-nano", temperature=0)
    if language == 'ger':
        with open('data/ger/gergec.wo.singleedit.50.json', 'r', encoding='utf-8') as f:
            data = json.load(f)  # parse JSON
    else:
        with open('data/est/estgec.wo.singleedit.50.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    new_data = []
    for entry in data:
        if language == 'est':
            text_incorrect = detokenization.detokenize_est(entry[0])
            text_correct = detokenization.detokenize_est(entry[2])
            annotation = entry[1]

        else:
            # For German
            text_incorrect = detokenization.detokenize_deu(entry[0])
            text_correct = detokenization.detokenize_deu(entry[2])
            annotation = entry[1]

    # init client

        if language == 'est':
            system_prompt = "Oled abivalmis keelespetsialist, kes on spetsialiseerunud keeleõppijate abistamisele. Oskad eriti hästi leida grammatilisi vigu ja selgitada, miks need on vead ja miks need vead on tekkinud."
        else:
            system_prompt = "Du bist ein hilfreicher Assistent, der Sprachlernenden hilft, ihre Fehler zu verstehen. Du erklärst grammatikalische Fehler kurz und verständlich."

        if setting == 0:
            if language == 'est':
                prompt = f"Siin on vähemalt ühe veaga tekst:\n{text_incorrect[2:]}\nEsita grammatikavigade selgitus."
            else:
                prompt = f"Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect[2:]}\n Gib mir eine Erklärung der/des grammatikalischen Fehler(s)."
        elif setting == 1:
            if language == 'est':
                prompt = f"Siin on vähemalt ühe veaga tekst:\n{text_incorrect[2:]}\nSiin on parandatud tekst:\n{text_correct}\nSelgita, miks on parandus(ed) vajalik(ud)."
            else:
                prompt = f"Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect[2:]}\n Hier ist der korrigierte Text: \n {text_correct[2:]}\n Bitte erkläre, warum die Korrektur(en) nötig ist/sind."
        elif setting == 2:
            if language == 'est':
                prompt = f"Siin on vähemalt ühe veaga tekst:\n{text_incorrect}\nSiin on parandatud tekst:\n{text_correct}\nSiin on M2-formaadis märgendus:\n{annotation}\nSelgita, miks on parandus(ed) vajalik(ud) kasutades märgendust."
            else:
                prompt = f"Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect[2:]}\n Hier ist der korrigierte Text: \n {text_correct[2:]}\n und dazu die Fehlerannotation im M2 Stil: \n {annotation} \n Bitte erkläre, warum die Korrektur(en) nötig ist/sind. Nutze dafür auch die Annotation"
        elif setting == 3:
            if language == 'ger':
                with open('few_shot_prompts_de.txt', 'r', encoding='utf-8') as f:
                    examples = f.read()
                    prompt = f"Hier ist ein Text mit mindestens einem Fehler: \n {text_incorrect[2:]}\n Gib mir eine Erklärung der/des grammatikalischen Fehler(s) \n Hier sind einige Beispiele, wie du das machen kannst: \n {examples}"
            else:
                with open('few_shot_prompts_et.txt', 'r', encoding='utf-8') as f:
                    examples = f.read()
                    prompt = f"Siin on vähemalt ühe veaga tekst:\n{text_incorrect[2:]}\nEsita grammatikavigade selgitus.\nSiin on mõned näited, kuidas seda teha:\n{examples}"


    
    
        conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt },
        ]
        print(prompt)

        client.set_conversation(conversation)

        response = client.query()
        print(response)
        new_data.append({
            "text_incorrect": text_incorrect[2:],
            "text_correct": text_correct[2:],
            "annotation": annotation,
            "response": response
        })
        with open('results/ger/gergec.wo.singleedit.50.response.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_data, ensure_ascii=False, indent=4))

        


if __name__ == "__main__":
    main()
