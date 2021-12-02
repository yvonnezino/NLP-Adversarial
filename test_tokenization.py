from transformers import BertTokenizer
import csv 
from transformers import DistilBertTokenizerFast
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')


def testingOutTokenization():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    text="Does this tokenize the sentence?"

    encoding = tokenizer.encode_plus(text, add_special_tokens = True, truncation = True,
    padding = "max_length", return_attention_mask = True, return_tensors = "pt")

    print(encoding)

def load_test_data():
    file = open("dreaddit-test.csv")
    csvreader = csv.reader(file)
    texts = []
    labels=[]
    for row in csvreader:
        texts.append(row[4])
        labels.append(row[5])
    file.close()
    return texts, labels

def load_training_data():
    file = open("dreaddit-train.csv")
    csvreader = csv.reader(file)
    texts = []
    labels=[]
    for row in csvreader:
        texts.append(row[4])
        labels.append(row[5])
    file.close()
    return texts, labels

def trainData():
    train_texts, train_labels=load_training_data()
    test_texts, test_labels=load_test_data()

    train_texts, val_texts, train_labels, val_labels = train_test_split(train_texts, train_labels, test_size=.2)

    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True)


    model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)
    training_args = TrainingArguments("test_trainer")
    trainer = Trainer(
        model=model, args=training_args, train_dataset=train_encodings, eval_dataset=test_encodings
    )
    trainer.train()


