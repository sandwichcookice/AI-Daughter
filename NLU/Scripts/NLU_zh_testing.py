import spacy
from spacy.util import minibatch, compounding
import random
from spacy.training import Example

# 加载英文的空模型
nlp = spacy.blank("zh")

spacy.prefer_gpu()

# 添加文本分类器到管道
# 使用默认配置来初始化一个 TextCatEnsemble 模型
if 'textcat' not in nlp.pipe_names:
    config = {
        "model": {
            "@architectures": "spacy.TextCatEnsemble.v2",
            "linear_model": {
                "@architectures": "spacy.TextCatBOW.v3",
                "exclusive_classes": True,
                "ngram_size": 1,
                "no_output_layer": False
            },
            "tok2vec": {
                "@architectures": "spacy.Tok2Vec.v2",
                "embed": {
                    "@architectures": "spacy.MultiHashEmbed.v2",
                    "width": 64,
                    "attrs": ["NORM", "LOWER", "PREFIX", "SUFFIX", "SHAPE"],
                    "rows": [2000, 2000, 500, 1000, 500],
                    "include_static_vectors": False
                },
                "encode": {
                    "@architectures": "spacy.MaxoutWindowEncoder.v2",
                    "width": 64,
                    "window_size": 1,
                    "maxout_pieces": 3,
                    "depth": 2
                }
            }
        }
    }
    textcat = nlp.add_pipe("textcat", config=config)
    textcat.add_label("GREETING")
    textcat.add_label("WEATHER_QUERY")

# 训练数据
train_data = [
    ("你好", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("早上好", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("今天天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("會下雨嗎?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("下午好", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("晚上好", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("你好嗎?", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("很開心見到你", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("你好呀", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("早上好呀", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("今天天气如何呀", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("會下雨嗎呀", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("很高興見到你", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("下午好呀", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("晚上好呀", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("你好呀", {"cats": {"GREETING": 1.0, "WEATHER_QUERY": 0.0}}),
    ("今天洛杉磯的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天台北的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天新北的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天桃園的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天台中的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天高雄的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天嘉義的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天宜蘭的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天花蓮的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天基隆的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天台東的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天澎湖的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天金門的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天馬祖的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天屏東的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天臺東的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天花蓮的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天宜蘭的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天臺南的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天臺中的天氣如何?", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("下雨了", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天天气如何", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天天气怎样", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天天气", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气呀", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气吧", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气哦", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气呢", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气吧", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气呀", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
    ("今天是个好天气呢", {"cats": {"GREETING": 0.0, "WEATHER_QUERY": 1.0}}),
]

# 训练模型
random.seed(1)
spacy.util.fix_random_seed(1)
optimizer = nlp.initialize()

# 批量训练
for i in range(10):
    random.shuffle(train_data)
    losses = {}
    batches = minibatch(train_data, size=compounding(4., 32., 1.001))
    for batch in batches:
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer, losses=losses)
    print(losses)


while True:
    test_text = input("请输入文本：")
    doc = nlp(test_text)
    # doc.cats 是一个字典，包含所有分类的预测概率
    if doc.cats:
        # 确定最可能的类别
        most_likely_category = max(doc.cats, key=doc.cats.get)
        if most_likely_category == "GREETING":
            print(f"输入：'{test_text}'，行为：问好")
        elif most_likely_category == "WEATHER_QUERY":
            print(f"输入：'{test_text}'，行为：问天气")
        else:
            print(f"输入：'{test_text}'，行为：未知")
    else:
        print(f"输入：'{test_text}'，无法确定行为")
