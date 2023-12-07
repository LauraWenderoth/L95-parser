import subprocess
import json
from stanfordcorenlp import StanfordCoreNLP
from pathlib import Path

def berkeley(sentence):
    jar_path = "/home/lw754/L95/l95/berkeleyparser/BerkeleyParser-1.7.jar"
    grammar_file = "/home/lw754/L95/l95/berkeleyparser/eng_sm6.gr"

    # Construct the command to run the Berkeley Parser
    command = f"java -jar {jar_path} -gr {grammar_file}"

    try:
        # Run the Berkeley Parser command with the sentence as input
        result = subprocess.run(command, input=sentence, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)

        if result.returncode == 0:
            parsed_sentence = result.stdout
        else:
            parsed_sentence = f"Error: {result.stderr}"
    except Exception as e:
        parsed_sentence = f"Error: {str(e)}"

    return parsed_sentence

def standford(text):
    '''
    cd /home/lw754/L95/l95/stanford-corenlp-4.5.5
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 150000
    '''
    nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)
    props = {'annotators': 'parse', 'pipelineLanguage': 'en', 'parse.model': 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'}
    parsed = nlp.annotate(text, properties=props)

    if parsed:
        try:
            parsed_json = json.loads(parsed)
            parsed_sentence = parsed_json['sentences'][0]['parse'].replace('\n', '')
            return parsed_sentence
        except (json.JSONDecodeError, KeyError):
            return "Error: Invalid JSON or missing key in the parsed data"
    else:
        return "Error: Parsed data is empty"

def read_sentences(path,parser):
    file_path = Path(path) / 'sentences.txt'
    with open(file_path, 'r') as input_file:
        lines = input_file.readlines()
    parser_name = parser.__name__.replace('_', ' ')
    result_path = Path(path)/'results'
    result_path.mkdir(parents=True, exist_ok=True)
    with open(Path(result_path)/f'constituency_{parser_name}.txt', 'w') as output_file:
        for idx,line in enumerate(lines):
            if idx != 0:
                output_file.write('\n')
            parsed_sentence=parser(line).replace('\n', '')
            output_file.write(parsed_sentence)
    print(parsed_sentence)


if __name__ == "__main__":
    path = '/home/lw754/L95/L95-parser'
    read_sentences(path, standford)
    #read_sentences(path, berkeley)