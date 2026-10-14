"""
Builds a string that describes
the character the chatbot will 
rolplay as
"""

def desc(persona):
    return (
        f" You are {persona["name"]}, "
        f"a {persona["who"]} "
        f"that is {", ".join(persona["traits"])}, "
        f"likes {", ".join(persona["likes"])}, "
        f"and hates {", ".join(persona["hates"])}"
    )
