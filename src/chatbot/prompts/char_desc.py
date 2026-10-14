"""
Builds a string that describes
the character the chatbot will 
rolplay as
"""

def desc(persona):
    return f"""
    You are {persona["name"]}
    a {persona["who"]} that
    is {" ,".join(persona["traits"])},
    likes and
    """
