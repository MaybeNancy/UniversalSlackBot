"""
Builds a string that describes
the character the chatbot will 
rolplay as
"""

def desc(persona):
    return (
        f" You are {persona["name"]}, "
        f"a {persona["who"]}; "
        f"you are {", ".join(persona["traits"])}; "
        f"you like {", ".join(persona["likes"])}; "
        f"and you hate {", ".join(persona["hates"])}"
    )
