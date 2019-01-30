from Naked.toolshed.shell import muterun_js
from lxml import etree

def unparse(node):

    if isinstance(node, str):
        return node

    if node.tag == 'msub':
        return '{%s}_{%s}' % (unparse(node[0]), unparse(node[1]))

    if node.tag == 'msup':
        return '{%s}^{%s}' % (unparse(node[0]), unparse(node[1]))

    if node.tag == 'mrow':
        return '{'+''.join(unparse(n) for n in node)+'}'

    return node.text

def get_variables(latex):
    processed = latex.replace(' ', '')
    processed = processed.replace('\\', '[backslash]')
    processed = processed.replace('(', '{')
    processed = processed.replace(')', '}')
    # print(processed)
    response = muterun_js('katex/parse.js', processed)
    # print(response.stdout)
    print(response.stderr)
    if response.stdout == b'-1\n' or not response.stdout:
        yield -1
        return

    tree = etree.fromstring(response.stdout)
    ast = tree.xpath('.//semantics')[0]
    # print(etree.tostring(ast))
    count = 0

    for c in ast.xpath('.//*'):
        c.attrib['id'] = str(count)
        count += 1

    ngram_kv = {}
    ngram = []
    for row in ast.xpath('.//mrow'):
        ngram.append([])
        for mi in row:
    
            if mi.text and mi.tag == 'mi':
                ngram_kv[mi.attrib['id']] = row.attrib['id']
                ngram[-1].append(mi.text)
            else:
                if len(ngram[-1]) > 0:
                    ngram.append([])

    for sup in tree.xpath('.//msup'):
        if 'None' not in unparse(sup):
            yield sup

    for sub in tree.xpath('.//msub'):
        if 'None' not in unparse(sub):
            yield sub

    for id in tree.xpath('.//mi'):
        if id.attrib['id'] not in ngram_kv:
            if 'None' not in unparse(id):
                yield id.text

    for _x in ngram:
        if len(_x) > 0:
            yield ''.join(_x)


if __name__ == '__main__':

    # import json
    # latex = json.load(open('latex.json', 'r'))[0]

    # variable_union = set()

    # for l in latex:
    #     variables = get_variables(l)
    #     # print(l, list(variables))
    #     if variables == -1:
    #         continue
    #     for v in variables:
    #         if isinstance(v, etree._Element):
    #             variable_union.add(
    #                 unparse(v)
    #             )
    #         else:
    #             variable_union.add(
    #                 v
    #             )

    # print(variable_union)

    for g in get_variables('{{Q}}=c^{2}{P}^{a}{e^{[backslash]gamma}{O}+{2}{P}^{a}}^{-l}e^{2}{Q}'):
        print(g)

    # for i in list(variable_union):
    #     unparse(i)


