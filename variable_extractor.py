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
    processed = latex.replace(' ', '[space]')
    processed = processed.replace('\\', '[backslash]')
    processed = processed.replace('(', '{')
    processed = processed.replace(')', '}')
    # print(processed)
    response = muterun_js('katex/parse.js', processed)
    # print(response.stdout)
    # print(response.stderr)
    if response.stdout == b'-1\n' or not response.stdout:
        yield -1
        return

    tree = etree.fromstring(response.stdout)
    ast = tree.xpath('.//semantics')[0]
    # print(etree.tostring(ast, pretty_print=True))
    count = 0

    for c in ast.xpath('.//*'):
        c.attrib['id'] = str(count)
        count += 1

    ngram_kv = {}
    ngram = []
    for row in ast.xpath('.//mrow'):
        ngram.append([])
        for mi in row:
            if mi.text and mi.tag == 'mi' and mi.text:
                ngram_kv[mi.attrib['id']] = row.attrib['id']
                if mi.text in ['=', '+', '-', '*', '/']:
                    ngram.append([])
                    continue
                ngram[-1].append(mi.text)
            else:
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

    for g in get_variables('{{Q}}=c^{2}{P}^{a}{e^{[backslash]gamma}{O}+{2}{P}^{a}}^{-l}e^{2}{Q}'):
        print(g)



