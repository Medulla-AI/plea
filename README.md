# PLEA: Progressive Language Enhancement Algorithm

# AUTHORS
Henry Ndubuaku\
henry@medullaai.com

# ABSTRACT
Language enhancement in this premise means the transformation of a bland body of text to a rich and nuanced paraphrase. Few-shot fine-tuning of large language models has become the panacea to all sequence-to-sequence problems. This approach is however complicated by dataset acquisition and training intricacies. Also, there is little control over the output during inference. To this end, this work introduces PLEA, an algorithm that employs controllable computational linguistics to progressively find positions in the input text to transform, and a frozen mask-filling transformer to find the most appropriate replacements or insertions for each.


# BACKGROUND
One of BERT's training pre-training process includes mask-filling (Delvin et. al, 2019). This invlolves randomly removing tokens from the input sentence and training the transformer to replace it, hence the model learns the most appropriate word to complete the sentence. Most inudtry applications of BERT focus on fewer shot transfer learning whereby the model (or some of its layers) is fine-tuned on relevant datasets. However, works like (Wu et. al, 2019), (Zhang et. al 2021) and (Luitel et. al, 2023) demonstrate BERT's ability to find appropriate words to complete a sentence.

Language enhancement is different from grammar correction, it involves subtle changes in the input sentence to embellish its grammar. Consider the an input text like "Today's sales is better than before, numbers were very bad yesterday." The sample sentence above is both synctatically and semantically correct. However, simply inserting the adjective "much" before "better" transforms the sentence to "Today's sales is much better than before, numbers were very bad yesterday." This strengthens the message it conveys. 

Minimal differences in input and output sequences are very difficult for accessible sequence-to-sequence models, (). To this end, this work proposes PLEA (Progressive Language Enhancement Algorithm).


# APPROACH
PLEA searches for words with specific fine-grained part-of-speech tags, then either inserts a supporting adjectvie/adverb before/after it or replaces the token. This is performed causally, while at each step optimizing for high sentence similarity between the input and the output.

Rule-based comptational linguistics often encounter many compicating edge-cases, hence the lingustic rules were limited to the 4 below with minimal edge cases.

| TAG | NAME                  | EXAMPLE                    | ACTION              | EXAMPLE                            |
| --- | --------------------  | -------------------------- | ------------------- | ---------------------------------- |
| JJR | Comparative Adjective | this is 'better'           | insert mask before  | this is 'significantly better'.    |
| PDT | Predeterminer         | this is 'half' the journey | insert mask before  | this is 'only half' the journey.   |
| RBR | Comparative Adverb    | she slept 'longer'         | insert mask before  | she slept 'relatively longer'      |
| MD  | Modal Auxillary Verb  | I 'can' call you           | replace mask        | I 'could' call you                 |

**PLEA**\
```
    let sentence (string): input sentence
    let n: number of possible sentences at each point 
    let *s*: sentence embedding
    let *P*: embeddings of potential sentences
    let c: confidence threshold
    let t: minimum sentencence similarity 
    
    For word in sentence:
    
       if POS-Tag of word is JJR or PDT or RBR:
           Insert mask token before word
    
       if POS-Tag of word is MD:
           replace word with mask token
         
       else:
          continue
              
       candidates = top-k replacement words where p(Word<sub>n</sub>|Word<sub>0</sub>...Word<sub>n-1</sub> & Word<sub>n+1</sub>...Word<sub>end</sub>) >= c
       extend choices = sentences where 
       
    return choices
```

# USAGE
1. Install requirements by running "pip install -r requirements.txt in the command line.
2. Import plea as a library with "from plea import PLEA"
3. Use to enhance a text by creating an instance "plea = PLEA()"
4. Then call the enhance_text with "output_texts = plea.enhance_text(input_text)"
