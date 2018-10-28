Search your notes
-------------------------------------------------------------------------------

181028

Search your notes, and grep the results:

    [mm] RNA-Puzzles-submission$ git:(master) ✗ geekbooksearch2.py for cp | grep docker
    docker.md:18:    docker cp /Users/magnus/work-src/rna-pdb-tools/rna_pdb_tools/pdbs 306468777bc5:/home/demo/
    docker.md:47:    8888/tcp -> 0.0.0.0:8888
    docker.md:53:    docker cp test:<path> <to-where>
    docker.md:54:    docker cp <file> test:<path>

this can be aliased to:

    alias geeksearch="geekbooksearch2.py for "
