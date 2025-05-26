from datetime import date
from llm.deepseek_client import call_deepseek

def generate_attestation_with_llm(employee):
    prompt = f"""
Tu es un assistant RH chez QuantFactory. Rédige une attestation d’emploi formelle et professionnelle pour l’employé suivant. Utilise un ton administratif et adapte le texte selon le genre du prénom.

Nom : {employee.first_name} {employee.last_name}
Poste : {employee.job_title}
Département : {employee.department}
Type de contrat : {employee.contract_type}
Date d’embauche : {employee.start_date.strftime('%d/%m/%Y')}
Date de rédaction : {date.today().strftime('%d/%m/%Y')}

Commence par “À qui de droit,” et termine avec “Fait pour servir et valoir ce que de droit.”
"""
    return call_deepseek(prompt)
