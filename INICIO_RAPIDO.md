# 🚀 Guía Rápida de Instalación

## Opción 1: Subir a GitHub (Recomendado)

### Paso 1: Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `adrenalyn-collection` (o el que prefieras)
3. Público o Privado (tu elección)
4. **NO** marques: "Add a README file"
5. Click en "Create repository"

### Paso 2: Subir los archivos

**Desde la web de GitHub:**
1. En tu nuevo repositorio, haz clic en "uploading an existing file"
2. Arrastra TODOS los archivos de esta carpeta
3. Commit changes

**Desde línea de comandos:**
```bash
cd adrenalyn-collection-github
git init
git add .
git commit -m "🎉 Inicializar colección"
git remote add origin https://github.com/TU-USUARIO/adrenalyn-collection.git
git branch -M main
git push -u origin main
```

### Paso 3: Activar GitHub Pages
1. En tu repositorio → Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` → `/ (root)` → Save
4. Espera 1-2 minutos

**Tu web estará en:** `https://TU-USUARIO.github.io/adrenalyn-collection/`

### Paso 4: Dar permisos a GitHub Actions
1. Settings → Actions → General
2. "Workflow permissions" → **Read and write permissions**
3. Marca: "Allow GitHub Actions to create and approve pull requests"
4. Save

## Opción 2: Ver localmente

```bash
# 1. Abrir una terminal en esta carpeta

# 2. Iniciar servidor local
python -m http.server 8000

# 3. Abrir en navegador
# http://localhost:8000
```

## 📝 Actualizar tu colección

### Desde GitHub:
1. Ve a tu repositorio
2. Click en `Checklist_Adrenalyn_XL_2025-26.xlsx`
3. Click en ✏️ (editar)
4. Sube tu Excel actualizado
5. Commit changes
6. ✨ ¡Actualización automática en 1 minuto!

### Desde tu PC:
```bash
git add Checklist_Adrenalyn_XL_2025-26.xlsx
git commit -m "📊 Actualizar colección"
git push
```

## ✅ ¡Listo!

Ahora cada vez que actualices el Excel en GitHub, la web se actualizará automáticamente.

## 🆘 ¿Problemas?

### No veo mi web
- Espera 2-3 minutos después de activar GitHub Pages
- Verifica que la URL sea correcta: `https://TU-USUARIO.github.io/NOMBRE-REPO/`

### La web no se actualiza
- Ve a la pestaña "Actions" en GitHub
- Verifica que el workflow se haya ejecutado correctamente
- Revisa los permisos de GitHub Actions

### Error en GitHub Actions
- Asegúrate de haber dado permisos de escritura
- Verifica que el Excel tenga el nombre correcto
- Revisa los logs en la pestaña Actions
