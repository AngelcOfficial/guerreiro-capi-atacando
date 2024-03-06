import pygame

# Inicialização
pygame.init()

# Medidas da tela
largura_tela, altura_tela = (1000, 720)

# Tela  
tela = pygame.display.set_mode((largura_tela, altura_tela))

#classe do personagem
class Guerreiro():
    #função para iniciar
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, largura_tela, altura_tela)) 
        self.y = y
        # reiniciando os frames para o primeiro frames na lista de frames 
        self.pulando = 0
        self.parado = 0 
        self.atacar = 0 
        
        self.velocidade = 20  # Velocidade de movimento do personagem
        self.direcao_anterior = "direita"

    # Movimento do personagem
    def mover_esquerda(self):
        if self.rect.x > 0:  # Verifica se o personagem está à esquerda do limite esquerdo da tela
            self.rect.x -= self.velocidade
        if self.direcao_anterior != "esquerda":
                self.rect.x -= self.velocidade
                self.direcao_anterior = "esquerda"
                
    def mover_direita(self):
        self.rect.x += self.velocidade
        if self.direcao_anterior != "direita":
                self.rect.x += self.velocidade
                self.direcao_anterior = "direita"

    # Função para rodar as sprites como parado ou atacando
    def desenhar(self,dicionario):
        # Parado
        personagem_imagem = dicionario['parado'][self.parado] # Pega imagem atual do personagem na posição parado
        self.parado += 1 # Incrementa a próxima imagem
        if self.parado >= len(dicionario['parado']): # Verifica a quantidade de frames
            self.parado = 0 # Reinicia a animação para a primeira imagem na lista anições parado

        # Atacar
        if self.atacar != 0: # Verifica se o personagem não está em estado de ataque
            if self.atacar < len(dicionario['atacando']):
                personagem_imagem = dicionario['atacando'][self.atacar] # Obtém as imagens do personagem na posição de ataque
                self.atacar += 1 # Incrementa a próxima imagem de animação
            else:
                self.atacar = 0    # Reinicia a animação
                pygame.time.delay(500)
        if (pygame.key.get_pressed()[pygame.K_SPACE]): # Verifica se a tecla de espaço foi pressionada
            personagem_imagem = dicionario['atacando'][self.atacar] # Obtém as imagens atual do personagem na posição de ataque
            self.atacar = 1 # Define a próxima imagem 
        else:
            self.atacar = 0 # Reinicia a animação
                
        # Pular   
        if self.y != self.rect.y:
            self.rect.y += 6
            if (self.y - self.rect.y) > 25:
                if self.pulando >= len(dicionario['pulando']):
                    self.pulando = 0
                personagem_imagem = dicionario['pulando'][self.pulando]
                   
        if (pygame.key.get_pressed()[pygame.K_UP]) and self.rect.top > 0:
                self.pulando = 0
                personagem_imagem = dicionario['pulando'][self.pulando]
                self.rect.y -= 30
    
        # Espelhar a imagem do personagem
        if self.direcao_anterior == "esquerda":
            personagem_imagem = pygame.transform.flip(personagem_imagem, True, False)
               
        # Andar
        tela.blit(personagem_imagem, self.rect)
        
# Variáveis para guardar as coordenadas da posição inicial
x , y = (300,200)

# Variável para guardar a classe e as coordenadas da posição inicial
personagem = Guerreiro(x,y)

# função para carregar as sprites
def carregar_sprites(self):
        # Lista de animações de sprites do Guerreiro
        guerreiro_sprites_lista = [
            pygame.image.load("guerreiro\imagens\personagem\Parado.png"),   # animações Parado
            pygame.image.load('guerreiro\imagens\personagem\Atacando.png'),  # animações Atacando
            pygame.image.load("guerreiro\imagens\personagem\Pulando.png"),
        ]
        
        # Dicionário para cada item da lista
        guerreiro_dicionario = {'parado': [], 
                                'atacando': [], 
                                'pulando': []
        }
        
        # Pegar a altura e largura das sprites sheets
        for x, tipo in enumerate(guerreiro_dicionario): # Percorre os itens do dicionário guerreiro_dicionario, x representa o índice do item na lista 
            sheet_largura = guerreiro_sprites_lista[x].get_width() #recebe a largura da imagem  
            sheet_altura = guerreiro_sprites_lista[x].get_height() #recebe a altura da imagem  
             
            # Percorrer todas as animações e separar cada animação das sprites sheets, altura por largura
            for i in range(int(sheet_largura / sheet_altura)): # Para determinar o número de animações 
                img = guerreiro_sprites_lista[x].subsurface( i * sheet_altura, 0, sheet_altura, sheet_altura)
                guerreiro_dicionario[tipo].append(pygame.transform.scale(img, (sheet_altura, sheet_altura)))
        return guerreiro_dicionario

# Variável auxiliar para guardar a função carregar_sprites
guerreiro = carregar_sprites(self = any)

# Função para desenhar o fundo
def desenhar_fundo():
    fundo = pygame.image.load('guerreiro\imagens\Fundo\medieval.jpg')  # Fundo qualquer
    fundo_ajustado = pygame.transform.scale(fundo, (largura_tela, altura_tela))
    tela.blit(fundo_ajustado, (0,0))

# Velocidade do ataque
velocidade_ataque = 30

# Rodar o jogo
jogando = True
while jogando:
    pygame.time.Clock().tick(10)
    
    #chamando a função do fundo
    desenhar_fundo()
    
    #chamando a função que desenha as sprites
    personagem.desenhar(guerreiro)

    # Movimentos do personagem
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        personagem.mover_esquerda()
    elif keys[pygame.K_RIGHT]:
        personagem.mover_direita()

    # sair do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
            
    # Aumentando a velocidade do ataque
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        if personagem.atacar == 0:
            personagem.atacar = 1
            pygame.time.Clock().tick(velocidade_ataque)

    pygame.display.flip()
pygame.quit()
