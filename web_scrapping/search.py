# -*- coding: utf-8 -*-
__author__ = "SirHades696"
__email__ = "djnonasrm@gmail.com"

import urllib.request
from bs4 import BeautifulSoup


class search_packages: 
    def __init__(self, package, page=1):
        """Simple tool for search packages on pypi.org
        with web scrapping

        Args:
            package (string): Python Package for search
            page (int, optional): Number of page in pypi.org . Defaults to 1.
        """
        self.package = package
        self.page = str(page)
        self._search()
    
    def _search(self):
        """
        Create a dictionary with all the necessary elements to display in the telegram bot. 
        """
        url = r"https://pypi.org/search/?q=" + self.package + "&page=" + self.page
        open_web = urllib.request.urlopen(url)
        html = BeautifulSoup(open_web, "html.parser")
        content = html.find_all("a", {"class": "package-snippet"})
        self._values = {}
        
        if len(content) < 1:
            self._values["Result " + str(0)] = {"No results": "There were no results for " + self.package}
            return self._values
        else:
            url_base = r"https://pypi.org"
            
            for i, cont in enumerate(content):
                # get values from primary link
                link = url_base + cont.get("href")
                name = cont.find("span", {"class": "package-snippet__name"}).getText()
                version  = cont.find("span", {"class": "package-snippet__version"}).getText()
                released = (cont.find("span", {"class": "package-snippet__released"}).getText()).split("\n")[1].split("  ")[1]
                summ = cont.find("p", {"class": "package-snippet__description"}).getText()
                summary =  summ if summ != "" else "No description"
                
                # get values from secondary link 
                open_web2 = urllib.request.urlopen(link)
                html2 = BeautifulSoup(open_web2,"html.parser")
                
                # Home page 
                vertical_tab = html2.find_all("a", {"class": "vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed"})
                home_page = "No official page"
                for hp in vertical_tab:
                    txt = hp.get_text().split("\n")[1]
                    if txt == "Homepage":
                        home_page = hp.get("href")
                        break
                
                # Pip install 
                pip_install = html2.find("span", {"id": "pip-command"}).getText()
                
                #Contains all downloads
                downloads = html2.find_all("th", {"scope": "row"})
                link_dwn = []
                for j, download in enumerate(downloads):
                    for dwn in download.find_all("a", href=True):
                        link_dwn.append(dwn.get("href"))
                
                #Author and Requires
                section_title = html2.find_all("p")
                a_r = self._get_author_requires(section_title)
                # Stupid python .l. 
                author = a_r[0] if not "Python" in a_r[0] else a_r[1]
                requires = a_r[0] if "Python" in a_r[0] else a_r[1] 
                #------------- 
                
                # creating a dictionary
                self._values["Result " + str(i+1)] = {"Project_name": name, 
                                            "Version": version, 
                                            "Released": released,
                                            "Summary": summary,        
                                            "PyPi_link": link,
                                            "PIP": pip_install,
                                            "Homepage":home_page,
                                            "Author": author,
                                            "Requires": requires,
                                            "Links_for_dwn" : link_dwn}
                
    def _get_author_requires(self, html):
        """Receives html and gets the fields Author and Requires

        Args:
            html ([String]): Html pre-filtering

        Returns:
            [list]: Index 0: Author, Index 1: Requires
        """
        lines = []
        for txt in html:
            lines.append(txt.getText().split("\n"))
        data = []
        for i in range(0, len(lines)):
            for j in range(0, len(lines[i])):
                if "Author" in str(lines[i][j]):
                    data.append(lines[i][j])
                if "Requires" in str(lines[i][j]):
                    data.append(lines[i][j])
        
        #Fields are repeated twice
        lista = list(set(data))
        values = []
        if len(lista) == 0:
            # No author no requires
            values.append("No Author")
            values.append("No Python Specific")
        elif len(lista) == 1:
            #Only has Author
            if "Author" in str(lista[0]):
                var = lista[0].split("Author: ")[1]
                values.append(var)
                values.append("No Python Specific")
            #Only has Requires
            elif "Requires" in str(lista[0]):
                values.append("No Author")
                var = lista[0].split("Requires: ")[1]
                #replace < or >
                if ">" or "<" in var:
                    req = var.replace('<', '&lt;')
                    req = req.replace('>', '&gt;')
                    values.append(req) 
        elif len(lista) == 2:
            #Contains both
            for i in range(0,2):
                if "Author" in lista[i]:
                    author = lista[i].split("Author: ")[1]
                    values.append(author)
                elif "Requires" in lista[i]:
                    requires = lista[i].split("Requires: ")[1]
                    #replace < or >
                    if ">" or "<" in requires:
                        req = requires.replace('<', '&lt;')
                        req = req.replace('>', '&gt;')
                        values.append(req)
        return values
    
    def get_values(self):
        """Returns all found values:
        
        For cero values the struct is returned as
        {"Result 0":{"No results" : "There were no results for [package]"}}
        
        For one or more values the struct is returned as
        {"Result 1":{"Project_name": Package, 
                    "Version": Version, 
                    "Released": Released,
                    "Summary": Summary,        
                    "PyPi_link": Link,
                    "PIP": pip install [package],
                    "Homepage": Homepage,
                    "Links_for_dwn" : [All links]}}
        Returns:
            [dict]: [Values]
        """
        return self._values