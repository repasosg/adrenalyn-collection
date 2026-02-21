#!/usr/bin/env python3
import pandas as pd
import json
from datetime import datetime
import sys

def process_excel_to_json(excel_path, output_path):
    """
    Procesa el Excel de Adrenalyn XL y genera un JSON
    """
    try:
        # Cargar el archivo Excel
        xls = pd.ExcelFile(excel_path)
        
        # 1. Procesar RESUMEN
        df_resumen = pd.read_excel(excel_path, sheet_name='RESUMEN', header=1)
        resumen = []
        for _, row in df_resumen.iterrows():
            if pd.notna(row.iloc[0]) and str(row.iloc[0]) != 'TOTAL COLECCIÓN':
                resumen.append({
                    'categoria': str(row.iloc[0]),
                    'total': int(row.iloc[1]) if pd.notna(row.iloc[1]) else 0,
                    'tengo': int(row.iloc[2]) if pd.notna(row.iloc[2]) else 0,
                    'faltan': int(row.iloc[3]) if pd.notna(row.iloc[3]) else 0,
                    'progreso': float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0
                })
        
        # 2. Procesar REGULARES (sin header)
        df_regulares = pd.read_excel(excel_path, sheet_name='REGULARES', header=None)
        regulares = []
        for _, row in df_regulares.iterrows():
            if pd.notna(row.iloc[0]):
                regulares.append({
                    'numero': str(row.iloc[0]),
                    'nombre': str(row.iloc[1]) if pd.notna(row.iloc[1]) else '',
                    'equipo': str(row.iloc[2]) if pd.notna(row.iloc[2]) else '',
                    'tengo': str(row.iloc[3]) == 'SI' if pd.notna(row.iloc[3]) else False,
                    'repetidos': int(row.iloc[4]) if pd.notna(row.iloc[4]) else 0
                })
        
        # 3. Procesar REPETIDOS (pestaña específica)
        df_repetidos_sheet = pd.read_excel(excel_path, sheet_name='REPETIDOS', header=None)
        repetidos_list = []
        for _, row in df_repetidos_sheet.iterrows():
            if pd.notna(row.iloc[0]):
                repetidos_list.append({
                    'numero': str(row.iloc[0]),
                    'nombre': str(row.iloc[1]) if pd.notna(row.iloc[1]) else '',
                    'equipo': str(row.iloc[2]) if pd.notna(row.iloc[2]) else '',
                    'copias': int(row.iloc[3]) if pd.notna(row.iloc[3]) else 0
                })
        
        # 4. Obtener lista de equipos únicos (se completa después de procesar especiales)
        equipos_set = set(c['equipo'] for c in regulares if c['equipo'])
        
        # 5. Procesar hojas especiales (incluyendo AMPLIACION y ESPECIALES)
        especiales = {}
        hojas_especiales = [
            ('Estadios', 'Estadios'),
            ('¡VAMOS! (361–380)', 'VAMOS'),
            ('Guantes de Oro (381–387)', 'Guantes de Oro'),
            ('Kryptonita (388–396)', 'Kryptonita'),
            ('Diamantes (397–414)', 'Diamantes'),
            ('Influencers (415–423)', 'Influencers'),
            ('Protas (424–441)', 'Protas'),
            ('Super Cracks (442–467)', 'Super Cracks'),
            ('Cartas Top y Únicas (468–478)', 'Cartas Top y Únicas'),
            ('AMPLIACION', 'Ampliación'),
            ('ESPECIALES', 'Especiales'),
        ]
        
        for hoja_nombre, categoria_nombre in hojas_especiales:
            if hoja_nombre in xls.sheet_names:
                df = pd.read_excel(excel_path, sheet_name=hoja_nombre, header=None)
                cartas = []
                for _, row in df.iterrows():
                    if pd.notna(row.iloc[0]):
                        cartas.append({
                            'numero': str(row.iloc[0]),
                            'nombre': str(row.iloc[1]) if pd.notna(row.iloc[1]) else '',
                            'equipo': str(row.iloc[2]) if pd.notna(row.iloc[2]) else '',
                            'tengo': str(row.iloc[3]) == 'SI' if pd.notna(row.iloc[3]) else False
                        })
                especiales[categoria_nombre] = cartas
                # Añadir equipos únicos de esta categoría
                for c in cartas:
                    if c['equipo']:
                        equipos_set.add(c['equipo'].upper())
                
                # Normalizar equipo a mayúsculas en las cartas para consistencia
                for c in cartas:
                    c['equipo'] = c['equipo'].upper()
                
                # Añadir al resumen si es Ampliación o Especiales (no están en la hoja RESUMEN)
                if categoria_nombre in ['Ampliación', 'Especiales']:
                    total = len(cartas)
                    tengo = sum(1 for c in cartas if c['tengo'])
                    faltan = total - tengo
                    progreso = tengo / total if total > 0 else 0
                    resumen.append({
                        'categoria': categoria_nombre,
                        'total': total,
                        'tengo': tengo,
                        'faltan': faltan,
                        'progreso': progreso
                    })
        
        # Finalizar lista de equipos únicos ordenada
        equipos = sorted(list(equipos_set))
        
        # 6. Calcular TOTAL COLECCIÓN sumando todas las categorías
        total_total = sum(r['total'] for r in resumen)
        total_tengo = sum(r['tengo'] for r in resumen)
        total_faltan = sum(r['faltan'] for r in resumen)
        total_progreso = total_tengo / total_total if total_total > 0 else 0
        resumen.append({
            'categoria': 'TOTAL COLECCIÓN',
            'total': total_total,
            'tengo': total_tengo,
            'faltan': total_faltan,
            'progreso': total_progreso
        })
        
        # 7. Construir el JSON final
        data = {
            'metadata': {
                'ultima_actualizacion': datetime.now().isoformat(),
                'version': '2.0'
            },
            'resumen': resumen,
            'regulares': regulares,
            'repetidos': repetidos_list,
            'especiales': especiales,
            'equipos': equipos
        }
        
        # Guardar JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON generado correctamente: {output_path}")
        print(f"📊 Estadísticas:")
        print(f"   - Categorías en resumen: {len(resumen)}")
        print(f"   - Cartas regulares: {len(regulares)}")
        print(f"   - Cartas repetidas: {len(repetidos_list)}")
        print(f"   - Categorías especiales: {len(especiales)}")
        print(f"   - Equipos: {len(equipos)}")
        for cat, cards in especiales.items():
            tengo = sum(1 for c in cards if c['tengo'])
            print(f"     · {cat}: {len(cards)} cartas ({tengo} tengo)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al procesar el Excel: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    excel_file = "Checklist_Adrenalyn_XL_2025-26.xlsx"
    output_file = "data/adrenalyn_data.json"
    
    import os
    os.makedirs('data', exist_ok=True)
    
    success = process_excel_to_json(excel_file, output_file)
    sys.exit(0 if success else 1)
