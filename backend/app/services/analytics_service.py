def calculate_kpis(leads):
    total_leads = len(leads)

    if total_leads == 0:
        return {
            "total_leads": 0,
            "avg_conversion": 0,
            "high_priority": 0,
            "total_value": 0
        }

    avg_conversion = sum(l.conversion_probability for l in leads) / total_leads

    high_priority = [l for l in leads if l.conversion_probability > 0.7]

    total_value = sum(l.budget or 0 for l in leads)

    return {
        "total_leads": total_leads,
        "avg_conversion": round(avg_conversion, 2),
        "high_priority": len(high_priority),
        "total_value": total_value
    }