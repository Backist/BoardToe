
# Conceptos y nuevas ideas.

```
En este archivo markdown colocaremos aquellas ideas que nos parezcan interesantes y
que puedan ayudar al juego a darle dinamismo, etc
```

## [+] Apartado 1: **TUI y Parte Grafica** 
- **Conceptios/ideas relacionadas con la parte grafica (TUI) y
las salidas de texto por terminal (textos de todo tipo, estilo de los textos, etc)**

### Concepto 1: Emojis interactivos
- Implementacion de **emojis interactivos** de cara al printeo de texto de cualquier 
contexto, pudiendole dar énfasi con los emojis y dinamismo.

- Lo que se busca es que se detecten facilmente las salidas de mensajes porque 
todas las salidas llevan un 'logger' con dos corchetes donde el primero
describe quien lo manda (constructor, funcion, etc) y el segundo el problema.

- El caso es que cada vez que salga algun mensaje en pantalla, de error, de victoriaz
de informacion, de narrador, ....
    - Algunos ejemplos:

        **Para errores:**

        1. **[⚙️][⛔️]** --> Los parametros deben de ser numeros!!
        2. **[⚠️][🔒]** --> Ops! Parece que esta posicion ya esta ocupada !!
        3. **[📢][❕]** --> Ya has colocado una ficha en esta posicion !!

        **Para informacion general**

        1. **[🔊][🌐]** Elige un idioma:

        **Para mensajes de victoria**

        1. **[🏆][🥇]** Player 1 ha ganado !!
        1. **[🦾][🥇]** La CPU ha ganado !
        2. **[🔊][🤝]** La partida ha quedado en un empate !!

        **Otros mensajes**

        1. **[🔊][🔍]** Obteniendo datos de la partida . . .
        2. **[🤖][🔍]** Buscando la mejor posicion . . .


### Concepto 2: Menu interactivo colorido y encasillado
- Hacer un menu limpio y con colores, y que este encasilado con las tres modalidades
del juego posibles.
- . . .


## [+] Apartado 2: **Core**
- Apartado solo dedicado para mejorar la parte logica del juego


## [+] Apartado 3: **Constructor**
- Solo se valoran aspectos a mejorar del constructor


### Concepto 3: Futuras implementaciones para el juego.
- Poder jugar el juego multijugador creando un servidor host en un puerto con ``socket``, pudiendo jugar desde dos maquinas distintas.
- Mejor formateo y parseo del juego en general. Implementar un sistema automático de paddings e interespaciados.
- . . .



