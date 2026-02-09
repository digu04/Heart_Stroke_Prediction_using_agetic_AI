from agents.helper_agent import helper_agent_process

input_text = """
I am a 55 year old man. I get chest pain when walking fast.
My BP is around 150. Cholesterol is high at 250.
Sugar is sometimes high. I get tired easily.
"""

result = helper_agent_process(input_text)
print(result)
