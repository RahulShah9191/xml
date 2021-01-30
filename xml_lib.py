"""
require conda install beautifulsoup
"""

import re
from bs4 import BeautifulSoup
from utils import string_lib


class XmlLib:

    def __init__(self, input_xml, features='xml'):
        self.input_xml = input_xml
        self.features = features
        if self.input_xml != "" and self.input_xml is not None:
            try:
                self.is_valid_xml()
                self.encrypted_cdata_xml = XmlLib.encrypt_xml_cdata(data=self.input_xml)
                self.encrypted_soup = BeautifulSoup(self.encrypted_cdata_xml, self.features)
                self.tags = [tag.name for tag in self.soup.find_all()]
                print("Valid XML!")
            except Exception as e:
                print(f"{TAG} | Failed to parse the XML: {input_xml} ")
        else:
            print(f"XML is Empty or None. \n input_xml :: {input_xml}")

    def is_valid_xml(self):
        """
        Check input string is valid XML.
        :param input_xml: String
        :return: return true if valid XML, else return false.
        """
        try:
            self.soup = BeautifulSoup(self.input_xml, self.features)
            return True
        except Exception as e:
            print(f"{TAG} | Failed to parse the XML: {self.input_xml} ")
            return False

    def is_element_present(self, xml_tag):
        """
        Validate if element present in XML
        :param xml_tag: The XML tag name
        :return: return True if element present, else return False
        """
        return True if xml_tag in self.tags else False

    def is_elements_present(self, xml_tags):
        """
        Validate if elements present in XML
        :param xml_tags: The XML tags name
        :return: return True if elements present, else return False
        """
        xml_tags_list = xml_tags.split(',')
        for xml_tag in xml_tags_list:
            if xml_tag in self.tags:
                continue
            else:
                return False
        return True

    def get_element_attribute(self, xml_tag, attr_name, first=False):
        string_lib.remove_space(xml_tag)
        result =  self.get_element(xml_tag, first)
        try:
            if isinstance(result, (str, int)):
                return result[attr_name]
            else:
                return [element[attr_name] for element in result]
        except Exception as e:
            print(TAG + " | Failed to find attribute : {} in XML ".format(xml_tag))
            return 0

    def get_element_attribute_encrypted(self, xml_tag, attr_name, first=False):
        string_lib.remove_space(xml_tag)
        result =  self.get_element_encrypted(xml_tag, first)
        try:
            if isinstance(result, (str, int)):
                return result[attr_name]
            else:
                return [element[attr_name] for element in result]
        except Exception as e:
            print(TAG + " | Failed to find attribute : {} in XML ".format(xml_tag))
            return 0

    def get_count(self, xml_tag):
        """
        Get element count from XML
        :param xml_tag: the Input XML tag
        :return: return count if element present, elsa return zero
        """
        string_lib.remove_space(xml_tag)
        try:
            data = self.soup.find_all(xml_tag)
            return len(data)

        except Exception as e:
            print(TAG + " | Failed to find tag : {} in XML ".format(xml_tag))
            return 0

    def get_element(self, xml_tag, first=False):
        """
        Get XML elements from XML String
        :param xml_tag: the XML tag to be return
        :param first: only need to return first tag, default false
        :return: element / list of element if found elase return None
        """
        string_lib.remove_space(xml_tag)
        try:
            if first:
                data = self.soup.find(xml_tag)
            else:
                data = self.soup.find_all(xml_tag)
            return data
        except Exception as e:
            print(f"Exception :: {e}")
            print(f"{TAG} | Failed to find tag : {xml_tag} in XML!")
            return None

    def get_element_encrypted(self, xml_tag, first=False):
        """
        Get XML elements from XML String
        :param xml_tag: the XML tag to be return
        :param first: only need to return first tag, default false
        :return: element / list of element if found elase return None
        """
        string_lib.remove_space(xml_tag)
        try:
            if first:
                data = self.soup.find(xml_tag)
            else:
                data = self.encrypted_soup.find_all(xml_tag)
            return data
        except Exception as e:
            print(f"Exception :: {e}")
            print(f"{TAG} | Failed to find tag : {xml_tag} in XML!")
            return None

    def get_element_value(self, xml_tag, first=False):
        """
        Get the value of all XML_tag
        :param xml_tag: The XML tag need to fetch
        :param first: if need to return value for only first tag
        :return: return value / list of value
        """
        string_lib.remove_space(xml_tag)
        try:
            result = self.get_element(xml_tag, first=first)
            return string_lib.remove_space(result.text) if isinstance(result, (str, int)) else [ element.text for element in result ]
        except Exception as e:
            print(TAG + " | Failed to find tag : {} in XML ".format(xml_tag))
            return None

    def is_element_empty(self,xml_tag):
        string_lib.remove_space(xml_tag)
        try:
            result = self.get_element(xml_tag, True)
            data = string_lib.remove_space(result.text)
            if data == "" or data == None:
                return True
            return False
        except Exception as e:
            print(TAG + " | Failed to find tag : {} in XML ".format(xml_tag))


    def get_element_cdata_value(self, xml_tag, first=False):
        string_lib.remove_space(xml_tag)
        try:
            if first:
                tag_content = list(self.encrypted_soup.find(xml_tag))[0]
                return XmlLib.get_cdata_value(data=tag_content.text)
            else:
                tag_content = [XmlLib.get_cdata_value(data=cdata.text) for cdata in list(self.encrypted_soup.find_all(xml_tag))]
            return tag_content
        except Exception as e:
            print(TAG + " | Failed to find tag : {} in XML ".format(xml_tag))
            return None

    @staticmethod
    def encrypt_xml_cdata(data):
        encrypt_cdata = re.sub(r"<!\[CDATA\[(.+?)\]\]>", r"X![CDATA[\1]]X", data)
        escaped_data = encrypt_cdata.replace('&', '__AMPERSAND__')
        return escaped_data

    @staticmethod
    def decrypt_xml_cdata(data):
        decrypt_cdata = re.sub(r"X!\[CDATA\[(.*?)\]\]X", r"<![CDATA[\1]]>", data)
        unescaped_data = decrypt_cdata.replace('__AMPERSAND__', '&')
        return unescaped_data

    @staticmethod
    def get_cdata_value(data):
        return re.sub(r".*X!\[CDATA\[(.*?)\]\]X.*", r"\1", data).replace('__AMPERSAND__', '&')

