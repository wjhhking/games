

DB ={
'hash_abc': ("tree", ["hash_a", "hash_b", "hash_c"]),
'hash_abbc': ("tree", ["hash_a", "hash_bb", "hash_c"]),
'hash_a': ("blob", "a"),
'hash_b': ("blob", "b"),
'hash_c': ("blob", "c"),
'hash_bb': ("blob", "bb"),
}


"""
/app/src/main.py


/app/src/main.py -> h_main_hash


commit-1 -> hash_dir_abc
hash_dir_abc -> hash_a, hash_b, hash_c
a, b, c


commit-2 -> hash_dir_abbc
hash_dir_abbc -> hash_a, hash_bb, hash_c
a, bb, c
"""

DB ={
'hash_abc': ("tree", ["hash_a", "hash_b", "hash_c"]),
'hash_abbc': ("tree", ["hash_a", "hash_bb", "hash_c"]),
'hash_a': ("blob", "a"),
'hash_b': ("blob", "b"),
'hash_c': ("blob", "c"),
'hash_bb': ("blob", "bb"),
}





"/app/src/main.py -> h_main_hash"

DB = {
'hash_app_commit_0': ("commit", "root_hash_v0"),
'hash_app_commit_1': ("commit", "root_hash_v1"),
'root_hash_v0': ("tree", ["hash_src_v0"]),
'hash_src_v0': ("tree", ["hash_main_py_v0"]),
'hash_main_py_v0': ("blob", "content"),
}

