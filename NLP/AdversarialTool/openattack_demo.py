import OpenAttack
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import datasets

def make_model():
    class MyClassifier(OpenAttack.Classifier):
        def __init__(self):
            try:
                self.model = SentimentIntensityAnalyzer()
            except LookupError:
                nltk.download('vader_lexicon')
                self.model = SentimentIntensityAnalyzer()
        
        def get_pred(self, input_):
            return self.get_prob(input_).argmax(axis=1)

        def get_prob(self, input_):
            ret = []
            for sent in input_:
                res = self.model.polarity_scores(sent)
                prob = (res["pos"] + 1e-6) / (res["neg"] + res["pos"] + 1e-6)
                ret.append(np.array([1 - prob, prob]))
            return np.array(ret)
    return MyClassifier()

def dataset_mapping(x):
    return {
        "x": x["sentence"],
        "y": 1 if x["label"] > 0.5 else 0,
    }

def text_input(model):
    text = input("Write a sentence: ")
    label = model.get_pred([text])
    
    adv_data = datasets.Dataset.from_dict({
    "x": [
        text
    ],
    "y": [
        label
    ]
})

    return adv_data


def main():

    print("New Attacker")
    attacker = OpenAttack.attackers.BERTAttacker()

    print("Build model")
    # clsf = OpenAttack.loadVictim("BERT.SST")
    clsf = make_model()

    adv_data = text_input(clsf)

    # dataset = datasets.load_dataset("sst", split="train[:100]").map(function=dataset_mapping)

    print("Start attack")
    attack_eval = OpenAttack.AttackEval( attacker, clsf, metrics=[
        OpenAttack.metric.Fluency(),
        OpenAttack.metric.GrammaticalErrors(),
        # OpenAttack.metric.SemanticSimilarity(),
        OpenAttack.metric.EditDistance(),
        OpenAttack.metric.ModificationRate()
    ] )
    # attack_eval.eval(adv_data, visualize=True, progress_bar=True)
    eval = attack_eval.ieval(adv_data)
    print( next(eval))


if __name__ == "__main__":
    main()