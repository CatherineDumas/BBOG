# convert Change.org pseudo-JSON file to csv

# command format:
#$ python change2csv.py changefile newfile.csv

import sys, re, ast, csv

# strip HTML, from
# http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

f1 = open(sys.argv[1], 'r')

# get header info from first line
l1 = f1.readline()
obj1 = ast.literal_eval(re.sub(r'^\d+,', '', l1))
# find the id field (hopefully)
id_int = [x for x in range(0, len(obj1.keys()))
          if re.search(r'id$', obj1.keys()[x])][0]
col_names = obj1.keys()
# make the id the first column name
col_names.insert(0, obj1.keys()[id_int])
col_names.pop(id_int + 1)
f1.seek(0)

with open(sys.argv[2], 'wb') as f2:
    writer = csv.DictWriter(f2, fieldnames = col_names)
    writer.writerow(dict((fn,fn) for fn in col_names))
    # prettier, but doesn't run on RIT (python 2.6.6):
    #writer.writeheader()

    for line in f1:
        object = ast.literal_eval(re.sub(r'^\d+,', '', line))
        # strip HTML from overview
        if 'overview' in object.keys():
            object['overview'] = remove_tags(object['overview'])
        # use utf-8 for text
        for key in object.keys():
            if isinstance(object[key], unicode):
                object[key] = object[key].encode('utf-8')
        writer.writerow(object)
