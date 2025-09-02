import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
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
            print("Conectado ao MongoDB com sucesso!")
        except ConnectionFailure:
            print("Erro: Não foi possível conectar ao MongoDB", file=sys.stderr)
            sys.exit(1)

    def fechar_conexao(self):
        if self.cliente:
            self.cliente.close()
            print("Conexão fechada")

    def get_next_sequence(self, collection_name):
        """Obtém o próximo ID sequencial para uma coleção"""
        try:
            counter = self.banco.counters.find_one_and_update(
                {'_id': collection_name},
                {'$inc': {'seq': 1}},
                upsert=True,
                return_document=True
            )
            return counter['seq']
        except Exception as e:
            print(f"Erro ao obter próximo ID sequencial: {e}")
            return None

    def criar_usuario(self, cpf, nome, email):
        try:
            self.banco.usuarios.insert_one({"_id": cpf, "nome": nome, "email": email})
            print("Usuário criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")

    def ler_usuarios(self):
        try:
            usuarios = list(self.banco.usuarios.find())
            if not usuarios:
                print("Nenhum usuário cadastrado.")
                return
                
            for usuario in usuarios:
                print(f"CPF: {usuario.get('_id')}, Nome: {usuario.get('nome')}, Email: {usuario.get('email')}")
        except Exception as e:
            print(f"Erro ao ler usuários: {e}")

    def atualizar_usuario(self, cpf, novo_nome, novo_email):
        try:
            aux = {}
            if novo_nome:
                aux['nome'] = novo_nome
            if novo_email:
                aux['email'] = novo_email
            if not aux:
                print("Nenhuma alteração informada")
                return
                
            result = self.banco.usuarios.update_one({"_id": cpf}, {"$set": aux})
            if result.matched_count == 0:
                print("Usuário não encontrado.")
            elif result.modified_count > 0:
                print("Usuário atualizado com sucesso!")
            else:
                print("Nenhuma alteração realizada.")
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")

    def deletar_usuario(self, cpf):
        try:
            result = self.banco.usuarios.delete_one({"_id": cpf})
            if result.deleted_count == 0:
                print("Usuário não encontrado.")
            else:
                print("Usuário deletado com sucesso!")
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")

    def criar_produto(self, nome, valor, quantidade):
        try:
            # Obter o próximo ID sequencial
            id_produto = self.get_next_sequence('produtos')
            if id_produto is None:
                print("Erro ao gerar ID para o produto")
                return None
                
            valor = float(valor)
            quantidade = int(quantidade)
            
            result = self.banco.produtos.insert_one({
                "_id": id_produto,
                "nome": nome, 
                "valor": valor, 
                "quantidade": quantidade
            })
            print("Produto criado com sucesso!")
            return id_produto
        except ValueError:
            print("Erro: Valor ou quantidade inválidos. Certifique-se de usar números.")
            return None
        except Exception as e:
            print(f"Erro ao criar produto: {e}")
            return None
    
    def ler_produtos(self):
        try:
            produtos = list(self.banco.produtos.find())
            if not produtos:
                print("Nenhum produto cadastrado.")
                return
                
            for produto in produtos:
                print(f"ID: {produto.get('_id')}, Nome: {produto.get('nome')}, Valor: R${produto.get('valor'):.2f}, Quantidade: {produto.get('quantidade')}")
        except Exception as e:
            print(f"Erro ao ler produtos: {e}")

    def atualizar_produto(self, id_produto, novo_valor):
        try:
            # Converter para inteiro
            id_produto = int(id_produto)
            result = self.banco.produtos.update_one(
                {"_id": id_produto},
                {"$set": {"valor": float(novo_valor)}}
            )
            if result.matched_count == 0:
                print("Produto não encontrado.")
            else:
                print("Produto atualizado com sucesso.")
        except ValueError:
            print("ID do produto inválido. Deve ser um número inteiro.")
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            
    def deletar_produto(self, id_produto):
        try:
            # Converter para inteiro
            id_produto = int(id_produto)
            result = self.banco.produtos.delete_one({"_id": id_produto})
            if result.deleted_count == 0:
                print("Produto não encontrado.")
            else:
                print("Produto deletado com sucesso.")
        except ValueError:
            print("ID do produto inválido. Deve ser um número inteiro.")
        except Exception as e:
            print(f"Erro ao deletar produto: {e}")

    def criar_endereco(self, rua, numero, bairro, cidade, cep, complemento):
        try:
            # Obter o próximo ID sequencial
            id_endereco = self.get_next_sequence('enderecos')
            if id_endereco is None:
                print("Erro ao gerar ID para o endereço")
                return None
                
            documento = {
                "_id": id_endereco,
                "rua": rua, 
                "numero": numero, 
                "bairro": bairro, 
                "cidade": cidade, 
                "cep": cep, 
                "complemento": complemento
            }
            result = self.banco.enderecos.insert_one(documento)
            print("Endereço criado com sucesso!")
            return id_endereco
        except Exception as e:
            print(f"Erro ao criar endereço: {e}")
            return None

    def ler_enderecos(self):
        try:
            enderecos = list(self.banco.enderecos.find())
            if not enderecos:
                print("Nenhum endereço cadastrado.")
                return
                
            for end in enderecos:
                print(f"ID: {end.get('_id')}, Rua: {end.get('rua')}, N°: {end.get('numero')}, Bairro: {end.get('bairro')}, Cidade: {end.get('cidade')}")
        except Exception as e:
            print(f"Erro ao ler endereços: {e}")

    def atualizar_endereco(self, id_endereco, nova_rua, novo_numero):
        try:
            # Converter para inteiro
            id_endereco = int(id_endereco)
            result = self.banco.enderecos.update_one(
                {"_id": id_endereco},
                {"$set": {"rua": nova_rua, "numero": novo_numero}}
            )
            if result.matched_count == 0:
                print("Endereço não encontrado.")
            else:
                print("Endereço atualizado com sucesso.")
        except ValueError:
            print("ID do endereço inválido. Deve ser um número inteiro.")
        except Exception as e:
            print(f"Erro ao atualizar endereço: {e}")

    def deletar_endereco(self, id_endereco):
        try:
            # Converter para inteiro
            id_endereco = int(id_endereco)
            result = self.banco.enderecos.delete_one({"_id": id_endereco})
            if result.deleted_count == 0:
                print("Endereço não encontrado.")
            else:
                print("Endereço deletado com sucesso.")
        except ValueError:
            print("ID do endereço inválido. Deve ser um número inteiro.")
        except Exception as e:
            print(f"Erro ao deletar endereço: {e}")

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
            try:
                id_end = int(input("ID do endereço a atualizar: "))
                nova_rua = input("Nova rua: ")
                novo_num = int(input("Novo número: "))
                mongo_manager.atualizar_endereco(id_end, nova_rua, novo_num)
            except ValueError:
                print("ID do endereço deve ser um número inteiro.")
        elif opcao == '4':
            try:
                id_end = int(input("ID do endereço a deletar: "))
                mongo_manager.deletar_endereco(id_end)
            except ValueError:
                print("ID do endereço deve ser um número inteiro.")
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
            try:
                id_produto = int(input("ID do produto a atualizar: "))
                novo_valor = float(input("Novo valor: "))
                mongo_manager.atualizar_produto(id_produto, novo_valor)
            except ValueError:
                print("ID do produto deve ser um número inteiro.")
        elif opcao == '4':
            try:
                id_produto = int(input("ID do produto a deletar: "))
                mongo_manager.deletar_produto(id_produto)
            except ValueError:
                print("ID do produto deve ser um número inteiro.")
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
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        if mongo_manager:
            mongo_manager.fechar_conexao()
    print("Programa encerrado")

if __name__ == "__main__":
    main()