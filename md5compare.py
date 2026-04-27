import os, hashlib, sys

def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

base = sys.argv[1]
feat = sys.argv[2]
skip = {'.git', 'node_modules', 'target', '.idea'}

diffs = []
for root, dirs, files in os.walk(feat):
    dirs[:] = [d for d in dirs if d not in skip]
    for fn in files:
        fp = os.path.join(root, fn)
        rel = os.path.relpath(fp, feat)
        bp = os.path.join(base, rel)
        if not os.path.exists(bp):
            diffs.append(('NEW', rel))
        elif md5(fp) != md5(bp):
            diffs.append(('MOD', rel))

for t, r in sorted(diffs):
    print(t, r)
