#!/usr/bin/env python3
"""
Script para convertir el Excel de Adrenalyn XL a JSON
Se ejecuta automáticamente cuando actualizas el Excel en GitHub
"""

import pandas as pd
import json
import sys
from pathlib import Path

def process_excel(excel_path, output_json_path):
    """Procesa el Excel y genera el JSON con los datos"""
    
    print(f"📖 Leyendo Excel: {excel_path}")
    xl_file = pd.ExcelFile(excel_path)
    
    # Procesar RESUMEN
    print("🔄 Procesando RESUMEN...")
    df_resumen = pd.read_excel(excel_path, sheet_name='RESUMEN', header=1)
    resumen_data = []
    
    for _, row in df_resumen.iterrows():
        if pd.notna(row.iloc[0]) and row.iloc[0] not in ['Categoría']:
            resumen_data.append({
                'categoria': str(row.iloc[0]),
                'total': int(row.iloc[1]) if pd.notna(row.iloc[1]) else 0,
                'tengo': int(row.iloc[2]) if pd.notna(row.iloc[2]) else 0,
                'faltan': int(row.iloc[3]) if pd.notna(row.iloc[3]) else 0,
                'progreso': float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0
            })
    
    # Procesar REGULARES
    print("🔄 Procesando REGULARES...")
    df_reg = pd.read_excel(excel_path, sheet_name='REGULARES', header=None)
    regulares_data = []
    
    for _, row in df_reg.iterrows():
        if pd.notna(row[0]):
            regulares_data.append({
                'numero': int(row[0]),
                'nombre': str(row[1]) if pd.notna(row[1]) else '',
                'equipo': str(row[2]) if pd.notna(row[2]) else '',
                'tengo': row[3] == 'SI',
                'repetidos': int(row[4]) if pd.notna(row[4]) else 0
            })
    
    # Obtener equipos únicos
    equipos = sorted(list(set([c['equipo'] for c in regulares_data if c['equipo']])))
    
    # Procesar cartas especiales
    print("🔄 Procesando cartas especiales...")
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
        ('Cartas Top y Únicas (468–478)', 'Cartas Top y Únicas')
    ]
    
    for hoja_name, categoria_name in hojas_especiales:
        if hoja_name in xl_file.sheet_names:
            df_esp = pd.read_excel(excel_path, sheet_name=hoja_name, header=None)
            cards = []
            
            for _, row in df_esp.iterrows():
                if pd.notna(row[0]):
                    cards.append({
                        'numero': int(row[0]),
                        'nombre': str(row[1]) if pd.notna(row[1]) else '',
                        'equipo': str(row[2]) if pd.notna(row[2]) else '',
                        'tengo': row[3] == 'SI' if len(row) > 3 and pd.notna(row[3]) else False
                    })
            
            especiales[categoria_name] = cards
            print(f"  ✓ {categoria_name}: {len(cards)} cartas")
    
    # Crear estructura completa
    data = {
        'resumen': resumen_data,
        'regulares': regulares_data,
        'especiales': especiales,
        'equipos': equipos,
        'metadata': {
            'ultima_actualizacion': pd.Timestamp.now().isoformat(),
            'total_cartas': len(regulares_data) + sum(len(cards) for cards in especiales.values()),
            'version': '1.0'
        }
    }
    
    # Guardar JSON
    print(f"💾 Guardando JSON: {output_json_path}")
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Mostrar resumen
    print("\n✅ Procesamiento completado!")
    print(f"📊 Total regulares: {len(regulares_data)}")
    print(f"⭐ Categorías especiales: {len(especiales)}")
    print(f"⚽ Equipos: {len(equipos)}")
    print(f"🎯 Total cartas: {data['metadata']['total_cartas']}")
    
    return data

if __name__ == '__main__':
    # Rutas por defecto
    excel_path = Path('Checklist_Adrenalyn_XL_2025-26.xlsx')
    output_json = Path('data/adrenalyn_data.json')
    
    # Crear directorio data si no existe
    output_json.parent.mkdir(exist_ok=True)
    
    # Procesar
    try:
        process_excel(excel_path, output_json)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
