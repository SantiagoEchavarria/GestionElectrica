# Informacion del parcial 2

## Ejecutar el proyecto

1. **Crear el entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   ```
2. **Activar el entorno virtual**
   ```bash
   # Windows (CMD o PowerShell)
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```
3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
## Ejecutar el proyecto  
```bash
python manage.py runserver
```

## Pasos para ejecutar el test del punto 4 

1. **Ejecutar en la terminal**
   ```bash
      locust -f C:\Users\admin\Desktop\GestionElectrica\simulador_energias\tests\locustfile.py --host=http://localhost:8000
   ```
2. **Ingresa a http://localhost:8089 en el navegador**
   ```bash
   http://localhost:8089
   ```
### Los resultados del test tambien estan agregados en GESTIONELECTRICA/TestsPunto4/
### Hay varios test en cada microServicio, no contemplan numero de usuarios solo procesos.
