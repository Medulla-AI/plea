# PLEA: Progressive Language Enhancement Algorithm

# AUTHORS
Henry Ndubuaku\
henry@medullaai.com

# ABSTRACT
Language enhancement in this premise means the transformation of a bland body of text to a rich and nuanced paraphrase. Few-shot fine-tuning of large language models has become the panacea to all sequence-to-sequence problems. This approach is however complicated by dataset acquisition and training intricacies. Also, there is little control over the output during inference. To this end, this work introduces PLEA, an algorithm that employs controllable computational linguistics to progressively find positions in the input text to transform, and a frozen mask-filling transformer to find the most appropriate replacements or insertions for each.


# USAGE
1. Install requirements by running "pip install -r requirements.txt in the command line.
2. Import plea as a library with "from plea import PLEA"
3. Use to enhance a text by creating an instance "plea = PLEA()"
4. Then call the enhance_text with "output_texts = plea.enhance_text(input_text)"
