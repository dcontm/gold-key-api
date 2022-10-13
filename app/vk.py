import os
import vk_api
from dotenv import load_dotenv

load_dotenv()

vk_session = vk_api.VkApi("+79854330111", "omgwtfrak22")
vk_session.auth()

api = vk_session.get_api()
