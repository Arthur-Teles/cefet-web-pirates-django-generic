from django.test.client import Client
from django.test.testcases import TestCase
from .models import Tesouro
from django.urls import reverse
from .views import *
from io import BytesIO

class TestTesouros(TestCase):
    def setUp(self):
        self.tesouros_existentes = []

        self.img = BytesIO(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
            b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00"
        )

        self.img.name = "imgzinha.png"

        self.tesouros_existentes.append(Tesouro.objects.create(nome="Coroa", quantidade=10, preco=2000, img_tesouro=self.img.name))
        self.tesouros_existentes.append(Tesouro.objects.create(nome="Moedas", quantidade=20, preco=100, img_tesouro=self.img.name))
    
    def listaTesouros(self):
        c = Client()

        requisicao_pedido = reverse("lista_tesouros")
        requisicao_resposta = c.get(requisicao_pedido)
        resultado_requisicao = requisicao_resposta.context
        
        tesouros_resposta = resultado_requisicao["object_list"]

        for tesouro in tesouros_resposta:
            encontrou = False

            for tesouro_inserido in self.tesouros_existentes:
                if tesouro["id"] == tesouro_inserido.id:
                    encontrou = True
                    self.assertEqual(tesouro["nome"], tesouro_inserido.nome, "Nome não correspondente à lista de tesouros")
            
            self.assertTrue(encontrou, "O tesouro de nome: " + tesouro["nome"] + " não foi encontrado")
    
    def inserirTesouro(self):
        c = Client()

        requisicao_pedido = reverse("inserir")
        c.post(requisicao_pedido, {"nome": "Rum", "quantidade": 4, "preco": 200, "img_tesouro": self.img})

        verificar_rum = Tesouro.objects.filter(quantidade=4)

        self.assertEqual(1, len(verificar_rum), "Tesouro não inserido!")
    
    def deletarTesouro(self):
        c = Client()

        id_tesouro_deletar = self.tesouros_existentes[1].id
        requisicao = reverse("excluir", kwargs={"pk":id_tesouro_deletar})

        c.post(requisicao)

        verificar_delete = Tesouro.objects.filter(nome="Moedas")
        self.assertEqual(0, len(verificar_delete), "Tesouro não deletado")

    def atualizarTesouro(self):
        c = Client()

        id_tesouro_atualizar = self.tesouros_existentes[0].id
        requisicao = reverse("editar", kwargs={"pk":id_tesouro_atualizar})

        c.post(requisicao, {"nome": "Novo Tesouro"})

        verificar_atualizacao = Tesouro.objects.filter(nome="Coroa")
        self.assertEqual(0, len(verificar_atualizacao), "Tesouro não modificado!")