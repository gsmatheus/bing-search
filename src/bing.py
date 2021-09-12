import requests
import json
import re


class Bing:

    def __init__(self):
        # Importa as config do Bing
        with open('./config/bing.json') as json_config:
            self.config = json.load(json_config)
        self.__session = requests.session()

    def search(self, keyword):
        """
        Busca os resultados pelo o bing
        :param keyword: Termo a ser procurado
        :return: Retorna uma lista com os sites encontrados
        """
        urls = []
        try:
            page = 1
            # Número de páginas a ser percorrido
            for _ in range(0, self.config['request']['page']):
                res = self.__session.get(
                    url=str(self.config['request']['url']).format(
                        keyword,
                        f'0{page}'  # Numero da pagina
                    ),
                    headers=self.config['request']['headers'],
                    timeout=10
                )
                # Não tem mais resultados para o keyword
                if 'Não há resultados para' in res.text:
                    return urls
                urls.extend(self.getUrls(res.text))
                page += 10
            return list(dict.fromkeys(urls))  # Retorna as urls, removendo valores repetidos
        except Exception as e:
            return False

    def getUrls(self, content):
        """
        Encontra todas as urls no codigo fonte
        :param content: Codigo fonte da pagina
        :return: Retorna a lista com as urls
        """
        return re.findall(f"{self.config['find_urls']['left']}(.*?){self.config['find_urls']['right']}", content)
