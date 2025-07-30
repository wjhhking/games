


def simplify(dir: str) -> str:
    print('   -simplifying: ', dir)
    assert dir[0] == '/'


    paths = dir[1:].split('/')
    ans = []

    for p in paths:
        if p == '..':
            if ans:
                ans.pop()
        else:
            ans.append(p)

    return '/' + '/'.join(ans)

def cd(current_dir:str, new_dir:str) -> str:
    ans = ''
    # 0. new_dir = ''
    if new_dir == '':
        return current_dir

    # 1. start with /
    if new_dir[0] == '/':
        return simplify(new_dir)

    if new_dir[0] == '~':
        return simplify('/home/user' + new_dir[1:])

    # 2. it will be /aa +  xx/yy/zz
    if current_dir == '/':
        return simplify('/' + new_dir)

    return simplify(current_dir + '/' + new_dir)

    pass



def test_cd_command():
    print(cd('/foo/bar', 'baz'))
    print(cd('/foor/bar', '../baz'))
    print(cd("/home", "/user/profile"))
    print(cd("/", "foo/bar/../../baz"))
    print(cd("/", ".."))

def test_home_commad():
    print(cd("/foo/bar", "~/documents"))
    print(cd("/foo", "bar/~/baz"))
    print(cd("/home/user/downloads", "~"))

test_cd_command()
print('-'*80)
test_home_commad()
print('-'*80)


def cd_with_symlinks(current_dir: str, new_dir: str, symlinks: dict[str, str]) -> str:
    current_dir = cd(current_dir, new_dir)
    visited = set()

    while True:
        if current_dir in visited:
            raise ValueError('Cycle')
        visited.add(current_dir)

        print ('   ', current_dir)
        if current_dir in symlinks:
            current_dir = symlinks[current_dir]
            continue

        pre = current_dir
        post = ''
        can_fold = False
        while len(pre) > 1 and '/' in pre:
            print('?', pre, post)
            i = pre.rfind('/')
            post = pre[i:] + post
            pre = pre[:i]
            print('?2', pre, post)
            if pre in symlinks:
                can_fold = True
                break

        print(can_fold, pre, post)

        if can_fold:
            current_dir = symlinks[pre] + post
            continue
        else:
            break

    return current_dir

def test_cd_with_symlinks():
    print(cd_with_symlinks("/foo", "bar", {"/foo/bar": "/abc"}), '\n')
    print(cd_with_symlinks("/foo", "bar/baz", {"/foo": "/a", "/foo/bar": "/b"}), '\n')
    print(cd_with_symlinks("/a", "b", {"/a/b": "/c", "/c": "/d/e"}), '\n')
    print('-'*80)

test_cd_with_symlinks()

def test_cycle():
    try:
        print(cd_with_symlinks("/", "a", {"/a": "/b", "/b": "/a"}))
    except ValueError:
        print('Good1')
        pass

    try:
        print(cd_with_symlinks("/", "start", {"/start": "/link1", "/link1": "/link2", "/link2": "/link1"}))
    except ValueError:
        print('Good2')
        pass

test_cycle()