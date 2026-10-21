# Umbral de percolación en una mezcla de cemento y material conductor
 
Simulación 3D en Python de cómo partículas conductoras se mueven, se agrupan en clústeres y forman una red que conecte dos caras opuestas de un material. Se estima cómo cambia el umbral de percolación con el tamaño del sistema.
 
> Proyecto individual de curso universitario (Universidad Nacional Mayor de San Marcos, julio de 2024).
![Evolución de los clústeres en OVITO](figures/iteraciones.gif)
<!-- Sustituye por un GIF o una imagen de las iteraciones exportadas desde OVITO -->
 
## Motivación
 
El cemento conductor se usa, por ejemplo, para calentar superficies o detectar incendios. Se fabrica mezclando cemento con materiales conductores; interesa usar la mínima cantidad posible para no degradar las propiedades mecánicas. Esa cantidad mínima es el **umbral de percolación**. Los experimentos reportan valores de alrededor de 3–4 % en volumen para mezclas cemento–carbón (Chanut et al., PNAS 2023).
 
## Modelo
 
1. Se llena una matriz cúbica `n×n×n` con partículas conductoras (1) y material aislante (0) según una concentración dada.
2. En cada iteración:
   - `scipy.ndimage.label` identifica los clústeres (partículas adyacentes).
   - Cada clúster se desplaza como un bloque rígido, con un paso aleatorio de −1, 0 o +1 en cada eje. Las partículas que saldrían de la matriz permanecen en su sitio.
   - Se reconstruye la matriz y se guarda un `.xyz` para visualizarlo en OVITO.
3. Al final se comprueba si hay un camino de partículas adyacentes entre dos caras opuestas (búsqueda en profundidad).
4. Para evitar el sesgo de las paredes (los clústeres se pegaban a un lado y dejaban la otra cara sin contacto), se simula una matriz de lado `n+8` y la conectividad se verifica solo en la región central de lado `n`.
## Metodología para estimar el umbral
 
- Se parte de una concentración alta y se reduce de 1 % en 1 %.
- Cerca del umbral se repiten al menos 15 simulaciones por concentración; si más de 10 resultan conductoras, se sigue bajando.
- Se repite para `n = 10, 15, …, 50`.
## Resultados
 
| Tamaño `n` | Umbral estimado |
|---|---|
| 10 | ≈ 30 % |
| 50 | ≈ 10 % |
 
| Dimensión (`n`) | Tamaño de matriz (`n × n × n`) | Umbral de percolación |
| :---: | :---: | :---: |
| 10 | 10 × 10 × 10 | 30% |
| 15 | 15 × 15 × 15 | 25% |
| 20 | 20 × 20 × 20 | 19% |
| 25 | 25 × 25 × 25 | 14.5% |
| 30 | 30 × 30 × 30 | 13% |
| 35 | 35 × 35 × 35 | 12.5% |
| 40 | 40 × 40 × 40 | 11% |
| 45 | 45 × 45 × 45 | 10.25% |
| 50 | 50 × 50 × 50 | 10% |
 
- Una red conductora se forma en pocas iteraciones (entre 4 y 13 según el tamaño).
- El umbral **disminuye al aumentar el tamaño del sistema**; la tendencia parece de tipo exponencial decreciente, pero no se hizo un ajuste cuantitativo.
- La tendencia es cualitativamente consistente con el rango experimental de 3–4 %, pero con `n ≤ 50` los valores simulados siguen siendo claramente mayores. No se puede afirmar concordancia cuantitativa.
## Limitaciones
 
- Modelo sin agua, hidrofobia, ruptura de clústeres ni interacción química.
- Los clústeres se mueven como bloques rígidos y no se impide que se solapen, así que el número de partículas puede no conservarse.
- Solo se probaron tamaños hasta `n = 50` (con `n = 100` no hubo resultado en 1,5 h por la búsqueda recursiva).
- Pocas repeticiones por punto y sin barras de error.
- La dependencia del umbral con `n` no se ha ajustado ni extrapolado a `n → ∞`.
## Trabajo futuro
 
- Ajustar el umbral con una forma de escalamiento de tamaño finito y extrapolar a `n → ∞` con incertidumbre.
- Graficar la probabilidad de percolación frente a la concentración para cada `n`.
- Sustituir la búsqueda recursiva por `scipy.ndimage.label` y comprobar si un mismo clúster toca ambas caras, para llegar a tamaños mayores.
- Conservar el número de partículas y comparar con el umbral estático de percolación de sitios en red cúbica (≈ 31 %).
## Uso
 
```bash
pip install numpy scipy
python percolacion.py      # genera output_0.xyz ... output_9.xyz y escribe si el material es conductor
```
 
Abre los `.xyz` en [OVITO](https://www.ovito.org/) para ver la evolución.
 
## Estructura
 
```
percolacion.py              # simulación
Umbral_de_percolacion.pdf   # informe completo
figures/                    # imágenes y GIF de OVITO
```
 
## Referencias
 
- Chanut et al. (2023). *Carbon–cement supercapacitors as a scalable bulk energy storage solution.* PNAS 120(32).
- Savytskyi et al. (2024). *Carbon materials for electrically conductive concrete.* E3S Web of Conferences 534.
- Obregón G. J. et al. (2019). *Algoritmo para determinar umbral de percolación en compuestos poliméricos con nanopartículas metálicas embebidas.*
## Autor
 
José Antonio Quinto Ciocca — joseantonio.quinto@unmsm.edu.pe
