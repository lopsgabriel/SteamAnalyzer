base_url = '/static/images/'



def define_player_type(genres_hours, categories_hours):
    top_genre = max(genres_hours, key=genres_hours.get)
    top_category = max(categories_hours, key=categories_hours.get)
    
    if top_genre == "Action" and top_category == "Pvp" or top_genre == "Action" and top_category == "Multi-player":
        return {
            "title": "Guerreiro Competitivo",
            "img": f'{base_url}GuerreiroCompetitivo.png',
            "description": "Com sede constante por desafio, o Guerreiro Competitivo busca a afirmação pessoal no campo de batalha. Seu território natural são jogos de ação com forte presença de PvP, especialmente shooters e arenas multiplayer. Determinado e resistente à pressão, encara cada partida como uma oportunidade de medir forças, aperfeiçoar sua habilidade e provar seu valor. Prefere confrontos diretos e exige resposta rápida tanto do próprio raciocínio quanto da mecânica de jogo. Para ele, vitórias não são apenas conquistas; são confirmações de uma identidade moldada na superação contínua."
        }
  
    if top_genre == "Action":
        return {
            "title": "Guerreiro Solitário",
            "img": f'{base_url}GuerreiroSolitario.png',
            "description": "O Guerreiro Solitário é impulsionado pelo desejo de escrever sua própria história em mundos que recompensam coragem e persistência. Sem a necessidade de aplausos ou apoio, encara jornadas repletas de desafios onde cada conquista depende apenas da sua decisão e habilidade. Prefere percorrer grandes distâncias, explorar territórios desconhecidos e enfrentar inimigos com a convicção de que seu caminho é único. Em sua jornada, a recompensa não está na glória pública, mas na construção silenciosa de uma trajetória marcada por escolhas, vitórias e cicatrizes pessoais."
          }
    
    if top_genre == "Adventure":
        return {
            "title": "O Explorador",
            "img": f'{base_url}OExplorador.png',
            "description": "Guiado pela curiosidade e pelo desejo de atravessar o desconhecido, o Explorador Instintivo se sente em casa em mundos que estimulam a descoberta e a narrativa envolvente. Para ele, cada jornada é uma trama de segredos, personagens e reviravoltas esperando para serem desvendados. Valoriza a liberdade de explorar no próprio ritmo, absorvendo os pequenos detalhes e as grandes aventuras com igual intensidade. Seu impulso natural é seguir além da próxima montanha, da próxima porta, do próximo mistério, movido não apenas pelo destino final, mas pelo próprio caminho."
          }
    
    if top_genre == "RPG":
        return {
            "title": "Herói de RPG",
            "img": f'{base_url}HeroiDeRPG.png',
            "description": "O Herói de RPG é movido pelo prazer da evolução constante e da construção cuidadosa de sua trajetória. Cada batalha vencida, cada habilidade aprimorada e cada decisão estratégica moldam não apenas o personagem, mas também sua experiência dentro do mundo que habita. Valorizando a progressão lenta e significativa, ele enxerga os desafios como degraus necessários para se tornar algo maior. Seus caminhos são definidos por escolhas táticas e planejamento, e não por sorte ou impulso. Para ele, crescer é uma jornada meticulosa, onde cada ponto investido carrega um peso real na história que está sendo escrita."
          }
    if top_genre == "Simulation":
        return {
            "title": "Mestre Tático",
            "img": f'{base_url}MestreTatico.png',
            "description": "Para o Arquiteto Estratégico, o verdadeiro domínio em um jogo não está na força imediata, mas na construção cuidadosa de vantagem a longo prazo. Ele observa padrões, gerencia recursos, antecipa reações e adapta suas táticas conforme o cenário evolui. Sua mente é voltada para estruturar sistemas complexos, seja comandando exércitos, cidades, economias inteiras ou um tabuleiro. Cada decisão é pensada como parte de um plano maior, onde a paciência e a leitura precisa do ambiente definem o ritmo da vitória. Para ele, vencer é o resultado natural de controlar todas as variáveis que importam."
          }
        
    if top_genre == "Racing":
        return {
            "title": "Piloto de Alta Velocidade",
            "img": f'{base_url}PilotoDeAltaVelocidade.png',
            "description": '"Eu sou a velocidade", diria o Piloto de Alta Velocidade, ele vive para dominar trajetos, não importa o veículo ou terreno. Seu foco está na adaptação instantânea, no domínio da trajetória ideal e na precisão de cada movimento. Para ele, a corrida é mais do que velocidade bruta: é um teste de controle, ritmo e antecipação. Cada partida é uma batalha silenciosa contra o relógio e contra si mesmo, onde erros não são tolerados e a vitória nasce da combinação perfeita entre técnica e ousadia. O verdadeiro prêmio está na fluidez do percurso conquistado através da mente e do instinto.'
          }
        
    if top_genre == "Sports":
        return {
            "title": "O Craque",
            "img": f'{base_url}OCraque.png',
            "description": "O Craque não é só talento, mas também disciplina, competitividade e a busca constante por evolução. Dentro do campo ou quadra, ele treina, refina habilidades e transforma a pressão em combustível para a vitória. Não importa o esporte, o objetivo é sempre dominar a dinâmica do jogo, antecipar movimentos e explorar cada oportunidade. Para ele, o sucesso vem tanto da técnica quanto da mentalidade forte, e cada partida é tratada com a seriedade de uma verdadeira disputa. A vitória não é só esperada, é construída lance a lance"
          }
        
    if top_genre == "Indie":
        return {
            "title": "Explorador Indie",
            "img": f'{base_url}ExploradorIndie.png',
            "description": "O Explorador Indie enxerga nos jogos independentes a oportunidade de viver experiências únicas, livres das fórmulas convencionais. Movido pela curiosidade e pela sensibilidade, busca narrativas acolhedoras, mecânicas inventivas e mundos que convidam à reflexão ou à cooperação. Prefere ambientes que estimulem a criatividade e a conexão emocional, seja explorando pequenas comunidades, superando desafios em dupla ou mergulhando em atmosferas tranquilas. Para ele, a verdadeira jornada não está na competição ou na conquista, mas na descoberta de novas formas de se relacionar com o jogo e com a própria imaginação."
          }
    
    if top_genre == "MMO":
        return {
            "title": "Viajante de Reinos",
            "img": f'{base_url}ViajanteDeReinos.png',
            "description": "O Viajante de Reinos é impulsionado pelo desejo de crescer e deixar sua marca em mundos vastos e vivos. Fascinado por sistemas complexos de evolução, comércio e conquista, ele encara cada jornada como uma construção contínua de identidade e poder. Valoriza a liberdade de explorar terras desconhecidas, criar alianças e enfrentar desafios que exigem tanto força quanto estratégia. Para ele, cada personagem é uma extensão da própria vontade, moldado pela paciência, pela persistência e pelas escolhas feitas ao longo do caminho. Sua verdadeira conquista está em pertencer e dominar realidades inteiras, um passo de cada vez."
          }
      

    return {
        "title": "Jogador Diferenciado",
        "img": f'{base_url}JogadorDiferenciado.png',
        "description": "O Jogador Diferenciado escolhe caminhos pouco comuns, buscando experiências que fogem das fórmulas tradicionais. Para ele, a diversão está em descobrir o novo, o estranho e o inesperado, sem se prender a gêneros ou padrões definidos. Cada escolha reflete a vontade de explorar possibilidades únicas, seja em jogos experimentais, híbridos ou fora do convencional. Sua jornada é guiada pela curiosidade e pela liberdade de não pertencer a um único estilo."
      }
        
        
    

   
