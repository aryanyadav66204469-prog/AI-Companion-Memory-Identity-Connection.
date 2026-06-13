def generate_memory_response(person):
    return f"""
This is {person['name']}.

They are your {person['relationship']}.

Memory:
{person['memory']}
"""