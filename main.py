from aiogram import executor

from modules.handlers import send_to_adm_su, send_to_adm_sd
from modules.run import dp


def main():
    settings = {"on_startup": send_to_adm_su, "on_shutdown": send_to_adm_sd}
    executor.start_polling(dp, **settings)


if __name__ == "__main__":
    main()
