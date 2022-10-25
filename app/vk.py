import os
import vk_api
from dotenv import load_dotenv

load_dotenv()

login = os.environ.get("VK_LOGIN")
password = os.environ.get("VK_PASSWORD")


vk_session = vk_api.VkApi(login, password)
#vk_session.auth()

#api = vk_session.get_api()
