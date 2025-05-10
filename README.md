# Ejecutar el proyecto

## Pasos básicos después de clonar el repositorio

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
4. **Si no existe `requirements.txt`, puedes generarlo con**
    ```bash
    pip freeze > requirements.txt
    ```
5. **Verificar instalación**
   ```bash
   python -m django --version
   ```
   
## Ejecutar el proyecto  
```bash
python manage.py runserver
```