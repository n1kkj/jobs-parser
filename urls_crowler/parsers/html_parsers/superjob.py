from urls_crowler.parsers import BaseHTMLUrlParser


class SuperJobParser(BaseHTMLUrlParser):
    title_key = 'h1|_1ONuf _3Xwez _CHVO _3SJX7 _2fnzI N49dX _2BOjv LvtXw'
    desc_key = 'span|mrLsm _1eDv3 N49dX Pjeuw _162Xb LvtXw'
    salary_key = 'span|kk-+S _2fnzI N49dX _162Xb'
    exp_key = 'span|_2aW__ N49dX _162Xb|0'
    city_key = 'span|_1eDv3 N49dX Pjeuw _162Xb'
    employer_key = 'span|_2fnzI N49dX Pjeuw _162Xb'
    work_format_key = 'span|_2aW__ N49dX _162Xb|-1'
