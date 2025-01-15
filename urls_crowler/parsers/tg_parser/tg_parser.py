import re
from typing import List, Optional

import settings
from urls_crowler.dto import ParseResultDTO
from urls_crowler.parsers.base_url_parser import BaseParser


class TGParser(BaseParser):
    @staticmethod
    def get_salary(text: str) -> Optional[str]:
        salary_pattern = r'З\\/П\s*от\s*\d+\s*до\s*\d+\s*(руб\\.|р\\.|р\\.|₽.)'
        return re.findall(salary_pattern, text)[0] if re.findall(salary_pattern, text) else None

    @classmethod
    def parse_all_links(cls, json_data: dict, redis_cache, chat_id, *args, **kwargs) -> (List[ParseResultDTO], List):
        results = []
        all_links = []
        keys = cls.get_keys()

        for channel in json_data:
            for message in json_data[channel]:
                link = message.get('message_link', None)
                all_links.append(link)
                message_text = message.get('caption', None)
                cached_data = redis_cache.get(link)
                if not cached_data:
                    try:
                        parse_result = cls.parse_message(message_text, link, keys)
                    except Exception:
                        parse_result = ParseResultDTO()
                    if parse_result.profession != '':
                        results.append(parse_result)
                        parse_result.users.append(chat_id)
                        parse_result.users = list(set(parse_result.users))
                        redis_cache.set(link, parse_result.model_dump_json())
                else:
                    parse_result = ParseResultDTO.model_validate_json(cached_data)
                    if settings.INCLUDE_PREVIOUS >= (chat_id in parse_result.users):
                        results.append(parse_result)
                        parse_result.users.append(chat_id)
                        parse_result.users = list(set(parse_result.users))
                        redis_cache.set(link, parse_result.model_dump_json())

        return results, all_links

    @classmethod
    def parse_message(cls, text: str, link: str, keys: dict) -> ParseResultDTO:
        result_values = {}

        skills = cls.find_skills(text)
        titles = cls.find_title(text)
        result_values['skills'] = ', '.join(skills)
        result_values['title'] = ', '.join(titles)

        result_values['desc'] = text[:40]

        result_values['tech_flag'] = cls.tech_true(text)
        result_values['manager_flag'] = cls.manager_true(text)

        specify_profession = cls.specify_profession(skills)
        result_values['direction'] = specify_profession[0]
        result_values['profession'] = specify_profession[1]

        salary = cls.format_salary(cls.get_salary(text))
        result_values['salary'] = salary
        result_values['salary_range'] = cls.determine_salary_range(salary)

        result_values['exp'] = cls.find_exp(text, None)
        result_values['link'] = link

        res_keys = result_values.keys()
        for key in keys.keys():
            if key not in res_keys:
                result_values[key] = ''

        return ParseResultDTO(**result_values)
