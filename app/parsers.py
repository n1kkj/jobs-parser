import abc
import enum
import time

from .dto import PageData
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class NoSuchParserError(Exception):
    pass


class ParserEngine(abc.ABC):
    @abc.abstractmethod
    def parse_data(
        self,
        url: str,
        name_selector: str,
        description_selector: str,
        source_selector: str | None,
    ) -> PageData: ...


class SeleniumParserEngine(ParserEngine):
    def __init__(self):

        options = ChromeOptions()

        options.add_experimental_option(
            "prefs",
            {
                # block image loading
                "profile.managed_default_content_settings.images": 2,
            },
        )

        self.__driver = Chrome(options=options)

    def parse_data(
        self,
        url: str,
        name_selector: str,
        description_selector: str,
        source_selector: str | None,
    ) -> PageData:
        self.__driver.get(url)

        # We use this to avoid instant loading
        # correspondig to antiparsers behavior
        time.sleep(0.25)

        return PageData(
            url,
            vacancy_name=self.__parse_name(name_selector),
            vacancy_description=self.__parse_description(description_selector),
            vacancy_source=(
                self.__parse_source(source_selector)
                if source_selector
                else None
            ),
        )

    def __parse_name(self, selector: str) -> str:

        vacancy_name = self.__driver.find_element(
            By.CSS_SELECTOR, selector
        ).text

        return vacancy_name

    def __parse_description(self, selector: str) -> str:
        description_block = self.__driver.find_element(
            By.CSS_SELECTOR, selector
        )

        return description_block.text

    def __parse_source(self, selector: str) -> str:
        source_block = self.__driver.find_element(By.CSS_SELECTOR, selector)

        return source_block.text

        # print("HEre")

        # soup = BeautifulSoup(description_html, "lxml")

        # return soup.text


class PageParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, url: str) -> PageData: ...


class CareerSpaceParser(PageParser):
    def __init__(self, parser_engine: ParserEngine) -> None:
        self.__parser_engine = parser_engine

    def parse(self, url: str) -> PageData:

        data = self.__parser_engine.parse_data(
            url,
            name_selector='h1[data-testid="csu-title"]',
            description_selector="div.j-d__dsc-vl",
            source_selector="span[data-v-27ef1e69]",  # FIXME
        )

        print(data.vacancy_source)

        return data


class RabotaSberParser(PageParser):
    def __init__(self, parser_engine: ParserEngine) -> None:
        self.__parser_engine = parser_engine

    def parse(self, url: str) -> PageData:
        data = self.__parser_engine.parse_data(
            url,
            name_selector='h1[data-gtm-vis-has-fired178144873_28="1"]',
            description_selector="div.styled__ContentColumn-vj1fq3-1",
            source_selector=None,
        )

        vacancy_source = "RABOTA_SBER"

        data.vacancy_source = vacancy_source

        return data


class DevelopersSberParser(PageParser):
    def __init__(self, parser_engine: ParserEngine) -> None:
        self.__parser_engine = parser_engine

    def parse(self, url: str) -> PageData:
        data = self.__parser_engine.parse_data(
            url,
            name_selector="h1[class='sc-45e1da05-0 sc-81d0f9f1-7 QPtSW kFPzMP']",
            description_selector="div[class='sc-dc74419e-0 gTvbPQ']",
            source_selector=None,
        )

        vacancy_source = "MTS"

        data.vacancy_source = vacancy_source

        return data


class YandexJobsParser(PageParser):

    def __init__(self, parser_engine: ParserEngine) -> None:
        self.__parser_engine = parser_engine

    def parse(self, url: str) -> PageData:
        data = self.__parser_engine.parse_data(
            url,
            name_selector='h1[class="lc-styled-text__text"]',
            description_selector=".lc-jobs-vacancy-mvp__description",
            source_selector=None,
        )

        vacancy_source = "YANDEX"

        data.vacancy_source = vacancy_source

        return data


class JobMTSParser(PageParser):
    def __init__(self, parser_engine: ParserEngine) -> None:
        self.__parser_engine = parser_engine

    def parse(self, url: str) -> PageData:

        data = self.__parser_engine.parse_data(
            url,
            name_selector="h1.title",
            description_selector="div[data-v-da002fab]",
            source_selector=None,
        )

        vacancy_source = "MTS"

        data.vacancy_source = vacancy_source

        return data


class JobOzonParser(PageParser):
    def __init__(self, parser_engine: ParserEngine) -> None:
        self.__parser_engine = parser_engine

    def parse(self, url: str) -> PageData:
        data = self.__parser_engine.parse_data(
            url,
            name_selector="h1[data-v-5e991654]",
            description_selector="div.vacancy__info__body",
            source_selector=None,
        )

        vacancy_source = "MTS"

        data.vacancy_source = vacancy_source

        return data


class ParserType(enum.Enum):
    CAREERSPACE = "CAREERSPACE"
    YANDEXJOBS = "YANDEXJOBS"
    RABOTASBER = "RABOTASBER"
    DEVELOPERSSBER = "DEVELOPERSSBER"
    JOBMTS = "JOBMTS"
    JOBOZON = "JOBOZON"


class ParserFactory:
    def __init__(self):
        pass

    def __get_parser_type(self, url: str) -> ParserType:
        if "careerspace.app" in url:
            return ParserType.CAREERSPACE

        if "yandex.ru/jobs" in url:
            return ParserType.YANDEXJOBS

        if "rabota.sber.ru" in url:
            return ParserType.RABOTASBER

        if "developers.sber.ru" in url:
            return ParserType.DEVELOPERSSBER

        if "job.mts.ru" in url:
            return ParserType.JOBMTS

        if "job.ozon.ru" in url:
            return ParserType.JOBOZON

        raise ValueError("Unknown parser type")

    def get_parser(self, url: str, parser_engine: ParserEngine) -> PageParser:

        match self.__get_parser_type(url):
            case ParserType.CAREERSPACE:
                return CareerSpaceParser(parser_engine=parser_engine)
            case ParserType.YANDEXJOBS:
                return YandexJobsParser(parser_engine=parser_engine)
            case ParserType.RABOTASBER:
                return RabotaSberParser(parser_engine=parser_engine)
            case ParserType.DEVELOPERSSBER:
                return DevelopersSberParser(parser_engine=parser_engine)
            case ParserType.JOBMTS:
                return JobMTSParser(parser_engine=parser_engine)
            case ParserType.JOBOZON:
                return JobOzonParser(parser_engine=parser_engine)
            case _:
                raise NoSuchParserError("Incorrect parser type")
