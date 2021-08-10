import os


rasp_ip = "203.252.240.75"
rasp_port = "9022"
rasp_id = "pi"
rasp_pw = "dblab6100!@#"
file_name = "image.jpg"
file_path = f"/home/pi/project/meat/{file_name}"

def shot_cam():
    os.system(f"plink -batch -pw {rasp_pw} -P {rasp_port} {rasp_id}@{rasp_ip} fswebcam {file_name}")

def get_img():
    os.system(f"pscp -batch -pw {rasp_pw} -P {rasp_port} {rasp_id}@{rasp_ip}:{file_path} {os.getcwd()}/web/static/img/cam")