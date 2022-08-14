from __future__ import print_function

import json
try:
    from urllib import urlencode
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

import click


CODE_MSG_MAP = {
    20: u'要翻译的文本过长',
    30: u'无法进行有效的翻译',
    40: u'不支持的语言类型',
    50: u'无效的key',
    60: u'无词典结果，仅在获取词典结果生效'
}


def request_youdao(q, keyfrom, key):
    url = 'http://fanyi.youdao.com/openapi.do'
    param = {
        'keyfrom': keyfrom,
        'key': key,
        'type': 'data',
        'doctype': 'json',
        'version': '1.1',
        'q': q
    }
    url += '?' + urlencode(param)
    req = Request(url)
    res = urlopen(req)
    return json.loads(res.read().decode('utf-8'))


def translate(q, keyfrom, key):
    json_data = request_youdao(q, keyfrom, key)
    error_code = json_data.get('errorCode')
    if error_code != 0:
        click.echo(f"[\033[1;32;40m{error_code}\033[0m] {CODE_MSG_MAP.get(error_code)}")
        return

    query = json_data.get('query')
    translations = json_data.get('translation')
    click.echo("[{query}]: \033[1;32;40m{translations}\033[0m".format(
        query=query, translations='\033[1;31;40m; \033[0m'.join(translations)))
    basic = json_data.get('basic')
    if basic and isinstance(basic, dict):
        phonetic = basic.get('phonetic', None)
        uk = basic.get('uk-phonetic', None)
        us = basic.get('us-phonetic', None)
        explains = basic.get('explains', [])
        click.echo("{phonetic}; [us] \033[1;32;40m{us}\033[0m; [uk] {uk}".format(phonetic=phonetic, us=us, uk=uk))
        click.echo()
        click.echo('\033[1;31;40m; \033[0m\n'.join(explains))
        click.echo()

    web = json_data.get('web')
    if web and isinstance(web, list):
        for item in web:
            click.echo('{k}: {v}'.format(k=item['key'], v='\033[1;31;40m; \033[0m'.join(item['value'])))
