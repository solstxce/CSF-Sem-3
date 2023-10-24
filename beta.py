# import gradio as gr

# def greet(name):
#     return "Hello " + name + "!"

# with gr.Blocks() as demo:
#     name = gr.Textbox(label="Name")
#     output = gr.Textbox(label="Output Box")
#     rad = gr.Radio(["park", "zoo", "road"], label="Location", info="Where did they go?")

#     greet_btn = gr.Button("Greet")
#     greet_btn.click(fn=greet, inputs=[name], outputs=output, api_name="greet")
   

# if __name__ == "__main__":
#     demo.launch()
import gradio as gr

theme='JohnSmith9982/small_and_pretty'

def variable_outputs(choice,*args):
    # k = int(k)
    print(args)
    if choice=="login" or "register":
        return
    #     return [gr.Textbox.update(visible=True)]*2 + [gr.Textbox.update(visible=False)]
    # elif choice=="api_tester" or "curl_it":
    #     return [gr.Textbox.update(visible=False)]
def myfun():
    textboxes = []
    # for i in range(max_textboxes):
    userbox = gr.Textbox(label="Enter username: ")
    # t = gr.Textbox(f"Textbox {i}")
    passbox = gr.Textbox(label="Enter password: ")
    tokenbox = gr.Textbox(label="Enter Authorization Token: ")

with gr.Blocks(theme='JohnSmith9982/small_and_pretty') as demo:
    # s = gr.Slider(1, max_textboxes, value=max_textboxes, step=1, label="How many textboxes to show:")
    textboxes = []
    # for i in range(max_textboxes):
    with gr.Row():  
        with gr.Column(scale=1,width=600):
            s = gr.Radio(["login", "register", "api_tester","curl_it"], label="API Endpoint", info="RESTful API Endpoint",theme='JohnSmith9982/small_and_pretty')
            userbox = gr.Textbox(label="Enter username: ")
            # t = gr.Textbox(f"Textbox {i}")
            passbox = gr.Textbox(label="Enter password: ")
            tokenbox = gr.Textbox(label="Enter Authorization Token: ")
            textboxes.append(userbox)
            textboxes.append(passbox)
            textboxes.append(tokenbox)
        with gr.Column(scale=2,width=600):
            out = gr.Textbox(label="API Endpoint Response",width=800)
    if s=="login" or s=="register":
        gr.Textbox.update(visible=False)*2
        
    elif s=="api_tester" or s=="curl_it":
        textboxes[0].update(visible=False)
        textboxes[1].update(visible=False)
        textboxes[2].update(visible=True)

    s.change(variable_outputs, inputs=[s]+[i for i in textboxes],outputs=out)

if __name__ == "__main__":
   demo.launch()
