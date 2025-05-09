from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'minha_chave'

livros = []


@app.route('/')
def index():
    return render_template('index.html', livros=livros)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        codigo = len(livros)
        novo_livro = {
            "codigo" : codigo,
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "ano": request.form['ano'],
            "emprestado": False,
            "data_devolucao": None,
            "atrasado": False,
            "multa": 0
        }
        livros.append(novo_livro)
        return redirect('/')
    return render_template('adicionar_livro.html')

@app.route('/editar/<int:codigo>', methods=['GET', 'POST'])
def editar(codigo):
    livro_encontrado = None
    for livro in livros:
        if livro['codigo'] == codigo:
            livro_encontrado = livro
            break

    if not livro_encontrado:
        return redirect('/')

    if request.method == 'POST':
        livro_encontrado['titulo'] = request.form['titulo']
        livro_encontrado['autor'] = request.form['autor']
        livro_encontrado['ano'] = request.form['ano']
        return redirect('/')

    return render_template('editar_livro.html', livro=livro_encontrado)


@app.route('/excluir/<string:titulo>')
def excluir(titulo):
    global livros
    livros = [livro for livro in livros if livro['titulo'] != titulo]
    return redirect('/')


@app.route('/emprestar/<string:titulo>')
def emprestar(titulo):
    for livro in livros:
        if livro['titulo'] == titulo:
            livro['emprestado'] = True
            livro['data_devolucao'] = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
            livro['atrasado'] = False
            livro['multa'] = 0
    return redirect('/')


@app.route('/devolver/<string:titulo>')
def devolver(titulo):
    for livro in livros:
        if livro['titulo'] == titulo:
            data_devolucao = datetime.strptime(livro['data_devolucao'], '%d/%m/%Y')
            if datetime.now() > data_devolucao:
                dias_atraso = (datetime.now() - data_devolucao).days
                livro['multa'] = 10 + (10 * 0.01 * dias_atraso)
                livro['atrasado'] = True
            else:
                livro['atrasado'] = False
                livro['multa'] = 0

            livro['emprestado'] = False

            return render_template('devolver.html',
                                livro=livro,
                                datetime=datetime)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)