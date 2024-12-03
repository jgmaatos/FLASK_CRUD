from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib

app = Flask(__name__)
app.secret_key = '12345'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_sql' 

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    if request.method == 'POST':
        # Captura dos dados do formulario
        nome = request.form['nome']
        email = request.form['email']
        senha = hashlib.sha256(request.form['senha'].encode()).hexdigest()

        # Conecta ao banco  de dados e insere o registro
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)', (nome, email, senha))
        mysql.connection.commit()
        cursor.close()
        flash('Usuário cadastrado com sucesso!')
        return redirect('/')
    return redirect('/')

@app.route('/dados')
def dados():
    # Conecta ao banco de dados e recupera os dados dos usuarios
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, nome, email FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('dados.html', usuarios=usuarios)

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        # Captura dos dados do formulario
        nome = request.form['nome']
        email = request.form['email']

        # Conecta ao banco de dados e atualiza o registro
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE usuarios SET nome=%s, email=%s WHERE id=%s', (nome, email, id))
        mysql.connection.commit()
        cursor.close()
        flash('Usuário editado com sucesso!')
        return redirect('/dados')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, nome, email FROM usuarios WHERE id=%s', (id,))
    usuario = cursor.fetchone()
    cursor.close()
    return render_template('editar.html', usuario=usuario)

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM usuarios WHERE id=%s', (id))
    mysql.connection.commit()
    cursor.close()

    flash('Usuário deletado co sucesso!')
    return redirect('/dados')


    

if __name__ == '__main__':
    app.run(debug=True)