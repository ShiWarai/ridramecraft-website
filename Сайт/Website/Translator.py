from Website import app
from os.path import join as path_join

source_lang = app.config['LANGUAGES'][0]
target_langs = app.config['LANGUAGES'][1:]

if app.debug: # Система для настройки на компьютере

    from Website.Repository import \
        getFilesList, root_dir, get_mo_file_path, get_po_file_path, templates_directory, fileExist, pot_file_path
    from Website.DatabaseClasses import database, Project

    from babel.messages.pofile import read_po, write_po
    from babel.messages.mofile import write_mo

    from requests import post
    from json import loads as json_loads

    from bs4 import BeautifulSoup
    from bs4.element import Comment
    from re import match as re_match
    from subprocess import Popen

    # Словарь HTML
    # Подготовка страниц к переводу

    def is_visible(element):
        if element in [' ', '\n']:
            return False
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        if re_match(r"[^>]*{{[^{}]*}}[^<]*", element) != None or re_match(r"[^>]*{%[^{}%]+%}[^<]*", element) != None:
            return False
        return True

    def text_from_html(doc):
        soup = BeautifulSoup(doc, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(is_visible, texts)
        for visible_text in visible_texts:
            visible_text.replace_with("{{ _(\"" + str(visible_text) + "\") }}")

        return soup.prettify(formatter="html")

    def deleteCommentsPO(path):
        data = None
        with open(path,'r', encoding='utf-8') as po:
            data = po.read()

        data = data[:data.find("#~ msgid")]

        with open(path,'w', encoding='utf-8') as po:
            po.write(data)

    templates_list = getFilesList(templates_directory) # Список всех шаблонов страниц html

    for template_path in templates_list:
        template_data = str()
        with open(template_path, "r", encoding='utf-8') as template:
            template_data = template.read()
        template_data = text_from_html(template_data)
        with open(template_path, "w", encoding='utf-8') as template:
            template.write(template_data)

    langs_dictionary_unfinished = False
    for lang in target_langs:
        if not fileExist(get_po_file_path(lang)):
            langs_dictionary_unfinished = True
            print("LANGS UNFINISHED!")

    # Извлечение слов в словарь (главный)
    with Popen(['pybabel','extract','-F','babel.cfg','-k','_l','-o','req_translation.pot','.'], cwd = root_dir) as process:
        process.wait()

    # Его пополнение БД

    catalog = None

    with open(pot_file_path, 'r', encoding='utf-8') as pot:
        catalog = read_po(pot)  # Загружаем список всех слов к переводу
        projects = Project.query.all()
        for project in projects:
            catalog.add(project.description)

        database.session.commit() # Сохраняем translated
    with open(pot_file_path, 'wb') as pot:
        write_po(pot, catalog) # Записываем новый каталог с текстами из БД

    # Создание или обновление языковых словарей

    if langs_dictionary_unfinished:
        for lang in target_langs:
            with Popen(['pybabel', 'init', '-i', path_join(root_dir, 'req_translation.pot'), '-d', path_join(root_dir, 'Website', 'translations', '--no-fuzzy-matching'), '-l', lang], cwd = root_dir) as process:
                process.wait()
    else:
        with Popen(['pybabel','update','-i', path_join(root_dir, 'req_translation.pot'),'-d', path_join(root_dir, 'Website', 'translations'), '--no-fuzzy-matching'], cwd = root_dir) as process:
            process.wait()

    # Отчистка от комментариев

    for lang in target_langs:
        deleteCommentsPO(get_po_file_path(lang))

    # Первод через Yandex Cloud

    def translate(texts, lang):
        data = {
            "sourceLanguageCode": source_lang,
            "targetLanguageCode": lang,
            "texts": texts
        }
        response = post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                        headers = {'Content-type': "application/plain; charset=utf-8",'Authorization' : f"Api-Key {app.api_key}"},
                        json = data)
        return json_loads(response.content.decode('utf-8'))['translations']

    for lang in target_langs:
        # Чтение и обновление словаря
        catalog = None
        req_update = False
        req_translate = list()
        with open(get_po_file_path(lang),'r', encoding='utf-8') as po:
            catalog = read_po(po) # Загружаем словарь оригинального текста для перевода

            for message in catalog:
                if message.id and not message.string:
                        print("Not translated: ", message.id)

                        if len(message.id):
                            req_translate.append(message.id)
                            req_update = True

        if len(req_translate) != 0:
            print("Start AI translation...")
            translations = translate(req_translate, lang)

            updated_dict = dict()
            for i in range(len(req_translate)):
                updated_dict[req_translate[i]] = translations[i]['text']

            # Записываем в каталог новые слова
            for message in catalog:
                if message.id and not message.string:
                    message.string = updated_dict[message.id]
                    message.flags = ['fuzzy',]
                    print(message.id, "Translated as:", message.string, sep='\n')

            # Сохранение словаря
            if req_update:
                with open(get_po_file_path(lang),'wb') as po:
                    write_po(po, catalog)

        # Компиляция словаря
        with open(get_mo_file_path(lang), 'wb') as mo:
            write_mo(mo, catalog)