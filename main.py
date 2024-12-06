import pygame as pg

pg.init()


x = 1280
y = 720

screen = pg.display.set_mode((x, y))
pg.display.set_caption('Dinossaurinhowwnn')


cenario = pg.image.load('img/cenario.jpg').convert_alpha()
cenario = pg.transform.scale(cenario, (x * 2, y)) 


pers_sprites = [
    pg.transform.scale(pg.image.load(f'perso/run/frame-{i}.png').convert_alpha(), (60, 60))
    for i in range(1, 4)
]
pos_pers_x = 250
pos_pers_y = 550  
vel_y = 0  
gravidade = 0.8
pulando = False
chao = 550
chao_obs = 610  
current_frame = 0
frame_rate = 10


obstaculo_tipos = [
    ('obst/2.png', 35, 90),
]
velocidade_cenario = -5 
obstaculos = []


clock = pg.time.Clock()


def criar_obstaculo():
    tipo = obstaculo_tipos[0]  
    imagem = pg.image.load(tipo[0]).convert_alpha()
    imagem = pg.transform.scale(imagem, (tipo[1], tipo[2]))
    novo_obstaculo_x = x  
    novo_obstaculo_y = chao_obs - tipo[2] 
    rect = pg.Rect(novo_obstaculo_x, novo_obstaculo_y, tipo[1], tipo[2])
    return (rect, imagem)


def adicionar_obstaculos():
    if len(obstaculos) < 3:  
        obstaculos.append(criar_obstaculo())


tempo_criar_obstaculo = 0.5


rel_x = 0  


pontos = 0
passou_por_obstaculo = []


tempo_inicial = pg.time.get_ticks()  
exibir_texto = True  


def reiniciar_jogo():
    global pos_pers_x, pos_pers_y, vel_y, pulando, pontos, obstaculos, tempo_criar_obstaculo, rel_x
    pos_pers_x = 250
    pos_pers_y = 550
    vel_y = 0
    pulando = False
    pontos = 0
    passou_por_obstaculo.clear()
    obstaculos.clear()
    tempo_criar_obstaculo = 1
    rel_x = 0

root = True
jogo_ativo = True

while root:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            root = False
        if event.type == pg.KEYDOWN and jogo_ativo:
            if event.key == pg.K_SPACE and not pulando: 
                pulando = True
                vel_y = -15  
        if event.type == pg.MOUSEBUTTONDOWN and not jogo_ativo:
            
            mouse_pos = pg.mouse.get_pos()
            if botao_reiniciar.collidepoint(mouse_pos):
                reiniciar_jogo()
                jogo_ativo = True

    if jogo_ativo:
        
        rel_x = (rel_x + velocidade_cenario) % cenario.get_rect().width
        screen.blit(cenario, (rel_x - cenario.get_rect().width, 0))
        screen.blit(cenario, (rel_x, 0))

       
        tempo_criar_obstaculo += 1
        if tempo_criar_obstaculo > 95:  
            adicionar_obstaculos()
            tempo_criar_obstaculo = 0

        
        for i, (obstaculo, imagem) in enumerate(obstaculos):
            obstaculo.x += velocidade_cenario

            
            if obstaculo.x + obstaculo.width < pos_pers_x and obstaculo not in passou_por_obstaculo:
                if pulando:
                    pontos += 1  
                    passou_por_obstaculo.append(obstaculo)  

        
        obstaculos = [obs for obs in obstaculos if obs[0].x + obs[0].width > 0]


        if pulando:
            pos_pers_y += vel_y
            vel_y += gravidade 

            if pos_pers_y >= chao:  
                pos_pers_y = chao  
                pulando = False 

      
        current_frame += 1
        if current_frame >= len(pers_sprites) * frame_rate:
            current_frame = 0
        pers = pers_sprites[current_frame // frame_rate]

     
        personagem_rect = pg.Rect(pos_pers_x, pos_pers_y, 60, 60)
        for obstaculo, _ in obstaculos:
            if personagem_rect.colliderect(obstaculo):
                jogo_ativo = False  

       
        for obstaculo, imagem in obstaculos:
            screen.blit(imagem, (obstaculo.x, obstaculo.y))  


        screen.blit(pers, (pos_pers_x, pos_pers_y))

        font = pg.font.SysFont("Arial black", 30)
        texto_pontos = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        screen.blit(texto_pontos, (50, 20))

        font_marca_dagua = pg.font.SysFont("Arial black", 20) 
        texto_marca_dagua = font_marca_dagua.render("@Igormaaciel", True, (0, 0, 0)) 
        largura_texto = texto_marca_dagua.get_width()  

        screen.blit(texto_marca_dagua, (x - largura_texto - 10, y - 30))  


        if exibir_texto:
            tempo_atual = pg.time.get_ticks()
            if tempo_atual - tempo_inicial < 9500: 
                font_bem_vindo = pg.font.SysFont("Comic Sans MS", 45, bold=True)
                texto_bem_vindo = font_bem_vindo.render("Bem vindo a minha versão da pré-história.", True, (0, 0, 50))
                screen.blit(texto_bem_vindo, (x // 2 - texto_bem_vindo.get_width() // 2, 140)) 
            else:
                exibir_texto = False 

        if exibir_texto:
            tempo_atual = pg.time.get_ticks()
            if tempo_atual - tempo_inicial < 9500:  
                font_bem_vindo = pg.font.SysFont("Comic Sans MS", 45, bold=True)
                texto_bem_vindo = font_bem_vindo.render("Divirta-se!", True, (20, 100, 0))
                screen.blit(texto_bem_vindo, (x // 2 - texto_bem_vindo.get_width() // 2, 210)) 
            else:
                exibir_texto = False         

    else:

        font = pg.font.SysFont("Arial black", 40)
        texto_fim = font.render(f"Pontos: {pontos}", True, (255, 0, 0))
        screen.blit(texto_fim, (x // 2 - texto_fim.get_width() // 2, y // 3))


        botao_reiniciar = pg.Rect(x // 2 - 100, y // 2 + 50, 200, 50)
        pg.draw.rect(screen, (0, 255, 0), botao_reiniciar)
        texto_botao = font.render("Reiniciar", True, (0, 0, 0))
        screen.blit(texto_botao, (x // 2 - texto_botao.get_width() // 2, y // 2 + 60))

    pg.display.update()
    clock.tick(30)

pg.quit()
