import configparser

def save_config(entry_excel_url, entry_whatsapp_number, window, main_window):
    from window import return_to_menu
    config = configparser.ConfigParser()
    config.read('.config')
    config.set("CONFIG", "GOOGLE_SHEET_URL", entry_excel_url.get())
    config.set("CONFIG", "GOOGLE_SHEET_ID", entry_excel_url.get().split("/")[5])
    config.set("CONFIG", "WHATSAPP_NUMBER", entry_whatsapp_number.get())
    with open('.config', 'w') as configfile:
        config.write(configfile)

    return_to_menu(window, main_window)