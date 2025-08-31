# BIBLIOTECA NECESSARIA P/ EXEC
# psycopg2-binary
# pip install psycopg2-binary


import psycopg2
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # carrega as credenciais do .env

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}


class PostgresManager:
    def __init__(self, config):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(**config)
            self.cursor = self.conn.cursor()
            print("Conectou")
        except psycopg2.OperationalError:
            print("Erro")
            sys.exit(1)

    def fechar_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Fechou")

    def criar_usuario(self, cpf, nome, email):
        sql = """
        INSERT INTO mydb.Usuario (cpf, nome, email, Dados_bancarios_idDados_bancarios) 
        VALUES (%s, %s, %s, 1) RETURNING cpf;
        """
        try:
            self.cursor.execute(sql, (cpf, nome, email))
            self.conn.commit()
            print("Criou")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")

    def ler_usuarios(self):
        self.cursor.execute("SELECT cpf, nome, email FROM mydb.Usuario;")
        aux = self.cursor.fetchall()
        if not aux:
            print("Não achou")
        for linha in aux:
            print(f"CPF: {linha[0]}, Nome: {linha[1]}, Email: {linha[2]}")

    def atualizar_usuario(self, cpf, email):
        sql = "UPDATE mydb.Usuario SET email = %s WHERE cpf = %s;"
        try:
            self.cursor.execute(sql, (email, cpf))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print("Não achou")
            else:
                print("E-mail atualizado")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")

    def deletar_usuario(self, cpf):
        sql = "DELETE FROM mydb.Usuario WHERE cpf = %s;"
        try:
            self.cursor.execute(sql, (cpf,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print("Não encontrado")
            else:
                print("Deletado")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")

    def criar_produto(self, nome, valor, quantidade):
        sql = """
        INSERT INTO mydb.Produto (nome, valor, quantidade, descricao, porcao_peso) 
        VALUES (%s, %s, %s, 'N/A', 0) RETURNING idProduto;
        """
        try:
            self.cursor.execute(sql, (nome, valor, quantidade))
            id_prod = self.cursor.fetchone()[0]
            self.conn.commit()
            print("Criou")
            return id_prod
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")
            return None

    def ler_produtos(self):
        self.cursor.execute("SELECT idProduto, nome, valor, quantidade FROM mydb.Produto;")
        aux = self.cursor.fetchall()
        if not aux:
            print("Nenhum produto encontrado.")
        for linha in aux:
            print(f"ID: {linha[0]}, Nome: {linha[1]}, Valor: R${linha[2]:.2f}, Qtd: {linha[3]}")


    def atualizar_produto(self, id_prod, valor):
        sql = "UPDATE mydb.Produto SET valor = %s WHERE idProduto = %s;"
        try:
            self.cursor.execute(sql, (valor, id_prod))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print("Não encontrado")
            else:
                print("Valor atualizado")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")
    
    def deletar_produto(self, id_prod):
        sql = "DELETE FROM mydb.Produto WHERE idProduto = %s;"
        try:
            self.cursor.execute(sql, (id_prod,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print("Não encontrado")
            else:
                print("Deletado")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")

    def criar_endereco(self, rua, numero, bairo, cidade, cep, complemento):
        sql = """
        INSERT INTO mydb.Endereco (rua, numero, bairo, cidade, cep, complemento) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING idEndereco;
        """
        try:
            self.cursor.execute(sql, (rua, numero, bairo, cidade, cep, complemento))
            id_endereco = self.cursor.fetchone()[0]
            self.conn.commit()
            print("Criou")
            return id_endereco
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")

    def ler_enderecos(self):
        self.cursor.execute("SELECT idEndereco, rua, numero, bairo, cidade, cep FROM mydb.Endereco;")
        aux = self.cursor.fetchall()
        if not aux:
            print("Não encontrado")
        for linha in aux:
            print(f"ID: {linha[0]}, Rua: {linha[1]}, Nº: {linha[2]}, Bairro: {linha[3]}, Cidade: {linha[4]}, CEP: {linha[5]}")

    def atualizar_endereco(self, id_endereco, rua, numero, complemento):
        sql = "UPDATE mydb.Endereco SET rua = %s, numero = %s, complemento = %s WHERE idEndereco = %s;"
        try:
            self.cursor.execute(sql, (rua, numero, complemento, id_endereco))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print("Não encontrado")
            else:
                print("Endereço atualizado")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")

    def deletar_endereco(self, id_endereco):
        sql = "DELETE FROM mydb.Endereco WHERE idEndereco = %s;"
        try:
            self.cursor.execute(sql, (id_endereco,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print("Não encontrado")
            else:
                print("Endereço deletado")
        except psycopg2.Error:
            self.conn.rollback()
            print("Erro")


# Menus foram gerados com auxílio de IA para ficarem mais bonitos e de fácil usabilidade
def menu_usuario(pg_manager):
    while True:
        print("\n--- 👤 Gerenciar Usuários ---")
        print("1. Criar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar E-mail de Usuário")
        print("4. Deletar Usuário")
        print("5. Voltar ao Menu Principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            cpf = input("Digite o CPF do usuário: ")
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o email do usuário: ")
            pg_manager.criar_usuario(cpf, nome, email)
        elif choice == '2':
            pg_manager.ler_usuarios()
        elif choice == '3':
            cpf = input("Digite o CPF do usuário que deseja atualizar: ")
            email = input(f"Digite o novo email para o usuário {cpf}: ")
            pg_manager.atualizar_usuario(cpf, email)
        elif choice == '4':
            cpf = input("Digite o CPF do usuário que deseja deletar: ")
            pg_manager.deletar_usuario(cpf)
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_produto(pg_manager):
    while True:
        print("\n--- 📦 Gerenciar Produtos ---")
        print("1. Criar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Valor de Produto")
        print("4. Deletar Produto")
        print("5. Voltar ao Menu Principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            nome = input("Digite o nome do produto: ")
            valor = float(input("Digite o valor do produto: "))
            qtd = int(input("Digite a quantidade do produto: "))
            pg_manager.criar_produto(nome, valor, qtd)
        elif choice == '2':
            pg_manager.ler_produtos()
        elif choice == '3':
            id_p = int(input("Digite o ID do produto que deseja atualizar: "))
            novo_valor = float(input(f"Digite o novo valor para o produto ID {id_p}: "))
            pg_manager.atualizar_produto(id_p, novo_valor)
        elif choice == '4':
            id_p = int(input("Digite o ID do produto que deseja deletar: "))
            pg_manager.deletar_produto(id_p)
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_endereco(pg_manager):
    while True:
        print("\n--- 📍 Gerenciar Endereços ---")
        print("1. Cadastrar Novo Endereço")
        print("2. Listar Endereços")
        print("3. Atualizar Endereço")
        print("4. Deletar Endereço")
        print("5. Voltar ao Menu Principal")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            rua = input("Digite a rua: ")
            numero = int(input("Digite o número: "))
            bairo = input("Digite o bairro: ")
            cidade = input("Digite a cidade: ")
            cep = input("Digite o CEP (8 dígitos): ")
            complemento = input("Digite o complemento: ")
            pg_manager.criar_endereco(rua, numero, bairo, cidade, cep, complemento)
        elif choice == '2':
            pg_manager.ler_enderecos()
        elif choice == '3':
            id_end = int(input("Digite o ID do endereço que deseja atualizar: "))
            rua = input("Digite a nova rua: ")
            numero = int(input("Digite o novo número: "))
            complemento = input("Digite o novo complemento: ")
            pg_manager.atualizar_endereco(id_end, rua, numero, complemento)
        elif choice == '4':
            id_end = int(input("Digite o ID do endereço que deseja deletar: "))
            pg_manager.deletar_endereco(id_end)
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_principal(pg_manager):
    while True:
        print("\n--- 🛠️ Menu Principal ---")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Produtos")
        print("3. Gerenciar Endereços")
        print("4. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            menu_usuario(pg_manager)
        elif choice == '2':
            menu_produto(pg_manager)
        elif choice == '3':
            menu_endereco(pg_manager)
        elif choice == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    pg_manager = None
    try:
        pg_manager = PostgresManager(DB_CONFIG)
        menu_principal(pg_manager)
    finally:
        if pg_manager:
            pg_manager.fechar_conexao()
    print("Programa finalizado.")

if __name__ == "__main__":
    main()