
import gradio
import requests
theme='JohnSmith9982/small_and_pretty'
def login_reg(option,userin,passin,token):
    # print(option)
    if option==None: return "Please choose any of the options"
    if option=="login":
        if userin=="": return "Username cannot be empty"
        if passin=="": return "Password cannot be empty"
        # data = {"username":userin,"password":passin}
        data = '{"username":"'+userin+'", "password":"'+passin+'"}'
        data = str(data)
        resp = requests.post("http://127.0.0.1:5000/login",data=data,headers={"Content-Type": "application/json"}).json()
        return resp
    elif option=="register":
            # if option=="login":
        if userin=="": return "Username cannot be empty"
        if passin=="": return "Password cannot be empty"
        data = '{"username":"'+userin+'", "password":"'+passin+'"}'
        resp = requests.post("http://127.0.0.1:5000/register",data=data,headers={"Content-Type": "application/json"}).json()
        return resp
    elif option=="api_tester":
        if token=="": return "Token field cannot be empty"
        # data = '{"Autho}'
        if option=="api_tester": option="secure"
        resp = requests.get(f"http://127.0.0.1:5000/{option}",headers={"Authorization": "Bearer "+token}).text
        return resp
    elif option=="curl_it":
        # if token="": 
        data = '{"Authorization" : "'+token+'"}'
        if token=="": return "Token field cannot be empty"
        resp = requests.post(f"http://127.0.0.1:5000/{option}",data=data,headers={"Content-Type": "application/json"}).text
        return resp
    # return  "Lorem ipsum dolor sit amet consectetur adipisicing elit. Vitae, ratione sequi nesciunt iste perspiciatis esse deleniti repudiandae aut quibusdam aperiam rem impedit. Illo iusto eaque fugiat totam. Quam, nam in? Iste numquam laborum temporibus asperiores magnam repellendus harum vero eaque eos eum aliquid nulla cum, ullam maxime perspiciatis a dolorum ratione iure soluta! Magnam, tempore dolorum architecto voluptatibus fugiat dolorem? Cupiditate vel totam omnis fugit unde veritatis praesentium, suscipit magni ex ut ducimus, tenetur dolore. Eligendi possimus, placeat harum corrupti non, quibusdam iure animi est adipisci nemo corporis dicta dolorem. Dolorum expedita ex iusto eligendi hic provident animi iste vero, voluptates facere sed at eius quae dolor ipsum dolorem quibusdam officiis aliquam optio consequuntur magnam natus. Dolore nam adipisci libero! Debitis natus eos ab praesentium. Blanditiis ipsam minima repellendus mollitia cum sint vitae repudiandae quibusdam obcaecati laboriosam, repellat at in officia nisi eius fugiat minus perferendis quia incidunt tempora et."
textboxes=[]
s = gradio.Radio(["login", "register", "api_tester","curl_it"], label="API Endpoint", info="RESTful API Endpoint")

userbox = gradio.Textbox(label="Enter username: ")
            # t = gradio.Textbox(f"Textbox {i}")
passbox = gradio.Textbox(label="Enter password: ")
tokenbox = gradio.Textbox(label="Enter Authorization Token: ")
textboxes.append(userbox)
textboxes.append(passbox)
textboxes.append(tokenbox)
op=gradio.Textbox(label="API Response Text")
# ip=gradio.inputs.Textbox(label="Prompt Text")
demo = gradio.Interface(fn=login_reg, inputs=[s]+textboxes, outputs=op,theme='JohnSmith9982/small_and_pretty')
    
demo.launch()  