import os

from flask import Flask

from flask import render_template, request, jsonify

import openai

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    
    @app.route('/', methods=['GET', 'POST'])
    def start_page():
        if request.method == "POST":
            data = request.get_json()
            print(data)
            model = 'text-davinci-003'
            temperature = 0.7
            max_tokens = 1000
            top_p = 1.0
            frequency_penalty = 0.0
            presence_penalty = 0.0
            
            failure_count = 0

            openai.api_key = "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"
            if data['type'] == 'main':
                prompt = data['context'] + "\n\nQuestion:\n" + data['question'] + "\n\nAnswer:\n"
            
                #return jsonify({'output':'SHIT'})            
                output = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )["choices"][0]['text']
                #output = "BOIIIIIIIIIIIIIIIIII"
                return jsonify({'output': output})        
            elif data['type'] == 'follow-up':

                #return jsonify({'output':'SHIT'})

                prompt = data['context']
                for qa in data['qa_list']:
                    if not qa['removed']:
                        prompt += "\n\nQuestion:\n" + qa['question'] + "\n\nAnswer:\n" + qa['output']
                prompt += "\n\nQuestion:\n" + data['question'] + "\n\nAnswer:\n"
                output = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )["choices"][0]['text']
                #output = prompt
                return jsonify({'output': output})
            elif data['type'] == 'combine':

                #return jsonify({'output':'SHIT'})
                prompt = ""
                
                for qa in data['qa_list']:
                    if not qa['removed']:
                        prompt += "\n\nQuestion:\n" + qa['question'] + "\n\nAnswer:\n" + qa['output']

                prompt = prompt[2:]

                prompt += "\n\nCombine the answers to these questions coherently: "

                output = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )["choices"][0]['text']
                #output = data['context'] + " length: " + str(len(data['qa_list']))
                
                return jsonify({'output':output})
            elif data['type'] == 'opt_insert':
                #test_str = "Vitamin K inhibitors this, but Vitamin K BOODFKJDFKJD supplementation might slow calcidddddddfication progression. The VitaKddddddd-CAC tri will assess how MK-7 supplementation impacts CAC scores, arterial structure and function as well as biomarkers in patients with coronary artery disease."
                #output = test_str
                
                #return jsonify({'output':'SHIT'})
                
                prompt = data['surround'] + "\n\nInsert this elaboration about \"" + data['h_text'] + "\" in the above passage appropriately:\n\n" + data['insert_output'] + "\n\nPassage with insertion:\n\n"

                output = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )["choices"][0]['text']

                print(output)

                output = output.replace("\n", "")

                return jsonify({'output':output})
        return render_template('base.html')
    
    return app
