import sqlite3
import os

def carregar_dados():
    # Conecta ao banco na mesma pasta (ideal para nuvem)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "gbm_platform.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        dados_formatados = {}
        cursor.execute("SELECT paciente_id, subtipo_molecular FROM pacientes")
        pacientes = cursor.fetchall()
        
        for row in pacientes:
            pid = row['paciente_id']
            nome = row['subtipo_molecular']
            # Query unificada
            query = """
                SELECT p.idade, p.sexo, p.kps_initial, p.mgmt_status, p.idh_status,
                e.volume_tumoral_cm3, e.edema_volume_cm3, g.mutacoes_somaticas, 
                g.assinatura_molecular as risco, r.uptake_tumoral, r.radiofarmaco_nome, s.os_meses
                FROM pacientes p
                LEFT JOIN exames_imagem e ON p.paciente_id = e.paciente_id
                LEFT JOIN dados_genomicos g ON p.paciente_id = g.paciente_id
                LEFT JOIN radiofarmacos r ON p.paciente_id = r.paciente_id
                LEFT JOIN sobrevida s ON p.paciente_id = s.paciente_id
                WHERE p.paciente_id = ?
            """
            cursor.execute(query, (pid,))
            full = cursor.fetchone()
            if full:
                dados_formatados[pid] = {
                    "id": pid,
                    "info_pessoal": { "nome": nome, "idade": full['idade'], "genero": full['sexo'], "kps_performance": full['kps_initial'] },
                    "modulo_1_estatistica": { "sobrevida_esperada_meses": full['os_meses'], "grupo_risco": full['risco'] },
                    "modulo_2_radiofarmacos": { "expressao_sstr2": full['uptake_tumoral'], "peso_kg": 70, "indicacao_lutetium": True if full['radiofarmaco_nome'] != "N/A" else False },
                    "modulo_3_teranostica": { "pet_suv_max": 8.5 if full['uptake_tumoral'] == "Alta" else 2.5, "viabilidade_terapia": 90.0 if full['uptake_tumoral'] == "Alta" else 30.0 },
                    "modulo_4_ml_features": { "mri_t1_gd_vol": full['volume_tumoral_cm3'], "mri_t2_flair_vol": full['edema_volume_cm3'], "mgmt_methylation": full['mgmt_status'], "idh_mutation": full['idh_status'] },
                    "modulo_5_genomica": { "mutacoes_detectadas": full['mutacoes_somaticas'].split(", ") if full['mutacoes_somaticas'] else [], "resistencias_conhecidas": [] }
                }
        conn.close()
        return dados_formatados
    except Exception as e:
        return {}
