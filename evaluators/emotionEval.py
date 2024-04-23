from openai import OpenAI

api_key = ""
client = OpenAI(api_key=api_key)

article = open("evaluators\\TestArticle.txt","r").read()

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": ("The following texts you will recieve will be news articles that may or may not contain elements of propaganda within. "
                                           "For each text I would like you to extract and return exact sentences from the article that contain examples of emotionally "
                                           "charged language. If you do not find any such examples then say 'I found none'.")},
              {"role": "user", "content": article}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")