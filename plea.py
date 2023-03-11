import spacy
import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer

class PLEA:
    def __init__(self, 
                 text_processing_model="en_core_web_sm",
                 text_embedding_model='sentence-transformers/all-MiniLM-L6-v2', 
                 mask_filling_model='distilroberta-base'):
        
        self.text_parser = spacy.load(text_processing_model)
        self.sentence_embedding_model = SentenceTransformer(text_embedding_model)
        self.mask_filling_model = pipeline('fill-mask', model=mask_filling_model)
        self.enhanced_texts = []

        """
        TAG  NAME                   EXAMPLE                     ENHANCEMENT     EXAMPLE
        JJR  Comparative Adjective  this is 'better'            insert before   this is 'significantly better'
        PDT  Predeterminer          this is 'half' the journey  insert before   this is 'only half' the journey
        RBR  Comparative Adverb     she slept 'longer'          insert before   she slept 'relatively longer'
        MD   Modal Auxillary Verb   I 'can' call you            replace         I 'could' call you
        """

        self.tags_to_enhance = set(["JJR", "PDT", "RBR"])
        self.tags_to_replace = set(["MD"])


    def enhance_text(self, text, top_k=1, confidence=0.2, tolerance=0.9):
        self.enhanced_texts.append(text)
        tags = self.get_granular_parts_of_speech(text)

        for index in range(len(tags)):
            if tags[index] in self.tags_to_enhance:
                masked_text = self.insert_mask(text, index)
            elif tags[index] in self.tags_to_replace:
                masked_text = self.replace_word_with_mask(text, index)
            else:
                continue

            candidates = self.fill_mask(masked_text, top_k, confidence)
            if len(candidates) < 1:
                continue

            similarity_scores = self.sentence_similarity(text, candidates)
            self.extend_enhanced_texts(candidates, similarity_scores, tolerance)

        return self.enhanced_texts


    def insert_mask(self, text, index):
        split_text = text.split(" ")
        return " ".join(split_text[:index] + ["<mask>"] + split_text[index:])

    
    def replace_word_with_mask(self, text, index, n_masks=1):
        split_text = text.split(" ")
        masks = ["<mask>" for _ in range(n_masks)]
        return " ".join(split_text[:index] + masks + split_text[index+1:])


    def get_granular_parts_of_speech(self, text):
        processed_text = self.text_parser(text)
        return [token.tag_ for token in processed_text]


    def fill_mask(self, masked_text, top_k=1, confidence=0.0):
        outputs = self.mask_filling_model(masked_text)[:top_k]
        confident_outputs = [output['sequence'] for output in outputs if output["score"]>=confidence]
        return confident_outputs


    def sentence_similarity(self, source, candidates):
        source_embedding = self.sentence_embedding_model.encode(source)
        candidates_embedding = self.sentence_embedding_model.encode(candidates)
        return self.cosine_similarity(source_embedding, candidates_embedding)


    def cosine_similarity(self, embedding1, embedding2):
        dot_product = np.dot(embedding2, embedding1.T).squeeze()
        norm_embedding1 = np.linalg.norm(embedding1)
        norm_embedding2 = np.sqrt(np.einsum('ij,ij->i', embedding2, embedding2))
        return dot_product / (norm_embedding1 * norm_embedding2)


    def extend_enhanced_texts(self, candidates, simiarity_scores, tolerance):
        for candidate, score in zip(candidates, simiarity_scores):
            if score >= tolerance:
                self.enhanced_texts.append(candidate)
