from urls_crowler.parsers import BaseHTMLUrlParser


class MegafonParser(BaseHTMLUrlParser):
    title_key = 'h1|mfui-header mfui-header_color_default mfui-header_level_h1 mfui-header_h-align_inherit vacancy-banner__title'
    desc_key = 'div|mfui-grid-column mfui-grid-column_all_12 mfui-grid-column_wide_7 mfui-grid-column_desktop_7 mfui-grid-column_tablet_7 mfui-grid-column_all-order_0 mfui-grid-column_wide-order_0 mfui-grid-column_desktop-order_0 mfui-grid-column_tablet-order_0 mfui-grid-column_mobile-order_0 mfui-grid__column mfui-grid__column_gutter-bottom_medium|1'
    salary_key = None
    exp_key = 'h5|mfui-header mfui-header_color_default mfui-header_level_h5 mfui-header_h-align_inherit mfui-header_space_wide vacancy-banner__text'
    city_key = 'p|city__name city__name_font-size_big'
    employer_key = None
    work_format_key = 'h5|mfui-header mfui-header_color_default mfui-header_level_h5 mfui-header_h-align_inherit mfui-header_space_wide vacancy-banner__text|1'

    fixed_employer = 'Мегафон'
