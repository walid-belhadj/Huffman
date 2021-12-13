import json # stocke le chemin vers le fichier source
from heapq import heappop, heappush # gestion de files
from bitstring import BitArray #conversion binaire/bytes/string
import time
import os #pour s'adapter au OS
import filecmp

# on ouvre et on charge le fichier à partir du fichier config.json
config = open('./config.json')
config_json = json.load(config)
# renvoie une liste contenant chaque ligne du fichier en tant qu'élément
# de liste
# utilise le paramètre d'encodage pour ouvrir le fichier et le lire
# dans n'importe quelle langue possible
file = open(config_json["filepath_text"], encoding="utf8").readlines()
# print(file)

def count_frequencies(file) -> dict:

    """
    Cette fonction ouvre un fichier texte en argument puis renvoie le
    fréquences chaque caractère apparaît dans le fichier texte. Les personnages
    sont ensuite triés par ordre en partant de la fréquence la plus basse jusqu'à
    le plus haut. Valeurs triées par ordre croissant.
    """

    dictionary = {}
    #boucle parcourt chaque ligne du fichier texte dans config.json
    for line in file:
    # boucle parcourt chaque caractère du fichier texte dans config.json
        for char in line:
            # vérifier si le caractère a déjà été ajouté au dictionnaire
            if char not in dictionary:
                dictionary[char] = 1
            else:
                # s'il n'est pas ajouté, il procède à l'ajout de ce caractère dans le dictionnaire
                dictionary[char] = dictionary[char] + 1
    # dictionary is returned
    return dictionary


# stocker le dictionnaire des fréquences dans une variable
# appelée "d" pour une utilisation ultérieure
d = count_frequencies(file)
#print(d)


def creation_of_huffmantree(d) -> list:

    """
    Cette fonction obtient le dictionnaire renvoyé par la fonction
    count_frequencies
     et renvoie une liste de listes qui représentent l'arbre de
     Huffman des personnages
     dans le fichier texte. Il est formaté de la manière suivante :
    [[character_frequency,[character,code]]
    Au début, le code sera une chaîne vide mais il aura du contenu plus tard.    """
    # affecte une variable aux listes de listes pour la représentation
    # de l'arbre de Huffman
    # utilise la méthode items() pour retourner un objet de vue
    # L'objet view contient les paires clé-valeur du dictionnaire,
    # sous forme de tuples dans une liste.
    huffman_tree = [[frequency, [char, ""]] for char, frequency in d.items()]
    # on utilise la boucle while pour créer un arbre huffman
    # tant que la longueur de la liste de l'arbre de Huffman est supérieure à 1
    while len(huffman_tree) > 1:
        # on utilise heappop pour supprimer et renvoyer le plus petit élément qui reste à l'index 0 de la branche droite
        right = heappop(huffman_tree)
        # print("right = ", right)
        # on use heappop pour supprimer et renvoyer le plus petit élément qui reste à l'index 0 de la branche gauche
        left = heappop(huffman_tree)
        # print("left= ", left)

        # boucle à travers la branche droite de l'arbre
        for pair in right[1:]:
            # ajoute zéro à toute la branche droite
            pair[1] = '0' + pair[1]
        # print("right add zero = ", right)

        # boucle dans la branche gauche de l'arbre
        for pair in left[1:]:
            # ajoute un à tout le nœud de gauche
            pair[1] = '1' + pair[1]
        # print("left add one = ", left)
        # print(" ")
        # utilise heappush pour ajouter un élément/des valeurs dans l'arbre huffman
        heappush(huffman_tree, [right[0] + left[0]] + right[1:] + left[1:])
        #renvoie une liste avec l'arbre terminé
        huffman_list = right[1:] + left[1:]
    return huffman_list
#print(creation_of_huffmantree(d))


def encoded_texts(huffman_list: list, new_list: list) -> str:

    """
    Cette fonction obtient la liste renvoyée par la fonction
    creation_of_huffmantree
    et une nouvelle liste comme paramètre aussi. Cette fonction permet
    d'obtenir le code
    texte, il remplace les caractères par le contexte du fichier
    texte d'origine par
    codes attendus et renvoie donc un texte encodé.
    """
    # dictionnaire utilisé pour stocker les valeurs de données dans la clé
    dictionary = {}
    # joint tous les éléments d'un dictionnaire dans une chaîne
    string = "".join(huffman_list)
    # parcourt la liste en boucle
    for i in new_list:
        dictionary[i[0]] = i[1]
    # print(dictionary)
    #utilise la méthode maketrans pour créer une table de mappage
    convert = string.maketrans(dictionary)
    # utilise la méthode translate pour renvoyer une chaîne où certains
    # caractères spécifiés sont remplacés
    # les caractères sont remplacés par les caractères décrits ci-dessus
    # à l'aide de la table de mappage
    encoded_text = string.translate(convert)
    # print(encoded_text)
    return dictionary, encoded_text

def padding_text(encoded_text: str):

    """
    Cette fonction obtient la chaîne encoded_text de la fonction
    encoded_text ci-dessus et renvoie la version complétée du texte encodé.
    Ajoute des caractères au format texte codé tel qu'il doit être affiché.
    ajoute des bits à la chaîne encodée donc la longueur
    est un multiple de 8 et peut donc être encodé efficacement.
    """
    # on obtient le remplissage supplémentaire du texte d'encodage
    padded_text = 8 - (len(encoded_text) % 8)
    # print(padded_text)
    # parcourt le texte rembourré
    for i in range(padded_text):
        encoded_text += "0"
    # fusionne les détails du remplissage supplémentaire dans des chaînes de bits avec du texte codé
    # cela aide à le raccourcir plus tard
    # utilise la méthode format pour formater les valeurs spécifiées et les insérer dans la chaîne
    padded_data = "{0:08b}".format(padded_text)
    # joint le texte rembourré et le texte encodé pour obtenir la version finale du texte encodé    encoded_text = padded_data + encoded_text
    return encoded_text

def compression():

    """
    Cette fonction est formatée pour être utilisée lors de la compression
     le fichier texte. Il utilise les valeurs renvoyées dans les
     fonctions pour obtenir un fichier correctement compressé :
     --> fonction count_frequencies
     --> fonction creation_of_huffmantree
     --> fonction encoded_text
     --> fonction padding_text
     Tout ce qui précède
    """

    path = config_json["filepath_text"]
    # la méthode splitext est utilisée pour diviser le nom du chemin en une paire root et ext.
    # ext étant l'extension (du chemin du fichier) et la racine étant tout sauf la partie extension
    filename, file_extension = os.path.splitext(path)
    # commande pour créer le chemin du fichier binaire
    output_path = filename+".bin"

    # ouvre et lit le fichier
    # utilise le paramètre d'encodage pour ouvrir le fichier et le lire dans n'importe quelle langue possible
    with open(path, "r", encoding="utf8") as file, open(output_path, "wb") as output:
        # uses read method that returns the specified number of bytes from the file
        # default is -1 (the whole file)
        text = file.read()
        # uses the rstrip method removes any trailing characters at the end of a string
        text = text.rstrip()
        # dictionary used to store data values in key
        d = {}
        frequency = count_frequencies(text)
        g = creation_of_huffmantree(frequency)

        # loops through each frequency element from dictionary
        for el in g:
            d[el[0]] = el[1]

        # uses maketrans method to create a mapping table
        table = text.maketrans(d)
        # uses translate method to return a string where some specified characters are replaced
        # characters are replaced with characters described above using mapping table
        encoded_text = text.translate(table)
        padded_encoded_text = padding_text(encoded_text)
        # saves bytes to a binary file
        b = BitArray(bin=padded_encoded_text)
        b.tofile(output)

    # returns fiichier compressé
    return output_path



def remove_padding(bit_string):

    """
     Cette fonction est utilisée dans la fonction de décompression pour
     décompresser le fichier texte. Sa fonctionnalité est de supprimer
     le remplissage ajouté à la fonction de remplissage de texte pour
     obtenir une décompression correcte du texte.
     Elle renvoie le texte encodé sans le remplissage.
    """

    padded_data = bit_string[:8]
    extra_padding = int(padded_data, 2)

    bit_string = bit_string[8:]
    encoded_text = bit_string[:-1*extra_padding]

    return encoded_text


def decompress(input_path):

    """
    Cette fonctionnalité de fonctions est de décompresser le déjà compressé
    fichier texte d'avant. Il utilise les valeurs renvoyées dans les
    fonctions pour obtenir un fichier correctement compressé :
    --> fonction creation_of_huffmantree
    --> fonction encoded_text
    --> fonction remove_padding
    Tout ce qui précède
    """

    # la méthode splitext est utilisée pour diviser le nom du chemin en une paire root et ext.
    # ext étant l'extension (du chemin du fichier) et la racine étant tout sauf la partie extension
    filename, file_extension = os.path.splitext(input_path)
    output_path = filename+"_decompressed" + ".txt"

    # ouvre et lit le fichier
    # on utilise le paramètre d'encodage pour ouvrir le fichier et le lire dans n'importe quelle langue possible
    with open(input_path, "rb") as file, open(output_path, "w", encoding="utf8") as output:
        bit_string = ""
        # renvoie le nombre d'octets spécifié du fichier
        # par défaut est -1 ce qui signifie le fichier entier
        byte = file.read(1)
        # on parcourt les octets jusqu'à ce qu'il ne reste plus d'octets à parcourir, donc la longueur sera nulle
        while len(byte) > 0:
            # en utilisant ord pour renvoyer le nombre qui représente le code unicode de chaque caractère spécifié
            byte = ord(byte)
            # l'utilisation de bin renvoie la chaîne binaire de chacun et supprime les zéros non significatifs
            # remplissage du nombre de l'index à la fin avec des 0 à gauche pour faire un octet
            # ajoute ceci à la chaîne
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits
            byte = file.read(1)

        encoded_text = remove_padding(bit_string)
        # print(encoded_text)
        decoded_text = decode_text(encoded_text, encoded_texts(file, creation_of_huffmantree(d))[0])
        # écraser tout contenu existant en texte décodé
        output.write(decoded_text)
    print("Fichier décompressé avec succès ! ")
    return output_path

def decode_text(encoded_text: str, reverse_mapping: dict):

    """
    Cette fonction renvoie le texte décodé du fichier texte.
    Utilise les boucles for et l'instruction if pour obtenir le texte décodé.
    """

    decoded_text = ""
    current_code = ""

    # itère sur les dictionnaires en utilisant des boucles for
    reverse_mapping = dict((y, x) for x, y in reverse_mapping.items())
    # print(reverse_mapping)

    #boucle sur chaque bit du texte compressé encodé
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_mapping:
            char = reverse_mapping[current_code]
            decoded_text += char
            current_code = ""

    #print("Le fichier texte a été décodé, the following displays the decoded text: ", decoded_text)

    return decoded_text

print("\n")
print("Huffman Coding...")
timeofcompress = time.time()
# Compter l'apparition de chaque charactère
with open('frequency.txt', 'w', encoding='utf-8') as f:
    f.write(str(count_frequencies(file)))
#calculer l'entropy
with open('entropy.txt', 'w', encoding='utf-8') as f:
    f.write(str(creation_of_huffmantree(d)))

    #print(count_frequencies(file))
    #print(creation_of_huffmantree(d))
#stock binary text
with open('binary_encoded.txt', 'w', encoding='utf-8') as f:
    f.write(str(encoded_texts(file, creation_of_huffmantree(d))[1]))
#print(encoded_texts(file, creation_of_huffmantree(d))[1])
with open('binary_decoded.txt', 'w', encoding='utf-8') as f:
    f.write(str(padding_text(encoded_texts(file, creation_of_huffmantree(d))[1])))
#print(padding_text(encoded_texts(file, creation_of_huffmantree(d))[1]))
with open('binary_unspaced.txt', 'w', encoding='utf-8') as f:
    f.write(compression())
print("\n")
print("Fichier compressé avec succès ! ")
timeofcompress = time.time()-timeofcompress
print("\n")
print('Compressing Time: ', end='')
print(str(round(timeofcompress * 1000, 3)) + 'ms')
inputsize=os.path.getsize("textfile.txt")
outputsize=os.path.getsize("textfile.bin")
compression_ratio=float(outputsize/inputsize)*100
print("\n")
print("Compression percentage (Compressed size/file size) (%): ",compression_ratio )
#print(compression())
print("\n")
print("Huffman DeCoding...")
timeofdecompress = time.time()
decompress(compression())
#print(decompress(compression()))
print("\n")
print('Deompressing Time: ', end='')
print(str(round(timeofdecompress * 1000, 3)) + 'ms')

print("\n")
#comparaison
print("Phase de comparaison")
with open('textfile.txt', 'r') as file1:
    with open('textfile_decompressed.txt', 'r') as file2:
        same = set(file1).intersection(file2)

check=False
same.discard('\n')
if same != check:

    print("les fichiers sont identiques")
else:
    print("les fichiers ne sont pas identiques")

with open('save_difference.txt', 'w') as file_out:
    for line in same:
        file_out.write(line)



"""timeofcompress = time.time()
with open('file.txt') as f:
    memory = f.read()
print("")
print("Huffman Coding...")
encoder = HuffmanEncoder()
frquency= HuffmanEncoder.return_frequency(memory)
with open('frequency.txt', 'w', encoding='utf-8') as f:
    f.write(str(frquency))
compressedMessage = encoder.encode(memory)
with open('binary_unspaced.txt', 'w', encoding='utf-8') as f:
    f.write(compressedMessage)
#Add spaces between each digit to allow text wrapping
with open('binary_spaced.txt', 'w', encoding='utf-8') as f:
    f.write(" ".join(compressedMessage))
print("")
encoder.viewCodes()
timeofcompress = time.time()-timeofcompress
print('Compressing Time: ', end='')
print(str(round(timeofcompress * 1000, 3)) + 'ms')"""