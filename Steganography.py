from PIL import Image
from collections import deque
import base64

def cipher(txt , n):
    lista= list(txt)
    for i in range(len(lista)):
        k= ord(lista[i])
        k=k+n
        if k>126 :  ##Limite tabla ASCII
            k=(k%126)+31  ##Los primeros 32 son funciones de caracteres de control
            
        lista[i]= chr(k)
        txt= ''.join(lista)
    return txt

def decipher(txt , n):
    lista= list(txt)
    for i in range(len(lista)):
        k= ord(lista[i])
        k=k-n
        if k<32:
            k=k+95      ##126-31=95
        lista[i]= chr(k)
        txt= ''.join(lista)
    return txt

def getKey(txt):
    lista= list(txt)
    sum=0
    for i in range(len(lista)):
        k= ord(lista[i])
        sum=k+sum
    n=sum%126
    if n==0:
        n=25
    return n

def binary_to_string(message):
    b64 = message.encode("utf8")
    bytes_ = base64.encodebytes(b64)
    bytestring = "".join(["{:08b}".format(x) for x in bytes_])
    bytestring += EOM
    return bytestring

def string_to_binary(bytestring):
    bytestring = bytestring.split(EOM)[0]
    binaryTemp=int(bytestring, 2)
    binary=binaryTemp.to_bytes(len(bytestring) // 8, byteorder='big')
    binary = base64.decodebytes(binary).decode("utf8")
    return binary



def printSample(image, n):
    for i in range (1):  ##width
        for j in range(n): ##height
            pixelx= image.getpixel((i,j))
            print (pixelx)
        
    print('--------------')
    # Altura y ancho de la imagen



    #Recorrer Imagen por pixel y volver los LSB de cada color en 0
def setImage(image1):
    for i in range (width):  ##width
        for j in range(height): ##height
        
            pixel = image1.getpixel((i,j))
            R = pixel[0]
            G = pixel[1]
            B = pixel[2]
           
            if (R%2!=0):
                image1.putpixel((i,j), (R-1,G,B))
                R=R-1
                
            if (G%2!=0):
                image1.putpixel((i,j), (R,G-1,B))
                G=G-1
                
            if (B%2!=0):
                image1.putpixel((i,j), (R,G,B-1))
                B=B-1
    return image1
       
#Mostrar valor pixeles    
'''   
for i in range (3):  ##width
    for j in range(3): ##height
        pixelx= image1.getpixel((i,j))
        print (pixelx)     
'''           
##print('--------------')
##print (text)


## Meter mensaje en la imagen    
def hideText(image1, text):    
    while(text):
        for i in range(width):
            for j in range (height):
                
                if len(text)==0:
                        break
                    
                pixel = image1.getpixel((i,j))
                R = pixel[0]
                G = pixel[1]
                B = pixel[2]
                
                for k in range(3):
                    
                    if len(text)==0:
                        break
                    elif text[0]=='1':
                        
                        text.pop(0)
                        if k==0:
                            image1.putpixel((i,j), (R+1,G,B))
                            R=R+1
                        if k==1:
                            image1.putpixel((i,j), (R,G+1,B))
                            G=G+1
                        if k==2:
                            image1.putpixel((i,j), (R,G,B+1))
                            B=B+1      
                    else:
                        text.pop(0)
    return image1
                

#Descifrar imagen
def readImage(image1):
    stack=deque()
   # digitos=10000
    for i in range(width):
        for j in range (height):
            #if digitos==0:
                  #  break
            
            pixel = image1.getpixel((i,j))
            
            for k in range (3):
                #if digitos==0:
                    #break
                
                if pixel[k]%2==1:
                    stack.append(1)
                   # digitos-=1
                else:
                    stack.append(0)
                    #digitos-=1
    return stack
   
         

##image1.show()  





#image1= Image.open('2257-paisajes.jpg') 




    #fin del mensaje
EOM= "010101010100011101101100011101010101100100110010011010000110110001001001010001110100111000110001011000110110110101101100011101100110001100110010001110000011110100001010"



loop=True
while loop:
    print("1| Esconder mensaje")
    print("2| Leer imagen")
    print("3| Salir ")
    x=int(input("Que desea hacer? Escriba el numero: "))
    
    if x==1:
        #Imagen a ingresar 
        ImgName=input("Ingrese el nombre de la imagen con la extension: ")
        image1=Image.open(ImgName)
        
        width , height = image1.size
        
        message= input("Ingrese el mensaje que desea esconder: ")
        pwd= input("Ingrese una contrasena: ")
        key= getKey(pwd)
        print("Espere un momento...")
        #Cifrar el mensaje, pasarlo a binario y convertirlo en lista
        message= cipher(message, key)
        binary= binary_to_string(message)
        text=[]
        text[:0]= binary
        
        #Preparar imagen cambiando los LSB por 0
        image1=setImage(image1)
        
        #Esconder texto en la imagen y guardarla
        image1=hideText(image1 , text)
        # Se debe guardar el archivo en .tif para no tener perdida de informacion al guardar la imagen
        image1.save('Encrypted.tif')
        print("La imagen se ha guardado con el nombre: Encrypted.tif")
        
    if x==2:
        ImgName=input("Ingrese el nombre de la imagen con la extension .tif: ")
        image2= Image.open(ImgName)
        width , height = image2.size
        pwd= input("Ingrese la contrasena de la imagen: ")
        key= getKey(pwd)
        print("Espere un momento...")        

        #Extraer texto de la imagen
        stack=readImage(image2)
        txt= ''.join([str(x) for x in stack])
        txt= string_to_binary(txt)
        txt= decipher(txt, key)
        print("El mensaje contenido en la imagen es: ")
        print(txt)
    
    if x==3:
        loop=False
    print('-------------------------------')     

print('-------------------------------')
