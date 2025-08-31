import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()  # carrega as credenciais do .env
MONGO_URI = os.getenv("DB_MONGO_URI")

class MongoManager:
    def __init__(self, uri):
        self.cliente = None
        self.banco = None
        try:
            self.cliente = MongoClient(uri)
            self.cliente.admin.command('ping')
            self.banco = self.cliente.sistema
            print("Conectou")
        except ConnectionFailure:
            print("Erro", file=sys.stderr)
            sys.exit(1)

    def fechar_conexao(self):
        if self.cliente:
            self.cliente.close()
            print("Fechou")

    def criar_usuario(self, cpf, nome, email):
        try:
            self.banco.usuarios.insert_one({"_id": cpf, "nome": nome, "email": email})
            print("Criou")
        except Exception:
            print("Erro")

    def ler_usuarios(self):
        for usuario in self.banco.usuarios.find():
            print(f"CPF: {usuario.get('_id')}, Nome: {usuario.get('nome')}, Email: {usuario.get('email')}")

    def atualizar_usuario(self, cpf, novo_nome, novo_email):
        aux = {}
        if novo_nome:
            aux['nome'] = novo_nome
        if novo_email:
            aux['email'] = novo_email
        if not aux:
            print("Nenhuma alteracao")
            return
        result = self.banco.usuarios.update_one({"_id": cpf}, {"$set": aux})
        if result.matched_count == 0:
            print("Nao achou")
        elif result.modified_count > 0:
            print("Atualizou")
        else:
            print("Nenhuma alteracao")

    def deletar_usuario(self, cpf):
        result = self.banco.usuarios.delete_one({"_id": cpf})
        if result.deleted_count == 0:
            print("Nao achou")
        else:
            print("Deletou")

    def criar_produto(self, nome, valor, quantidade):
        try:
            result = self.banco.produtos.insert_one({"nome": nome, "valor": valor, "quantidade": quantidade})
            print("Criou")
            return result.inserted_id
        except Exception:
            print("Erro")
            return None
    
    def ler_produtos(self):
        for produto in self.banco.produtos.find():
            print(f"ID: {produto.get('_id')}, Nome: {produto.get('nome')}, Valor: {produto.get('valor')}")

    def atualizar_produto(self, id_produto, novo_valor):
        result = self.banco.produtos.update_one({"_id": ObjectId(id_produto)}, {"$set": {"valor": novo_valor}})
        if result.matched_count == 0:
            print("Nao achou")
        else:
            print("Atualizou")
            
    def deletar_produto(self, id_produto):
        result = self.banco.produtos.delete_one({"_id": ObjectId(id_produto)})
        if result.deleted_count == 0:
            print("Nao achou")
        else:
            print("Deletou")

    def criar_endereco(self, rua, numero, bairro, cidade, cep, complemento):
        try:
            documento = {"rua": rua, "numero": numero, "bairro": bairro, "cidade": cidade, "cep": cep, "complemento": complemento}
            result = self.banco.enderecos.insert_one(documento)
            print("Criou")
            return result.inserted_id
        except Exception:
            print("Erro")
            return None

    def ler_enderecos(self):
        for end in self.banco.enderecos.find():
            print(f"ID: {end.get('_id')}, Rua: {end.get('rua')}, N°: {end.get('numero')}, Cidade: {end.get('cidade')}")

    def atualizar_endereco(self, id_endereco, nova_rua, novo_numero):
        result = self.banco.enderecos.update_one(
            {"_id": ObjectId(id_endereco)},
            {"$set": {"rua": nova_rua, "numero": novo_numero}}
        )
        if result.matched_count == 0:
            print("Nao achou")
        else:
            print("Atualizou")

    def deletar_endereco(self, id_endereco):
        result = self.banco.enderecos.delete_one({"_id": ObjectId(id_endereco)})
        if result.deleted_count == 0:
            print("Nao achou")
        else:
            print("Deletou")

# Menus foram gerados com auxílio de IA para ficarem mais bonitos e de fácil usabilidade
def menu_endereco(mongo_manager):
    while True:
        print("\n--- Menu Endereço (MongoDB) ---")
        print("1. Criar Endereço")
        print("2. Listar Endereços")
        print("3. Atualizar Endereço")
        print("4. Deletar Endereço")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            rua = input("Rua: ")
            numero = int(input("Número: "))
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            cep = input("CEP: ")
            complemento = input("Complemento: ")
            mongo_manager.criar_endereco(rua, numero, bairro, cidade, cep, complemento)
        elif opcao == '2':
            mongo_manager.ler_enderecos()
        elif opcao == '3':
            id_end = input("ID do endereço a atualizar: ")
            nova_rua = input("Nova rua: ")
            novo_num = int(input("Novo número: "))
            mongo_manager.atualizar_endereco(id_end, nova_rua, novo_num)
        elif opcao == '4':
            id_end = input("ID do endereço a deletar: ")
            mongo_manager.deletar_endereco(id_end)
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

def menu_usuario(mongo_manager):
    while True:
        print("\n--- Menu Usuário (MongoDB) ---")
        print("1. Criar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Deletar Usuário")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cpf = input("CPF: ")
            nome = input("Nome: ")
            email = input("Email: ")
            mongo_manager.criar_usuario(cpf, nome, email)
        elif opcao == '2':
            mongo_manager.ler_usuarios()
        elif opcao == '3':
            cpf = input("CPF do usuário a atualizar: ")
            novo_nome = input("Novo nome (deixe em branco para manter): ")
            novo_email = input("Novo email (deixe em branco para manter): ")
            mongo_manager.atualizar_usuario(cpf, novo_nome or None, novo_email or None)
        elif opcao == '4':
            cpf = input("CPF do usuário a deletar: ")
            mongo_manager.deletar_usuario(cpf)
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

def menu_produto(mongo_manager):
    while True:
        print("\n--- Menu Produto (MongoDB) ---")
        print("1. Criar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Deletar Produto")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            valor = float(input("Valor: "))
            quantidade = int(input("Quantidade: "))
            mongo_manager.criar_produto(nome, valor, quantidade)
        elif opcao == '2':
            mongo_manager.ler_produtos()
        elif opcao == '3':
            id_produto = input("ID do produto a atualizar: ")
            novo_valor = float(input("Novo valor: "))
            mongo_manager.atualizar_produto(id_produto, novo_valor)
        elif opcao == '4':
            id_produto = input("ID do produto a deletar: ")
            mongo_manager.deletar_produto(id_produto)
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

def menu_mongo(mongo_manager):
    while True:
        print("\n--- Menu Principal MongoDB ---")
        print("1. CRUD Usuário")
        print("2. CRUD Produto")
        print("3. CRUD Endereço")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_usuario(mongo_manager)
        elif opcao == '2':
            menu_produto(mongo_manager)
        elif opcao == '3':
            menu_endereco(mongo_manager)
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def main():
    mongo_manager = None
    try:
        mongo_manager = MongoManager(MONGO_URI)
        menu_mongo(mongo_manager)
    finally:
        if mongo_manager:
            mongo_manager.fechar_conexao()
    print("Fechou")

if __name__ == "__main__":
    main()