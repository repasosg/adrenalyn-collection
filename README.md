# 🃏 Adrenalyn XL 2025-26 - Gestor de Colección

Aplicación web interactiva para gestionar tu colección de cromos Adrenalyn XL de LaLiga 2025-26.

## 🚀 Características

- ✅ **Actualización automática**: Actualiza el Excel y la web se actualiza sola
- 📊 **Dashboard visual**: Progreso por categorías con gráficos
- 🔍 **Filtros avanzados**: Por equipo, categoría, estado (tengo/falta/repetidos)
- 📱 **Responsive**: Funciona perfectamente en móvil y desktop
- ⚡ **GitHub Pages**: Hosting gratuito y automático

## 📋 Estructura del proyecto

```
adrenalyn-collection/
├── index.html                          # Aplicación web
├── Checklist_Adrenalyn_XL_2025-26.xlsx # Tu Excel de control
├── process_excel.py                    # Script de conversión
├── data/
│   └── adrenalyn_data.json            # Datos procesados (generado automáticamente)
├── .github/
│   └── workflows/
│       └── update-data.yml            # GitHub Action para actualización automática
└── README.md                          # Este archivo
```

## 🔧 Configuración inicial

### 1. Crear el repositorio en GitHub

1. Ve a GitHub y crea un nuevo repositorio (por ejemplo: `adrenalyn-collection`)
2. **NO** inicialices con README, .gitignore o licencia

### 2. Subir los archivos

```bash
# Clona o descarga este proyecto
cd adrenalyn-collection

# Inicializa git
git init
git add .
git commit -m "🎉 Inicializar colección Adrenalyn XL"

# Conecta con tu repositorio de GitHub
git remote add origin https://github.com/TU-USUARIO/adrenalyn-collection.git
git branch -M main
git push -u origin main
```

### 3. Activar GitHub Pages

1. Ve a tu repositorio en GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `main` → `/ (root)` → Save

¡Tu web estará disponible en: `https://TU-USUARIO.github.io/adrenalyn-collection/`

### 4. Configurar permisos para GitHub Actions

1. Ve a Settings → Actions → General
2. En "Workflow permissions" selecciona: **Read and write permissions**
3. Marca: **Allow GitHub Actions to create and approve pull requests**
4. Save

## 📝 Cómo actualizar tu colección

### Método 1: Desde GitHub (web)

1. Ve a tu repositorio en GitHub
2. Haz clic en `Checklist_Adrenalyn_XL_2025-26.xlsx`
3. Haz clic en el icono del lápiz (Edit)
4. Arrastra tu Excel actualizado
5. Haz clic en "Commit changes"
6. ✨ ¡En menos de 1 minuto tu web se actualiza automáticamente!

### Método 2: Desde tu computadora

```bash
# 1. Actualiza el Excel en tu computadora
# 2. Súbelo a GitHub

git add Checklist_Adrenalyn_XL_2025-26.xlsx
git commit -m "📊 Actualizar colección"
git push

# ✨ La web se actualiza automáticamente
```

## 🤖 Cómo funciona

1. **Editas el Excel** y lo subes a GitHub
2. **GitHub Actions detecta** el cambio automáticamente
3. **Se ejecuta** `process_excel.py` que convierte el Excel a JSON
4. **Se guarda** el JSON en `data/adrenalyn_data.json`
5. **La web carga** los datos del JSON automáticamente
6. **¡Listo!** Tu colección está actualizada

## 🛠️ Desarrollo local

Si quieres probar cambios localmente:

```bash
# 1. Instalar Python y dependencias
pip install pandas openpyxl

# 2. Procesar el Excel
python process_excel.py

# 3. Servir la web localmente
python -m http.server 8000

# 4. Abrir en navegador
# http://localhost:8000
```

## 📊 Contenido de la colección

- **Regulares**: 360 cartas base
- **Estadios**: 20 cartas
- **¡VAMOS!**: 20 cartas
- **Guantes de Oro**: 7 cartas
- **Kryptonita**: 9 cartas
- **Diamantes**: 18 cartas
- **Influencers**: 9 cartas
- **Protas**: 18 cartas
- **Super Cracks**: 26 cartas
- **Cartas Top y Únicas**: 11 cartas

**Total**: 498 cartas

## 🎨 Personalización

### Cambiar colores

Edita las variables CSS en `index.html`:

```css
:root {
  --primary: #ff0050;      /* Color principal */
  --secondary: #00d4ff;    /* Color secundario */
  --accent: #ffd500;       /* Color de acento */
  --success: #00ff88;      /* Color de éxito */
}
```

### Modificar la estructura del Excel

Si cambias la estructura del Excel, actualiza `process_excel.py` en las secciones correspondientes.

## 🐛 Solución de problemas

### La web no se actualiza

1. Verifica que GitHub Actions tenga permisos de escritura
2. Revisa la pestaña "Actions" en GitHub para ver si hay errores
3. Asegúrate de que el Excel tenga la estructura correcta

### Error al procesar el Excel

1. Verifica que las hojas del Excel tengan los nombres correctos
2. Revisa que las columnas estén en el orden correcto
3. Mira los logs en la pestaña "Actions" de GitHub

## 📄 Licencia

Este proyecto es de código abierto. Siéntete libre de modificarlo y adaptarlo a tus necesidades.

## 🙌 Contribuciones

¿Tienes ideas para mejorar? ¡Las contribuciones son bienvenidas!

1. Fork el repositorio
2. Crea una rama: `git checkout -b mi-mejora`
3. Haz commit: `git commit -m "✨ Agregar nueva feature"`
4. Push: `git push origin mi-mejora`
5. Abre un Pull Request

## 📧 Contacto

¿Preguntas? Abre un Issue en GitHub.

---

Hecho con ❤️ para coleccionistas de Adrenalyn XL
