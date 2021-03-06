# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc

class Calculator(object):

    """受け取った文字列を字句・構文解析して四則演算を行うためのクラス"""

    def __init__(self):
        pass

    # トークンリスト
    tokens = (
        "NUMBER",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE"
    )

    # 正規表現によるルール
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    # 正規表現とアクションコード
    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    # スペース及びタブを無視
    t_ignore = " \t"

    # エラー処理
    def t_error(self, t):
        # print("Illegal Character: {0}".format(t.value[0]))
        pass

    # 文法定義
    def p_program_expr(self, p):
        'program : expression'
        p[0] = p[1]

    def p_expression_plus_minus(self, p):
        '''expression : term
                      | expression PLUS term
                      | expression MINUS term'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[2] == '+':
                p[0] = p[1] + p[3]
            elif p[2] == '-':
                p[0] = p[1] - p[3]

    def p_expression_times(self, p):
        '''term : NUMBER
                | term TIMES NUMBER
                | term DIVIDE NUMBER'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[2] == '*':
                p[0] = p[1] * p[3]
            elif p[2] == '/':
                p[0] = p[1] // p[3]

    # 構文エラー
    def p_error(self, p):
        raise yacc.YaccError("Syntax Error")

    def build(self, **kwargs):
        # Lexer構築
        self.lexer = lex.lex(module=self)
        # Parser構築
        self.parser = yacc.yacc(module=self)

    def calc(self, s):
        self.build()
        result = self.parser.parse(s)
        return result


if __name__ == '__main__':
    c = Calculator()
    s = input("Input Formula > ")
    res = c.calc(s)
    print(res)