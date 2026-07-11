# ==========================================
# FUNCIONES DE VALIDACIÓN
# ==========================================

def validar_codigo(codigo, productos):
    if not codigo.strip():
        return False
    if codigo.upper() in [k.upper() for k in productos.keys()]:
        return False
    return True

def validar_string_no_vacio(texto):
    return bool(texto.strip())

def validar_es_importado(entrada):
    return entrada.lower() in ['s', 'n']

def validar_es_cachorro(entrada):
    return entrada.lower() in ['s', 'n']

def validar_precio(precio_str):
    try:
        precio = int(precio_str)
        return precio > 0
    except ValueError:
        return False

def validar_unidades(unidades_str):
    try:
        unidades = int(unidades_str)
        return unidades >= 0
    except ValueError:
        return False


# ==========================================
# FUNCIONES DEL SISTEMA
# ==========================================

def mostrar_menu():
    """Imprime las opciones del menú principal en pantalla."""
    print("========== MENÚ PRINCIPAL ==========")
    print("1. Unidades por categoría")
    print("2. Búsqueda de productos por rango de precio")
    print("3. Actualizar precio de productos")
    print("4. Agregar productos")
    print("5. Eliminar productos")
    print("6. Salir")
    print("=====================================")


def leer_opcion():
    while True:
        try:
            opcion_str = input("Ingrese opción: ")
            opcion = int(opcion_str)
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


def unidades_categoria(categoria, productos, stock):
    total_unidades = 0
    for codigo, info in productos.items():
        if info[1].lower() == categoria.lower():
            total_unidades += stock[codigo][1]
    print(f"El total de unidades disponibles es: {total_unidades}")


def busqueda_precio(p_min, p_max, productos, stock):
    resultados = []
    for codigo, info_stock in stock.items():
        precio = info_stock[0]
        unidades = info_stock[1]
        
        if p_min <= precio <= p_max and unidades > 0:
            nombre_productos =productos[codigo][0]
            resultados.append(f"{nombre_productos}--{codigo}")
    
    if resultados:
        resultados.sort()
        print(f"Las productos encontradas son: {resultados}")
    else:
        print("No hay productos en ese rango de precios.")


def buscar_codigo(codigo, diccionario):
    for k in diccionario.keys():
        if k.upper() == codigo.upper():
            return True
    return False


def obtener_clave_real(codigo, diccionario):
    for k in diccionario.keys():
        if k.upper() == codigo.upper():
            return k
    return codigo


def actualizar_precio(codigo, nuevo_precio, stock):
    if buscar_codigo(codigo, stock):
        clave_real = obtener_clave_real(codigo, stock)
        stock[clave_real][0] = nuevo_precio
        return True
    return False


def agregar_productos(codigo, nombre, categoria, marca, peso, cachorro, es_importado, precio, unidades,productos, stock):
    if buscar_codigo(codigo, productos):
        return False
    
    importado_bool = True if es_importado.lower() == 's' else False
    codigo_up = codigo.upper()
    
    productos[codigo_up] = [nombre, categoria, marca, peso, cachorro, importado_bool]
    stock[codigo_up] = [precio, unidades]
    return True


def eliminar_productos(codigo, productos, stock):
    if buscar_codigo(codigo, productos):
        clave_productos = obtener_clave_real(codigo, productos)
        clave_stock = obtener_clave_real(codigo, stock)
        del productos[clave_productos]
        del stock[clave_stock]
        return True
    return False


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================
def principal():
    productos = {
    'M001': ['Alimento Premium', 'comida', 'DogPlus', 10, True, False],
    'M002': ['Arena Aglomerante', 'higiene', 'CatClean', 8, False, False],
    'M003': ['Snack Dental', 'snack', 'BiteJoy', 1, True, True],
    'M004': ['Shampoo Suave', 'higiene', 'PetCare', 0.5, False, True],
    'M005': ['Correa Nylon', 'accesorio', 'WalkPro', 0.3, True, False],
    'M006': ['Cama Mediana', 'accesorio', 'CozyPet', 2, False, False],
        
    } 


    stock = {
    'M001': [32990, 12],
    'M002': [9990, 0],
    'M003': [5490, 25],
    'M004': [7990, 5],
    'M005': [11990, 7],
    'M006': [24990, 3],
    
    }


    ejecutando = True
    while ejecutando:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            cat = input("Ingrese categoría a consultar: ")
            unidades_categoria(cat,  productos, stock)

        elif opcion == 2:
            while True:
                try:
                    p_min_str = input("Ingrese precio mínimo: ")
                    p_min = int(p_min_str)
                    p_max_str = input("Ingrese precio máximo: ")
                    p_max = int(p_max_str)
                    
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        busqueda_precio(p_min, p_max, productos, stock)
                        break
                    else:
                        print("Debe ingresar valores válidos (mínimo menor o igual al máximo y mayores a cero).")
                except ValueError:
                    print("Debe ingresar valores enteros")

        elif opcion == 3:
            while True:
                cod = input("Ingrese código de la productos: ")
                precio_str = input("Ingrese nuevo precio: ")
                
                if validar_precio(precio_str):
                    nuevo_precio = int(precio_str)
                    if actualizar_precio(cod, nuevo_precio, stock):
                        print("Precio actualizado")
                    else:
                        print("El código no existe")
                else:
                    print("Precio inválido. Debe ser un entero mayor a cero.")
                
                resp = input("¿Desea actualizar otro precio (s/n)?: ").lower()
                if resp != 's':
                    break

        elif opcion == 4:
            cod = input("Ingrese código de la productos: ")
            nom = input("Ingrese nombre: ")
            cat = input("Ingrese categoría: ")
            marca = input("Ingrese marca: ")
            peso = input("Ingrese peso(kg): ")
            imp = input("¿Es importado? (s/n): ")
            cach = input("¿Es para cachorro? (s/n): ")
            pre_str = input("Ingrese precio: ")
            unid_str = input("Ingrese unidades: ")

            if not validar_codigo(cod, productos):
                print("Error: El código está vacío o ya existe en el sistema.")
            elif not validar_string_no_vacio(nom):
                print("Error: El nombre no puede estar vacío.")
            elif not validar_string_no_vacio(cat):
                print("Error: La categoría no puede estar vacía.")
            elif not validar_string_no_vacio(marca):
                print("Error: La marca no puede estar vacía.")
            elif not validar_string_no_vacio(peso):
                print("Error: El peso no puede estar vacío.")
            elif not validar_es_cachorro(cach):
                print("Error: Debe ingresar 's' o 'n' .")
            elif not validar_es_importado(imp):
                print("Error: Debe ingresar 's' o 'n' .")
            elif not validar_precio(pre_str):
                print("Error: El precio debe ser un número entero mayor que cero.")
            elif not validar_unidades(unid_str):
                print("Error: Las unidades deben ser un número entero mayor o igual a cero.")
            else:
                precio_int = int(pre_str)
                unidades_int = int(unid_str)
                #(codigo, nombre, categoria, marca, peso, cachorro, es_importado, precio, unidades,productos, stock)
                if agregar_productos(cod, nom, cat,marca, peso, cach, imp, precio_int, unidades_int, productos, stock):
                    print("productos agregada")
                else:
                    print("El código ya existe")

        elif opcion == 5:
            cod = input("Ingrese código de la productos a eliminar: ")
            if eliminar_productos(cod, productos,stock):
                print("productos eliminada")
            else:
                print("El código no existe")

        elif opcion == 6:
            print("Programa finalizado.")
            ejecutando = False


if __name__ == "__main__":
    principal()