import GIS_Programming.useful_functions_1 as uf

headers, body = uf.get_textfile_from_web("http://mf2.dit.ie/gettysburg.txt")
split_body = body.strip().split()
counts = uf.count_items_in_collection(split_body)
print(counts)

