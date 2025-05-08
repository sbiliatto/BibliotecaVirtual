from flask import Flask, request, redirect, render_template, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'

livros = []
emprestimos = {}


@app.route('/')
def index():
    return render_template('index.html', livros=livros, emprestimos=emprestimos)


@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        codigo = len(livros)
        livros.append([codigo, titulo, autor, ano])
        flash('Livro adicionado com sucesso!')
        return redirect('/')
    return render_template('adicionar_livro.html')


@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        livros[codigo] = [codigo, titulo, autor, ano]
        flash('Livro editado com sucesso!!')
        return redirect('/')

    livro = livros[codigo]
    return render_template('editar_livro.html', livro=livro)


@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    del livros[codigo]
    if codigo in emprestimos:
        del emprestimos[codigo]
    flash('Livro excluído com sucesso!!')
    return redirect('/')


@app.route('/emprestar_livro/<int:codigo>')
def emprestar_livro(codigo):
    data_emprestimo = datetime.now()
    data_devolucao = datetime.now() + timedelta(days = 7).strftime('%d/%m/%y')

    emprestimos[codigo] = {
        'data_emprestimo': data_emprestimo,
        'data_devolucao': data_devolucao,
    }

    flash(f'Livro emprestado com sucesso! Data de devolução: {data_devolucao}')
    return redirect('/')


@app.route('/devolver_livro/<int:codigo>')
def devolver_livro(codigo):
    if codigo in emprestimos:
        emprestimo = emprestimos[codigo]
        data_atual = datetime.now()
        data_devolucao = datetime.now() + timedelta(days = 7).strftime('%d/%m/%y')

        if data_atual > data_devolucao:
            dias_atraso = (data_atual - data_devolucao).days
            multa = 10 + (0.01 * dias_atraso * 10)
            flash(f'Livro devolvido com atraso de {dias_atraso} dias. Multa: R${multa:.2f}')
        else:
            flash('Livro devolvido com sucesso!')


    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)