from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import string
import os

app = Flask(__name__)

def generate_word(word_length):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'words.txt')
    
    with open(file_path, 'r') as f:
        words = [word.strip() for word in f.readlines() if len(word.strip()) == word_length]
    return random.choice(words).upper()

def compare_words(word1, word2):
    result = ''
    for i, c in enumerate(word1):
        if c == word2[i]:
            result += 'X'
        elif c in word2:
            result += 'O'
        else:
            result += '.'
    return result

@app.route('/')
def index():
    word = generate_word(5)
    return render_template('index.html', word=word)

@app.route('/check', methods=['POST'])
def check_word():
    word = request.form['word'].upper()
    guess = request.form['guess'].upper()

    if len(guess) != 5 or not guess.isalpha():
        return jsonify({'error': 'Invalid input. Please enter a 5-letter word.'})

    result = compare_words(word, guess)
    guessed = result == 'XXXXX'

    return jsonify({'result': result, 'guessed': guessed})

if __name__ == '__main__':
    app.run(debug=True)

