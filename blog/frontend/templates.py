# -*- coding: utf-8 -*-
from config import Config

root = Config.THEME

templates = dict(
    home="frontend/themes/%s/home.html" % root,
    diary_detail="frontend/themes/%s/diary/detail.html" % root,
    diary_list="frontend/themes/%s/diary/list.html" % root,
    cat_list="frontend/themes/%s/category/list.html" % root,
    page="frontend/themes/%s/page/index.html" % root,
    not_found="frontend/themes/%s/404.html" % root
)
