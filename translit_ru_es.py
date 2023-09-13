# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 21:59:19 2023

TRANSLITERACIÓN RUSO -> CASTELLANO

Sigue las normas establecidas por la Sección de Traducción al Español de la 
Oficina de las Naciones Unidas en Ginebra.

https://ls-sts.unog.ch/section-files/normas-transliteracion-ru-es

@author: Usuario
"""

#%% THE FUNCTION

def translit_ru_es(s, check_all_upper=True):
    
    # DEFINIR TRANSLITERACIÓN BÁSICA
    # 
    # Nota:
    # Hay excepciones dependiendo de la posición dentro de la palabra, así como
    # del carácter que pueda venir anteriormente. Se consideran más abajo.
    # 
    # Nota 2:
    # Depediendo del editor empleado para visualizar el script, puede que ponga
    # en cursiva los strings y algunos carácteres cirílicos se vean diferente a
    # lo esperado. En esos casos en puesto un comentario a la derecha para ver 
    # ese carácter sin la cursiva. Es meramente orientativo, la cursiva no 
    # afecta al resultado.
    # 
    # Nota 3: si toda la palabra rusa está en mayúsculas por defecto se fuerza
    # a que la función devuelva la transliteración todo en mayúsculas. Esto
    # afecta principalmente a las letras que se transliteran en dos letras,
    # p. ej. 'Ж' = 'Zh'. Puede que este no sea el efecto deseado en siglas, 
    # p. ej. VTsIK, por lo que se puede deshabilitar estableciendo
    # check_all_upper=False.
    # 
    # Nota 4: no hay forma de saber la acentuación de las palabras rusa por los
    # carácteres, no se marca. Por tanto no es posible automatizar la 
    # colocación de tildes. Deberá hacerse a posteriori de forma manual, caso
    # por caso, siguiendo las normas del castellano.
    
    basic_translit = {
        'А': 'A',
        'а': 'a',
        'Б': 'B',
        'б': 'b',
        'В': 'V',
        'в': 'v', # в
        'Г': 'G',
        'г': 'g', # г
        'Д': 'D',
        'д': 'd', # д
        'Е': 'E',
        'е': 'e',
        'Ё': 'Yo',
        'ё': 'yo',
        'Ж': 'Zh',
        'ж': 'zh',
        'З': 'Z',
        'з': 'z',
        'И': 'I',
        'и': 'i', # и
        'Й': 'I',
        'й': 'i', # й
        'К': 'K',
        'к': 'k', 
        'Л': 'L',
        'л': 'l',
        'М': 'M',
        'м': 'm',
        'Н': 'N',
        'н': 'n',
        'О': 'O',
        'о': 'o',
        'П': 'P',
        'п': 'p', # п
        'Р': 'R',
        'р': 'r',
        'С': 'S',
        'с': 's',
        'Т': 'T',
        'т': 't', # т
        'У': 'U',
        'у': 'u',
        'Ф': 'F',
        'ф': 'f',
        'Х': 'J',
        'х': 'j',
        'Ц': 'Ts',
        'ц': 'ts',
        'Ч': 'Ch',
        'ч': 'ch',
        'Ш': 'Sh',
        'ш': 'sh',
        'Щ': 'Sch',
        'щ': 'sch',
        'ъ': '', # se omite
        'Ы': 'Y', # * 
        'ы': 'y',
        'ь': '', # se omite
        'Э': 'E',
        'э': 'e',
        'Ю': 'Yu',
        'ю': 'yu',
        'Я': 'Ya',
        'я': 'ya',
        ' ': ' ', # espacio
        '.': '.', # signos de puntuacion para permitir translit. de frases
        ',': ',',
        '?': '?',
        '!': '!',
        ':': ':',
        ';': ';'
        }
    
    upper_list = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К',
                  'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц',
                  'Ч', 'Ш', 'Щ', 'ъ', 'Ы', 'ь', 'Э', 'Ю', 'Я']
    
    # * "There are no native Russian words that begin with ⟨ы⟩ (except for the 
    # specific verb ыкать: "to say the ⟨ы⟩-sound"), but there are many proper 
    # and common nouns of non-Russian origin (including some geographical names
    # in Russia) that begin with it." -> en.wikipedia.org/wiki/Yery
    
    
    out = ""
    for i, v in enumerate(s):
        
        # Check if s is a string
        if not s.__class__==str:
            raise ValueError('Input needs to be a string.')
        
        # Realizar transliteración básica:
        bt = basic_translit[v]
        
        # Considerar excepciones:
        
        # INCLUYE CONDICIONES PARA ASEGURAR QUE s[i+1], s[i-1] no se salgan de 
        # la palabra:
        # - Para s[i+1] tiene que darse que i<(len(s)-1) [i empieza de 0, len() 
        #   cuenta desde 1]
        # - Para s[i-1] tiene que darse que i>0
        
        # Гг -> gu — delante de "e" y "и":
        if (v=='Г') & (i<(len(s)-1)):
            if s[i+1] in ['е', 'и']:
                bt = 'Gu'
        if (v=='г') & (i<(len(s)-1)):
            if s[i+1] in ['е', 'и']:
                bt = 'gu'
                
        # Ее -> ye — inicial o tras vocal, "ъ" o "ь":
        if (v=='Е') & (i==0):
            bt = 'Ye'
        if (v=='Е') & (i>0):
            if s[i-1] in ['А', 'Я', 'Э', 'Е', 'Ы', 'И', 'О', 'Ё', 'У', 'Ю', 'ъ', 'ь']:
                bt = 'Ye'
        if (v=='е') & (i==0):
            bt = 'ye'
        if (v=='е') & (i>0):
            if s[i-1] in  ['а', 'я', 'э', 'е', 'ы', 'и', 'о', 'ё', 'у', 'ю', 'ъ', 'ь']:
                bt = 'ye'        
        
        # Ёё -> o — tras "ж", "ч", "ш" o "щ":
        if (v=='Ё') & (i>0):
            if s[i-1] in ['Ж', 'Ч', 'Ш', 'Щ']:
                bt = 'O'
        if (v=='ё') & (i>0):
            if s[i-1] in ['ж', 'ч', 'ш', 'щ']:
                bt = 'o'
                
        # Йй -> (se omite tras "y" (ы) u otra "i") | y – tras "a", "e", "o", "у" al final de palabra (ESTO DEBE REFERIRSE AL CIRILICO (y=u), SI NO NO TENDRÍA SENTIDO "y" después de "y")
        if (v=='Й') & (i>0):
            if out[-1] in ['Y', 'y', 'I', 'i']:
                bt = ''
            elif ((i==(len(s)-1)) & (s[i-1] in ['А', 'а', 'Е', 'е', 'О', 'о', 'У', 'у'])): 
                bt = 'Y'
        if (v=='й') & (i>0):
            if out[-1] in ['Y', 'y', 'I', 'i']:
                bt = ''
            elif ((i==(len(s)-1)) & (s[i-1] in ['а', 'е', 'о', 'у'])):
                bt = 'y'
            
        # Яя -> a – tras “и” al final de palabra:
        if (v=='Я') & (i==(len(s)-1)) & (s[i-1]=='И'):
            bt='A'
        if (v=='я') & (i==(len(s)-1)) & (s[i-1]=='и'):
            bt='a'
        
        # Unir con anterior:     
        out = out + bt
    
    # Chequear si toda la palabra en ruso son mayúsculas para hacer lo propio
    # con la transliteración:
    if check_all_upper:
        # primero quitar signos de puntuación antes de chequear mayus:
        s2 = s
        chars = " .,?!:;"
        for c in chars:
            s2 = s2.replace(c, '')
        # comprobar mayúsculas:
        if all(x in upper_list for x in s2): out = out.upper()
    
    # Devolver resultado final:
    return(out)

#%% THE TESTS

# Comprobar que se transliteran correctamente todos los ejemplos proporcionados
# por la Sección de Traducción al Español de la Oficina de las Naciones Unidas 
# en Ginebra:

# Palabras en ruso:
test_words = ['Амур', 'Белгород', 'Воронеж', 'Гродно', 'Адыгея', 'Дагестан',
              'Кемерово', 'Ейск', 'Пугачёв', 'Приозёрск', 'Житомир',
              'Кызылорда', 'Иваново', 'Райчихинск', 'Нижний Новгород',
              'Алтай', 'Калмыкия', 'Липецк', 'Мурманск', 'Новгород', 'Орёл',
              'Псков', 'Ростов', 'Саратов', 'Томск', 'Удмуртия', 'Ефремов',
              'Кохма', 'Крестцы', 'Чувашия', 'Ош', 'Верещагино', 'Подъячев',
              'Атырау', 'Алатырь', 'Энгельс', 'Вилюйск', 'Ярославль', 
              'Ингушетия']

# Transliteración que deben tener:
target_translit = ['Amur', 'Belgorod', 'Voronezh', 'Grodno', 'Adygueya',
                   'Daguestan', 'Kemerovo', 'Yeisk', 'Pugachov', 'Priozyorsk',
                   'Zhitomir', 'Kyzylorda', 'Ivanovo', 'Raichijinsk', 
                   'Nizhni Novgorod', 'Altay', 'Kalmykia', 'Lipetsk', 
                   'Murmansk', 'Novgorod', 'Oryol', 'Pskov', 'Rostov',
                   'Saratov', 'Tomsk', 'Udmurtia', 'Yefremov', 'Kojma', 
                   'Kresttsy', 'Chuvashia', 'Osh', 'Vereschaguino',
                   'Podyachev', 'Atyrau', 'Alatyr', 'Enguels', 'Vilyuisk',
                   'Yaroslavl', 'Ingushetia']

# Aplicar función:
test_results = [translit_ru_es(tw) for tw in test_words] 

# Comprobar resultados:
for i, v in enumerate(test_results):
    tr = test_results[i]==target_translit[i]
    print(test_words[i] + " -> " + str(tr).upper() + " (" + target_translit[i] + " vs " + test_results[i] + ")")
if test_results==target_translit:
    print("\n¡Bien! ¡Transliteraciones realizadas correctamente!\n")
else:
    print("\nHay transliteraciones con errores...\n ")

# Otros ejemplos:
# test_text = u"Всероссийский Центральный Исполнительный Комитет"
# translit_ru_es(test_text, check_all_upper=False)
