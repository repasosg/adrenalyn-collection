import pandas as pd
import json
import os

def process_excel(excel_path='Checklist_Adrenalyn_XL_2025-26.xlsx', output_json='data/adrenalyn_data.json'):
    print(f"🚀 Iniciando procesamiento de: {excel_path}")
    xl = pd.ExcelFile(excel_path)
    
    # 1. Dashboard: Resumen de progreso
    df_resumen = pd.read_excel(xl, 'RESUMEN', header=1)
    resumen = []
    for _, row in df_resumen.iterrows():
        cat = str(row.iloc[0])
        if pd.notna(row.iloc[0]) and "TOTAL" not in cat.upper():
            resumen.append({
                "categoria": cat,
                "total": int(row.iloc[1]) if pd.notna(row.iloc[1]) else 0,
                "tengo": int(row.iloc[2]) if pd.notna(row.iloc[2]) else 0,
                "progreso": round(float(row.iloc[4]) * 100, 1) if pd.notna(row.iloc[4]) else 0
            })

    # 2. Base de Datos de Cartas
    hojas_mapeo = [
        ('REGULARES', 'REGULAR'), ('Estadios', 'ESTADIO'), 
        ('¡VAMOS! (361–380)', '¡VAMOS!'), ('Guantes de Oro (381–387)', 'GUANTES DE ORO'),
        ('Kryptonita (388–396)', 'KRYPTONITA'), ('Diamantes (397–414)', 'DIAMANTE'),
        ('Influencers (415–423)', 'INFLUENCER'), ('Protas (424–441)', 'PROTA'),
        ('Super Cracks (442–467)', 'SUPER CRACK'), ('Cartas Top y Únicas (468–478)', 'TOP/ÚNICA')
    ]

    todas_las_cartas = []
    for nombre_hoja, cat_label in hojas_mapeo:
        if nombre_hoja in xl.sheet_names:
            df = pd.read_excel(xl, nombre_hoja)
            # Buscamos la fila donde empiezan los datos (donde el primer valor es un número)
            df.columns = [f"col_{i}" for i in range(len(df.columns))]
            
            for _, row in df.iterrows():
                try:
                    num_id = str(row.iloc[0])
                    if num_id.isdigit():
                        tengo_check = str(row.iloc[3]).upper()
                        todas_las_cartas.append({
                            "id": int(num_id),
                            "nombre": str(row.iloc[1]).strip(),
                            "equipo": str(row.iloc[2]).strip(),
                            "categoria": cat_label,
                            "tengo": "SI" in tengo_check or "X" in tengo_check,
                            "repetidos": int(row.iloc[4]) if pd.notna(row.iloc[4]) else 0
                        })
                except: continue

    # 3. Exportar JSON
    output_data = {
        "resumen": resumen,
        "cartas": todas_las_cartas,
        "actualizado": pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")
    }
    
    os.makedirs('data', exist_ok=True)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ ¡Éxito! {len(todas_las_cartas)} cartas procesadas.")

if __name__ == "__main__":
    process_excel()