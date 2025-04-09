def generate_recommendations(report_text):
    """
    Analyse le contenu du rapport et génère une liste de recommandations.
    """
    lines = report_text.splitlines()
    suggestions = []

    # Exemple de règles simples :
    if any("SQLi détectée" in line for line in lines):
        suggestions.append("Utilisez des requêtes préparées pour éviter les injections SQL.")
    if any("XSS détectée" in line for line in lines):
        suggestions.append("Échappez les caractères spéciaux pour éviter les attaques XSS.")
    if any("Ports ouverts détectés" in line for line in lines):
        suggestions.append("Fermez les ports non utilisés et configurez votre pare-feu correctement.")
    if any("Serveur Web détecté" in line for line in lines):
        suggestions.append("Mettez à jour votre serveur web et désactivez les modules superflus.")

    if not suggestions:
        suggestions.append("Aucune vulnérabilité critique détectée, surveillez régulièrement votre système.")

    return suggestions
