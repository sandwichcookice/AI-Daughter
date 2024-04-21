# nlp_process.py
import sys
import json
import spacy

# zh_core_web_trf 中文
# en_core_web_trf

nlp = spacy.load("zh_core_web_sm")

spacy.prefer_gpu()

def process_text(text):
    doc = nlp(text)

    tokens = []

    for token in doc:
        token_info = {'text': token.text, 'pos': token.pos_}
        tokens.append(token_info)

    return tokens

if __name__ == "__main__":
    input_text = sys.argv[1]
    processed_tokens = process_text(input_text)
    print(json.dumps(processed_tokens))  # 輸出JSON格式的結果
