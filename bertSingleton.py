from transformers import pipeline

class Bert:

    _instance = None

    def __init__(self):
        self.some_attribute = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            model_checkpoint = 'bert-large-uncased-whole-word-masking-finetuned-squad'
            qa_pipeline = pipeline('question-answering', model=model_checkpoint, tokenizer=model_checkpoint)
            cls._instance = qa_pipeline
        return cls._instance