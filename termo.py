# Para as cores funcionarem no terminal do Windows, use o codigo abaixo no cmd como admin
# reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f
# link para o banco de palavras abaixo
# https://github.com/fserb/pt-br

# biblioteca auxiliar
from random import shuffle
import io
from time import time
from math import floor

# nome do banco de palavras
NO_ACCENT_DICT_2 = 'word_processing/result/no_accent_dictionary_2.txt'
COMPLETE_DICT = 'words_dataset/complete_dictionary.txt'
FILE_NAME_3 = 'words_dataset/no_accent_complete_dictionary.txt'

MAX_ROUNDS = 6

# lista com as palavras
playable_words = []
words = []
words_display = []

# list com todas as letras
alphabet = [ 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 
            'Z', 'X', 'C', 'V', 'B', 'N' , 'M']

# abrindo o banco de palavras, para popular a lista

for word in open( NO_ACCENT_DICT_2 ):
    playable_words.append( word.replace( '\n', '' ) )

for word in io.open( COMPLETE_DICT, mode = 'r', encoding = 'utf-8' ):
    word = word.strip()
    words_display.append( word )

for word in open( FILE_NAME_3 ):
    words.append( word.replace( '\n', '' ) )

def chooseWord( list_of_words:list = words ) -> str:
    '''Sorteia a palavra do jogo'''
    aux_list = [] + list_of_words
    shuffle( aux_list ) # embaralha a lista de palavras
    return aux_list[0]

def displayAttempts(attempts:list = [], round:int = 6) -> None:
    '''Imprime as tentativas no terminal, colorindo as letras caso necessario'''
    for i in range( len( attempts ) ):
        if ( i%2 == 0 ): print( f'\u001b[36m{i + 1}:', end = '\u001b[37m ' )
        else: print( f'\u001b[31m{i + 1}:', end = '\u001b[37m ' )
        for j in range( len( attempts[i] ) ):
            l_aux = attempts[i][j]
            aux_word = ''
            for k in attempts[i]:
                aux_word += k[0]

            index = words.index( aux_word )
            # print( aux_word, index, words_display[index] )
            l = words_display[index][j]
            if ( len( l_aux ) > 1 ): l += l_aux[1]
            if ( len( l ) > 1 ):
                # chama a funcao para alterar a cor da letra l
                l = colorLetter( l[0], l[1] )
            print( f'{l}', end = '\u001b[37m ' )
        print() # apenas uma quebra de linha
    if ( round < 6 ): print( f'{round+1}: _ _ _ _ _')

def colorLetter( l:str, token:str ) -> str:
    '''Colore a letra l de acordo com o token'''
    pallete = { 'g': '\u001b[32m',
                'y': '\u001b[33m',
                'w': '\u001b[37m'} # dicionario com os codigos de cores no terminal
    new_l = pallete[token] + l[0] + pallete['w']
    return new_l

def colorLetterBG( l:str, token:str ) -> str:
    '''Colore a letra l de acordo com o token'''
    pallete = { 'g': '\u001b[42m',
                'y': '\u001b[43m',
                'w': '\u001b[40m'} # dicionario com os codigos de cores no terminal
    new_l = pallete[token] + l[0] + pallete['w']
    return new_l

def checkRepetitions( position_colors:list, victory_word:str, repeated_letters:list ) -> tuple:
    '''Checa se a palavra tem letras repetidas,
    para acertar a quantidade de tokens "g" e "y"'''
    for i in range( len( position_colors ) ):
        if ( repetitionAnalize( victory_word, position_colors, repeated_letters, i ) ):
            if ( len( position_colors[i] ) > 1 ):
                if ( position_colors[i][1] == 'y' ):
                    repeated_letters.remove( position_colors[i][0] )
                    position_colors[i] = position_colors[i][0]
    return repeated_letters, position_colors

def analyzeLetterPosition( guess_letter:str, victory_letter:str, victory_word:str, repeated_letters:list ) -> str:
    '''Atrela tokens nas letras que seguirem os padroes abaixo
    "g" se a letra pertencer a palavra e estiver na posicao certa
    "y" se a letra pertencer a palavra, mas estiver na posicao errada'''
    if ( guess_letter == victory_letter ): return guess_letter + 'g' 
    else:
        guess_letter_occurences = victory_word.count( guess_letter )
        if ( repeated_letters.count( guess_letter ) < guess_letter_occurences ): return guess_letter + 'y'
        else: return guess_letter
    
def analyzeWord( user_guess:str, victory_word:str ) -> list:
    '''Analisa quantas letras a palavra teste tem em comum com a palavra real
    e chama outra funcao para atrelar um token nas letras que estiverem certas'''
    position_colors = [] # lista com as letras e seus respectivos tokens
    repeated_letters = [] # lista de letras repetidas que pertencem a palavra real
    for i in range( len( user_guess ) ):
        if ( user_guess[i] in victory_word ): 
            marked_letter = analyzeLetterPosition(user_guess[i], victory_word[i], victory_word, repeated_letters)
            repeated_letters.append( user_guess[i] )
        else: marked_letter = user_guess[i]
        position_colors.append(marked_letter)
    repeated_letters, position_colors = checkRepetitions(position_colors, victory_word, repeated_letters)
    return position_colors

def repetitionAnalize( real_word:str, position_colors:list, repeated_letters:list, pos:int ) -> bool:
    '''Analisa se alguma letra foi contada mais do que devia'''
    return ( real_word.count( position_colors[pos][0] ) < repeated_letters.count( position_colors[pos][0] ) 
            and ( position_colors.count( position_colors[pos] ) == repeated_letters.count( position_colors[pos][0] )
            or position_colors.count( position_colors[pos][0] + 'y' ) + 
            position_colors.count( position_colors[pos][0] + 'g' ) == repeated_letters.count( position_colors[pos][0] ) ) )

def finalMessage( guess:list , chosen_word:str, w_display:str , round:int, start_time:float ) -> None:
    '''Imprime a mensagem final do jogo'''
    elapsed_time = stopWatch( start_time, time() )
    formatted_time = formatTime( elapsed_time )
    if ( formatted_time[0] == '0' ): print( f'\n\u001b[32mParabéns, você acertou em {round} tentativas no período de {formatted_time} segundos!\u001b[37m')
    elif ( guess == chosen_word ): print( f'\n\u001b[32mParabéns, você acertou em {round} tentativas no período de {formatted_time} minutos!\u001b[37m')
    else: print( f'\n\u001b[31mA palavra era {w_display}, mais sorte da próxima vez!\u001b[37m')

def reduceAlphabet( letters:list, used_letters:list ) -> list:
    '''Retira da lista de letras possiveis
    as letras testadas que nao fazem parte da palavra'''
    for l in used_letters:
        if ( len( l ) > 1 ): 
            letters[alphabet.index( l[0] )] = colorLetter( l[0], l[1] )
        if ( l in letters ): letters[letters.index( l )] = ' '
    return letters

def printAlphabet( letters:list ) -> None:
    '''Imprime o teclado de letras possiveis'''
    print( f'+---------------------+\n| ', end = '' )
    for i in range( len( letters ) ):
        print( f'{letters[i]}', end = ' ' )
        if ( i == 9 ): print( '|\n| ', end = ' ')
        if ( i == 18 ): print( ' |\n|  ', end = ' ')
    print( f'    |\n+---------------------+' )

def stopWatch( ti:float, tf:float ) -> float:
    '''Calcula o tempo total de uma partida'''
    return round( ( tf - ti )/60, 1 )

def formatTime( t:float ) -> str:
    '''Coloca o tempo no formato minutos:segundos'''
    minutes = floor( t )
    frac = t - minutes
    seconds = round( frac * 60 )
    if ( seconds < 10 ): return str( minutes ) + ':0' + str( seconds )
    return str( minutes ) + ':' + str( seconds )

def getDisplayableFormat( chosen_word:str ) -> str:
    '''Pega a palavra escolhida pelo jogo e encontra a analoga 
    na lista de palavras com acentos'''
    index_word = words.index( chosen_word )
    return words_display[index_word]

def getPlayerGuess( round:int ) -> str :
    '''Recebe o palpite do jogador'''
    guess = input( f'\nTentativa {round}: ').upper()
    while ( guess not in words ): 
        print( f'\n\u001b[31m---------------------------------------' +
                '\n-- Palavra inválida, tente outra vez --' +
                '\n---------------------------------------\u001b[37m\n' )
        guess = input( f'Tentativa {round}: ').upper()
    return guess

def processRoundsGuess( chosen_word:str ) -> tuple:
    '''Processa cada rodada do jogo'''
    attempts = []
    possible_letters = [] + alphabet
    for round in range( 1, MAX_ROUNDS+1 ):
        printAlphabet( possible_letters )
        guess = getPlayerGuess(round)
        if ( round == 1 ): start = time()
        result = analyzeWord( guess, chosen_word )
        possible_letters = reduceAlphabet( possible_letters, result )
        attempts.append( result )
        if ( guess == chosen_word ): 
            displayAttempts( attempts )
            break
        displayAttempts( attempts, round )
    return round, start, guess

def beginGame():
    '''Da inicio ao jogo'''
    chosen_word = chooseWord( playable_words )
    chosen_word_display = getDisplayableFormat( chosen_word )
    final_round, start, guess = processRoundsGuess( chosen_word )
    finalMessage( guess, chosen_word ,chosen_word_display, final_round, start )

def main():
    beginGame()
    play_again = input( "Quer jogar de novo? ( S/N ): ").upper()
    while play_again != 'N':
        beginGame()
        play_again = input( "Quer jogar de novo? ( S/N ): ").upper()

main()